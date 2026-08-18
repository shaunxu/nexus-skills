---
title: 'Nexus 应用开发指南：从零创建并部署'
description: '面向 AI 的 PingCode Nexus 应用创建、开发、调试、部署与安装指南。'
platform: platform
product: nexus
category: devguide
subcategory: guides
date: '2026-08-06'
---

# Nexus 应用开发指南：从零创建并部署

## 1. 指南范围与必读章节

本指南整合 `wiki/guide` 中与“从零创建并部署一个 Nexus 应用”直接相关的章节，给出唯一推荐路径。ALWAYS 按本指南顺序执行；NEVER 在未完成部署和企业安装前宣称应用已经可用。

## 2. 唯一推荐路径总览

ALWAYS 使用以下路径从零创建并部署第一个应用：

1. 安装并验证 Node.js 与 Nexus CLI。
2. 使用 PingCode 开发者令牌执行 `nexus login`。
3. 运行 `nexus create my-first-app` 创建应用。
4. 使用 `manifest.yaml`、`src/resolvers/index.ts` 和 `web/main` 实现 Custom UI 应用。
5. 运行 `npm run build-web` 构建前端，运行 `nexus deploy -e development` 部署到开发环境。
6. 运行 `nexus distribute -s <site> -e development` 分发，再由企业管理员在企业管理后台安装。

ALWAYS 在应用根目录执行所有 `nexus` 命令。运行前先确认目录：

```shell
pwd
ls
```

期望当前目录包含 `manifest.yaml`、`package.json`、`src/` 和 `web/`。

NEVER 使用 `forge` 命令、Atlassian 包名或 Jira/Confluence API 示例。Nexus CLI 是 `nexus`，SDK 包名前缀是 `@pc-nexus/*`。

## 3. 第一步：准备环境、创建应用并实现功能

### 3.1 环境准备与身份验证

#### 3.1.1 安装 Node.js

ALWAYS 使用 Node.js 24.x 或更高版本（`@pc-nexus/cli` 要求 `node >=24.0.0`）。

```shell
node -v
npm -v
```

如果主版本低于 24，ALWAYS 先安装或切换到 Node.js 24，再继续后续步骤。

#### 3.1.2 安装 Nexus CLI

安装最新版 CLI：

```shell
npm install -g @pc-nexus/cli
nexus --version
```

查看可用命令：

```shell
nexus --help
```

如果终端提示 `command not found: nexus`，ALWAYS 检查 npm 全局安装路径和 shell 的 `PATH`。

NEVER 使用 `sudo npm install -g` 或 root 用户安装 Nexus CLI。Linux 环境不依赖 Keychain 或系统密钥环；如果出现权限错误，ALWAYS 修复 npm 全局目录权限后重新安装。

#### 3.1.3 注册开发者账号并创建令牌（用户操作）

需要用户本人完成以下操作：

1. 访问 `https://developer.pingcode.com/console/signup` 注册或登录 PingCode 开放平台。
2. 进入开发者中心的个人设置页面。
3. 创建个人访问令牌并复制。

ALWAYS 在用户确认已经复制令牌后再运行登录命令。NEVER 替用户猜测、生成或保存令牌。

#### 3.1.4 登录 CLI

```shell
nexus login
```

CLI 会提示：

```text
Log in to your PingCode Developer account.
Press Ctrl+C to cancel.

? Enter your PingCode API token:
```

粘贴令牌后，期望输出：

```text
✔ Logged in as yourname.

Now try running 'nexus create' to start a new app.
```

如果登录失败，ALWAYS 显示完整错误输出，并检查令牌是否复制完整、账号是否已完成注册、网络是否可访问 PingCode 开放平台。NEVER 在输出、日志或提交内容中记录令牌。

### 3.2 创建第一个应用

#### 3.2.1 创建应用

进入你的工作目录，运行：

```shell
nexus create my-first-app
cd my-first-app
pwd
```

