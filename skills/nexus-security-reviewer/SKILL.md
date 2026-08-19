---
name: nexus-security-reviewer
description: >
  对 PingCode Nexus 应用执行结构化、Nexus 专属的白盒安全审查，产出证据驱动的安全审计报告。
  当用户要求对 Nexus 应用进行安全审查、安全审计、漏洞评估、渗透式代码审查、授权（AuthZ）审查、
  租户隔离分析、Webhook/Exposer 加固或运行静态分析时使用。不要用于通用 PingCode 配置审查、
  自动化规则，或脱离 Nexus 应用上下文的 PingCode REST API 调用审查。
license: Apache-2.0
labels:
  - pingcode
  - nexus
  - security
  - review
  - audit
maintainer: pingcode
namespace: nexus
---

# Nexus Security Review

对 PingCode Nexus 应用执行聚焦于平台特性的白盒安全审查，报告经证据验证的发现，包含可利用性、影响、代码证据和修复建议。

## Token 高效默认

默认使用 manifest 驱动的规则路由以降低 token 用量。不要一次性加载所有规则文件。

## 规则资产

审查规则打包在本 skill 的 `assets/security-rules/` 目录下：

- 全局基线：`assets/security-rules/_global-nexus.mdc`
- 分类索引：`assets/security-rules/nexus-*/_index-*.mdc`
- 分类深度检查：`assets/security-rules/nexus-*/*.mdc`

## 执行强制要求

当本 skill 被触发时：

1. 首先从本 skill 目录运行 manifest 摘要脚本（等价于 Forge review 中 FSRT 的位置，但**不做**过程间数据流分析，仅产出结构化清单与机械性观察）。脚本输出与后续所有扫描产物 MUST 写入**被审查项目目录之外**的临时 artifact 目录，NEVER 写入目标项目源码树：
   - 先创建临时目录（示例，agent 可按运行环境调整）：
     `ARTIFACT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/nexus-security-review.XXXXXX")"`
   - 生成 Markdown 摘要到 stdout 供 agent 直接阅读：
     `python3 scripts/summarize_manifest.py <nexus-project-root-directory> --format markdown`
   - 同时写入一份 JSON 证据到 artifact 目录：
     `python3 scripts/summarize_manifest.py <nexus-project-root-directory> --format json -o "$ARTIFACT_DIR/manifest-summary.json"`
   - 若项目根目录同时存在 `manifest.yaml` 与 `manifest.yml`，以 `manifest.yaml` 为准（与 `nexus-app-builder` 一致）。
   - 若脚本报错（无 manifest、YAML 解析失败等），停止并把错误展示给用户，不要猜测 manifest 内容。
   - 审查结束后告知用户 `ARTIFACT_DIR` 路径；除非用户明确要求，不要自动删除（用户可能需要留存证据），也不要把它移到目标项目内。
2. 在任何深度代码审查前阅读脚本输出的 manifest 摘要（entrypoints、scopes、egress、remotes、exposer、event triggers、storage、environment variables、observations）。
3. 首先加载 `assets/security-rules/_global-nexus.mdc`。
4. 仅加载与 manifest/代码信号相关的分类索引规则。
5. 只有在代码中观察到匹配的检测启发式时才加载深度子规则。
6. 基于证据进行安全审查，覆盖：
   - AuthN/AuthZ（`as: "app"` 越权、Resolver/Exposer 授权缺失、display 条件绕过）
   - 注入与输入校验（XSS、RCE、SSRF、原型污染、CES/NOS/api.invoke 路径注入）
   - 租户隔离与跨租户泄漏（FaaS warm start、全局状态、KVS/CES/NOS key 作用域）
   - 密钥与存储（硬编码凭据、KVS secret、environment.variables 误用、NOS 预签名 URL）
   - 出站、remotes、CSP 与 manifest 权限（通配符域名、unsafe-inline/unsafe-eval、NIT JWT 校验、token 透传）
   - 公开入口点（Webhook、Exposer、系统/生命周期/定时事件）
   - 依赖项（SCA）与其他杂项风险
7. 除非用户明确要求修复，不要修改应用代码。
8. 所有扫描输出与生成物（Semgrep/gitleaks/npm audit 结果、manifest JSON 摘要、PoC 脚本等）写入上面创建的 `ARTIFACT_DIR`，即被审查项目目录之外的单一专用临时目录。NEVER 写入被审查项目的源码树（包括其根目录、`security-audit-artifacts/` 或任何子目录），即使用户的 `.gitignore` 已忽略对应路径也不例外。

