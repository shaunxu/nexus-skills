---
title: 'Nexus Custom UI 开发者指南'
description: '面向 AI 的 PingCode Nexus Custom UI 前端开发指南：iframe 架构、框架选择、Bridge/Capability API、多语言、存储、调试与排错。'
platform: platform
product: nexus
category: devguide
subcategory: guides
date: '2026-08-10'
---

# Nexus Custom UI 开发者指南

## 相关工具

- nexus-development-guide
- nexus-app-manifest-guide
- nexus-resolvers-guide
- nexus-network-guide
- nexus-storage-guide
- nexus-i18n-guide

## 1. 指南范围与必读章节

本指南聚焦 Nexus Custom UI 前端特定的内容：iframe 运行模型、前端框架工程结构、`@pc-nexus/bridge` 与 `@pc-nexus/capabilities`、与 Resolver 的通信契约、多语言、文件存储、HMR 调试与常见错误。

应用从零创建、部署、分发、安装的完整流程见 `nexus-development-guide`，本指南不重复这些步骤，但默认你已经：

1. 安装 Node.js 24 与 `@pc-nexus/cli@latest`。
2. 使用 `nexus create` 创建应用，并选择 `React Custom UI`、`Angular Custom UI`、`Vue Custom UI` 或 `JavaScript Custom UI` 模板之一。
3. 安装 `@pc-nexus/core`、`@pc-nexus/network`（服务端）和 `@pc-nexus/bridge`（前端）。

ALWAYS 按本指南顺序阅读前端相关章节；NEVER 将 Forge UI Kit 的组件模型、`@forge/react`、`render: native` 或 Atlassian 包名照搬到 Nexus。Nexus Custom UI 运行在标准浏览器 iframe 中，你使用普通的 React / Angular / Vue / 原生 JavaScript，而不是平台自定义组件运行时。

## 2. Custom UI 核心概念

### 2.1 Custom UI 与 Native UI 的区别

Nexus 提供两种构建前端界面的方式：

- **Native UI**：基于 React / Angular 框架，使用平台提供的 `Nx*` 组件（如 `NxText`、`NxButton`），由 PingCode 产品在宿主页面原生渲染，风格与产品完全一致。
- **Custom UI（本指南）**：赋予开发者完全控制权构建 UI。应用运行在独立的 **iframe** 中，为界面展示提供隔离环境。你可以使用任意前端框架、任意 HTML/CSS、任意第三方浏览器库。

选择 Custom UI 的典型场景：

- 需要使用团队既有的 React/Vue/Angular 组件库或设计系统。
- 需要复杂交互、富文本、画布、图表、第三方 Web SDK。
- Native UI 提供的组件不足以表达界面。

NEVER 在 Custom UI 中导入 `@pc-nexus/react` 的 `Nx*` 组件期望它们以 Native UI 方式渲染。Custom UI 与 Native UI 是两套不同的渲染路径。`wiki/reference/interface/react-hooks/use-app-context.md` 中描述的 `useAppContext` 与 `NexusReconciler.render` 属于 Native UI；在 Custom UI 中读取上下文 MUST 使用 `@pc-nexus/bridge` 的 `view.getContext()`，不要使用 `useAppContext`。

### 2.2 iframe 运行模型

所有 Custom UI 应用都在 iframe 中运行，平台为 iframe 预设了权限策略和沙箱属性，开发者 **无法修改**。

功能策略（Permissions Policy）：

| 功能策略 | 描述 |
|---|---|
| `camera` | 允许使用视频输入设备 |
| `clipboard-write` | 允许向剪贴板写入数据 |
| `display-capture` | 允许使用屏幕捕获 API |
| `fullscreen` | 允许使用 `Element.requestFullscreen()` |
| `microphone` | 允许使用音频输入设备 |

沙箱属性（sandbox）：

| 沙箱属性 | 描述 |
|---|---|
| `allow-downloads` | 允许通过用户手势启动下载 |
| `allow-forms` | 允许资源提交表单 |
| `allow-modals` | 允许资源打开模态窗口 |
| `allow-pointer-lock` | 允许资源使用指针锁定 API |
| `allow-same-origin` | 允许将 iframe 内容视为与其父页面同源 |
| `allow-scripts` | 允许资源运行脚本，但不得创建弹出窗口 |

由此带来的约束：

- iframe 与宿主 PingCode 页面跨源隔离，不能直接访问宿主 DOM、`window.parent` 或 PingCode 前端内部状态。
- 与产品的交互 **必须** 通过 `@pc-nexus/bridge` 提供的 JavaScript API。
- 弹出新窗口受沙箱限制；需要打开页面时使用 `router.open` 或 `dialog.open`，而不是 `window.open`。
- 摄像头、麦克风、屏幕捕获、剪贴板写入、全屏等能力默认可用；其他浏览器能力可能被禁用，使用前先在真实 iframe 中验证。

### 2.3 前端与后端分离

