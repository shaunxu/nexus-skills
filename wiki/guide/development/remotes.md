---
title: "远程服务"
lastUpdated: 2026-07-16T14:43:06.000Z
---

# 远程服务

Nexus 允许你将应用与其他平台托管的服务进行集成，支持在应用内向远程服务发起请求。与请求标准的 REST APIs 和外部资源 URL相比，远程调用提供了很多额外的能力，使的应用与远程服务之间的相同通信更加简单。

- 能够配置你的应用向远程端点发送身份验证令牌，使得远程端点可以使用身份令牌向 PingCode 平台发起经过身份验证的回调，以访问 PingCode APIs 和 Nexus 数据存储
- 定义扩展模块，将远程服务直接链接到扩展点，以便减少代码维护量
- 能够验证传入远程服务的请求，确实来自于 Nexus 平台
- 在远程服务调用中，会自动将关于调用来源的关键信息发送到你的远程服务，这样你就不必手动将站点的 Base URL、认证状态以及其他常用信息复制到请求中

## 请求参数

当 Nexus 调用你的远程服务时，会向配置的地址发起一个请求。除了应用自身传入的 `method` 、 `headers` 、 `body` 之外，Nexus 平台还会自动附加一组标准请求头，其中最核心的是 Nexus 调用令牌（Nexus Invocation Token，简称 NIT）。借助这些信息，远程服务无需应用手动传递站点地址、认证状态等上下文。

Nexus 附加的请求头如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.78%" /><col style="width: 14.83%" /><col style="width: 53.39%" /></colgroup><thead><tr><th>请求头</th><th>是否必有</th><th>说明</th></tr></thead><tbody><tr><td><code>Authorization</code></td><td>Y</td><td>形如 <code>Bearer &lt;NIT&gt;</code> ，携带 Nexus 调用令牌（NIT），用于向远程服务证明请求来自 Nexus 平台。</td></tr><tr><td><code>traceparent</code></td><td>Y</td><td>本次调用的追踪 ID，便于在 Nexus 与远程服务之间关联日志，遵循W3C Trace Context 规范。</td></tr><tr><td><code>Content-Type</code></td><td></td><td>当请求体为 JSON 字符串且应用未显式设置时，自动补充为 <code>application/json</code> 。</td></tr><tr><td><code>x-nexus-app-token</code></td><td></td><td>应用级别的 REST API 令牌，仅当对应 <code>remote</code> / <code>endpoint</code> 的 <code>auth.appToken</code> 开启时下发。</td></tr><tr><td><code>x-nexus-user-token</code></td><td></td><td>当前用户级别的 REST API 令牌，仅当 <code>auth.userToken</code> 开启且调用上下文中存在用户时下发。</td></tr><tr><td><code>x-nexus-api-base-url</code></td><td>Y</td><td>远程服务回调 PingCode REST APIs 时使用的基础地址。</td></tr></tbody></table>

在使用远程服务调用时，有一些特殊的注意事项：

- `x-nexus-app-token` 、 `x-nexus-user-token` 用于让远程服务以 PingCode 令牌回调 PingCode REST APIs 与 Nexus 数据存储，请将其视为不透明令牌，不要解析、记录或外泄其内容。
- 出于安全考虑，Nexus 平台会在附加标准请求头之前，剔除应用可能传入的一组受保护请求头（ `authorization` 、 `host` 、 `content-length` 、 `transfer-encoding` 、 `connection` 、 `upgrade` 、 `te` 、 `trailer` ），以确保应用代码无法覆盖 NIT 等协议级请求头。

## 调用令牌

Nexus 调用令牌（NIT） 是一个由 Nexus 平台使用 **RS256** 算法签名的 JWT，具备以下固定特征：

- 签名算法： `RS256`
- 密钥标识（ `kid` ）： `nexus-nit-1`

NIT 的 `payload` 中携带了本次调用的上下文信息，远程服务在验证通过后可直接信任并使用：

```typescript
{
  // 标准 JWT 声明
  "iss": "nexus/invocation-token",
  "aud": "nexus",
  "iat": 1718000000,
  "exp": 1718000300,
  "jti": "…",

  // 上下文信息
  "context" : {
    "app":         { "id": "…", "version": "…" },
    "environment": { "id": "…", "type": "development | production" },
    "team":        { "id": "…", "url": "https://…", "locale": "…", "timezone": "…" },
    "installation": { "id": "…" },
    "invocation":   { "id": "…" },
    "user":      { "id": "…", "locale": "…", "timezone": "…" },
    "extension": { "key": "…", "local_id": "…", "target": "…", "location": "…", "data": {} },
    "event":     { "trigger": { "key": "…", "type": "…" } }
  }
}
```