## 规则路由工作流

### Phase 1：侦察（强制）

首先通过 `summarize_manifest.py` 输出与 `manifest.yaml` 本身抽取：

- `permissions.scopes`
- `permissions.external.fetch.backend` / `permissions.external.fetch.client`
- `permissions.content.scripts` / `permissions.content.styles`
- 其他 CSP 指令（`fonts`、`styles`、`frames`、`images`、`media`、`scripts`）
- `extensions[]`（target、resource、resolver.function、display 条件）
- `functions[]`（key、handler）
- `event.triggers[]`（system / app / lifecycle / webhook / scheduled）
- `remotes[]`（baseUrl、auth.userToken/appToken、operations）
- `endpoints[]`
- `exposer.routes[]` 与 `exposer.scopes[]`（自定义 `ncp:` scope）
- `storage.entities[]`
- `async.queues[]` / `async.consumers[]`
- `environment.variables[]`

构建执行映射：

- Custom UI 入口 → `@pc-nexus/bridge` `invoke()` / `remote.invoke()` → Resolver / Endpoint / Remote handler
- 外部入口（Webhook、Exposer、事件处理器、定时任务、异步消费者）
- `api.invoke(path, { as: "app" })` vs `api.invoke(path, { as: "user", userId })` 路径
- 后端 `fetch.request` 出站目标及其域名
- `remote.invoke` 调用及其 remote key

脚本的 `functions.handler_refs` 字段已经反向汇总了每个后端函数被哪些入口引用，可直接作为执行映射的起点。`observations` 数组列出机械性问题（wildcard scope、unsafe-eval、未解析 handler、Webhook 公开入口提醒等），这些是**线索而非已确认漏洞**，必须按相应分类规则验证后才能写入最终报告。

### Phase 2：索引规则选择（两层加载）

始终先加载：

- `assets/security-rules/_global-nexus.mdc`

然后根据信号加载对应分类索引：

| 信号 | 加载 |
| --- | --- |
| 任何有意义的 scope 使用、写/变更操作或 `as: "app"` 调用 | `assets/security-rules/nexus-authn-authz/_index-authn-authz.mdc` |
| `event.triggers[].type: webhook`，或存在 exposer 路由 | `assets/security-rules/nexus-webhook-entrypoints/_index-webhook-entrypoints.mdc` |
| `permissions.external.fetch`、`remotes`、`endpoints` 或后端 `fetch.request` 调用 | `assets/security-rules/nexus-egress-remotes/_index-egress-remotes.mdc` |
| `eval`/`new Function`、`dangerouslySetInnerHTML`、CES 条件构造、NOS key、`fetch.request` 用户可控 URL 等注入 sink | `assets/security-rules/nexus-injection/_index-injection.mdc` |
| 多租户模式、模块级/全局状态、缓存复用、KVS/CES/NOS key 拼接 | `assets/security-rules/nexus-tenant-isolation/_index-tenant-isolation.mdc` |
| 凭据/token/secret 处理、`environment.variables`、KVS `secret: true`、NOS 预签名 URL | `assets/security-rules/nexus-secrets-storage/_index-secrets-storage.mdc` |
| 过宽或可疑 scope、CSP 放宽、通配符出站域名、manifest/remotes/exposer 配置异常 | `assets/security-rules/nexus-manifest-config/_index-manifest-config.mdc` |
| 基线日志/错误处理/静态分析/可观测性问题 | `assets/security-rules/nexus-auditing/_index-auditing.mdc` |
| 依赖/package 风险、过时或停维包、许可证合规 | `assets/security-rules/nexus-misc/_index-misc.mdc` |

子规则策略：

- 读完索引后，只加载与代码中实际观察到的检测启发式匹配的子规则。
- 不要预先加载某个分类下的所有子规则。

### Phase 3：分析与验证

对每个加载的分类：

1. 枚举可达入口点。
2. 追踪 来源 → 校验/授权 → 汇聚点。
3. 用代码证据确认可利用性。
4. 对已确认的发现按 CVSS v3.1 评分。

## 聚焦审查模式

如果用户要求狭窄范围的审查（例如仅授权），加载：

- 全局基线
- 请求的分类索引
- 该分类下匹配的子规则

