---
name: nexus-app-reviewer
description: >
  对 PingCode Nexus 应用执行轻量级发布前就绪审查，覆盖 manifest/模块连线、架构、运行时兼容性、
  依赖姿态、测试、部署就绪以及明显的安全或可靠性信号。当用户说"审查我的 Nexus 应用"、
  "部署前检查"、"这个应用能发布了吗"、"审查 manifest"、"通用应用审查"、"发布就绪检查"，
  或要求做一次广泛的质量检查时使用。不要用于深度安全审计/SAST/可利用性审查，
  或诊断已知故障；这些分别路由到 nexus-security-reviewer 和 nexus-debugger。
license: Apache-2.0
labels:
  - pingcode
  - nexus
  - review
  - release
  - readiness
maintainer: pingcode
namespace: nexus
---

# Nexus App Review

对 PingCode Nexus 应用执行一次通用的发布就绪审查。本 skill 是广泛应用审查的入口，不替代安全或调试等专业 skill。

## 边界

适用场景：

- 部署前与发布就绪检查。
- 通用架构与可维护性审查。
- Manifest/模块/资源/函数连线检查。
- 运行时、依赖、包与脚本的健全性检查。
- 基础测试/部署就绪与运维卫生检查。
- 发现应触发更深入专业审查的明显安全或可靠性信号。

当用户主要意图是以下情况时，改用其他 skill：

- 深度安全审计、SAST、授权（AuthZ）、密钥、租户隔离、可利用性或 CVSS 报告 -> `nexus-security-reviewer`。
- 已知故障、错误信息、白屏、部署/安装失败、Resolver 报错、应用缺失或日志/隧道诊断 -> `nexus-debugger`。

Nexus 目前没有成本优化相关的 skill，平台也没有公开的计费规则；如用户关心资源消耗，仅作为代码模式观察记录，不做具体成本估算或交接。

如果广泛审查中发现深度安全/调试问题，将其作为交接建议列出，而不是复制专业工作流。

## 审查规则

- 先审计，不修改。除非用户明确要求应用修复，否则不要修改应用文件。
- 在读代码之前不要下结论。
- 优先给出具体的文件/行证据。
- 发现聚焦于 bug、发布阻塞项、有意义的风险以及缺失的校验。
- 不要在本 skill 中运行完整 SAST 工具。在必要时推荐专业 skill。
- 不要把推测性的安全观察报告为已确认的漏洞。

## 工作流

1. 读取 `manifest.yaml`（若同时存在 `manifest.yml`，以 `manifest.yaml` 为准，与 `nexus-app-builder` 一致）。
   - 识别 `extensions`（扩展点 target、resource、resolver.function、display 条件）、`functions`（key、handler）、`resources`（key、path）、`permissions`（scopes、external.fetch、content、其他 CSP 类别）、`event.triggers`（system/app/lifecycle/webhook/scheduled）、`remotes`、`endpoints`、`exposer`、`storage.entities`、`async.queues`/`async.consumers`、`environment.variables`。
   - 验证被引用的 handler、resource path、function key、extension target 是否存在且互相一致。
2. 读取 `package.json`（根目录与 `web/main/`）。
   - 检查 `@pc-nexus/*` 包是否匹配、scripts、运行时假设（Node.js >= 24）、直接依赖、明显未使用/缺失的包。
3. 检查源文件。
   - 后端/Resolver：`resolver.define`、handler 具名导出、`api.invoke` 调用（注意 `as: "app"` vs `as: "user"`）、存储使用（KVS/CES/NOS）、`fetch.request` 外部调用、`remote.invoke`、日志、错误处理、异步队列。
   - 前端（Custom UI）：`web/main/` 入口、`@pc-nexus/bridge` 的 `invoke()`/`api.invoke()`/`remote.invoke()` 模式、loading/error 状态、`web/main/package.json` 中的构建脚本（`build`/`build-web`）。不要把 `web/main/dist` 是否存在作为检查项——它是被 `.gitignore` 的本地产物，干净 checkout 中缺失是正常的。
4. 检查测试与项目文档（如存在）。
   - 仅当行为风险足以支撑时才记录缺失测试。
5. 运行 `nexus lint`（可在非交互环境安全运行），收集 manifest 与代码的机械性问题作为证据。
6. 产出优先级排序的就绪报告。

## 检查项

### 发布阻塞项

- Manifest 引用了缺失的 handler 文件/具名导出、resource path 或 function key。
- 前端 `invoke('name')` 调用的名称与后端 `resolver.define('name')` 注册的名称不匹配（逐字区分大小写）。
- `extensions[].resolver.function` 不等于任何 `functions[].key`。
- `extensions[].resource` 不等于任何 `resources[].key`。
- 实际 API/外部 fetch 使用所需的 scopes 或 `permissions.external.fetch.backend`/`client` 条目缺失。
- `functions[].handler` 格式不符合 `<file>.<export>` 正则约束，或指向不存在的文件/导出。
- 运行时（Node.js < 24）、包版本或模块语法可能导致 `nexus lint`、构建、部署或安装失败。
- `resources[].path` 未指向 `web/main/dist`，或 `web/main/package.json` 缺少构建脚本（`build-web` 或 `build`）。注意：`web/main/dist` 在干净 checkout 中缺失是正常的（该目录被 `.gitignore`），不要把 dist 缺失本身当作问题；部署时 `nexus-app-builder` 的部署脚本会自动执行 `npm install` 与 `npm run build-web`。仅当 dist 已存在但明显早于 `web/main/src` 源码改动时，才作为提示性信息记录。
- 应用没有明确的方式触达其主用户流程（例如扩展点 target 错误或 display 条件恒为 false）。
- `manifest.yaml` 中 `app.version` 缺失或不是有效的语义化版本。注意：部署到 Production 时版本号必须严格高于上一版本、Development 要求不低于原版本，这一比较无法机械判断，需在部署时人工确认目标环境的当前版本。

