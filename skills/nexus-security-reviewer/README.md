# Nexus 应用安全审查 Skill

对 PingCode Nexus 应用执行结构化、聚焦平台特性的白盒安全审查，产出证据驱动的安全审计报告。

## Skill 文件

- `SKILL.md`：触发条件、工作流与报告规范，供 agent 宿主读取。
- `assets/security-rules/`：全局与分类 Nexus 安全规则。
- `scripts/summarize_manifest.py`：manifest 结构化摘要脚本（仅做 manifest 层抽取与机械性观察，**不做**代码级数据流分析）。

## 规则布局

- `assets/security-rules/_global-nexus.mdc`
  - 所有 Nexus 白盒审查的全局基线与强制报告标准。
- `assets/security-rules/nexus-*/_index-*.mdc`
  - 分类索引文件，指向更深层的子规则并给出检测启发式。
- `assets/security-rules/nexus-*/*.mdc`
  - 分类下的深度检查项。

当前分类：

- `nexus-authn-authz/`：`as: "app"` 越权、Resolver/Exposer 授权缺失、display 条件绕过等。
- `nexus-injection/`：XSS、RCE、SSRF、SQL 注入、原型污染等。
- `nexus-tenant-isolation/`：FaaS warm start、全局状态、KVS（键值对存储，Key Value Pair Store）/CES（自定义实体存储，Custom Entity Store）/NOS（对象存储，Object Store）key 作用域等跨租户泄漏风险。
- `nexus-secrets-storage/`：硬编码凭据、KVS secret、`environment.variables` 误用、NOS 预签名 URL 等。
- `nexus-egress-remotes/`：后端出站、remotes、token 透传与重定向风险。
- `nexus-manifest-config/`：scope 最小化、CSP、egress URL 条目等 manifest 配置问题。
- `nexus-webhook-entrypoints/`：Webhook、Exposer 等公开入口点的认证与鉴权。
- `nexus-auditing/`：日志、错误处理、静态分析工作流与可观测性。
- `nexus-misc/`：依赖项（SCA）、许可证合规等杂项风险。

Nexus 当前没有与 Forge `forge-rovo-agents` 等价的智能体/Agent 扩展点分类。

## 使用流程

1. 首先阅读 `manifest.yaml`（若同时存在 `manifest.yml`，以 `manifest.yaml` 为准）。
2. 运行 `scripts/summarize_manifest.py` 生成 manifest 摘要，并在任何深度代码审查前阅读其输出。
3. 应用 `assets/security-rules/_global-nexus.mdc`。
4. 根据 manifest/代码信号，仅加载 `assets/security-rules/nexus-*/_index-*.mdc` 中相关的分类索引。
5. 仅当索引中的检测启发式与实际代码模式匹配时，才加载对应的深度子规则。
6. 对每个发现追踪「来源 → 校验/授权 → 汇聚点」，并以代码证据确认可利用性。
7. 报告已验证的发现，给出 CVSS v3.1 评分、影响、CWE 映射与可复现的测试线索。

### 产物目录约束

所有脚本输出与扫描产物（manifest JSON 摘要、Semgrep/gitleaks/npm audit 结果、PoC 脚本等）必须写入被审查项目目录**之外**的临时 artifact 目录，例如：

```bash
ARTIFACT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/nexus-security-review.XXXXXX")"
python3 scripts/summarize_manifest.py <project-root> --format markdown
python3 scripts/summarize_manifest.py <project-root> --format json -o "$ARTIFACT_DIR/manifest-summary.json"
```

NEVER 将产物写入被审查项目的源码树（包括其根目录、`security-audit-artifacts/` 或任何子目录），即使对应路径已被 `.gitignore` 忽略。

### Token 高效的规则加载

本 skill 使用两层加载模型：

- 第一层：全局基线 + 根据信号选中的分类索引。
- 第二层：仅对触发启发式的条目按需加载深度子规则。

避免一次性加载所有规则文件，以降低大型审查中的 token 消耗。

### 聚焦审查模式

当用户要求狭窄范围（例如仅 AuthN/AuthZ）时，只加载：

- `assets/security-rules/_global-nexus.mdc`
- 被请求分类的索引
- 该分类下匹配的子规则

即使在聚焦模式下，若在范围外观察到明显的关键发现，仍应在报告中提示。

## 与 Forge 安全审查的关键差异