Custom UI 应用由两部分组成：

- **前端（Custom UI）**：位于 `web/main`，使用所选框架构建，通过 `@pc-nexus/bridge` 与平台通信。
- **后端（Resolver）**：位于 `src/resolvers`，使用 `@pc-nexus/core` 的 `Resolver` 定义函数，可使用 `@pc-nexus/network` 调用 PingCode REST API 或外部 API。

通信方式：

- 前端通过 `invoke(functionKey, payload)` 调用后端 Resolver。
- 前端可通过 `api.invoke(path)` 直接以当前用户身份调用 PingCode REST API。
- 前端可通过 `remote` / `fetch` 等方式与远程服务或外部 API 集成。

Resolver 是前端调用后端逻辑的唯一契约边界。详细的 Resolver 定义、权限和超时限制见 `nexus-development-guide` 与 `nexus-resolvers-guide`。

> 关键限制：UI Invoke 超时为 **5 秒**。NEVER 在被前端 `invoke` 直接调用的 Resolver 中执行长耗时任务；耗时任务应拆分或改用异步队列。

## 3. 工程结构与框架

### 3.1 创建应用与选择模板

运行：

```shell
nexus create my-first-app
```

在模板选择步骤选择 Custom UI 模板之一：

- `React Custom UI`（推荐）
- `Angular Custom UI`
- `Vue Custom UI`
- `JavaScript Custom UI`

ALWAYS 优先选择 React Custom UI，除非团队明确要求其他框架。`nexus create` 会自动安装根目录和 `web/main` 的依赖。

### 3.2 目录结构

React Custom UI 模板结构：

```text
my-first-app/
├── src/
│   ├── resolvers/
│   │   └── index.ts        # Resolver 函数入口
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

Angular / Vue / JavaScript 模板的差异仅在 `web/main/src` 内部文件命名和构建配置，`src/resolvers`、`manifest.yaml` 结构保持一致。Angular 模板使用 `angular.json` 与 `src/app/app.ts`；Vue 模板使用 `App.vue`；JavaScript 模板使用 `main.js` 与 `styles.css`。

目录职责：

- `src/resolvers/index.ts`：后端 Resolver 定义。
- `web/main/`：前端 Custom UI 工程，独立的 `package.json` 与构建配置。
- `web/main/dist/`：前端构建产物，由 `npm run build-web` 生成。
- `manifest.yaml`：应用元数据、扩展模块、函数、资源、权限、远程服务、多语言等声明。

### 3.3 依赖版本

ALWAYS 固定到当前已确认版本：

| 包 | 版本 | 安装位置 |
|---|---|---|
| `@pc-nexus/cli` | `0.5.1` | 全局 |
| `@pc-nexus/core` | `0.5.0` | 根目录 |
| `@pc-nexus/network` | `0.5.0` | 根目录（调用 REST / 外部 API 时） |
| `@pc-nexus/bridge` | `0.5.0` | `web/main` |
| `@pc-nexus/event` | `0.5.0` | 根目录（仅事件处理函数） |
| `@pc-nexus/capabilities` | `0.5.0` | `web/main`（调用产品能力时） |
| `@pc-nexus/store` | `0.5.0` | `web/main`（对象存储时） |

```shell
npm install @pc-nexus/core@0.5.0 @pc-nexus/network@0.5.0
npm install --prefix web/main @pc-nexus/bridge@0.5.0
```

使用产品能力或对象存储时按需安装：

```shell
npm install --prefix web/main @pc-nexus/capabilities@0.5.0 @pc-nexus/store@0.5.0
```

`store` 从 `@pc-nexus/bridge` 导入（`import { store } from "@pc-nexus/bridge"`），类型与预签名 URL 的服务端实现依赖 `@pc-nexus/storage`（详见 §4.9）。

### 3.4 Manifest 中声明 Custom UI 资源

最小可用 Custom UI 应用的 `manifest.yaml`：

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

- `extensions[].resource` MUST 与 `resources[].key` 完全一致（示例中为 `main`）。
- `extensions[].resolver.function` MUST 与 `functions[].key` 完全一致。
- `resources[].path` MUST 指向构建产物目录 `web/main/dist`，NEVER 指向 `web/main/src` 等源码目录。
- `permissions.scopes` MUST 存在，即使为空数组 `[]`。
- 文件名 MUST 为 `manifest.yaml`。NEVER 使用 `manifest.json` 或 `manifest.yml`。
- `app.id` 由 `nexus create` 生成，NEVER 手动修改。

部分扩展模块支持额外字段：

- `viewport.size`：弹窗类扩展的尺寸，可选 `small`、`medium`、`large`、`xlarge`、`max`、`fullscreen`。
- `title`：支持字符串或 `i18n` 对象（`title: { i18n: page.title }`）。
- `icon`：扩展菜单项图标，部分模块支持。

具体扩展点支持的字段以 `wiki/reference/resource/extensions` 下对应模块文档为准。

### 3.5 构建前端

部署前 ALWAYS 手动构建前端：

```shell
npm run build-web
```

产物输出到 `web/main/dist`。`nexus deploy` 不会自动构建前端；前端代码改动后 MUST 重新运行 `npm run build-web` 再部署。

## 4. Bridge API（`@pc-nexus/bridge`）

Bridge API 是运行在 iframe 中的前端与 PingCode 产品安全集成的唯一方式。安装：

```shell
npm install --prefix web/main @pc-nexus/bridge
```

当前提供的 Bridge API：

| API | 描述 |
|---|---|
| `invoke` | 调用后端 Resolver 函数 |
| `view` | 获取与操作当前视图上下文（`getContext`、`refresh`、`close`、`createHistory`、`submit`、`emitReadyEvent` 等） |
| `api` | 以当前用户身份调用 PingCode REST API |
| `dialog` | 打开包含指定资源的模态框或确认框 |
| `router` | 在 PingCode 内导航、打开页面、生成 URL、重新加载 |
| `i18n` | 获取翻译资源或创建翻译器 |
| `events` | 在同一应用的不同 UI 之间订阅/发送自定义事件 |
| `remote` | 调用已配置的外部远程服务 |
| `store` | 对象存储文件的上传、下载、元数据与删除 |
| `realtime` | 实时通信（见 §10） |

### 4.1 `invoke`：调用后端 Resolver

函数签名：

```typescript
function invoke<TPayload, TResult>(functionKey: string, payload?: TPayload): Promise<TResult>;
```

- `functionKey` MUST 与后端 `resolver.define(functionKey, handler)` 中定义的 key 完全一致。
- 返回 `Promise<TResult>`，超时时间 5 秒。

使用 TypeScript 泛型建立前后端类型契约：

```typescript
import { invoke } from "@pc-nexus/bridge";

