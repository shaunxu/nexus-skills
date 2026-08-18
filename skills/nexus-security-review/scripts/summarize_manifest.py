#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


def _load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore

        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ModuleNotFoundError:
        with path.open("r", encoding="utf-8") as f:
            return _MiniYaml().parse(f.read())


class _MiniYaml:
    def parse(self, text: str) -> Any:
        self.lines: list[tuple[int, str]] = []
        for raw in text.splitlines():
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            stripped = raw.rstrip()
            indent = len(stripped) - len(stripped.lstrip(" "))
            self.lines.append((indent, stripped.strip()))
        self.pos = 0
        return self._parse_block(0)

    def _peek(self) -> tuple[int, str] | None:
        if self.pos < len(self.lines):
            return self.lines[self.pos]
        return None

    def _parse_block(self, indent: int) -> Any:
        peek = self._peek()
        if peek is None:
            return None
        if peek[0] < indent:
            return None
        if peek[1].startswith("- "):
            return self._parse_seq(indent)
        return self._parse_map(indent)

    def _parse_seq(self, indent: int) -> list[Any]:
        items: list[Any] = []
        while True:
            peek = self._peek()
            if peek is None or peek[0] < indent or not peek[1].startswith("- "):
                break
            cur_indent, content = self.lines[self.pos]
            self.pos += 1
            rest = content[2:].strip()
            if not rest:
                child_peek = self._peek()
                if child_peek is not None and child_peek[0] > cur_indent:
                    items.append(self._parse_block(child_peek[0]))
                else:
                    items.append(None)
                continue
            inline_kv = re.match(r"^([A-Za-z_][\w.-]*):\s+(.+)$", rest)
            block_kv = re.match(r"^([A-Za-z_][\w.-]*):\s*$", rest)
            child_peek = self._peek()
            if inline_kv:
                key = inline_kv.group(1)
                value = inline_kv.group(2).strip()
                obj = {key: self._parse_scalar(value)}
                if child_peek is not None and child_peek[0] > cur_indent:
                    nested = self._parse_map(child_peek[0])
                    if isinstance(nested, dict):
                        obj.update(nested)
                items.append(obj)
            elif block_kv:
                key = block_kv.group(1)
                if child_peek is not None and child_peek[0] > cur_indent:
                    items.append({key: self._parse_block(child_peek[0])})
                else:
                    items.append({key: None})
            else:
                items.append(self._parse_scalar(rest))
        return items

    def _parse_map(self, indent: int, first_key: str | None = None, first_value: Any = None) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if first_key is not None:
            result[first_key] = first_value
        while True:
            peek = self._peek()
            if peek is None or peek[0] < indent:
                break
            if peek[1].startswith("- "):
                break
            cur_indent, content = self.lines[self.pos]
            if cur_indent != indent:
                break
            self.pos += 1
            if ":" not in content:
                continue
            key, _, val = content.partition(":")
            key = key.strip()
            val = val.strip()
            if val:
                result[key] = self._parse_scalar(val)
            else:
                child_peek = self._peek()
                if child_peek is not None and child_peek[0] > cur_indent:
                    result[key] = self._parse_block(child_peek[0])
                else:
                    result[key] = None
        return result

    def _parse_scalar(self, raw: str) -> Any:
        if raw in ("true", "True"):
            return True
        if raw in ("false", "False"):
            return False
        if raw in ("null", "~", ""):
            return None
        if raw.startswith("'") and raw.endswith("'"):
            return raw[1:-1]
        if raw.startswith('"') and raw.endswith('"'):
            return bytes(raw[1:-1], "utf-8").decode("unicode_escape")
        if re.fullmatch(r"-?\d+", raw):
            return int(raw)
        if re.fullmatch(r"-?\d+\.\d+", raw):
            return float(raw)
        return raw


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _fn_of(node: Any) -> str | None:
    if not isinstance(node, dict):
        return None
    fn = node.get("function") or node.get("handler", {}).get("function")
    return str(fn) if fn else None


