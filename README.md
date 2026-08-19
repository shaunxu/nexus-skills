# PingCode Nexus Skills

PingCode Nexus 让你可以直接在 PingCode 平台上构建和部署自定义应用——项目页面、工作项面板、仪表盘部件、Wiki 内容块、事件处理函数、Webhook 等等。Nexus Skills 插件打包了多个面向 Nexus 的技能，让你的智能体可以脚手架应用、在部署前审查应用、排查生产环境问题，并围绕 Nexus CLI、Resolver、Custom UI、manifest 权限等平台专属概念提供结构化工作流。

## 包含内容

### 技能

插件在 `skills/` 下提供多个技能，每个技能都带有一个可供宿主加载的 `SKILL.md`：

**Nexus App Builder**（`skills/nexus-app-builder/`）引导从脚手架到上线的完整流程：`nexus create`、模板选择、Custom UI（React/Vue/Angular/JavaScript）与事件/Webhook 模板、部署与分发、扩展点 target 选择、跨产品 scope、外部域名，以及常见 CLI 与权限问题。

**Nexus App Reviewer**（`skills/nexus-app-reviewer/`）支持发布前的轻量级就绪审查与审计：manifest/模块连线、架构、运行时兼容性、依赖姿态、测试、部署就绪，以及明显的安全或可靠性信号。

**Nexus Debugger**（`skills/nexus-debugger/`）在出现问题时提供系统化排查：`nexus`/部署错误、Resolver 失败、白屏或 UI 缺失、scopes 与权限、外部 API 被拦截、UI Invoke 超时、事件/Webhook 不触发，以及在 PingCode 各产品中“突然不工作”的应用。

**Nexus Security Reviewer**（`skills/nexus-security-reviewer/`）执行结构化、Nexus 专属的白盒安全审计，基于规则资产检查授权（AuthZ）、注入、租户隔离、密钥处理、出站/外部域名、Webhook/Exposer 入口，并产出带 CVSS 评分、代码证据与 PoC 的报告。

| 组件 | 新增能力 | 示例 |
| --- | --- | --- |
| **Nexus App Builder 技能** | 脚手架、部署、分发、模块选择、CLI 工作流 | `nexus create`、`nexus deploy`、`nexus distribute`、扩展点 target、跨产品 scopes |
| **Nexus App Reviewer 技能** | 发布前审查：manifest 连线、架构、依赖、运维卫生 | 发布前审计、发现连线错误、检查部署就绪 |
| **Nexus Debugger 技能** | 诊断部署、运行时、UI 与权限问题 | 日志、白屏面板、Resolver 错误、应用安装后不可见 |
| **Nexus Security Reviewer 技能** | 白盒安全审计与可利用性报告 | AuthZ 越权、注入、租户隔离、Webhook 加固、静态分析工作流 |

## 前置条件

安装前请确保你拥有：