创建向导会要求选择模板。当前只选择 `Angular Custom UI` 或 `React Custom UI`。ALWAYS 优先选择 `React Custom UI`；只有团队明确要求 Angular 时才选择 `Angular Custom UI`。

创建成功时，CLI 输出会包含 `Created app my-first-app successfully.`。NEVER 依赖输出中的环境数量判断创建结果；平台默认为应用创建 Development、Staging 和 Production 三种环境。

#### 3.2.2 安装依赖

`nexus create` 会自动安装根目录和 `web/main` 的依赖。NEVER 在创建后重复执行 `npm install`，除非安装失败或依赖文件发生变更。

#### 3.2.3 项目结构

React Custom UI 模板应包含以下结构：

```text
my-first-app/
├── src/
│   ├── resolvers/
│   │   └── index.ts
│   └── index.ts
├── web/
│   └── main/
│       ├── src/
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── index.html
│       ├── package.json
│       ├── tsconfig.app.json
│       ├── tsconfig.json
│       ├── tsconfig.node.json
│       └── vite.config.ts
├── manifest.yaml
├── package.json
└── tsconfig.json
```

目录职责如下：

- `src/`：服务端函数源码目录。
- `src/resolvers/index.ts`：Resolver 函数入口。
- `web/main/`：前端 Custom UI 工程。
- `web/main/dist/`：前端构建产物目录，由 `npm run build-web` 生成。
- `manifest.yaml`：应用元数据、扩展模块、函数、资源和权限声明。

NEVER 把清单文件命名为 `manifest.json` 或 `manifest.yml`。文档正文出现过 `manifest.json` 和 `manifest.yml` 字样，但示例和架构文档均使用 `manifest.yaml`。ALWAYS 统一使用 `manifest.yaml`。

#### 3.2.4 安装 SDK

ALWAYS 安装最新稳定版，不锁版本：

```shell
npm install @pc-nexus/core @pc-nexus/network
npm install --prefix web/main @pc-nexus/bridge
```

只有实现事件处理函数时才安装：

```shell
npm install @pc-nexus/event
```

| 包 | 安装位置 |
|---|---|
| `@pc-nexus/cli` | 全局 |
| `@pc-nexus/core` | 根目录 |
| `@pc-nexus/bridge` | `web/main` |
| `@pc-nexus/network` | 根目录 |
| `@pc-nexus/event` | 根目录（仅事件处理函数） |

如果 npm 安装失败，ALWAYS 先检查 Node.js 版本和网络访问。

### 3.3 实现应用

#### 3.3.1 配置 manifest.yaml

ALWAYS 在应用根目录维护 `manifest.yaml`。最小可用 Custom UI 应用如下：

```yaml
app:
  id: e481d841-e3dc-4b4d-907a-7d7954acee57
  version: 1.0.0

extensions:
  - key: my-first-app-project-page
    title: New title
    target: pcm:pjm:project:page
    resource: main
    resolver:
      function: resolver

functions:
  - key: resolver
    handler: index.resolver

resources:
  - key: main
    path: web/main/dist

permissions:
  scopes: []
```

字段规则：

- `app.id`：创建应用时生成的应用唯一 ID；NEVER 手动修改。
- `app.version`：语义化版本，格式为 `主版本.次版本.修订号`，例如 `1.0.0`。
- `extensions[].key`：扩展模块唯一键。
- `extensions[].target`：PingCode 扩展点，例如 `pcm:pjm:project:page`。
- `extensions[].resource`：必须与 `resources[].key` 完全一致。
- `extensions[].resolver.function`：必须与 `functions[].key` 完全一致。
- `functions[].handler`：函数处理器，示例为 `index.resolver`。
- `resources[].path`：Custom UI 构建产物目录，React/Angular 模板使用 `web/main/dist`。
- `permissions.scopes`：PingCode REST API 权限作用域；即使为空也必须声明为 `[]`。

#### 3.3.2 实现 Resolver

ALWAYS 将 UI Invoke 对应的后端逻辑放在 Resolver 中。创建或替换 `src/resolvers/index.ts`：