- **清单文件**：Nexus 使用 `manifest.yaml`（优先）/`manifest.yml`；Forge 使用 `manifest.yml`。
- **入口形态**：Nexus 关注 Custom UI + `@pc-nexus/bridge`、Resolver、Exposer、Webhook、事件触发器（system/app/lifecycle/scheduled）、异步消费者；Forge 关注 UI Kit、Custom UI、Web Trigger 等。
- **授权模型**：Nexus 通过 `api.invoke(path, { as: "app" | "user", userId })` 区分应用身份与用户身份，越权风险集中在 `as: "app"` 路径与 Resolver/Exposer 授权缺失；Forge 对应 `asApp()`/`asUser()`。
- **存储抽象**：Nexus 使用 KVS（键值对存储）/CES（自定义实体存储）/NOS（对象存储），需关注 key 的租户/用户作用域与 NOS 预签名 URL；Forge 使用 Storage/Properties/Confluence 与 Jira 实体存储。
- **出站与远程**：Nexus 通过 `permissions.external.fetch`、`remotes[]`、`endpoints[]`、`exposer.routes[]` 控制；Forge 通过 `permissions.external.fetch` 与 `remotes` 控制。
- **SAST 工具链**：Forge 提供 FSRT（自研 IR/CFG + 跨过程数据流）；Nexus 目前**没有**等价的官方跨过程 SAST，`summarize_manifest.py` 只做 manifest 层抽取，代码级数据流依赖规则 + 人工/LLM 追踪。静态分析仅使用 Semgrep 社区 ruleset（`p/javascript`、`p/typescript`、`p/nodejsscan`）、`npm audit`、Snyk、gitleaks；`nexus-rules/` 自定义 Semgrep 规则目前未随 skill 分发，不要声称已运行。
- **Endpoint→Scope 映射**：Forge FSRT 依赖机器可读的 Atlassian REST endpoint 与 scope 映射表；PingCode 目前没有公开的同类数据，因此无法机械判定某个 `api.invoke` 路径所需的最小 scope，此类判断必须标注为「需人工核对 PingCode REST API 文档」。

## 示例提示词

### 1) 完整 Nexus 应用安全审查

```text
对这个 Nexus 应用源码执行白盒安全审查。
应用：
1) assets/security-rules/_global-nexus.mdc
2) assets/security-rules/nexus-*/ 下相关的分类索引与子规则
```

### 2) 聚焦 AuthN/AuthZ 审查

```text
对这个 Nexus 应用执行聚焦的 AuthN/AuthZ 审查。
应用：
- assets/security-rules/_global-nexus.mdc
- assets/security-rules/nexus-authn-authz/_index-authn-authz.mdc
- 相关的 nexus-authn-authz 子规则（asApp 越权、Resolver 授权缺失、display 条件绕过等）
```

### 3) 租户隔离与泄漏审查

```text
对这个 Nexus 应用执行租户隔离与数据泄漏审查。
应用：
- assets/security-rules/_global-nexus.mdc
- assets/security-rules/nexus-tenant-isolation/_index-tenant-isolation.mdc
- assets/security-rules/nexus-secrets-storage/_index-secrets-storage.mdc
```

### 4) 完整静态分析扫描

```text
按照 assets/security-rules/nexus-auditing/static-analysis-nexus.mdc 的完整工作流审查这个 Nexus 应用。
要求：
1) 应用 assets/security-rules/_global-nexus.mdc 以及所有相关的 nexus-* 索引/子规则。
2) 执行该子规则描述的完整静态分析工作流，包括：
   - Semgrep（p/javascript、p/typescript、p/nodejsscan 社区 ruleset）
   - npm audit
   - snyk test
   - gitleaks detect
3) 若缺少某个工具，安装后继续（告知安装了什么）。
注意：summarize_manifest.py 只做 manifest 抽取，不是跨过程 SAST；不要声称运行了未随 skill 分发的 Nexus 自定义 Semgrep 规则。
```

### 5) Manifest 权限与出站面审计

```text
审计这个 Nexus 应用的 manifest 权限、scopes、remotes、endpoints、exposer 与外部域名。
先运行 scripts/summarize_manifest.py 输出摘要，然后应用：
- assets/security-rules/_global-nexus.mdc
- assets/security-rules/nexus-manifest-config/_index-manifest-config.mdc
- assets/security-rules/nexus-egress-remotes/_index-egress-remotes.mdc
```