interface GetTextPayload { example: string; }
interface GetTextResult { text: string; }

const result = await invoke<GetTextPayload, GetTextResult>(
  "getText",
  { example: "my-invoke-variable" }
);
console.log(result.text);
```

NEVER 在前端直接使用 `any` 绕过类型检查。SHOULD 将前后端共享的 payload/result 类型放在可被两端复用的位置（例如 `src/types/`），避免前后端字段漂移。

### 4.2 `view`：当前视图上下文

```typescript
import { view } from "@pc-nexus/bridge";
```

| 方法 | 描述 |
|---|---|
| `getContext()` | 获取当前扩展的上下文数据（应用、环境、团队、账号、扩展模块及 `extension.data`） |
| `setWindowTitle(newTitle)` | 修改当前 `document` 标题，标题后会自动追加 ` - {产品名}`；仅部分扩展模块支持 |
| `refresh()` | 刷新父页面数据而不整页重载；仅部分扩展模块支持 |
| `close(payload?)` | 关闭当前视图（Dialog 或动态菜单打开的视图），可向 `onClose` 回调传递 payload |
| `onClose(callback)` | 注册 Dialog 关闭时的回调 |
| `isDialog()` | 判断当前资源是否运行在 Dialog 中 |
| `createHistory()` | 获取 `NexusHistory` 对象，用于全页面应用内路由 |
| `submit(payload?)` | 在上下文配置视图上提交表单；仅部分扩展模块支持 |
| `emitReadyEvent()` | 通知 Nexus 当前扩展的业务内容已加载完成 |

`getContext()` 返回结构（节选）：

```typescript
interface NexusAppContext<T = Record<string, any>> {
  app: { id: string; version: string };
  environment: { id: string; type: string };
  team: { id: string; url: string; locale: string; timezone: string };
  installation: { id: string };
  account: { id: string; locale: string; timezone: string };
  extension: {
    key: string;
    local_id: string;
    target: string;
    location: string;
    data: T;
  };
}
```

> 注意：`extension.data` 的具体字段由扩展点决定。通过 `dialog.open` 传入的自定义上下文可在 Dialog 资源中通过 `extension.data.dialog` 读取。具体字段以 `wiki/reference/resource/context` 与对应扩展点文档为准。

`createHistory()` 返回的 `NexusHistory` 提供 `push`、`replace`、`go`、`back`、`forward`、`listen`，路径始终相对于应用自身的 URL。

### 4.3 `api`：前端调用 PingCode REST API

```typescript
import { api } from "@pc-nexus/bridge";

const response = await api.invoke("/v1/myself");
console.log(await response.json());
```

函数签名：

```typescript
function invoke(path: string, options?: ApiInvokeOptions): Promise<Response>;
type ApiInvokeOptions = Omit<RequestInit, "signal">;
```

关键规则：

- 前端 REST 调用 **始终以当前交互用户的身份** 执行，不存在与服务端 `as: "app"` 等效的选项。
- 除应用在 `manifest.yaml` 中声明 scope 外，当前用户本身还必须具备对应 PingCode 权限；否则即使 scope 正确也会失败。
- 调用前 MUST 在 `manifest.yaml` 的 `permissions.scopes` 中声明所需 scope：

```yaml
permissions:
  scopes:
    - "pcp:read:pjm:workitem"
    - "pcp:write:pjm:workitem"