### 架构与可维护性

- 扩展点 `target` 与预期 UX 面匹配（项目页面、工作项面板、仪表盘部件、Wiki 内容块等）；逐字对照官方扩展点列表，不编造 target。
- Resolver 边界清晰，没有随应用规模变得过度单体化。
- 敏感或特权逻辑保留在后端；前端不直接处理凭据、令牌或授权决策。
- `display` 条件仅用于前端展示，不作为安全边界；敏感操作应在后端通过 `authorize` 或业务逻辑校验。
- 仅用于 UI 格式化/转换的逻辑不被不必要地强制经过后端函数。
- 用户工作流的错误处理充分。
- UI Invoke 中不执行长耗时任务（UI Invoke 超时 5 秒；其他调用超时 60 秒）；长任务应使用异步队列（`async.queues`/`async.consumers`）。
- 代码组织与现有项目风格一致。

### 轻量级安全信号

仅标记明显信号，深度验证推荐使用 `nexus-security-reviewer`：

- 宽泛的写/管理员 scope，但代码中看不到对应使用。
- 用户触发的 Resolver 中使用 `api.invoke(path, { as: "app" })` 而没有明显的授权检查。
- 硬编码凭据或 token 样式字面量。
- 后端 `fetch.request` 调用的外部域名未在 `permissions.external.fetch.backend` 中声明。
- 前端访问外部资源（字体、样式、脚本、图片、frame、媒体）未在 `permissions.external` 对应类别中声明。
- Webhook 事件触发器（`event.triggers[].type: webhook`）没有可见的认证策略。
- Exposer 路由没有可见的授权/scope 校验。
- 完整 payload/请求日志可能暴露用户、租户或密钥数据。

注意：PingCode 目前没有公开的 REST endpoint 到 scope 的机器可读映射表，因此**不能**机械判定某个 `api.invoke` 路径所需 scope 是否最小化。此类观察标注为「需人工核对 PingCode REST API 文档」，给出待核对的路径与当前 scope，不要猜测。

### 轻量级可调试性信号

仅标记就绪缺口；观察到实际故障时使用 `nexus-debugger`：

- 异步 UI 路径周围缺少 loading/error 状态。
- 重要失败周围日志要么过于嘈杂，要么缺失。
- README 或脚本没有说明如何 lint/build/deploy/test。
- 除了 `nexus lint` 之外，应用没有明显的本地验证命令。
- `nexus logs` 仅支持开发环境；Staging/Production 需在开发者中心查看日志——检查应用是否有足够的错误日志以便生产排障。

### 运维与部署就绪

- `manifest.yaml` 中 `app.id`、`app.version` 必需字段齐全（`app.id` 由 `nexus create` 生成，不应手动修改；应用名在开发者中心设置，不在 manifest 中声明，不要将 `app.name` 缺失误报为问题）。
- 根目录与 `web/main/` 的 `package.json` 中 scripts 健全（典型为 `build`、`build-web`、`lint` 等）。
- `.gitignore` 覆盖 `node_modules/`、`web/main/dist/`、`__pycache__/`、`.DS_Store` 等本地产物。
- 依赖未锁定到已知有漏洞或过旧的版本（仅做明显信号标记，不运行 `npm audit`——那属于安全审查范围）。
- `environment.variables` 中不包含明文密钥；Nexus 没有提供官方推荐的密钥注入方式，密钥管理由开发人员自行负责，审查时仅标记疑似硬编码的密钥字面量（深度检查移交 `nexus-security-reviewer`）。
- 分发/安装流程已记录：Nexus 没有 `nexus install` CLI，分发后需企业管理员在「应用审核」中手动安装。

## 输出格式

返回简洁的 Markdown 报告：

```markdown
# Nexus 应用审查结果

## 摘要
- 就绪状态：就绪 | 需修改 | 阻塞
- 最高风险领域：<manifest | resolver 连线 | 权限 | 依赖 | 测试 | 运维卫生>
- 已检查文件：<简短列表>
- 专业 skill 交接建议：<无 | 安全 | 调试>

## 发现

1. [严重 | 警告 | 信息] <标题>
   - 证据：`<file:line>` 与观察到的模式
   - 影响：<为什么影响发布就绪>
   - 建议：<具体修复或专业 skill 交接>

## 无问题领域
- <已检查且无问题的重要类别>

## 建议下一步
- <应用修复 | 运行专业审查 | deploy/lint/test 命令>
```

如果没有发现，说明应用从本次通用审查角度看起来就绪，并列出本次有意不覆盖的专业审查项。

## 已知限制

- 本 skill 不运行完整 SAST、`npm audit` 或 gitleaks；这些属于 `nexus-security-reviewer` 的范围。
- PingCode 目前没有公开的 REST endpoint 到 scope 的映射表，无法机械判定 scope 最小化；相关发现标注为需人工核对。
- `nexus lint` 可在非交互环境安全运行，审查时应执行它来收集 manifest/代码问题证据；但不应执行 `nexus deploy`、`nexus distribute` 或任何修改应用/远程状态的命令，除非用户明确要求。
- 本 skill 不替代 `nexus-app-builder` 的创建/部署工作流，也不替代 `nexus-debugger` 的故障诊断。

## 示例触发短语

- "审查我的 Nexus 应用，我准备部署了。"
- "这个 Nexus 应用能发布了吗？"
- "对这个 manifest 和源码做一次通用应用审查。"
- "检查这个 Nexus 应用是否发布就绪，有深度安全问题就路由到对应 skill。"
- "Review my Nexus app before I deploy it."
- "Is this Nexus app ready to ship?"