各字段说明如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 34.46%" /><col style="width: 65.54%" /></colgroup><thead><tr><th>字段</th><th>说明</th></tr></thead><tbody><tr><td><code>iss</code></td><td>签发者</td></tr><tr><td><code>aud</code></td><td>受众（给谁用）</td></tr><tr><td><code>iat</code></td><td>签发时间</td></tr><tr><td><code>exp</code></td><td>过期时间，默认5分钟</td></tr><tr><td><code>jti</code></td><td>令牌唯一标识</td></tr><tr><td><code>context</code></td><td>应用上下文信息，请参考 <a href="/reference/functions/core/app">app</a></td></tr></tbody></table>

## 验证调用令牌

为确保进入远程服务的请求确实来自 Nexus 平台，远程服务必须验证 `Authorization` 头中的 NIT。任何验证失败的请求都应被拒绝（返回 `401` ）。

验证流程如下：

1. 从 `Authorization` 头中取出 `Bearer` 令牌
1. 从 Nexus 的 JWKS 端点获取用于验签的公钥： `/api/nexus/nit/.well-known/jwks.json` （公开端点，无需认证，可缓存）。该端点返回 `kid` 为 `nexus-nit-1` 的 RS256 公钥
1. 根据令牌头中的 `kid` 选择对应公钥，校验 `RS256` 签名
1. 校验声明： `aud` 必须为 `nexus` ， `iss` 必须为 `nexus/invocation-token` ，并校验 `exp` 未过期
1. 校验通过后，即可信任并读取载荷中的调用上下文声明

下面是使用 Python（ [PyJWT](https://pyjwt.readthedocs.io/) ）验证 NIT 的示例。先安装依赖：

```python
pip install "pyjwt[crypto]"
```

验证逻辑：

```python
import jwt
from jwt import PyJWKClient

# Nexus JWKS 端点（请替换为你所在环境的实际域名）
JWKS_URL = "https://<your-nexus-host>/api/nexus/nit/.well-known/jwks.json"

# PyJWKClient 会按 token header 中的 kid 自动选择公钥，并在内部缓存
_jwk_client = PyJWKClient(JWKS_URL)


def verify_nit(authorization_header: str) -> dict:
    """验证 Nexus 调用令牌（NIT），返回其中的调用上下文声明。"""
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise ValueError("缺少 Authorization Bearer 令牌")

    token = authorization_header[len("Bearer "):]

    # 根据 token 的 kid 从 JWKS 获取对应公钥
    signing_key = _jwk_client.get_signing_key_from_jwt(token)

    # 校验签名、audience、issuer 与有效期（exp）
    claims = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience="nexus",
        issuer="nexus/invocation-token",
        options={"require": ["exp", "aud", "iss"]},
    )
    return claims
```

在 Web 框架（以 Flask 为例）中使用：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.post("/compute")
def compute():
    try:
        context = verify_nit(request.headers.get("Authorization", ""))
    except Exception:
        # 验证失败一律拒绝
        return jsonify({"error": "invalid nexus invocation token"}), 401

    # 验证通过后即可信任 NIT 中的上下文声明
    team_id = context["team"]["id"]
    app_id = context["app"]["id"]
    invocation_id = context["invocation"]["id"]

    # … 业务逻辑
    return jsonify({"ok": True})
```

在校验 NIT 之前，不要信任请求中的任何其他请求头或参数。 `x-nexus-app-token` / `x-nexus-user-token` 等令牌也应在 NIT 验证通过后再使用，且始终作为不透明令牌处理，不要解析或记录。

## 开发指南

远程服务能力的一些具体使用指南，请参考：

- [前端调用远程服务](/guide/development/remotes-calling-from-frontend)
- [服务端调用远程服务](/guide/development/remotes-calling-from-function)
- [远程服务作为模块解析器](/guide/development/remotes-used-extension-resolver)
- [远程服务作为事件处理函数](/guide/development/remotes-used-events-handler)
- [远程服务调用 REST APIs](/guide/development/remotes-call-rest-apis)