```

- 需要以应用自身身份调用 API 时，ALWAYS 改用服务端 Resolver（`@pc-nexus/network` 的 `api.invoke` 配合 `as: "app"`）。

### 4.4 `dialog`：模态框

```typescript
import { dialog } from "@pc-nexus/bridge";
```

`dialog.open(options)` 打开包含指定静态资源的模态框：

```typescript
const dialogRef = await dialog.open({
  resource: "dialog-resource",
  size: "max",
  context: { message: "from dialog context" },
  title: "Dialog Title",
  icon: "icons/bell-fill:#ff4d4f",
  backdropClosable: true,
  onClose: (payload) => console.log("closed", payload),
});
```

`DialogOpenOptions` 字段：

| 字段 | 类型 | 描述 |
|---|---|---|
| `resource` | `string` | 在模态框中打开的资源 key（MUST 在 `resources` 中声明） |
| `size` | `small \| medium \| large \| xlarge \| max \| fullscreen` | 模态框尺寸 |
| `context` | `Record<string, unknown>` | 传入 Dialog 资源的自定义数据，通过 `view.getContext()` 的 `extension.data.dialog` 读取 |
| `backdropClosable` | `boolean` | 点击遮罩或按 ESC 是否可关闭，默认 `true` |
| `onClose` | `(payload?) => void` | Dialog 关闭回调，payload 来自 Dialog 内调用 `view.close(payload)` |
| `title` | `string` | 头部标题，有值时显示头部 |
| `icon` | `string` | 头部图标，仅在 `title` 有值时生效 |

返回 `DialogRef`，通过 `dialogRef.close(payload?)` 主动关闭。

Dialog 资源内判断并读取上下文：

```typescript
import { view } from "@pc-nexus/bridge";

if (await view.isDialog()) {
  const ctx = await view.getContext();
  const message = ctx.extension.data.dialog.message;
  await view.close({ ok: true });
}
```

`dialog.confirm(options)` 打开风格统一的确认框：

```typescript
dialog.confirm({
  title: "Confirm",
  content: "Are you sure you want to confirm?",
  operationType: "danger", // "danger" | "primary"，默认 "danger"
  onConfirm: async (payload?: unknown) => { /* 执行操作，结束后自动关闭 */ },
  onCancel: () => { /* 可选 */ },
});
```

`onConfirm` 回调可以接收一个 `payload` 参数，用于区分确认操作的上下文；具体类型以使用场景为准。

### 4.5 `router`：页面导航

```typescript
import { router } from "@pc-nexus/bridge";
```

| 方法 | 描述 |
|---|---|
| `navigate(urlOrLocation)` | 在当前 tab 内导航到 PingCode 内部路径、完整 URL 或 `NavigationLocation` 对象 |
| `open(urlOrLocation)` | 在新标签页或窗口中打开页面 |
| `generateUrl(location)` | 根据 `NavigationLocation` 生成 `URL` 对象 |
| `reload()` | 重新加载当前页面 |

`NavigationTarget` 枚举：

```typescript
enum NavigationTarget {
  Workitem = "workitem",
  Testcase = "testcase",
  Page = "page",
  Idea = "idea",
  Ticket = "ticket",
  Project = "project",
  Library = "library",
  Space = "space",
  Product = "product",
}
```

示例：

```typescript
router.navigate("/pjm/workitems/123");
router.navigate({ target: NavigationTarget.Workitem, id: "123" });
router.open("https://example.com/");
```

`NavigationTarget` 的枚举成员为首字母大写形式（例如 `Workitem`、`Testcase`、`Page`），使用时以 SDK 实际导出的类型定义为准。

### 4.6 `i18n`：多语言

```typescript
import { i18n } from "@pc-nexus/bridge";

const translator = await i18n.createTranslator();
const title = translator.translate("page.title");
const content = translator.translate("page.content", { name: "Nexus" });

const { translations, locale } = await i18n.getTranslations();
```

- `createTranslator(locale?)` 返回 `{ translate(key, params?) }`，支持 `{{name}}` 形式的变量替换。
- `getTranslations(locale?)` 返回原始翻译 JSON，方便接入 i18next 等第三方库。
- 不显式传 `locale` 时使用当前用户的语言设置。

多语言资源在 `manifest.yaml` 中配置（见 §8）。

### 4.7 `events`：UI 间自定义事件

`events` 允许同一应用内的不同 UI（例如主页面与 Dialog）之间通过自定义事件名通信，支持传递普通数据和 `Blob`。

```typescript
import { events } from "@pc-nexus/bridge";

