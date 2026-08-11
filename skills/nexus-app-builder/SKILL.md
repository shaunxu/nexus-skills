---
name: nexus-app-builder
description: 引导构建、部署、分发、排查和安装 PingCode Nexus 应用——使用 Nexus CLI（`nexus create`、`nexus deploy`、`nexus distribute`）以及 Custom UI（React/Vue/Angular/JavaScript）或事件/Webhook 模板构建的自定义扩展。当用户希望创建 Nexus 应用（项目页面、工作项面板、仪表盘部件、Wiki 内容块、事件处理函数、Webhook 等），遇到 Nexus CLI 或部署报错，或需要了解 Resolver、Custom UI、manifest 权限、scope、外部域名、日志/调试等 Nexus 专属概念时使用。不要用于通用的 PingCode 配置、自动化规则，或脱离 Nexus 应用上下文的 PingCode REST API 调用。
license: Apache-2.0
labels:
  - pingcode
  - nexus
  - custom-ui
  - pjm
  - ship
  - wiki
  - testhub
maintainer: pingcode
namespace: nexus
---
# Nexus App Builder

**构建 Nexus 应用时，agent MUST 按顺序完成本工作流。不要跳步，也不要用手动说明代替运行下方脚本。**

## 关键规则

1. **始终使用 `nexus create` 脚手架应用**——它会注册应用并生成有效的 `app.id`。
2. **绝不手动脚手架**——没有有效 `app.id` 的应用无法部署。
3. **如果 `nexus create` 失败，STOP**——告知用户并提供需要在交互式终端中手动运行的命令。
4. **绝不在对话中索要或接收 API 令牌**——令牌属于敏感信息；引导用户在自己的终端运行 `nexus login` 并在提示时粘贴令牌。
5. **存在多个可选项时始终让用户选择**（例如开发环境、站点域名、模板）——绝不代为决定。
6. **安装/分发时始终向用户询问 PingCode 站点域名**——绝不尝试从其他应用、环境变量或其他来源推断。站点只传域名（如 `your-domain.pingcode.com`），不带协议、端口或路径。
7. **部署与分发始终运行部署脚本**——不要只把手动的 `nexus deploy` / `nexus distribute` 命令作为主要产出交给用户，应自行运行 `scripts.deploy_nexus_app`。
8. **Nexus 没有 `nexus install` CLI 命令**——应用分发后必须由企业管理员在企业管理后台「应用审核」中手动安装；在管理员安装完成前，NEVER 宣称应用已上线。
9. **所有包名使用 `@pc-nexus/*` 前缀，CLI 命令为 `nexus`**——NEVER 照搬 Atlassian Forge 的 `forge` 命令、`@forge/*` 包名、Jira/Confluence API 或模块名。
10. **文件名固定为 `manifest.yaml`**——NEVER 使用 `manifest.json` 或 `manifest.yml`；NEVER 手动修改 `nexus create` 生成的 `app.id`。
11. **前端改动后 ALWAYS 先 `npm run build-web` 再 `nexus deploy`**——`nexus deploy` 不会自动构建前端，`resources[].path` 必须指向 `web/main/dist`。
## 参考文档

本技能允许引用 `references/` 目录中的以下文档：

| 文档 | 用途 |
| --- | --- |
| `references/nexus-development-guide.md` | 从零创建、部署、分发、安装、调试的完整路径与平台限制 |
| `references/nexus-app-manifest-guide.md` | `manifest.yaml` 结构、字段、权限、scopes、外部资源、事件、存储等 |
| `references/nexus-backend-developer-guide.md` | Resolver、事件处理函数、PingCode/外部 API 调用、存储、异步队列、Exposer |
| `references/nexus-custom-ui-developer-guide.md` | Custom UI iframe 模型、Bridge/Capability API、前端框架、HMR 调试 |
| `references/list-nexus-extensions.md` | 按产品（PJM、Ship、Wiki、TestHub、Platform）分类的扩展点 `target` 列表 |

NEVER 引用 `samples/` 或 `wiki/` 目录下的内容。

### 在线文档搜索

当本地 `references/` 无法回答以下类型的问题时，MUST 使用 `scripts/search_nexus_docs.py` 在线检索官方文档（数据源：`https://developer.alpha.pingcode.live/sitemap.xml`），而不是凭记忆回答：