- 一个 [PingCode 开发者账号](https://developer.pingcode.com)
- 一个 [PingCode 注册企业](https://pingcode.com/signup)（用于分发、安装和验证应用）
- **Node.js 24+**（`node -v`）——Nexus CLI（`@pc-nexus/cli`）要求 `node >=24.0.0`
- **Python 3** 在 PATH 上可用（技能内的辅助脚本使用）

## 安装

使用 `skills` CLI 从 GitHub 安装全部技能：

```bash
npx skills@latest add shaunxu/nexus-skills --all
```

这会把四个技能安装到当前项目的 `.agents/skills/` 目录，并自动链接到受支持的智能体宿主。

只安装到全局（用户级）：

```bash
npx skills@latest add shaunxu/nexus-skills --all --global
```

只安装指定技能：

```bash
npx skills@latest add shaunxu/nexus-skills --skill nexus-app-builder
```

安装后重启你的智能体宿主，以便重新索引技能。

## 验证安装

安装完成后，尝试以下几项快速检查。

### 1. 验证技能层

提问：

> 帮我构建一个展示客户支持工单的项目页面。

你应该得到一个结构化的 Nexus 工作流：前置条件检查、模板选择、`nexus create`、代码定制、部署与分发——而不是泛泛的代码片段。

也可以确认其他技能是否可用：

- **审查：**例如“部署前帮我审查一下这个 Nexus 应用的 manifest 和源码。”
- **调试：**例如“我的 Nexus 工作项面板部署后白屏——帮我排查。”
- **安全：**例如“对这个 Nexus 应用做一次白盒安全审查，给出 CVSS 评分的发现。”

### 2. 验证 Nexus App Builder 技能

提问：

> 我想用 React Custom UI 创建一个仪表盘部件，从外部 API 拉取数据并展示。从哪里开始？

你应该得到涵盖模板选择（`react-custom-ui`）、扩展点 target、`nexus create`、Resolver 与 Bridge 调用、外部域名声明、`npm run build-web` 与部署分发的完整引导——而不是通用的 Nexus 教程。

## 可尝试的提示词

插件安装后，可以尝试如下提示：

- `创建一个工作项面板，展示来自外部 API 的相关支持工单。`
- `构建一个 Wiki 内容块，嵌入一个支持柱状、折线、饼图切换的交互式图表。`
- `添加一个仪表盘部件，按优先级汇总未关闭的工作项。`
- `创建一个事件处理函数，在工作项状态变更时发送 Webhook 通知。`
- `我的 nexus create 一直失败——帮我看看！`
- `把我的 Nexus 应用部署到开发环境。`
- `一个同时读取项目和 wiki 数据的应用需要哪些 scopes？`
- `部署前帮我审查这个 Nexus 应用的质量和安全。`
- `对这个 Nexus 应用做一次白盒安全审计，重点看 asApp 越权和 Webhook 认证。`
- `nexus deploy 报错 [error]——我应该检查什么？`

## 你会得到什么

| 组件 | 默认位置 | 用途 |
| --- | --- | --- |
| **Nexus App Builder** | `skills/nexus-app-builder/` | 创建、部署、分发；辅助脚本与参考文档（`SKILL.md`、`references/`、`scripts/`） |
| **Nexus App Reviewer** | `skills/nexus-app-reviewer/` | 发布前就绪审查（`SKILL.md`、README） |
| **Nexus Debugger** | `skills/nexus-debugger/` | 故障诊断与排查（`SKILL.md`、README） |
| **Nexus Security Reviewer** | `skills/nexus-security-reviewer/` | 白盒安全审计与规则资产（`SKILL.md`、`assets/`、`scripts/`） |
| **插件清单** | `plugin.json`、`.mcp.json` | 插件元数据 |

## 认证

Nexus CLI 负责认证：

```bash
nexus login
```

系统会引导你访问 [PingCode 开放平台](https://developer.pingcode.com/console/signup) 注册或登录，并在开发者中心「个人设置」中创建个人访问令牌。**只在你的终端中输入凭据——永远不要把令牌粘贴到对话中。**

验证登录状态：

```bash
nexus whoami --json
```

> **重要：** Nexus 没有 `nexus install` CLI 命令。应用通过 `nexus distribute` 分发后，必须由企业管理员在企业管理后台「应用审核」中手动安装；在管理员安装完成前，应用尚未上线。

## 故障排查

### 智能体没有使用 Nexus 技能

- 确认插件已通过 `npx skills@latest add shaunxu/nexus-skills --all` 成功安装
- 确认 `skills/`（安装后为 `.agents/skills/`）目录下包含 `nexus-app-builder`、`nexus-app-reviewer`、`nexus-debugger`、`nexus-security-reviewer`，且每个都带有 `SKILL.md`
- 重新加载或重启智能体宿主，使其重新索引技能

### Nexus 命令报认证错误

- 重新运行 `nexus login`
- 在 [PingCode 开放平台](https://developer.pingcode.com/console/signup) 创建新的个人访问令牌
- 用 `nexus whoami --json` 确认已登录

### `nexus create` 失败

- **CLI 需要交互式终端/无法渲染提示：** 在你自己的交互式终端中运行 `nexus create <app-name> --template <template>`
- **`nexus: command not found`：** 运行 `npm install -g @pc-nexus/cli`
- **Node 版本过低：** 安装或切换到 Node.js 24（`nvm install 24 && nvm use 24`）
- **未登录 / Unauthorized：** 引导用户创建令牌并在终端运行 `nexus login`

### 部署后白屏或资源 404

- `nexus deploy` 不会自动构建前端，前端改动后必须先运行 `npm run build-web`
- 确认 `manifest.yaml` 中 `resources[].path` 指向 `web/main/dist`
- 重新构建并部署：`npm run build-web && nexus deploy -e development`

## 了解更多

- [PingCode Nexus 开发者文档](https://developer.pingcode.com)
- [PingCode 开放平台](https://developer.pingcode.com/console/signup)

## 许可证

[MIT](LICENSE)