```typescript
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<string, string>("greeting", async (_context, payload) => {
  console.log("Handler invoked: greeting");
  return `Hello, ${payload}`;
});

export { resolver };
```

NEVER 在 Resolver 中访问未授权域名、写入本地持久文件或记录敏感信息。运行时只有 `/tmp` 可写，且数据只在单次调用期间保留。

#### 3.3.3 实现 React 前端

创建或替换 `web/main/src/App.tsx`：

```typescript
import { useEffect, useState } from "react";
import { invoke } from "@pc-nexus/bridge";

function App() {
  const [result, setResult] = useState<string | null>(null);

  useEffect(() => {
    runGreeting();
  }, []);

  function runGreeting() {
    invoke<string>("greeting", "Nexus")
      .then((res: string) => setResult(res))
      .catch((err: Error) => setResult(`Error: ${err.message}`));
  }

  return <p>{result ?? "Loading..."}</p>;
}

export default App;
```

ALWAYS 通过 `@pc-nexus/bridge` 的 `invoke` 调用 Resolver。NEVER 在前端尝试读取 PingCode 用户会话、令牌或密码。

如果使用 TypeScript 严格模式，ALWAYS 为 payload、返回值和业务对象定义明确类型。NEVER 使用 `any` 掩盖类型错误。

#### 3.3.4 调用 PingCode REST API

只有在调用 PingCode REST API 时才添加 scope。ALWAYS 使用英文直引号，不要复制中文弯引号。

```yaml
permissions:
  scopes:
    - "pcp:read:pjm:workitem"
    - "pcp:write:pjm:workitem"
```

服务端调用示例：

```typescript
import { api } from "@pc-nexus/network";
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<{ workitemId: string }, unknown>("getWorkItem", async (context, payload) => {
  const response = await api.invoke(`/v1/pjm/work_items/${payload.workitemId}`, {
    as: "user",
    userId: context.user?.id ?? "",
  });

  return response.json();
});

export { resolver };
```

NEVER 在未声明 scope 的情况下调用 REST API。未声明的接口调用会因权限不足失败。

#### 3.3.5 调用外部 API

调用外部 HTTPS API 时，ALWAYS 在 `permissions.external.fetch.backend` 声明域名：

```yaml
permissions:
  scopes: []
  external:
    fetch:
      backend:
        - "api.example.com"
        - "*.example-dev.com"
```

服务端调用示例：

```typescript
import { fetch } from "@pc-nexus/network";
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<void, unknown>("fetchExternal", async () => {
  const response = await fetch.request("https://api.example.com", {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });

  return response.json();
});

export { resolver };
```

NEVER 调用未声明域名。未声明域名会被运行时拦截。

## 4. 第二步：构建、部署、分发、安装和迭代

### 4.1 构建、部署、分发和安装

#### 4.1.1 构建前端

ALWAYS 在部署前构建前端静态资源：

```shell
npm run build-web
```

期望构建产物输出到：

```text
web/main/dist
```

如果前端构建失败，NEVER 继续部署。先修复 TypeScript、Vite/Angular 或依赖错误，再重新运行构建命令。

`nexus deploy` 不会自动构建前端。ALWAYS 在部署前手动运行 `npm run build-web`。

#### 4.1.2 部署到 Development

```shell
nexus deploy -e development
```

期望输出：

```text
ℹ Manifest is valid.
ℹ Lint passed.
ℹ Packaged successfully.
ℹ Uploaded successfully.

✔ Deploy completed successfully.
```

基于指定构建号部署：

```shell
nexus build -t 7d392hf
nexus deploy -e development -t 7d392hf
```

仅在排查构建器自身问题时才跳过预检查：

```shell
nexus build --no-verify
```

NEVER 在正常开发流程中使用 `--no-verify`。跳过检查可能把 manifest 错误、类型错误或打包错误推迟到运行时。

#### 4.1.3 分发到 PingCode 企业站点