// 订阅
const subscription = await events.on<{ file: Blob }>("FILE_CHANGE", async (payload) => {
  const text = await payload?.file?.text();
  console.log(text);
});

// 发送
const file = new Blob(["hello world"], { type: "text/plain" });
await events.emit("FILE_CHANGE", { file });

// 取消订阅
subscription.unsubscribe();
```

事件 payload 支持对象、数组、字符串以及 `Blob`；bridge 会自动序列化/还原 `Blob`。

### 4.8 `remote`：调用远程服务

`remote` 用于调用在 `manifest.yaml` 的 `remotes` 中声明的外部后端服务。

```typescript
import { remote } from "@pc-nexus/bridge";

// invoke：转发前进行校验并按配置附加 OAuth 令牌
const res1 = await remote.invoke({
  path: "/my-api",
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ message: "hello" }) as BodyInit,
});

// request：直接发送请求，即使远程配置了 OAuth 令牌也不会附带
const res2 = await remote.request("my-remote", {
  path: "/my-api",
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ message: "hello" }),
});
```

`remote.invoke` 与 `remote.request` 的 `body` 类型均为 WHATWG `RequestInit` 中的 `BodyInit`。发送 JSON 时 MUST 自行 `JSON.stringify`，不要直接传普通对象。具体远程服务的声明方式（`remotes[].key`、`baseUrl`、OAuth 配置等）见 manifest 与远程服务相关文档。

### 4.9 `store`：对象存储（文件上传/下载）

`store` 通过预签名 URL 机制完成文件传输，所有方法都需要一个 `functionKey` 指向用于生成预签名 URL 的后端 Resolver。

| 方法 | 描述 |
|---|---|
| `upload(functionKey, objects)` | 上传一个或多个 `File`/`Blob` |
| `download(functionKey, keys)` | 按键名下载文件，返回 `Blob` |
| `getMetadata(functionKey, keys)` | 获取文件元数据 |
| `delete(functionKey, keys)` | 删除文件 |

前端上传示例：

```typescript
import { store } from "@pc-nexus/bridge";

const input = document.getElementById("fileInput") as HTMLInputElement;
const files = Array.from(input.files || []);
const results = await store.upload("filterAndGenerateUploadUrls", files);
console.log(results); // { success, key, status?, error? }[]
```

对应的后端 Resolver 使用 `@pc-nexus/storage` 的 `nos.createUploadUrl` / `nos.createDownloadUrl` / `nos.getMetadata` / `nos.delete` 生成预签名 URL 并返回平台要求的映射结构。完整服务端实现见 `wiki/reference/interface/bridge/store.md`。

平台限制：单文件最大 1 GB，预签名 URL 有效期 1 小时。详见 `nexus-development-guide` 中的平台限制表。

## 5. Capability API（`@pc-nexus/capabilities`）

Capability API 让前端直接复用 PingCode 产品能力，无需重复开发。安装：

```shell
npm install --prefix web/main @pc-nexus/capabilities
```

当前提供的能力：

| API | 描述 |
|---|---|
| `notify` | 显示与 PingCode 风格一致的通知消息（`show`/`success`/`info`/`warning`/`error`） |
| `user` | 企业成员选择器（`openDialog` / `openPopover`） |
| `processor` | 打开进程管理器组件 |
| `workitem` | 打开工作项创建/详情弹窗 |
| `idea` | 打开需求创建/详情弹窗 |
| `ticket` | 打开工单创建/详情弹窗 |
| `testcase` | 打开测试用例创建/详情弹窗 |
| `page` | 打开页面创建/详情弹窗 |
| `richtext` | 富文本展示与编辑组件 |

### 5.1 `notify`：通知消息

```typescript
import { notify } from "@pc-nexus/capabilities";

const ref = await notify.success({
  title: "Saved",
  description: "Your changes have been saved.",
  detail: { link: "View", content: "..." },
  isAutoClose: true, // 默认 true，4.5 秒后关闭
  actions: [
    { text: "Undo", icon: "undo", onClick: () => ref.close() },
  ],
});
```

`notify.show(options)` 允许通过 `type` 指定 `success | error | warning | info`；`notify.success/info/warning/error` 是对应快捷方法。返回 `NotifyRef`，调用 `ref.close()` 可手动关闭。

### 5.2 `user`：成员选择器

模态选择（适合多选、人数较多）：

```typescript
import { user, UserInfo } from "@pc-nexus/capabilities";

await user.openDialog({
  title: "选择成员",
  selection: ["user-id-1"],
  onConfirm: async (ids?: string[], users?: UserInfo[]) => {
    console.log(ids, users);
  },
  onClose: () => {},
});
```

下拉选择（适合快速单选/多选，需要锚点元素）：

```typescript
await user.openPopover({
  origin: event.currentTarget as HTMLElement,
  multiple: true,
  selection: ["user-id-1", "user-id-2"],
  onConfirm: async (ids?: string[], users?: UserInfo[]) => {},
});
```

`UserInfo` 包含 `id`、`display_name?`、`name?`。

### 5.3 业务对象弹窗

通过对应模块打开业务对象详情或创建弹窗，例如：

```typescript
import { workitem } from "@pc-nexus/capabilities";