- 具体的 CLI 命令参数、字段或版本差异（例如 `nexus variables set`、`nexus ces`、`nexus webtrigger`）。
- `manifest.yaml` 中不熟悉的字段、权限 scope、exposer、realtime、async 等细节。
- SDK / Bridge / Capability 的具体 API 签名、返回值或版本行为。
- 扩展点 `target` 的属性、上下文（context）字段、display 条件。
- 任何你不确定、可能编造或本地参考资料未覆盖的 Nexus 专属概念。

```bash
python3 -m scripts.search_nexus_docs "<关键词>" [--max-pages 3] [--json]
```

脚本会在线抓取 sitemap → 按 URL 与页面标题/描述打分 → 下载排名靠前页面并返回 `<main>` 正文片段。**无本地缓存**，每次实时检索。NEVER 用记忆或猜测替代检索；检索后引用具体页面 URL 作为依据。

> **注意：** sitemap 中的 URL 路径均为英文关键词（例如 `custom-ui-with-react`、`permissions-content`、`functions-resolvers`），首轮打分依赖 URL 匹配。调用时 **MUST 尽量使用英文关键词**（如 `custom ui react`、`manifest permissions`、`resolver`、`webhook`），而非中文，否则会显著降低命中率。正文片段支持中文显示，仅搜索词需用英文。

## Agent 工作流

**按顺序完成步骤 0–5。脚本应由你亲自运行，而不是只指示用户运行。**

### 步骤 0：前置条件（缺失时自动安装）

在做任何其他操作之前，按 `references/nexus-development-guide.md` 检查并安装：

1. **Node.js** — 运行 `node -v`。必须为 Node.js 24.x 或更高版本（`@pc-nexus/cli@0.5.1` 要求 `node >=24.0.0`，文档示例版本 `v24.14.1`）。低于 24 时：
   - **macOS（Homebrew）：** `brew install node`
   - **nvm：** `nvm install 24 && nvm use 24`
   - **fnm：** `fnm install 24 && fnm use 24`
   - **其他：** 通过 Node.js 官网下载安装。

2. **Nexus CLI** — 运行 `nexus --version`。缺失时固定安装已确认版本：
   ```bash
   npm install -g @pc-nexus/cli@0.5.1
   ```
   NEVER 使用 `sudo npm install -g` 或 root 用户安装；如遇权限错误，修复 npm 全局目录权限后重试。
3. **Nexus 登录** — 运行 `nexus whoami --json`。未登录时：
   - **绝不在对话中索要或接收令牌**。
   - 引导用户：访问 `https://developer.pingcode.com/console/signup` 注册或登录 PingCode 开放平台，在开发者中心个人设置中创建个人访问令牌并复制。
   - 让用户**在自己的终端**（不要通过 agent）运行 `nexus login`，按提示输入令牌。
   - 示例话术：*“你需要登录 Nexus。请访问 https://developer.pingcode.com/console/signup 创建个人访问令牌，然后在你的终端运行 `nexus login` 并在提示时粘贴令牌——不要把令牌贴在这里。”*
   - 用户确认登录后重试工作流。

按顺序安装：先 Node.js（npm 依赖），再 Nexus CLI，再登录。安装后重试工作流。

### 步骤 1：确认模板与扩展点

根据用户需求选择模板和扩展点：

- 模板由 `scripts/create_nexus_app.py` 维护，支持：
  - `react-custom-ui`（推荐）
  - `angular-custom-ui`
  - `vue-custom-ui`
  - `javascript-custom-ui`
  - `event-typescript`
  - `webhook-typescript`
- Custom UI 模板优先选择 `react-custom-ui`；仅当团队明确要求时才选择 Angular/Vue/JavaScript。
- 查阅 `references/list-nexus-extensions.md` 确定合适的扩展点 `target`（例如 `pcm:pjm:project:page`、`pcm:pjm:workitem:panel`、`pcm:global:dashboard:widget`、`pcm:wiki:document:block` 等）。**复制 `target` 时必须逐字照抄，NEVER 编造。**

### 步骤 2：询问必要信息

在创建应用前确认：

- 应用名称。
- 使用的模板（多个可选时让用户选择，不要代为决定）。
- 应用创建的**父目录**（`--directory`，默认为当前目录）。
- 如已确定目标站点，记录 PingCode 站点域名。

NEVER 替用户猜测站点域名、模板或开发者身份。

### 步骤 3：创建应用

所有 `python3 -m scripts.*` 命令 MUST 在技能目录（即包含本 SKILL.md 的目录）下运行。从系统提示中给出的 SKILL.md 路径推导该目录。macOS 上若 `python` 不可用则使用 `python3`。