将 `<site>` 替换为目标 PingCode 站点域名：

```shell
nexus distribute -s your-domain.pingcode.com -e development
```

测试环境可使用对应测试域名：

```shell
nexus distribute -s at.alpha.pingcode.live -e development
```

ALWAYS 只传入站点域名，不添加协议、端口或路径。域名不区分生产、测试或私有部署环境。

#### 4.1.4 企业管理员安装（用户操作）

Nexus 没有用于企业安装的 `nexus install` CLI 命令。ALWAYS 让企业管理员执行安装：

1. 进入 PingCode 企业管理后台。
2. 打开「应用审核」列表。
3. 找到已分发的应用。
4. 点击「安装」。
5. 查看应用基本信息和权限范围。
6. 按需设置是否允许记录日志。
7. 确认安装。

安装成功后，进入目标产品页面验证扩展是否出现。对于示例应用，进入项目页面后应看到标题为 `New title` 的项目页面组件。

#### 4.1.5 私有部署打包

私有部署时，生成 `.npk` 安装包：

```shell
nexus packup
```

`nexus packup` 不接受参数，`.npk` 文件名称由平台生成，不能配置。然后由企业管理员进入企业管理后台「应用审核」列表，点击「上传应用」并选择 `.npk` 文件。

#### 4.1.6 版本升级规则

在 `manifest.yaml` 中升级版本：

```yaml
app:
  id: e481d841-e3dc-4b4d-907a-7d7954acee57
  version: 1.0.1
```

规则如下：

- 部署到 `Development`：版本号必须不低于原版本号。
- 部署到 `Production`：版本号必须高于原版本号。
- 部署到 `Staging`：没有版本号必须升级的要求。
- 公有云环境中，新版本部署到对应环境后，安装该应用的企业会自动升级。
- 私有部署需要重新生成并上传 `.npk` 包。

#### 4.1.7 迭代循环

后端代码变更后：

```shell
nexus deploy -e development
```

前端代码变更后：

```shell
npm run build-web
nexus deploy -e development
```

`manifest.yaml` 变更后，ALWAYS 重新部署。NEVER 假设 `nexus serve` 会让所有 manifest 变更立即生效。

## 5. 第三步：调试、日志和排错

### 5.1 调试与日志

#### 5.1.1 首次调试前置条件

在启动本地调试前，ALWAYS 先完成：

1. `nexus deploy -e development`。
2. `nexus distribute -s <site> -e development`。
3. 企业管理员安装应用。
4. 绑定 PingCode 测试账号。

#### 5.1.2 启动本地后端隧道

```shell
nexus serve -e development
```

首次运行且未绑定账号时，CLI 会提示打开浏览器绑定账号：

```text
✔ Select target environment: development

⚠ Warning: PingCode account not bound yet.

? Do you want to open the browser to bind your account? (Y/n)
```

启动成功时：

```text
✔ Select target environment: development
✓ Connected to development.

Listening for requests...
```

只调试指定函数：

```shell
nexus serve -e development --function resolver
nexus serve -e development --function resolver my-event-handler
```

Event 函数不依赖测试账号绑定，并且永远匹配最近一次建立隧道连接的本地服务。多人同时调试事件函数时，ALWAYS 协调避免隧道抢占。

`nexus serve` 默认监听 `app/src` 目录。

#### 5.1.3 前端 HMR

先启动前端 Dev Server，并记录实际端口。React/Vite 常用端口为 `5173`，Angular 常用端口可能为 `4200`。

在应用根目录创建 `nexus.json`：

```json
{
  "serve": {
    "resources": {
      "main": {
        "port": 5173
      }
    }
  }
}
```

ALWAYS 保证 `main` 与 `manifest.yaml` 中 `resources[].key` 完全一致，并且端口号与前端 Dev Server 实际端口一致。

#### 5.1.4 IDE 断点调试

VS Code：

```shell
nexus serve --debug
```