await workitem.openDetail("GON-24"); // 支持工作项标识或 ID
```

`idea`、`ticket`、`testcase`、`page`、`processor`、`richtext` 的完整签名见 `wiki/reference/interface/capabilities/` 下对应文档。

## 6. 前端开发模式

### 6.1 React

`web/main/src/App.tsx`：

```tsx
import { useEffect, useState } from "react";
import { invoke } from "@pc-nexus/bridge";

function App() {
  const [result, setResult] = useState<string | null>(null);

  useEffect(() => {
    invoke<string>("greeting", "Nexus")
      .then(setResult)
      .catch((err: Error) => setResult(`Error: ${err.message}`));
  }, []);

  return <p>{result ?? "Loading..."}</p>;
}

export default App;
```

### 6.2 Angular

`app.ts` 通过 `invoke` 调用 Resolver，模板中用 signal 绑定：

```typescript
import { Component, signal } from "@angular/core";
import { invoke } from "@pc-nexus/bridge";

@Component({
  selector: "app-root",
  templateUrl: "./app.html",
  styleUrl: "./app.scss",
})
export class App {
  protected readonly result = signal<string | null>(null);

  constructor() {
    invoke<string>("greeting", "Nexus")
      .then((res) => this.result.set(res))
      .catch((err: Error) => this.result.set(`Error: ${err.message}`));
  }
}
```

```html
<p>{{ result() }}</p>
```

### 6.3 Vue

```vue
<script setup lang="ts">
import { onMounted, ref } from "vue";
import { invoke } from "@pc-nexus/bridge";

const result = ref<string | null>(null);

onMounted(() => {
  invoke<string>("greeting", "Nexus")
    .then((res) => (result.value = res))
    .catch((err: Error) => (result.value = `Error: ${err.message}`));
});
</script>

<template>
  <p>{{ result }}</p>
</template>
```

### 6.4 原生 JavaScript

`main.js`：

```javascript
import { invoke } from "@pc-nexus/bridge";

const resultEl = document.getElementById("result");

invoke("greeting", "Nexus")
  .then((res) => { resultEl.textContent = res; })
  .catch((err) => { resultEl.textContent = `Error: ${err}`; });
```

`index.html` 中通过 `<script type="module" src="/src/main.js"></script>` 引入。

### 6.5 UI 组件与样式

Custom UI 允许使用任意 HTML/CSS 与第三方组件库。平台目前没有为 Custom UI 提供官方的 React 组件库或设计 token 包；`wiki/reference/interface/ui-components` 下文档化的 `NxButton` 等 `Nx*` 组件从 `@pc-nexus/react` / `@pc-nexus/angular` 导入，属于 Native UI 组件体系，不适用于 Custom UI。

在 Custom UI 中可自由选用团队自有的组件库或开源组件库（配合自有设计规范），或直接使用原生 HTML 元素。NEVER 臆造 `@pc-nexus/components`、`@pingcode/components` 等并不存在的包名。

由于应用运行在 iframe 中，CSS 不会泄漏到宿主页面，宿主页面样式也不会影响应用内部。可放心使用 CSS reset、CSS-in-JS、Tailwind 等方案。

## 7. 状态管理与通信模式

### 7.1 本地状态

UI 局部状态使用各框架原生能力（React `useState`/`useReducer`、Angular signal、Vue `ref`/`reactive`）。仅当数据需要持久化或跨用户共享时才走 Resolver / 存储。

```tsx
const [data, setData] = useState<Item[] | null>(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);

useEffect(() => {
  invoke<unknown, Item[]>("listItems")
    .then(setData)
    .catch((e: Error) => setError(e.message))
    .finally(() => setLoading(false));
}, []);

if (loading) return <p>Loading...</p>;
if (error) return <p role="alert">{error}</p>;
return <ul>{(data ?? []).map((it) => <li key={it.id}>{it.name}</li>)}</ul>;
```

### 7.2 表单提交与类型契约

前端提交给 Resolver 的数据 MUST 与共享 TypeScript 类型一致。组件产出的表单值若与后端类型不一致，MUST 在提交前显式转换，不要把组件原始事件对象直接传给 `invoke`。

```typescript
interface CreateItemPayload { name: string; assigneeIds: string[]; }