`--directory` 指定**父目录**，应用文件夹（以 `--name` 命名）会在其下创建（例如 `<parent-directory>/<app-name>/`）。脚本会 `cd` 到该父目录后再运行 `nexus create`。省略时在当前目录创建。

```bash
python3 -m scripts.create_nexus_app \
  --template <template> \
  --name <app-name> \
  --directory <parent-directory>
```

脚本会自动：校验 Node.js 与 Nexus CLI、校验模板、通过 `nexus whoami --json` 检查登录状态、检查父目录与目标目录是否已存在，然后运行 `nexus create <app-name> --template <template>`。

NEVER 手动脚手架或绕过 `nexus create`——没有有效 `app.id` 的应用无法部署。

### 步骤 4：定制代码

`nexus create` 会自动安装根目录与 `web/main` 的依赖；NEVER 在创建成功后无条件重复 `npm install`，除非安装失败或依赖文件发生变更。

Custom UI 模板（React）的典型结构：

```text
<app-name>/
├── src/
│   ├── resolvers/
│   │   └── index.ts        # Resolver 入口
│   └── index.ts
├── web/
│   └── main/
│       ├── src/
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── index.html
│       ├── package.json
│       └── vite.config.ts
├── manifest.yaml
├── package.json
└── tsconfig.json
```

固定 SDK 版本（见 `references/nexus-development-guide.md` §3.2.4）：

| 包 | 版本 | 安装位置 |
| --- | --- | --- |
| `@pc-nexus/cli` | `0.5.1` | 全局 |
| `@pc-nexus/core` | `0.5.0` | 根目录 |
| `@pc-nexus/network` | `0.5.0` | 根目录（调用 REST/外部 API 时） |
| `@pc-nexus/bridge` | `0.5.0` | `web/main` |
| `@pc-nexus/event` | `0.5.0` | 根目录（仅事件处理函数） |
| `@pc-nexus/capabilities` | `0.5.0` | `web/main`（调用产品能力时） |
| `@pc-nexus/store` | `0.5.0` | `web/main`（对象存储时） |

```bash
npm install @pc-nexus/core@0.5.0 @pc-nexus/network@0.5.0
npm install --prefix web/main @pc-nexus/bridge@0.5.0
```

#### Custom UI 与 Native UI——不要混淆

- **Custom UI**（`nexus create` 的 `*-custom-ui` 模板）：`manifest.yaml` 中 `extensions[].resource` 指向 `web/main/dist`，前端在 iframe 中运行，使用普通 React/Vue/Angular/JavaScript。通过 `@pc-nexus/bridge` 与平台通信。
- **Native UI**：仍在开发中，当前不可用。NEVER 选择 Native UI，也不要臆造 `Nx*` 组件、`@pc-nexus/react`、`NexusReconciler.render` 等 API。

NEVER 在 Custom UI 中导入 `@pc-nexus/react` 的 `Nx*` 组件期望原生渲染，也 NEVER 照搬 Forge UI Kit / `@forge/react`。

#### 实现时使用的参考文档

- `references/nexus-custom-ui-developer-guide.md` — 前端 iframe、Bridge（`invoke`、`view`、`api`、`dialog`、`router`、`i18n`、`events`、`remote`、`store`）、Capability API、HMR。
- `references/nexus-backend-developer-guide.md` — Resolver、事件处理、`api.invoke`、`fetch.request`、`remote.invoke`、存储（KVS/CES/NOS）、异步队列、Exposer、权限校验 `authorize`。
- `references/nexus-app-manifest-guide.md` — `app`、`extensions`、`functions`、`resources`、`permissions`（scopes、external、content）、`event`、`async`、`storage`、`exposer`、`translations`、`environment`。
- `references/list-nexus-extensions.md` — 选择扩展点 `target`。

关键约束：

- UI Invoke 超时 **5 秒**，其他调用超时 **60 秒**；NEVER 在被前端 `invoke` 直接调用的 Resolver 中执行长耗时任务，改用异步队列。
- 调用 PingCode REST API 前必须在 `permissions.scopes` 中声明 scope，并在对应接口文档中确认 scope 名称——NEVER 编造 scope。
- 调用外部 HTTPS API 前必须在 `permissions.external.fetch.backend` 中声明域名（支持域名、`*.subdomain` 通配符、完整 HTTPS URL、`*`）。
- 前端通过 `@pc-nexus/bridge` 的 `invoke` 调用 Resolver，NEVER 在前端读取用户凭据、会话或令牌。
- `display` 显示条件仅在前端生效，NEVER 作为安全边界；敏感操作 ALWAYS 在后端用 `authorize` 或业务逻辑校验。