创建 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Nexus Serve",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "restart": true,
      "skipFiles": [
        "<node_internals>/**"
      ]
    }
  ]
}
```

在 VS Code 中选择 `Nexus Serve` 并按 F5 挂载调试器。

IntelliJ IDEA / WebStorm 使用 `Attach to Node.js/Chrome`，Host 为 `localhost`，Port 为 `9229`，并勾选 `Reconnect automatically`。

#### 5.1.5 查看日志

本地 `nexus serve` 会把服务端日志直接输出到终端：

```shell
nexus serve -e development
```

远程开发环境日志：

```shell
nexus logs
nexus logs --grouped
nexus logs --invocation <invocation-id>
nexus logs --since 2d
nexus logs --environment development --verbose
```

服务端记录日志：

```typescript
console.log("Info message");
console.info("Info message");
console.debug("Debug message");
console.warn("Warn message");
console.error("Error message");
```

日志字段包括级别、时间、Invocation ID、Trace ID、Extension、Function、Version 和 Site。同一 Invocation ID 的日志属于同一次函数调用。

NEVER 在日志中输出访问令牌、用户凭证、个人隐私数据或其他敏感信息。NEVER 期待前端 `console` 出现在 `nexus logs`；前端日志只能通过浏览器开发者工具查看。

`nexus logs` 仅支持开发环境。Staging 和 Production 不支持 CLI 日志输出。

### 5.2 不要做的事

ALWAYS 遵守以下禁止项：

- NEVER 使用 `manifest.json`、`manifest.yml` 或其他文件名替代 `manifest.yaml`。
- NEVER 修改创建应用时生成的 `app.id`。
- NEVER 在 `resources[].path` 中指向未构建的前端源码目录；Custom UI 必须指向 `web/main/dist`。
- NEVER 忘记在前端改动后运行 `npm run build-web`。
- NEVER 在企业管理员安装前宣称应用已上线。
- NEVER 使用不存在的 `nexus install` CLI 命令。
- NEVER 在前端保存或读取 PingCode 用户登录凭据、会话或令牌。
- NEVER 调用未在 `permissions.scopes` 中声明的 PingCode REST API。
- NEVER 调用未在 `permissions.external.fetch.backend` 中声明的外部域名。
- NEVER 假设运行时文件系统可持久写入；只有 `/tmp` 可写，且不保证跨调用保留。
- NEVER 在生产日志中输出敏感信息。
- NEVER 在 Staging 或 Production 中使用调试隧道或 `nexus logs`。
- NEVER 对 Production 使用低于或等于当前版本的版本号。
- NEVER 使用 `sudo` 运行 Nexus CLI 或全局 npm 安装来绕过权限问题。
- NEVER 将 API token、`.env` 密钥、私有证书或 `.npk` 安装包提交到代码仓库。
- NEVER 照搬 Atlassian Forge 文档中的命令、包名、模块名或 API。

### 5.3 常见报错与处理

#### 5.3.1 `command not found: nexus`

原因：Nexus CLI 未安装，或 npm 全局安装路径不在 `PATH` 中。

处理：

```shell
npm install -g @pc-nexus/cli
nexus --version
```

如果仍失败，重新安装 Node.js 24 和 Nexus CLI，并确认当前 shell 能找到 `nexus`。

#### 5.3.2 `node` 版本过低

原因：Node.js 版本低于 Nexus CLI 要求。

处理：安装 Node.js 24，并确认：

```shell
node -v
```

期望主版本为 `v24.x`。

#### 5.3.3 `Manifest is valid` 未出现或 manifest 校验失败

处理步骤：

1. 确认文件名为 `manifest.yaml`。
2. 确认 YAML 缩进使用两个空格。
3. 确认 `extensions[].resource` 与 `resources[].key` 完全一致。
4. 确认 `extensions[].resolver.function` 与 `functions[].key` 完全一致。
5. 确认 `resources[].path` 为 `web/main/dist`。
6. 确认 `permissions.scopes` 存在，即使为空数组。

NEVER 在 manifest 校验失败时使用 `nexus build --no-verify` 跳过问题。

#### 5.3.4 前端页面空白或资源 404

原因：未构建前端，或 `resources[].path` 未指向构建产物。

处理：

```shell
npm run build-web
ls web/main/dist
nexus deploy -e development
```

如果使用 HMR，确认 `nexus.json` 中资源 key 和端口正确。

#### 5.3.5 UI Invoke 超时

原因：UI Invoke 超时限制为 5 秒。Resolver 执行时间超过 5 秒会失败。

处理：

- 将耗时任务拆分为短请求。
- 检查外部 API 延迟和重试逻辑。
- 不要在 UI Invoke 中执行长耗时任务。

#### 5.3.6 外部 API 请求被拦截

原因：外部域名未加入 `permissions.external.fetch.backend`。

处理：在 `manifest.yaml` 中加入域名：

```yaml
permissions:
  scopes: []
  external:
    fetch:
      backend:
        - "api.example.com"
