# Nexus 应用调试器 Skill

诊断并修复 PingCode Nexus 应用中已知的故障模式。当存在可观察的症状、错误信息、行为异常、失败的命令或日志输出需要排查时使用。

本技能是故障/调试通道。它从 `nexus lint`、部署输出、`nexus logs`、`nexus serve` 隧道输出、堆栈跟踪、应用可见性问题、Resolver 错误、白屏、外部 API 拦截、UI Invoke 超时、事件/Webhook 不触发等证据出发，定位根因并直接修复。

## 适用场景

- `nexus deploy`、`nexus distribute`、`nexus lint`、`nexus serve` 或其他 Nexus CLI 失败
- 白屏、面板/项目页面/工作项面板/仪表盘部件/Wiki 内容块不显示，或安装后扩展点不出现
- Resolver 报错、`invoke()` 名称与 `resolver.define()` 不匹配、handler 路径问题、未定义（undefined）返回
- 权限/scope 失败、403/Unauthorized，或开发环境与生产/预发布环境行为不一致
- Custom UI 构建/部署问题、静态资源缺失（404）、前端不渲染
- 外部 API 请求被拦截、CSP 拦截外部字体/样式/脚本/图片/frame/媒体
- UI Invoke 超过 5 秒超时、请求/响应负载超限、内存/磁盘溢出、频率限制
- 事件处理函数、Webhook、定时任务未触发
- `nexus serve` 本地隧道断开、HMR 不生效、测试账号未绑定
- 此前正常运行的应用突然失败

## 不适用场景

- 没有观察到具体故障时的通用上线前就绪检查
- 深度安全审计、SAST、AuthZ、密钥、租户隔离、可利用性分析或 CVSS 评分
- 成本优化、调用次数缩减、存储/日志调优、内存调优或触发频率优化
- 从零创建一个新的 Nexus 应用

## 与其他技能的协作

- 使用 `nexus-app-builder` 完成新 Nexus 应用的创建、部署、分发与安装流程。
- 使用 `nexus-security-reviewer` 进行深度安全审计、SAST、AuthZ、密钥、租户隔离、出站/remotes 风险与 CVSS 评分。
- 对应的 `nexus-app-reviewer`（上线前架构/就绪评审）尚未编写；目前没有与平台资源消耗/成本优化对应的技能。

## 检查项

- **CLI 与环境**：Node.js 版本（必须 24.x 或更高）、`@pc-nexus/cli` 版本与登录状态（`nexus whoami`）、是否在应用根目录运行命令。
- **Manifest 装配**：模块/扩展点 key、`resources[].path`、`functions[].handler` 路径解析、`extensions[].resolver.function` 与 `functions[].key` 一致性、scopes、外部域名/CSP、products（PJM、Ship、Wiki、TestHub、Platform）。
- **构建/部署状态**：`nexus lint`（含 `--fix`）、Custom UI 构建产物（`web/main/dist`）、`nexus deploy`/`nexus distribute` 输出、开发/预发布/生产环境差异、版本号规则（Production 必须严格高于上一版本）。
- **运行时证据**：`nexus logs -e development`（仅限开发环境，保留 30 天）、按 Invocation ID 分组、单次调用日志、`nexus serve` 终端输出、Resolver 堆栈、权限错误、PingCode REST API 响应状态、Trace ID/Invocation ID。
- **源码装配**：前端 `invoke('name')` 与后端 `resolver.define('name')` 名称一致性、handler 具名导出、缺失文件、前后端契约不匹配、`remotes[].key` 与 `exposer.routes` 配置。
- **事件/Webhook**：`event.triggers[].events` 名称、filter 条件（如 `ignoreSelf`）、scheduled interval、隧道抢占、Webhook 触发 URL。
- **清理**：根因确认后移除临时调试日志（`console.error("[DEBUG] ...")`）、verbose 标记和临时配置。

## 调试流程

1. 分类症状：部署期、安装/可见性、运行时、UI 渲染、权限、生产/预发布专属、事件/Webhook，或回归。
2. 先跑低成本检查：`node -v`、`nexus --version`、`nexus lint`、依赖安装与前端构建状态。
3. 跟随证据：部署输出、`nexus logs`、`nexus serve` 隧道输出、堆栈、manifest 与源码装配。
4. 在确认第一个根因后立即修复，再继续更深层；多重独立缺陷时先修部署错误、重新部署，再查运行时日志。
5. 用最窄的相关命令验证，必要时重新 `nexus deploy` / `nexus distribute` 并由企业管理员在「应用审核」中重新确认安装。
6. 清理调试代码，最后再跑一次 `nexus lint`。

交互式例外：`nexus login` 与 `nexus serve` 必须由用户在自己的终端运行；其他诊断与修复命令由 agent 直接执行。

## 平台关键约束

- **CLI 与运行时**：使用 `nexus deploy/distribute/lint/logs/serve`；应用必须经企业管理员在「应用审核」中安装后才可见。
- **环境与日志**：`nexus logs` **仅支持 Development 环境**（保留 30 天）；Staging/Production 需到开发者中心「监控 > 日志记录」查看，且生产日志是否记录取决于企业管理员的安装设置。
- **本地调试**：`nexus serve` 支持 `-f/--debugFunctionHandlers` 限定函数、`--debug` 在 9229 端口挂载 IDE 断点，并通过 `nexus.json` 配置前端 HMR 端口。
- **Node 版本**：`@pc-nexus/cli` 要求 Node.js 24.x 或更高。
- **前端构建**：`nexus deploy` 不会自动构建 Custom UI，`resources[].path` 必须指向 `web/main/dist`；需手动执行 `npm run build-web`。
- **版本与分发**：Production 强制版本号严格递增；公有云自动升级，私有部署需通过 `nexus packup` 生成 `.npk` 由企业管理员上传。
- **平台限制**：UI Invoke 超时为 5 秒，请求负载上限 512 KB、响应上限 5 MB，单次调用内存/磁盘各 512 MB，仅 `/tmp` 可写；频率限制按用户/安装实例/应用单环境分级。
- **出站与 CSP**：`permissions.external.fetch.backend/client` 控制前后端出站；iframe 还需按 `fonts/styles/scripts/images/frames/media` 分类声明 CSP；`*.example.com` 不匹配父域名本身。
- **身份与授权**：通过 `api.invoke(path, { as: "user" | "app", userId })` 区分用户身份与应用身份。

## 示例提示词

```text
我的 Nexus 工作项面板部署后白屏，帮我调试。
```

```text
nexus deploy 报 manifest 校验失败，错误是：<粘贴错误>
```

```text
我的 Resolver 返回 undefined，nexus logs 里也没有报错。
```

```text
应用在开发环境正常，但生产环境 on customer.pingcode.com 上 403。
```

```text
调用 PingCode REST API 时返回 Unauthorized，我刚加了新功能。
```

```text
nexus serve 隧道一直断开，HMR 也不生效。
```

```text
事件处理函数/Webhook 完全不触发。
```

完整诊断工作流与常见错误模式见 [SKILL.md](SKILL.md)。