### 步骤 5：部署与分发（运行部署脚本）

**你 MUST 运行部署脚本**——不要只把手动的 `nexus deploy` / `nexus distribute` 命令交给用户。从技能目录运行：

- **如果已经拿到用户的 PingCode 站点域名**，一次完成部署和分发：

  ```bash
  python3 -m scripts.deploy_nexus_app \
    --app-dir <app-directory> \
    --deploy --distribute \
    --site <site-domain> \
    --env development
  ```

- **如果还没有站点域名**：先只部署，再询问站点，再带站点运行分发：

  ```bash
  # 1) 仅部署
  python3 -m scripts.deploy_nexus_app \
    --app-dir <app-directory> \
    --deploy \
    --env development

  # 2) 询问用户：“你的 PingCode 站点域名是什么（例如 your-domain.pingcode.com）？”
  #    只传域名，不带协议、端口或路径。

  # 3) 用户回复后，带站点运行完成分发；脚本会先通过 nexus deploy list 确认该环境已有部署
  python3 -m scripts.deploy_nexus_app \
    --app-dir <app-directory> \
    --distribute \
    --site <site-domain> \
    --env development
  ```

`--deploy` 会自动完成：检查 Node.js / Nexus CLI / 登录状态 → `npm install` → `npm run build-web` → `nexus lint` → 检查/执行 `nexus register` → 确认目标环境 → `nexus deploy --non-interactive -e <env>`。`--distribute` 会先确认目标环境已有部署，再执行 `nexus distribute -s <site> -e <env>`。

常用参数：

| 参数 | 作用 |
| --- | --- |
| `--app-dir` | **（必填）** Nexus 应用目录路径 |
| `--site` | PingCode 站点域名（例如 `your-domain.pingcode.com`）；使用 `--distribute` 时必填或交互输入 |
| `--env` | 目标环境，默认 `development`；`staging`/`production` 不可通过 CLI 创建 |
| `--tag` | 部署指定构建号（来自先前 `nexus build`）；省略时 `nexus deploy` 构建新包 |
| `--app-name` | 应用未注册时传给 `nexus register` 的名称 |
| `--deploy` | 执行构建与部署流程；与 `--distribute` 至少传一个 |
| `--distribute` | 执行分发流程；会先确认目标环境已有部署；与 `--deploy` 至少传一个 |
| `--skip-deps` | 跳过 `npm install` |
| `--skip-build-web` | 跳过 `npm run build-web` |
| `--skip-env-check` | 跳过目标环境检查/创建 |
| `--no-verify` | 部署时跳过预检查（仅排查构建器问题时使用，NEVER 在正常流程中使用） |
| `--lint-fix` | 传 `--fix` 给 `nexus lint` 自动修复 |
| `--show-logs` / `--log-limit` | 部署后拉取日志 |

版本升级规则（见 `references/nexus-development-guide.md` §4.1.6）：

- 部署到 `Development`：版本号必须不低于原版本号。
- 部署到 `Production`：版本号必须严格高于原版本号。
- 部署到 `Staging`：无版本号必须升级的要求。
- 公有云环境下，新版本部署到对应环境后，安装该应用的企业会自动升级；私有部署需重新生成并上传 `.npk` 包（`nexus packup`）。

#### 企业管理员安装（用户操作）

分发完成后，**Nexus 没有 `nexus install` 命令**，必须由企业管理员完成安装：

1. 以管理员身份登录目标 PingCode 站点。
2. 进入企业管理后台。
3. 打开「应用审核」列表。
4. 找到已分发的应用，点击「安装」。
5. 查看应用基本信息与权限范围。
6. 按需设置是否允许记录日志。
7. 确认安装。

安装成功后，进入目标产品页面验证扩展是否出现。

如果 scopes、外部域名或其他权限发生变化，需要重新 `nexus deploy` 与 `nexus distribute`，并由企业管理员重新确认安装。

#### 私有部署打包

私有部署环境生成 `.npk` 安装包：

```bash
nexus packup
```

`.npk` 文件名由平台生成，不可配置；由企业管理员在「应用审核」中点击「上传应用」并选择 `.npk` 文件。