```

然后重新部署：

```shell
nexus deploy -e development
```

#### 5.3.7 PingCode REST API 返回权限不足

原因：缺少 scope，或当前调用身份没有对应 PingCode 权限。

处理：

1. 在接口文档中确认所需 scope。
2. 在 `permissions.scopes` 中声明 scope。
3. 重新部署并重新分发。
4. 如使用用户身份调用，确认该用户本身有权访问目标资源。

前端调用 REST API 始终以当前用户身份执行。需要应用身份或服务端权限时，ALWAYS 通过服务端函数处理。

#### 5.3.8 看不到运行日志

处理：

- 本地调试时查看运行 `nexus serve` 的终端。
- 开发环境云端运行时执行 `nexus logs`。
- 前端日志打开浏览器开发者工具。
- Staging/Production 不支持 CLI 日志，需通过开发者中心或企业设置确认日志权限。

## 6. 第四步：发布前检查、平台限制和 Agent guidance

### 6.1 平台限制

发布前 ALWAYS 检查以下限制：

| 类别 | 限制 |
|---|---|
| Node.js | `>=24.0.0` |
| 应用包大小 | `128 MB` |
| Manifest 文件大小 | `256 KB` |
| 扩展模块数量 | `128` |
| 静态资源数量 | `16` |
| 单资源文件数 | `512` |
| Development 环境数量 | 最多 `16` |
| Staging/Production 环境数量 | 各 `1`，不可删除 |
| 相同环境同时部署数 | `1` |
| 单开发者并行构建数 | `2` |
| 安装包保留时长 | 未使用或被替换后 `30 天` |
| UI Invoke 超时 | `5 秒` |
| 其他调用超时 | `60 秒` |
| 请求负载 | `512 KB` |
| 响应负载 | `5 MB` |
| 每次调用内存 | `512 MB` |
| 每次调用磁盘 | `512 MB` |
| 可写目录 | 仅 `/tmp` |
| KVS Key 长度 | `512` |
| KVS Value 深度 | `32` |
| KVS Value 大小 | `256 KB` |
| 对象存储文件大小 | `1 GB` |
| 对象存储 URL 有效期 | `1 小时` |
| 日志写入 | `128 条/分钟/次调用`，`256 KB/分钟/次调用` |
| 日志保留 | `30 天` |

### 6.2 Agent guidance

执行本指南时，AI agent 应遵守以下工作方式：

- ALWAYS 先检查 `node -v`、`nexus --version` 和当前目录。
- ALWAYS 在需要令牌、企业管理员安装或生产发布时暂停，等待用户确认。
- ALWAYS 在命令失败时展示完整命令和完整输出。
- ALWAYS 优先修复根因，不要用 `--no-verify`、`sudo` 或修改 `app.id` 绕过问题。
- NEVER 编造 CLI 参数、SDK API、扩展点、scope、错误码或平台行为。
- NEVER 提交代码、安装包或密钥，除非用户明确要求提交。