仍需提及在范围外观察到的任何明显关键发现。

## 审查工作流

1. 构建执行映射：
   - Custom UI 入口与 Bridge 调用
   - Resolver、Exposer、Webhook、事件、异步消费者 handler
   - `api.invoke(..., { as: "app" })` / `as: "user"` 调用路径
   - 外部 egress、remotes、endpoints 与触发入口
2. 对每个发现追踪 来源 → 校验/授权 → 汇聚点。
3. 在分类为已确认漏洞前验证可利用性。
4. 把不可利用的加固观察放在独立的「需验证」章节。
5. 为每个问题提供文件级证据和实用的测试线索。

## 静态分析模式

如果用户要求完整扫描，按以下文件描述的完整工作流执行：

- `assets/security-rules/nexus-auditing/static-analysis-nexus.mdc`

期望使用的工具（在本机可用时）：Semgrep（社区 ruleset `p/javascript`、`p/typescript`、`p/nodejsscan`）、`npm audit`、Snyk、gitleaks。

注意：与 Forge 的 FSRT 不同，Nexus 目前**没有**官方的跨过程数据流 SAST 工具；`summarize_manifest.py` 仅做 manifest 层结构化抽取与机械性观察，不替代代码级数据流分析。

`assets/security-rules/nexus-auditing/static-analysis-nexus.mdc` 中示例了一组 `./nexus-rules/` 自定义 Semgrep 规则，但该目录目前未随 skill 分发。审查时仅使用 Semgrep 社区 ruleset（`p/javascript`、`p/typescript`、`p/nodejsscan`）；对 `as: "app"` 授权、Webhook 认证、token 流向外部域等关键类别，依赖 MDC 规则 + 代码阅读追踪，不要声称已运行 Nexus 自定义 Semgrep 规则。

## 输出要求

- 提供 Markdown 安全审计报告。
- 已确认可利用的发现按 CVSS v3.1 严重性与影响排序。
- 每个已确认发现包含：
  - CVSS 向量字符串与基础评分
  - 严重性等级
  - 可利用性与影响
  - 文件证据与 来源→汇聚点 追踪
  - CWE 映射
  - 可复现的 PoC/测试步骤（具体命令、完整路径、方法、头与 body）
- 包含假设与证据缺口。
- 存在漏洞时不得只报告扫描器计数。

报告模板与更细的强制要求（PoC 格式、依赖项发现字段、artifact 目录约束等）以 `assets/security-rules/_global-nexus.mdc` 中「强制报告标准」章节为准。

## 已知限制（不要在这些方向上编造工具能力）

- **无跨过程 SAST**：Forge FSRT 用自研 IR/CFG + 数据流检查 `asApp()` 授权路径、token 流向外部域、Web trigger 认证守卫等。Nexus 暂无等价工具。这些类别必须通过阅读代码 + 应用对应 MDC 规则完成，结论中要说明证据来源是人工/LLM 代码追踪而非自动分析器。
- **无 endpoint→scope 映射表**：Forge FSRT 的 `PermissionChecker` 依赖一份机器可读的 Atlassian REST endpoint 与 scope 映射（`atlassian_rest_api_endpoints.txt`）来判断「代码实际调用 vs manifest 声明的 scope」。PingCode 目前没有公开的同类映射数据。因此 `summarize_manifest.py` 只能标记通配符/过宽 scope、scope 与 remote auth 不匹配、storage scope 缺失等可机械判定的问题，**不能**判定某个 `api.invoke` 路径的 scope 是否最小化。遇到此类判断时，MUST 标注为「需人工核对 PingCode REST API 文档」并给出待核对的路径与 scope，不要猜测。
- **自定义 Semgrep 规则未内置**：见上方「静态分析模式」章节说明，仅使用社区 ruleset。
- **脚本本身不解析代码**：它只读 manifest。所有代码级信号（`api.invoke`、`fetch.request`、`kvs.set`、`dangerouslySetInnerHTML` 等）仍需通过代码阅读/搜索或 Semgrep 收集。

## 示例触发短语

- "Review this Nexus app for security"
- "对我的 Nexus 应用做一次白盒安全审计"
- "检查这个应用的 asApp 越权、Webhook 认证和租户隔离问题"
- "Run full static analysis for this Nexus codebase"
- "审计这个 Nexus 应用的 manifest 权限、scopes 和外部域名"