def _collect_handler_refs(manifest: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    refs: dict[str, list[dict[str, str]]] = {}

    def add(fn: str | None, source: str, detail: str = "") -> None:
        if not fn:
            return
        refs.setdefault(fn, []).append({"source": source, "detail": detail})

    for ext in _as_list(manifest.get("extensions")):
        ext_d = _as_dict(ext)
        add(_fn_of(ext_d.get("resolver")), "extension", str(ext_d.get("key", "")))

    for trig in _as_list(_as_dict(manifest.get("event")).get("triggers")):
        trig_d = _as_dict(trig)
        add(_fn_of(trig_d.get("handler")), f"event:{trig_d.get('type', 'unknown')}", str(trig_d.get("key", "")))

    for con in _as_list(_as_dict(manifest.get("async")).get("consumers")):
        con_d = _as_dict(con)
        add(_fn_of(con_d.get("handler")), "async:consumer", str(con_d.get("key", "")))

    for route in _as_list(_as_dict(manifest.get("exposer")).get("routes")):
        route_d = _as_dict(route)
        add(_fn_of(route_d.get("handler")), "exposer", f"{route_d.get('method', '')} {route_d.get('path', '')}".strip())

    return refs


def _normalize_backend_entry(entry: Any) -> str | None:
    if isinstance(entry, dict):
        if "remote" in entry:
            return f"remote:{entry['remote']}"
        return None
    if entry is None:
        return None
    return str(entry)


_HOST_RE = re.compile(r"^[A-Za-z0-9.*-]+(?::\d+)?$")


def _classify_host(value: str) -> str:
    if value == "*":
        return "wildcard-all"
    if value.startswith("remote:"):
        return "remote-ref"
    if "://" in value:
        parsed = urlparse(value)
        host = (parsed.hostname or "").lower()
        if host == "*" or host.startswith("*."):
            return "wildcard-subdomain"
        if host:
            return "exact-url"
    if _HOST_RE.match(value):
        if value.startswith("*."):
            return "wildcard-subdomain"
        return "domain"
    return "unknown"


_SECRET_HINT = re.compile(
    r"(secret|token|api[_-]?key|password|passwd|pwd|private[_-]?key|access[_-]?key|client[_-]?secret)",
    re.IGNORECASE,
)


def summarize(manifest_path: Path) -> dict[str, Any]:
    manifest = _as_dict(_load_yaml(manifest_path))
    permissions = _as_dict(manifest.get("permissions"))
    external = _as_dict(permissions.get("external"))
    content = _as_dict(permissions.get("content"))
    event = _as_dict(manifest.get("event"))
    exposer = _as_dict(manifest.get("exposer"))
    remotes = _as_list(manifest.get("remotes"))
    async_cfg = _as_dict(manifest.get("async"))
    storage = _as_dict(manifest.get("storage"))
    app = _as_dict(manifest.get("app"))

    scopes = [str(s) for s in _as_list(permissions.get("scopes"))]
    fetch_backend_raw = _as_list(_as_dict(external.get("fetch")).get("backend"))
    fetch_client = [str(s) for s in _as_list(_as_dict(external.get("fetch")).get("client"))]
    csp: dict[str, list[str]] = {}
    for key in ("scripts", "styles"):
        csp[key] = [str(s) for s in _as_list(content.get(key))]
    csp_other = {
        k: [str(x) for x in _as_list(v)]
        for k, v in external.items()
        if k not in ("fetch",)
    }

    backend_entries = [e for e in (_normalize_backend_entry(x) for x in fetch_backend_raw) if e is not None]
    backend_classified = [
        {"value": v, "classification": _classify_host(v)} for v in backend_entries
    ]

    declared_functions = {str(f.get("key")) for f in _as_list(manifest.get("functions")) if isinstance(f, dict) and f.get("key")}

    handler_refs = _collect_handler_refs(manifest)
    unresolved_handlers = sorted(fn for fn in handler_refs if fn not in declared_functions)

    triggers = []
    for trig in _as_list(event.get("triggers")):
        trig_d = _as_dict(trig)
        triggers.append({
            "key": trig_d.get("key"),
            "type": trig_d.get("type"),
            "events": [str(e) for e in _as_list(trig_d.get("events"))],
            "handler": _fn_of(trig_d.get("handler")),
            "interval": trig_d.get("interval"),
            "timeout": trig_d.get("timeout"),
            "filter": trig_d.get("filter"),
        })

    webhook_triggers = [t for t in triggers if t.get("type") == "webhook"]

    routes_summary = []
    for route in _as_list(exposer.get("routes")):
        route_d = _as_dict(route)
        route_scopes = [str(s) for s in _as_list(route_d.get("scopes"))]
        routes_summary.append({
            "key": route_d.get("key"),
            "method": route_d.get("method"),
            "path": route_d.get("path"),
            "handler": _fn_of(route_d.get("handler")),
            "scopes": route_scopes,
            "scopes_declared": bool(route_scopes),
        })

    exposer_scope_defs = [str(s.get("name")) for s in _as_list(exposer.get("scopes")) if isinstance(s, dict) and s.get("name")]

    remotes_summary = []
    remote_keys = set()
    for remote in remotes:
        remote_d = _as_dict(remote)
        key = str(remote_d.get("key", ""))
        remote_keys.add(key)
        auth = _as_dict(remote_d.get("auth"))
        remotes_summary.append({
            "key": key,
            "baseUrl": remote_d.get("baseUrl"),
            "operations": [str(o) for o in _as_list(remote_d.get("operations"))],
            "auth": {
                "userToken": bool(auth.get("userToken")),
                "appToken": bool(auth.get("appToken")),
            },
        })

    for ep in _as_list(manifest.get("endpoints")):
        ep_d = _as_dict(ep)
        auth = _as_dict(ep_d.get("auth"))
        if auth:
            key = str(ep_d.get("remote", ""))
            for remote in remotes_summary:
                if remote["key"] == key:
                    remote.setdefault("endpoint_auth", []).append({
                        "endpoint": ep_d.get("key"),
                        "userToken": bool(auth.get("userToken")),
                        "appToken": bool(auth.get("appToken")),
                    })

    entities = []
    for ent in _as_list(storage.get("entities")):
        ent_d = _as_dict(ent)
        entities.append({
            "name": ent_d.get("name"),
            "attributes": [str(a.get("name")) for a in _as_list(ent_d.get("attributes")) if isinstance(a, dict)],
            "indexes": [str(i.get("name")) for i in _as_list(ent_d.get("indexes")) if isinstance(i, dict)],
        })

    env_vars = []
    for var in _as_list(_as_dict(manifest.get("environment")).get("variables")):
        var_d = _as_dict(var)
        default = var_d.get("default")
        default_str = "" if default is None else str(default)
        env_vars.append({
            "key": var_d.get("key"),
            "has_default": default is not None,
            "default_looks_secret": bool(_SECRET_HINT.search(str(var_d.get("key", "")))) and bool(default_str),
            "default_preview": (default_str[:6] + "..." + default_str[-2:]) if default_str and _SECRET_HINT.search(str(var_d.get("key", ""))) and len(default_str) > 8 else default_str,
        })

    observations: list[dict[str, str]] = []

    def add_obs(code: str, severity: str, message: str, evidence: str = "") -> None:
        observations.append({"code": code, "severity": severity, "message": message, "evidence": evidence})

    if permissions.get("scopes") is None:
        add_obs("PERM_SCOPES_MISSING", "high", "permissions.scopes is not declared. Nexus requires scopes to be present even when empty.")
    if not scopes:
        add_obs("PERM_SCOPES_EMPTY", "info", "permissions.scopes is empty. Confirm the app makes no PingCode REST calls requiring scopes.")

    if "*" in scopes:
        add_obs("SCOPE_WILDCARD", "critical", "A wildcard '*' scope is declared, which grants over-broad access.")
    for scope in scopes:
        if scope.startswith("*") or scope.endswith("*"):
            add_obs("SCOPE_WILDCARD_LIKE", "high", f"Scope '{scope}' appears wildcard-like; verify it is a real Nexus scope.")

    for entry in backend_classified:
        if entry["classification"] == "wildcard-all":
            add_obs("EGRESS_BACKEND_WILDCARD_ALL", "high", "permissions.external.fetch.backend contains '*', allowing outbound calls to any host from backend functions.")
        elif entry["classification"] == "wildcard-subdomain":
            add_obs("EGRESS_BACKEND_WILDCARD_SUBDOMAIN", "medium", f"Backend egress '{entry['value']}' uses a wildcard subdomain. Verify all subdomains are trusted.")

    client_wildcards = [v for v in fetch_client if v == "*" or urlparse(v).hostname in ("*",) or (urlparse(v).hostname or "").startswith("*.")]
    for v in client_wildcards:
        add_obs("EGRESS_CLIENT_WILDCARD", "medium", f"permissions.external.fetch.client contains wildcard entry '{v}'.")

    for key in ("scripts", "styles"):
        for value in csp.get(key, []):
            if value == "unsafe-eval":
                add_obs("CSP_UNSAFE_EVAL", "critical", "permissions.content.scripts contains 'unsafe-eval', enabling dynamic code execution in Custom UI.")
            elif value == "unsafe-inline":
                add_obs("CSP_UNSAFE_INLINE", "medium", f"permissions.content.{key} contains 'unsafe-inline'. Review whether XSS sinks (dangerouslySetInnerHTML, innerHTML) are reachable.")
            elif value == "unsafe-hashes":
                add_obs("CSP_UNSAFE_HASHES", "low", f"permissions.content.{key} contains 'unsafe-hashes'; verify inline event handlers are necessary and safe.")

    if not scopes and any(t.get("type") == "system" for t in triggers):
        add_obs("EVENT_SYSTEM_NO_SCOPES", "info", "System event triggers exist but scopes are empty. Confirm handlers do not call PingCode APIs.")

    if webhook_triggers:
        add_obs("WEBHOOK_PUBLIC", "high", "Webhook triggers are public URLs with no platform-provided authentication. Each handler must implement HMAC signature verification, timestamp/nonce replay protection, and input validation.", evidence=", ".join(str(t.get("key")) for t in webhook_triggers))

    for route in routes_summary:
        if not route["scopes_declared"]:
            add_obs("EXPOSER_ROUTE_NO_SCOPE", "high", f"Exposer route {route['method']} {route['path']} declares no scopes; it may be reachable without access control.", evidence=str(route.get("key")))

    for scope in exposer_scope_defs:
        if not scope.startswith("ncp:"):
            add_obs("EXPOSER_SCOPE_BAD_PREFIX", "medium", f"Custom scope '{scope}' must start with 'ncp:'.")
    if len(exposer_scope_defs) > 16:
        add_obs("EXPOSER_TOO_MANY_SCOPES", "medium", f"{len(exposer_scope_defs)} custom scopes declared; Nexus allows a maximum of 16.")

    for remote in remotes_summary:
        if remote["auth"]["userToken"] and "pcp:read:user:token" not in scopes:
            add_obs("REMOTE_USERTOKEN_WITHOUT_SCOPE", "high", f"Remote '{remote['key']}' enables auth.userToken but 'pcp:read:user:token' scope is not declared.")
        if remote["auth"]["appToken"] and "pcp:read:app:token" not in scopes:
            add_obs("REMOTE_APPTOKEN_WITHOUT_SCOPE", "high", f"Remote '{remote['key']}' enables auth.appToken but 'pcp:read:app:token' scope is not declared.")
        base_url = str(remote.get("baseUrl", ""))
        if base_url.startswith("http://"):
            add_obs("REMOTE_PLAIN_HTTP", "medium", f"Remote '{remote['key']}' uses plain HTTP baseUrl. Tokens will be transmitted in cleartext.")

    for entry in backend_classified:
        if entry["classification"] == "remote-ref":
            remote_key = entry["value"].split(":", 1)[1]
            if remote_key not in remote_keys:
                add_obs("EGRESS_REMOTE_UNRESOLVED", "high", f"permissions.external.fetch.backend references undefined remote '{remote_key}'.")

    if entities and "pcp:storage:app" not in scopes:
        add_obs("STORAGE_NO_SCOPE", "high", "storage.entities is declared but 'pcp:storage:app' scope is missing.")

    for var in env_vars:
        if var["default_looks_secret"]:
            add_obs("ENV_DEFAULT_LOOKS_SECRET", "high", f"environment.variables '{var['key']}' has a default value that looks like a secret. Secrets must come from KVS secret storage, not manifest defaults.", evidence=var["default_preview"])

    for fn in unresolved_handlers:
        refs = handler_refs.get(fn, [])
        sources = ", ".join(f"{r['source']}:{r['detail']}".rstrip(":") for r in refs)
        add_obs("HANDLER_UNRESOLVED", "high", f"Handler function '{fn}' is referenced but not declared in functions[].", evidence=sources)

    consumers = _as_list(async_cfg.get("consumers"))
    queues = {str(q.get("key")) for q in _as_list(async_cfg.get("queues")) if isinstance(q, dict) and q.get("key")}
    for con in consumers:
        con_d = _as_dict(con)
        queue = con_d.get("queue")
        if queue and str(queue) not in queues:
            add_obs("ASYNC_QUEUE_UNRESOLVED", "high", f"Async consumer '{con_d.get('key')}' references undefined queue '{queue}'.")

    summary = {
        "manifest_path": str(manifest_path),
        "app": {
            "id": app.get("id"),
            "version": app.get("version"),
            "licensing_enabled": bool(_as_dict(app.get("licensing")).get("enabled")),
        },
        "permissions": {
            "scopes": scopes,
            "external_fetch_backend": backend_classified,
            "external_fetch_client": fetch_client,
            "content": csp,
            "other_csp_directives": csp_other,
        },
        "functions": {
            "declared": sorted(declared_functions),
            "handler_refs": [
                {"function": fn, "references": refs}
                for fn, refs in sorted(handler_refs.items())
            ],
            "unresolved": unresolved_handlers,
        },
        "entrypoints": {
            "extensions": [
                {
                    "key": ext.get("key"),
                    "target": ext.get("target"),
                    "resource": ext.get("resource"),
                    "resolver_function": _fn_of(ext.get("resolver")),
                    "has_display": isinstance(ext.get("display"), dict) and bool(ext.get("display")),
                }
                for ext in _as_list(manifest.get("extensions"))
                if isinstance(ext, dict)
            ],
            "event_triggers": triggers,
            "exposer_routes": routes_summary,
            "async_consumers": [
                {
                    "key": con.get("key"),
                    "queue": con.get("queue"),
                    "handler_function": _fn_of(con.get("handler")),
                    "concurrency": con.get("concurrency"),
                }
                for con in consumers
                if isinstance(con, dict)
            ],
        },
        "remotes": remotes_summary,
        "endpoints": [
            {
                "key": ep.get("key"),
                "remote": ep.get("remote"),
                "route": ep.get("route"),
                "auth": {
                    "userToken": bool(_as_dict(ep.get("auth")).get("userToken")),
                    "appToken": bool(_as_dict(ep.get("auth")).get("appToken")),
                },
            }
            for ep in _as_list(manifest.get("endpoints"))
            if isinstance(ep, dict)
        ],
        "exposer_custom_scopes": exposer_scope_defs,
        "storage_entities": entities,
        "environment_variables": env_vars,
        "observations": observations,
    }
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    app = summary["app"]
    lines.append(f"# Nexus Manifest Summary: {summary['manifest_path']}")
    lines.append("")
    lines.append(f"- App ID: `{app.get('id')}`")
    lines.append(f"- Version: `{app.get('version')}`")
    lines.append(f"- Licensing enabled: `{app.get('licensing_enabled')}`")
    lines.append("")

    perm = summary["permissions"]
    lines.append("## Permissions")
    lines.append("")
    lines.append(f"- Scopes ({len(perm['scopes'])}):")
    for scope in perm["scopes"] or ["(none)"]:
        lines.append(f"  - `{scope}`")
    lines.append(f"- Backend egress ({len(perm['external_fetch_backend'])}):")
    if perm["external_fetch_backend"]:
        for entry in perm["external_fetch_backend"]:
            lines.append(f"  - `{entry['value']}` — {entry['classification']}")
    else:
        lines.append("  - (none)")
    lines.append(f"- Client egress ({len(perm['external_fetch_client'])}):")
    for value in perm["external_fetch_client"]:
        lines.append(f"  - `{value}`")
    if not perm["external_fetch_client"]:
        lines.append("  - (none)")
    lines.append("- Content security:")
    for key, values in perm["content"].items():
        lines.append(f"  - {key}: {', '.join(f'`{v}`' for v in values) if values else '(none)'}")
    other = perm.get("other_csp_directives", {})
    for key, values in other.items():
        if values:
            lines.append(f"  - {key}: {', '.join(f'`{v}`' for v in values)}")
    lines.append("")

    lines.append("## Entry points")
    lines.append("")
    ext = summary["entrypoints"]["extensions"]
    lines.append(f"- UI extensions ({len(ext)}):")
    for e in ext:
        disp = " [display conditions]" if e.get("has_display") else ""
        lines.append(f"  - `{e.get('key')}` target=`{e.get('target')}` resolver=`{e.get('resolver_function')}` resource=`{e.get('resource')}`{disp}")
    if not ext:
        lines.append("  - (none)")

    triggers = summary["entrypoints"]["event_triggers"]
    lines.append(f"- Event triggers ({len(triggers)}):")
    for t in triggers:
        extra = []
        if t.get("events"):
            extra.append("events=" + ",".join(t["events"]))
        if t.get("interval"):
            extra.append(f"interval={t['interval']}")
        lines.append(f"  - `{t.get('key')}` type=`{t.get('type')}` handler=`{t.get('handler')}` {' '.join(extra)}".rstrip())
    if not triggers:
        lines.append("  - (none)")

    routes = summary["entrypoints"]["exposer_routes"]
    lines.append(f"- Exposer routes ({len(routes)}):")
    for r in routes:
        scopes = ",".join(r.get("scopes") or []) or "(no scopes)"
        lines.append(f"  - `{r.get('key')}` {r.get('method')} `{r.get('path')}` handler=`{r.get('handler')}` scopes={scopes}")
    if not routes:
        lines.append("  - (none)")

    custom_scopes = summary.get("exposer_custom_scopes") or []
    lines.append(f"- Exposer custom scopes ({len(custom_scopes)}):")
    for s in custom_scopes:
        lines.append(f"  - `{s}`")
    if not custom_scopes:
        lines.append("  - (none)")

    consumers = summary["entrypoints"]["async_consumers"]
    lines.append(f"- Async consumers ({len(consumers)}):")
    for c in consumers:
        lines.append(f"  - `{c.get('key')}` queue=`{c.get('queue')}` handler=`{c.get('handler_function')}` concurrency={c.get('concurrency')}")
    if not consumers:
        lines.append("  - (none)")
    lines.append("")

    lines.append("## Remotes")
    lines.append("")
    for remote in summary["remotes"]:
        auth = remote.get("auth", {})
        flags = []
        if auth.get("userToken"):
            flags.append("userToken")
        if auth.get("appToken"):
            flags.append("appToken")
        lines.append(f"- `{remote.get('key')}` -> `{remote.get('baseUrl')}` ops={','.join(remote.get('operations') or []) or '-'} auth={','.join(flags) or 'none'}")
    if not summary["remotes"]:
        lines.append("- (none)")
    lines.append("")

    endpoints = summary.get("endpoints") or []
    lines.append("## Endpoints")
    lines.append("")
    for ep in endpoints:
        auth = ep.get("auth", {})
        flags = []
        if auth.get("userToken"):
            flags.append("userToken")
        if auth.get("appToken"):
            flags.append("appToken")
        lines.append(f"- `{ep.get('key')}` remote=`{ep.get('remote')}` route=`{ep.get('route')}` auth={','.join(flags) or 'none'}")
    if not endpoints:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Storage")
    lines.append("")
    for ent in summary["storage_entities"]:
        lines.append(f"- entity `{ent.get('name')}`: attributes={len(ent.get('attributes') or [])}, indexes={len(ent.get('indexes') or [])}")
    if not summary["storage_entities"]:
        lines.append("- (no custom entities)")
    lines.append("")

    lines.append("## Environment variables")
    lines.append("")
    for var in summary["environment_variables"]:
        flag = " [default looks secret]" if var.get("default_looks_secret") else ""
        lines.append(f"- `{var.get('key')}` has_default={var.get('has_default')}{flag}")
    if not summary["environment_variables"]:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Handler references")
    lines.append("")
    declared = summary["functions"].get("declared") or []
    lines.append(f"- Declared functions ({len(declared)}): {', '.join(f'`{f}`' for f in declared) if declared else '(none)'}")
    unresolved = summary["functions"].get("unresolved") or []
    if unresolved:
        lines.append(f"- **Unresolved handlers (referenced but not declared):** {', '.join(f'`{f}`' for f in unresolved)}")
    for ref in summary["functions"]["handler_refs"]:
        sources = ", ".join(f"{r['source']}({r['detail']})" for r in ref["references"])
        lines.append(f"- `{ref['function']}` <- {sources}")
    if not summary["functions"]["handler_refs"]:
        lines.append("- (none)")
    lines.append("")

    observations = summary["observations"]
    lines.append(f"## Observations ({len(observations)})")
    lines.append("")
    if not observations:
        lines.append("- No mechanical observations. Continue with rule-based review.")
    else:
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        for obs in sorted(observations, key=lambda o: (order.get(o["severity"], 9), o["code"])):
            evidence = f" — {obs['evidence']}" if obs.get("evidence") else ""
            lines.append(f"- **[{obs['severity'].upper()}] {obs['code']}** {obs['message']}{evidence}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize a Nexus manifest.yaml for security review. Produces a compact structured inventory plus mechanical observations (no dataflow analysis)."
    )
    parser.add_argument("project_root", help="Path to the Nexus project root containing manifest.yaml (or a direct path to a manifest file).")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format (default: markdown).")
    parser.add_argument("--output", "-o", help="Write output to this file instead of stdout.")
    args = parser.parse_args(argv)

    target = Path(args.project_root).expanduser().resolve()
    if target.is_dir():
        manifest_path = target / "manifest.yaml"
        if not manifest_path.exists():
            manifest_path = target / "manifest.yml"
    else:
        manifest_path = target

    if not manifest_path.is_file():
        print(f"Error: manifest not found at {manifest_path}", file=sys.stderr)
        return 2

    summary = summarize(manifest_path)
    rendered = json.dumps(summary, indent=2, ensure_ascii=False) if args.format == "json" else render_markdown(summary)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered + ("\n" if not rendered.endswith("\n") else ""), encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