## 处理 `nexus create` 失败

`nexus create` 失败时，**NEVER 尝试绕过或手动脚手架**。

| 错误 | 处理 |
| --- | --- |
| 缺少前置条件（Node.js、Nexus CLI） | 运行步骤 0 的安装命令后重试 |
| CLI 需要交互式终端/无法渲染提示 | 让用户在自己的交互式终端运行 `nexus create <app-name> --template <template>` |
| 未登录 / `Unauthorized` | 引导用户创建令牌并在终端运行 `nexus login` |
| 模板名不被识别 | 脚本会给出建议；从 `react-custom-ui`、`angular-custom-ui`、`vue-custom-ui`、`javascript-custom-ui`、`event-typescript`、`webhook-typescript` 中选择 |
| 父目录不存在 | 检查 `--directory` 指向的目录是否存在 |
| 目标目录已存在 | 父目录下已存在同名文件夹，更换名称或删除已有文件夹 |
| 其他错误 | 展示完整 stdout/stderr，向用户求助 |

失败时的示例回复：

```text
nexus create 需要在交互式终端中运行。请在你的终端执行：

  nexus create my-app-name --template react-custom-ui

创建完成后告诉我，我会帮你定制代码。
```

## 扩展模块选择

按 `references/list-nexus-extensions.md` 浏览按产品分类的扩展点，并将对应 `target` 逐字复制到 `manifest.yaml` 的 `extensions[].target`。常见产品分类：

- **全局/Platform**：`pcm:global:header:banner`、`pcm:global:app:hub`、`pcm:global:create:action`、`pcm:global:workspace:page`、`pcm:global:dashboard:widget`、`pcm:global:personal:setting` 等。
- **项目管理（PJM）**：`pcm:pjm:project:page`、`pcm:pjm:project:setting`、`pcm:pjm:workitem:panel`、`pcm:pjm:workitem:action`、`pcm:pjm:sprint:page`、`pcm:pjm:release:page`、`pcm:pjm:baseline:page` 等。
- **产品管理（Ship）**：`pcm:ship:product:page`、`pcm:ship:idea:panel`、`pcm:ship:idea:action`、`pcm:ship:ticket:panel`、`pcm:ship:plan:page`、`pcm:ship:baseline:page` 等。
- **知识管理（Wiki）**：`pcm:wiki:space:page`、`pcm:wiki:space:setting`、`pcn:wiki:context:action`、`pcm:wiki:page:action`、`pcm:wiki:document:block` 等。
- **测试管理（TestHub）**：`pcm:testhub:library:page`、`pcm:testhub:testcase:panel`、`pcm:testhub:testcase:action`、`pcm:testhub:plan:page`、`pcm:testhub:baseline:page` 等。

每个扩展点支持的属性（例如 `viewport.size`、`icon`、`display` 条件、上下文字段）以对应模块文档为准；NEVER 编造字段名。

## 脚本

所有脚本从技能目录以 `python3 -m scripts.<name>` 方式运行。

| 脚本 | 作用 |
| --- | --- |
| `scripts/create_nexus_app.py` | 校验前置条件、模板与登录状态，然后运行 `nexus create <name> --template <template>`。`--directory` 设置父目录。运行：`python3 -m scripts.create_nexus_app --template <template> --name <name> [--directory <dir>]` |
| `scripts/deploy_nexus_app.py` | 部署与分发脚本；`--deploy` 执行前置条件检查、`npm install`、`npm run build-web`、`nexus lint`、`nexus register`（如需）、环境确认、`nexus deploy`；`--distribute` 在确认目标环境已有部署后执行 `nexus distribute`。运行：`python3 -m scripts.deploy_nexus_app --app-dir <dir> (--deploy|--distribute|--deploy --distribute) [--site <domain>] [--env development]` |
| `scripts/search_nexus_docs.py` | 在线检索官方文档（sitemap.xml + 页面正文），返回相关页面标题、URL 与片段。运行：`python3 -m scripts.search_nexus_docs "<关键词>" [--max-pages N] [--json]` |

## 完成清单

在认为工作流完成之前，确认：