async function handleSubmit(form: { name: string; assignees: UserInfo[] }) {
  const payload: CreateItemPayload = {
    name: form.name.trim(),
    assigneeIds: (form.assignees ?? []).map((u) => u.id),
  };
  await invoke<CreateItemPayload, { id: string }>("createItem", payload);
}
```

### 7.3 错误处理

Bridge 与 Capability 调用失败时，错误对象通常包含 `code` 和 `message`：

```typescript
try {
  await invoke("doSomething");
} catch (error) {
  const { code, message } = error as { code: string; message: string };
  console.error(`${code}: ${message}`);
  if (code === "ERR_REMOTE_INVALID_KEY") {
    // 针对性处理
  }
}
```

面向用户的错误提示 SHOULD 使用 `notify.error`，并避免在 UI 上直接暴露原始堆栈或敏感信息。

### 7.4 视图就绪事件

对需要等业务数据加载完成后再展示的扩展，SHOULD 在首屏内容就绪后调用：

```typescript
import { view } from "@pc-nexus/bridge";
await view.emitReadyEvent();
```

## 8. 多语言（i18n）

### 8.1 配置翻译资源

在 `manifest.yaml` 中声明：

```yaml
translations:
  resources:
    - key: zh-CN
      path: locales/zh-CN.json
    - key: en-US
      path: locales/en-US.json
  fallback:
    default: zh-CN
```

当前支持 `zh-CN`（简体中文）与 `en-US`（美式英语）。

### 8.2 翻译文件

`locales/zh-CN.json`：

```json
{
  "common": { "ok": "确定", "cancel": "取消" },
  "page": { "greeting": "你好，{{name}}" }
}
```

`locales/en-US.json`：

```json
{
  "common": { "ok": "OK", "cancel": "Cancel" },
  "page": { "greeting": "Hello, {{name}}" }
}
```

最佳实践：

- 按功能模块组织 key（`checklist.*`、`setting.*`），通用词汇放在 `common.*`。
- 各语言文件保持相同 JSON 结构。
- 动态值使用 `{{变量名}}` 语法。
- `title` 等 manifest 字段可通过 `title: { i18n: page.title }` 引用翻译 key。

### 8.3 前端使用

推荐使用 `createTranslator`：

```typescript
import { i18n } from "@pc-nexus/bridge";