- 用户在存在多个可选项时已选择（模板、环境、站点等），或只有唯一可选项。
- 应用通过 `scripts.create_nexus_app` 创建（或失败后由用户在交互式终端运行 `nexus create`）。
- `manifest.yaml` 中 `extensions[].resource` 等于 `resources[].key`，`extensions[].resolver.function` 等于 `functions[].key`，`resources[].path` 指向 `web/main/dist`，且 `permissions.scopes` 存在。
- 代码已定制；按需安装 `@pc-nexus/*` 固定版本依赖。
- 前端改动后已运行 `npm run build-web`。
- **部署脚本由 agent 亲自执行**（而不是只给出手动命令），并至少传入 `--deploy` 或 `--distribute` 之一。
- 分发时已向用户询问站点域名，并使用 `--distribute --site` 运行脚本；站点只传域名。
- 已明确告知用户：分发完成后需要企业管理员在企业管理后台「应用审核」中手动安装；在管理员安装前，应用尚未上线。
- 如 scope、外部域名或其他权限变化，已重新部署和分发，并提示管理员重新确认安装。

## 常见 agent 错误（避免）

- **在多个模板/环境/站点存在时代为选择**——始终让用户选择。
- **跳过部署脚本**——只给出“运行 `nexus deploy` 和 `nexus distribute`”的指令，而不是亲自运行 `scripts.deploy_nexus_app`。
- **不询问站点域名**——分发需要站点域名时必须询问，不要猜测或跳过分发。
- **误以为存在 `nexus install` 命令**——Nexus 必须由企业管理员在后台安装。
- **前端改动后忘记 `npm run build-web`**，或把 `resources[].path` 指向源码目录。
- **照搬 Atlassian Forge 命令/包名/API**（`forge`、`@forge/*`、Jira/Confluence 模块名）。
- **编造 scope、事件名、扩展点 target、权限点或 REST 路径**。
- **不查阅文档就回答不熟悉的 CLI/manifest/SDK 细节**——本地 references 未覆盖时 MUST 运行 `scripts.search_nexus_docs` 在线检索。
- **使用 `manifest.json`/`manifest.yml`、修改 `app.id`、使用 `--no-verify` 或 `sudo` 绕过问题。**
- **在对话或日志中输出令牌、凭证或个人隐私。**

## 调试与排错

参考 `references/nexus-development-guide.md` 第 5 节与 `references/nexus-custom-ui-developer-guide.md` 第 11–12 节。

- **本地调试前置条件**：先 `nexus deploy -e development`、`nexus distribute -s <site> -e development`、企业管理员安装、绑定测试账号，再启动本地隧道。
- **后端隧道**：`nexus serve -e development`（可加 `--function <key>` 只调试指定函数；IDE 断点用 `nexus serve --debug`，Node 调试端口 9229）。
- **前端 HMR**：启动前端 Dev Server，在应用根目录创建 `nexus.json`，在 `serve.resources.<key>.port` 中填写实际端口（React/Vite 常用 `5173`，Angular 常用 `4200`），key 必须与 `manifest.yaml` 的 `resources[].key` 一致。
- **查看日志**：`nexus logs`、`nexus logs --grouped`、`nexus logs --invocation <id>`、`nexus logs --since 2d`、`nexus logs -e development --verbose`。`nexus logs` 仅支持开发环境；Staging/Production 不支持 CLI 拉取日志。前端 `console.*` 只出现在浏览器开发者工具中，NEVER 期待它们出现在 `nexus logs`。
- **`command not found: nexus`**：`npm install -g @pc-nexus/cli@0.5.1`，并检查 npm 全局路径是否在 `PATH` 中。
- **Node 版本过低**：安装/切换到 Node.js 24。
- **Manifest 校验失败**：确认文件名 `manifest.yaml`、YAML 两空格缩进、引用 key 一致、`resources[].path` 为 `web/main/dist`、`permissions.scopes` 存在；NEVER 用 `nexus build --no-verify` 跳过。
- **页面空白或资源 404**：`npm run build-web` 后重新 `nexus deploy -e development`；HMR 下检查 `nexus.json` 的资源 key 与端口。
- **UI Invoke 超时（5 秒）**：拆分 Resolver，耗时任务改用异步队列。
- **外部 API 被拦截**：在 `permissions.external.fetch.backend` 中声明域名后重新部署；`*.example.com` 不匹配父域名本身。
- **PingCode REST API 权限不足**：在接口文档中确认 scope，在 `permissions.scopes` 声明后重新部署分发；前端调用以当前用户身份执行，需要应用身份时改用服务端 Resolver。
- **应用安装后不可见**：管理员确认已在「应用审核」中安装；使用 `nexus logs -e development --limit 50` 排查；scope/权限变更后需要管理员重新确认安装。