const translator = await i18n.createTranslator();
const text = translator.translate("page.greeting", { name: "Nexus" });
```

接入 i18next 等第三方库时，使用 `i18n.getTranslations()` 一次性取出当前语言资源。

服务端也可通过 `@pc-nexus/core` 的 `i18n` 模块翻译文案，详见 `nexus-i18n-guide`。

## 9. 性能与平台限制

### 9.1 前端性能建议

- UI Invoke 超时 5 秒，后端逻辑应轻量；耗时任务走异步队列。
- 对高频更新使用稳定回调（`useCallback`）与记忆化（`useMemo`），避免不必要的重渲染。
- 加载态 MUST 明确（骨架屏或 spinner），错误态 MUST 可被用户感知。
- 列表数据在 `.map` 前做空值保护：`(items ?? []).map(...)`。
- HMR 仅用于本地开发，部署前 ALWAYS 执行 `npm run build-web` 验证生产构建。

### 9.2 与 Custom UI 相关的平台限制

| 类别 | 限制 |
|---|---|
| 静态资源数量 | 16 |
| 单资源文件数 | 512 |
| 应用包大小 | 128 MB |
| UI Invoke 超时 | 5 秒 |
| 其他调用超时 | 60 秒 |
| 请求负载 | 512 KB |
| 响应负载 | 5 MB |
| 对象存储单文件 | 1 GB |
| 对象存储预签名 URL 有效期 | 1 小时 |

完整限制表（含 KVS、日志、构建、环境数量等）见 `nexus-development-guide` §6.1。

## 10. Realtime（实时通信）

`@pc-nexus/bridge` 导出了 `realtime` API，但 `wiki/reference/interface/bridge/realtime.md` 与 `wiki/guide/development/realtime-frontend.md` 当前为空文档。在官方文档补齐前，NEVER 臆造 `realtime.subscribe` / `realtime.publish` 等方法；需要实时能力时可临时通过 `events` 实现同应用 UI 间通信，或通过 Resolver 轮询，并在使用前确认 SDK 实际导出。

## 11. 调试与 HMR

### 11.1 首次调试前置条件

启动本地调试前，ALWAYS 先完成：

1. `nexus deploy -e development`
2. `nexus distribute -s <site> -e development`
3. 企业管理员安装应用
4. 绑定 PingCode 测试账号

### 11.2 启动后端隧道

```shell
nexus serve -e development
```

只调试指定函数：

```shell
nexus serve -e development --function resolver
```

IDE 断点调试使用 `nexus serve --debug`（Node 调试端口 9229），详见 `nexus-development-guide` §5.1.4。

### 11.3 前端 HMR

1. 启动前端 Dev Server 并记录实际端口（React/Vite 常用 `5173`，Angular 常用 `4200`）。
2. 在应用根目录创建 `nexus.json`：

```json
{
  "serve": {
    "resources": {
      "main": { "port": 5173 }
    }
  }
}
```

`resources` 下的 key（`main`）MUST 与 `manifest.yaml` 中 `resources[].key` 完全一致；端口 MUST 与 Dev Server 实际端口一致。

### 11.4 查看日志

- 服务端 `console.*` 由 `nexus serve` 直接输出到终端；远程开发环境使用 `nexus logs`。
- 前端 `console.*` 只出现在浏览器开发者工具中，NEVER 期待它们出现在 `nexus logs`。
- Staging / Production 不支持 CLI 日志输出。
- NEVER 在日志中输出访问令牌、用户凭证或个人隐私数据。

## 12. 常见错误与处理

### 12.1 页面空白或静态资源 404

原因：未构建前端，或 `resources[].path` 未指向 `web/main/dist`。

处理：

```shell
npm run build-web
ls web/main/dist
nexus deploy -e development
```

HMR 模式下检查 `nexus.json` 中资源 key 与端口是否正确。

### 12.2 `invoke` 超时（5 秒）

- 拆分 Resolver 逻辑，将耗时任务改为异步队列。
- 检查外部 API 延迟与重试策略。
- 对大数据集做分页/懒加载。

### 12.3 PingCode REST API 返回权限不足

- 在接口文档中确认所需 scope。
- 在 `manifest.yaml` 的 `permissions.scopes` 中声明 scope 并重新部署、重新分发。
- 前端调用以当前用户身份执行，确认该用户本身有 PingCode 权限。
- 需要应用身份时改为服务端 Resolver 调用。

### 12.4 外部 / 远程 API 被拦截

- 服务端 Resolver 调用外部 HTTPS API 时，在 `permissions.external.fetch.backend` 中声明域名。
- 前端使用 `remote` 时，确认 `remotes` 中已声明对应服务且 key 正确。
- NEVER 调用未声明域名。

### 12.5 Dialog 关闭后拿不到返回值

- 打开时传入 `onClose` 回调。
- Dialog 资源内使用 `view.close(payload)` 关闭并传值。
- 用 `view.isDialog()` 判断当前是否运行在 Dialog 中。

### 12.6 多语言文案不生效

- 确认 `manifest.yaml` 中 `translations.resources` 文件路径正确。
- 确认 `fallback.default` 已设置。
- 确认 JSON key 与 `translate(key)` 调用完全匹配，变量占位符为 `{{name}}` 形式。
- 修改 manifest 或翻译文件后重新部署。

## 13. 安全与不要做的事

ALWAYS 遵守以下规则：

- NEVER 在前端保存或读取 PingCode 用户的登录凭据、会话、令牌或密码。
- NEVER 直接访问宿主页面 DOM、`window.parent` 或 PingCode 前端内部状态；所有产品集成通过 Bridge / Capability API。
- NEVER 调用未在 `permissions.scopes` 中声明的 PingCode REST API。
- NEVER 调用未在 `permissions.external.fetch.backend` 或 `remotes` 中声明的外部服务。
- NEVER 把 Resolver 当作可长耗时运行的服务；UI Invoke 5 秒超时。
- NEVER 在日志或错误提示中输出敏感信息。
- NEVER 修改 `app.id`，NEVER 使用 `manifest.json` / `manifest.yml`。
- NEVER 在未构建前端（`npm run build-web`）的情况下部署。
- NEVER 在未由企业管理员安装前宣称应用已上线。
- NEVER 照搬 Atlassian Forge 的命令、包名（`@forge/*`）、模块名或 API；Nexus CLI 是 `nexus`，SDK 前缀为 `@pc-nexus/*`。
- NEVER 臆造 SDK 中不存在的 Bridge、Capability、组件或 hook；使用前以 `wiki/reference/interface/` 下的 API 文档与实际安装的 SDK 类型定义为准。

## 14. 文档资源

开发 Custom UI 时常用的参考文档：

- 应用创建、部署、分发、安装、平台限制：`nexus-development-guide`
- Manifest 字段：`wiki/guide/development/architecture-manifest.md`、`wiki/reference/manifest/`
- Resolver 函数：`wiki/guide/development/functions-resolvers.md`
- 前端网络：`wiki/guide/development/network-calling-apis-from-frontend.md`
- Bridge API：`wiki/reference/interface/bridge.md` 及 `wiki/reference/interface/bridge/` 下各 API 文档
- Capability API：`wiki/reference/interface/capabilities.md` 及 `wiki/reference/interface/capabilities/`
- React Hooks：`wiki/reference/interface/react-hooks.md`
- UI 组件：`wiki/reference/interface/ui-components.md`
- 多语言：`wiki/guide/development/internationalization.md`
- iframe 权限：`wiki/guide/development/custom-ui-iframe-permission.md`
- 框架指南：`wiki/guide/development/custom-ui-with-react.md`、`custom-ui-with-angular.md`、`custom-ui-with-vue.md`、`custom-ui-with-javascript.md`
- 扩展点与上下文：`wiki/reference/resource/extensions/`、`wiki/reference/resource/context`
- 错误处理：`wiki/guide/development/error-handling.md`
