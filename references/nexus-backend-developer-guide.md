---
title: 'Nexus 后端开发者指南'
description: '面向 AI 的 PingCode Nexus 后端函数、Resolver、事件处理、网络、存储与异步队列开发指南。'
platform: platform
product: nexus
category: devguide
subcategory: guides
date: '2026-08-10'
---

# Nexus 后端开发者指南

## 相关指南

- nexus-development-guide
- nexus-app-manifest-guide

## 1. 指南范围与前置条件

本指南聚焦 Nexus 应用的后端实现：Resolver 函数、事件处理函数、PingCode REST API 调用、外部 API 调用、远程服务、存储、异步队列、自定义 REST API、错误处理和日志。

在使用本指南前：

- 已阅读 **nexus-development-guide**，完成 Node.js 24、Nexus CLI `0.5.1` 的安装，并能成功 `nexus create`、`nexus deploy`、`nexus distribute`。
- 已阅读 **nexus-app-manifest-guide**，理解 `manifest.yaml` 中 `functions`、`permissions`、`event`、`storage`、`async`、`exposer`、`remotes`、`endpoints` 的写法。
- 熟悉 TypeScript 与现代 JavaScript。
- 后端 SDK 包统一使用 `@pc-nexus/*` 前缀。NEVER 照搬 Atlassian Forge 的 `@forge/api`、`@forge/resolver` 等包名或 API。

> 文档约定：Nexus 平台仍在快速演进，scope、事件名、REST 路径等可能随版本变化。在编写真实应用前，ALWAYS 由人工核对最新官方文档或实际运行结果，NEVER 仅凭文档中的示例直接交付代码。

## 2. 后端运行模型与核心概念

### 2.1 运行模型

- Nexus 后端运行在 PingCode 托管的无服务器函数中，无需自建服务器或数据库。
- 每次调用在隔离运行时中执行，应用之间相互隔离。
- 运行时只有 `/tmp` 可写，且不保证跨调用保留；NEVER 将 `/tmp` 当作持久存储。
- 出站网络请求只允许访问 `permissions.external.fetch.backend` 中声明的域名或 `remotes`。
- 应用不能读取 PingCode 用户的登录凭据或会话，也不能修改用户身份、权限或密码。

### 2.2 两类后端函数

Nexus 后端函数分为两类：

1. **Resolver 函数**：响应前端 `@pc-nexus/bridge` 的 `invoke` 调用，或作为扩展模块的 resolver。
2. **事件处理函数**：响应订阅的事件（system、lifecycle、webhook、scheduled、app）。

此外还有两种由 manifest 驱动的后端工作负载：

- **异步消费者（Consumer）**：处理 `@pc-nexus/async` 队列消息。
- **Exposer 路由处理函数**：处理应用对外暴露的自定义 REST API 请求。

所有这些处理函数都接收统一的 `context: NexusAppContext` 作为第一个参数。

### 2.3 调用与运行时限制

发布前 ALWAYS 检查以下限制：

| 类别 | 限制 |
|---|---|
| UI Invoke 超时 | `5 秒` |
| 其他调用超时（网络等） | `60 秒` |
| Webhook 处理函数响应超时 | `60 秒` |
| Scheduled `timeout` 最小值 | `60 秒` |
| 请求负载 | `512 KB` |
| 响应负载 | `5 MB` |
| 每次调用内存 | `512 MB` |
| 每次调用磁盘 | `512 MB`（仅 `/tmp` 可写） |
| 出站请求（每环境） | `300000 次/分钟` |
| 出站请求（每安装） | `10000 次/分钟` |
| 用户调用频率 | `1200 次/分钟/用户/安装` |
| 安装调用频率 | `5000 次/分钟/安装` |
| 应用调用频率（跨安装） | `30000 次/分钟/环境` |

NEVER 在 UI Invoke 中执行超过 5 秒的任务；耗时任务 ALWAYS 改用异步队列或事件处理。

### 2.4 推荐的后端分层结构

Resolver 只负责：校验输入、协调领域服务、返回结果。业务逻辑放在 service 层，外部系统调用放在 infrastructure 层：

```text
src/
├── resolvers/
│   └── index.ts          # Resolver 定义（@pc-nexus/core）
├── handlers/
│   └── index.ts          # 事件处理函数（@pc-nexus/event）
├── consumers/
│   └── index.ts          # 异步消费者（@pc-nexus/async）
├── domain/
│   ├── entities/
│   └── services/
├── infrastructure/
│   ├── pingcode-api/     # api.invoke 封装
│   ├── external-api/     # fetch.request / remote.invoke 封装
│   └── storage/          # kvs / ces / nos 封装
└── shared/
    ├── errors/
    └── types.ts
```

ALWAYS 为前后端共享的 payload、返回值和业务对象定义明确的 TypeScript 类型；NEVER 使用 `any` 或非刻意设计的 `unknown` 掩盖类型错误。

## 3. 应用上下文 `NexusAppContext`

所有 Resolver、事件处理函数和消费者的第一个参数都是 `context`，类型为 `NexusAppContext`：

```typescript
import { app } from "@pc-nexus/core";

const ctx = app.getContext();
```

`NexusAppContext` 结构：

```typescript
export interface NexusAppContext {
    app: { id: string; version: string };
    environment: { id: string; type: "development" | "production" };
    team: { id: string; url: string; locale: string; timezone: string };
    installation: { id: string };
    invocation: { id: string };
    user?: { id: string; locale: string; timezone: string };
    extension?: {
        key: string;
        local_id: string;
        target: string;
        location: string;
        data?: Record<string, unknown>;
    };
    event?: { trigger: { key: string; type: string } };
}
```

要点：

- `context.user` 在 scheduled 触发器中恒为 `undefined`；在匿名访问场景也可能缺失。
- `context.extension` 仅在扩展模块 Resolver 调用中存在，`data` 由扩展点上下文决定。
- `context.event.trigger` 在事件处理函数中标识触发该次调用的触发器。
- 在处理函数内部无需再调用 `app.getContext()`，直接使用入参 `context`。

## 4. Resolver 函数

### 4.1 安装依赖

```shell
npm install @pc-nexus/core@0.5.0
```

`@pc-nexus/core` 后端版本固定为 `0.5.0`，与 `@pc-nexus/cli@0.5.1` 兼容；其他 `@pc-nexus/*` 包同样安装与该 CLI 兼容的 `0.5.0` 版本。

### 4.2 定义 Resolver

在 `src/resolvers/index.ts` 中：

```typescript
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<string, string>("greeting", async (_context, payload) => {
    return `Hello, ${payload}`;
});

resolver.define<{ name: string }, { message: string }>(
    "exampleFunctionKey",
    async (_context, payload) => {
        return { message: `Hello, ${payload.name}!` };
    },
);

export { resolver };
```

方法签名：

```typescript
public define<P, R = unknown>(key: string, fn: (context: NexusAppContext, payload: P) => Promise<R>): this;
```

规则：

- `key` 必须与前端 `invoke(key, payload)` 完全一致。
- `payload` 和返回值 ALWAYS 定义明确类型；前后端类型不一致时，修改前端使其与后端契约一致。
- Resolver 返回值会被序列化后返回给前端，响应负载不得超过 `5 MB`。

### 4.3 在 manifest 中关联扩展模块

```yaml
extensions:
  - key: hello-world-project-page
    title: Hello World
    target: "pcm:pjm:project:page"
    resource: main
    resolver:
      function: resolver

functions:
  - key: resolver
    handler: index.resolver

resources:
  - key: main
    path: web/main/dist
```

`functions[].handler` 格式为 `file.function` 或 `dir/file.function`，最大长度 `1024`，必须匹配正则：

```text
/^([\p{Alpha}\d_-]+(?:\/[\p{Alpha}\d_-]+)*)\.([\p{Alpha}\d_-]+)$/u
```

Custom UI 模板中 Resolver 入口通常为 `src/resolvers/index.ts`，对应 handler 为 `index.resolver`（以构建配置为准）。

### 4.4 Resolver 相关错误

| 错误码 | 含义 |
|---|---|
| `ERR_FUNCTION_EXTENSION_NOT_FOUND` | 调用所指向的扩展不在 `manifest.extensions` 中 |
| `ERR_FUNCTION_RESOLVER_INVALID` | 扩展未配置 `resolver` |
| `ERR_FUNCTION_RESOLVER_FUNCTION_INVALID` | `resolver.function` 字段缺失 |
| `ERR_FUNCTION_FUNCTION_NOT_FOUND` | `resolver.function` 指向的 key 不在 `functions` 中 |

## 5. 事件处理函数

### 5.1 安装依赖与文件结构

```shell
npm install @pc-nexus/event
```

推荐结构：

```text
src/handlers/index.ts
```

事件处理器类型统一从 `@pc-nexus/event` 导入：

```typescript
import type {
    SystemEventHandler,
    LifecycleEventHandler,
    WebhookEventHandler,
    ScheduledEventHandler,
} from "@pc-nexus/event";
```

所有事件处理器类型（`SystemEventHandler`、`LifecycleEventHandler`、`WebhookEventHandler`、`ScheduledEventHandler` 等）统一从 `@pc-nexus/event` 导入，NEVER 从 `@pc-nexus/core` 导入。

所有事件处理器均为 `(context, event) => Promise<unknown>`，触发器信息位于 `context.event.trigger`。

### 5.2 System 事件

manifest：

```yaml
event:
  triggers:
    - key: system-trigger
      type: system
      events:
        - pce:pjm:workitem:created
        - pce:pjm:workitem:updated
      handler:
        function: system-handler
      filter:
        ignoreSelf: true
functions:
  - key: system-handler
    handler: index.handler
```

处理器：

```typescript
import type { SystemEventHandler } from "@pc-nexus/event";

export const handler: SystemEventHandler = async (context, event) => {
    console.log(event.event_type);
    console.log(event.self_generated);
    console.log(JSON.stringify(event.payload.data));
};
```

事件结构：

```typescript
interface HandlerFunctionEvent {
    event_type: string;
    self_generated: boolean;
    payload: {
        data: unknown;          // 主体资源，结构对应该资源的 REST GET 响应
        changelog?: {           // 仅修改类事件（updated 等）存在；创建/删除类事件无此字段
            origin?: unknown;
            target?: unknown;
            property?: unknown;
        };
        source?: string;
    };
}
```

规则：

- 事件名称以 `pce:` 开头，例如 `pce:pjm:workitem:created`、`pce:ship:idea:updated`。
- 必须在 `permissions.scopes` 中声明对应读权限，例如 `pcp:read:pjm:workitem`，否则可能收不到事件或数据不完整。
- `self_generated` 表示事件是否由本应用自身的 REST 操作触发；ALWAYS 对更新/创建类订阅设置 `filter.ignoreSelf: true`，避免循环。
- 事件处理器以系统身份运行，不具备交互式用户上下文；资源级权限仍可能拒绝访问。
- `payload.data` 的精确结构因事件而异，ALWAYS 以对应事件的 REST 资源文档为准。

### 5.3 Lifecycle 事件

```yaml
event:
  triggers:
    - key: lifecycle-trigger
      type: lifecycle
      events:
        - pce:nexus:app:install
      handler:
        function: lifecycle-handler
```

支持事件：

- `pce:nexus:app:install`：安装完成后触发。
- `pce:nexus:app:uninstall`：卸载前触发（由 UI 操作发起）。
- `pce:nexus:app:upgrade`：升级时触发。

```typescript
import type { LifecycleEventHandler } from "@pc-nexus/event";

interface LifecycleEventPayload {
    installation_id: string;
    app: { id: string; version: string; name: string; publisher: string };
    environment: { id: string; type: string; name: string };
    operated_by: string;
}

export const handler: LifecycleEventHandler = async (context, event) => {
    const payload = event.payload as LifecycleEventPayload;
    console.log(payload.installation_id);
};
```

NEVER 在 lifecycle handler 中执行长耗时任务；这些任务应通过异步队列解耦。

### 5.4 Webhook 事件

manifest：

```yaml
event:
  triggers:
    - key: webhook-trigger
      type: webhook
      handler:
        function: webhook-handler
functions:
  - key: webhook-handler
    handler: index.handler
```

运行时获取 Webhook URL：

```typescript
import { webhook } from "@pc-nexus/event";

const url = await webhook.getUrl("webhook-trigger");
const url2 = await webhook.getUrl("webhook-trigger", { forceCreate: true });
const all = await webhook.queryUrls();
await webhook.deleteUrl(url);
```

API：

```typescript
webhook.getUrl(webTriggerKey: string, options?: { forceCreate?: boolean }): Promise<string>;
webhook.queryUrls(webTriggerKey?: string): Promise<Array<{ webTriggerKey: string; url: string }>>;
webhook.deleteUrl(webhookUrl: string): Promise<void>;
```

URL 格式：

```text
https://{appid}.webhook.pingcodex.com/x1/{webhook_id}
```

处理器：

```typescript
import type { WebhookEventHandler } from "@pc-nexus/event";

export const handler: WebhookEventHandler = async (context, event) => {
    const { method, path, headers, body, queryParameters } = event.payload;
    return {
        statusCode: 200,
        headers: { "Content-Type": "application/json" },
        body: { ok: true },
    };
};
```

`event.payload` 字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `method` | `string` | `GET`/`POST`/`PUT`/`DELETE`/`PATCH` |
| `path` | `string` | 请求路径 |
| `headers` | `Record<string, string[]>` | 请求头 |
| `body` | `string \| JSON \| XML \| x-www-form-urlencoded` | 请求体 |
| `queryParameters` | `Record<string, string \| string[]>` | 查询参数 |

返回值必须为：

```typescript
interface WebhookEventResult {
    statusCode: number;
    headers?: Record<string, string | string[]>;
    body?: unknown;
}
```

安全要点：

- Nexus **不对 Webhook 请求做任何鉴权**。如果端点不是公开的，ALWAYS 在 handler 内自行校验签名、令牌或来源 IP。
- 每个应用最多 `8` 个 webhook 触发器，每个 trigger key 最多 `32` 个 URL。

### 5.5 Scheduled 事件

```yaml
event:
  triggers:
    - key: scheduled-trigger
      type: scheduled
      interval: hour
      timeout: 60
      handler:
        function: scheduled-handler
```

属性：

- `interval`（必填）：`tenMinute`、`hour`、`day`、`week`。
- `timeout`（可选）：超时秒数，最小 `60`。

```typescript
import type { ScheduledEventHandler } from "@pc-nexus/event";

export const handler: ScheduledEventHandler = async (context) => {
    // event.payload 为 {}，event.event_type 为 undefined，context.user 为 undefined
};
```

行为约束：

- 首次执行时间由安装时间和间隔决定；重新部署会重置所有定时触发器。
- 至少一次投递（at-least-once），handler 必须幂等。
- 执行失败不会重试，下一次按正常间隔触发。
- 每个应用最多 `8` 个定时触发器，且最多 `1` 个 `tenMinute` 触发器。

### 5.6 App 自定义事件

订阅其他应用通过 `event.registries` 声明的自定义事件：

```yaml
event:
  triggers:
    - key: app-trigger
      type: app
      events:
        - nae:app:466d303d-a2c4-4ec4-ad7c-5435be94583b:event-key
      handler:
        function: app-event-handler
```

发布事件通过 `event.registries` 声明：

```yaml
event:
  registries:
    - key: event-key
      name: Event name
      allowedRecipients:
        - app:466d303d-a2c4-4ec4-ad7c-5435be94583b
```

### 5.7 事件相关错误码

| 错误码 | 含义 |
|---|---|
| `ERR_EVENT_FUNCTION_NOT_FOUND` | `handler.function` 指向的函数未在 `functions` 中声明 |
| `ERR_EVENT_LIFECYCLE_HANDLER_INVALID` | lifecycle 触发器缺少有效的 `handler.function` 或 `handler.endpoint` |
| `ERR_EVENT_WEBHOOK_*` | webhook 路径、方法、Content-Type、URL、触发器或 handler 无效（具体码见 wiki） |
| `ERR_EVENT_SCHEDULE_UNIT_INVALID` / `ERR_EVENT_SCHEDULE_INTERVAL_INVALID` | 定时触发器配置无效 |

## 6. 调用 PingCode REST API

### 6.1 安装与 manifest 权限

```shell
npm install @pc-nexus/network@0.5.0
```

```yaml
permissions:
  scopes:
    - "pcp:read:pjm:workitem"
    - "pcp:write:pjm:workitem"
```

NEVER 调用未声明 scope 的接口；NEVER 编造 scope，ALWAYS 在对应 REST API 文档中确认。

### 6.2 使用 `api.invoke`

```typescript
import { api } from "@pc-nexus/network";
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<{ workitemId: string }, unknown>("getWorkItem", async (context, payload) => {
    const response = await api.invoke(`/v1/pjm/work_items/${payload.workitemId}`, {
        as: "user",
        userId: context.user?.id ?? "",
    });
    if (!response.ok) {
        throw new Error(`PingCode API error: ${response.status}`);
    }
    return response.json();
});

export { resolver };
```

签名：

```typescript
api.invoke(path: string, options?: RequestInit & { as?: "app" | "user"; userId?: string }): Promise<Response>;
```

调用身份：

- `as: "user"`：以指定用户身份调用，必须传 `userId`。用户本身还必须拥有 PingCode 中的对应资源权限。
- `as: "app"`：以应用身份调用，可访问 scope 允许的全部数据。
- 省略 `as`：不附加任何认证信息，仅用于公开接口。

POST 示例：

```typescript
const response = await api.invoke("/v1/pjm/work_items", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ title: "新建工作项", type: "story" }),
    as: "app",
});
```

错误码：

- `ERR_REST_API_PATH_INVALID`：API 路径为空。
- `ERR_REST_API_SCOPE_FORBIDDEN`：未声明所需 scope 或身份无权限。

PingCode REST API 路径统一以 `/v1/pjm/...` 等产品模块前缀开头（例如工作项为 `/v1/pjm/work_items/...`），NEVER 使用已废弃的 `/v1/project/...` 写法。

## 7. 调用外部 API 与远程服务

### 7.1 使用 `fetch.request` 调用外部 HTTPS API

manifest：

```yaml
permissions:
  scopes: []
  external:
    fetch:
      backend:
        - "api.example.com"
        - "*.example-dev.com"
```

支持的域名格式：完整 HTTPS URL、裸域名、`*.subdomain` 通配符（不含父域名本身）、`*`（允许任意域名）。

```typescript
import { fetch } from "@pc-nexus/network";

const response = await fetch.request("https://api.example.com/users", {
    method: "GET",
    headers: { Accept: "application/json" },
});
const data = await response.json();
```

签名：

```typescript
fetch.request(url: string, options?: RequestInit): Promise<Response>;
```

约束：

- 基于 undici 的 Fetch 实现，不支持 `dispatcher` 选项。
- 以 `x-nexus-` 开头的头部为保留头，应用设置的值会被覆盖。
- 未声明的域名会被运行时拦截。
- 单次外部请求超时 `60 秒`。
- `body` 遵循标准 `RequestInit` 语义：发送 JSON 时 ALWAYS 传入 `JSON.stringify(obj)` 并设置 `Content-Type: application/json`，NEVER 直接将普通对象作为 `body`。

错误码：`ERR_FETCH_HEADER_INVALID`、`ERR_FETCH_PERMISSION_INVALID`、`ERR_FETCH_PERMISSION_FORBIDDEN`。

### 7.2 使用 `remotes` 与 `remote.invoke`

当外部服务需要 Nexus 注入调用令牌（NIT）、用户令牌或应用令牌时，使用 `remotes`：

manifest：

```yaml
permissions:
  scopes:
    - "pcp:read:user:token"
remotes:
  - key: my-remote
    baseUrl: "https://api.example.com"
    auth:
      userToken: true
      appToken: false
```

- `auth.userToken: true` 必须声明 `pcp:read:user:token`。
- `auth.appToken: true` 必须声明 `pcp:read:app:token`。
- `baseUrl` 最长 `2048`，匹配 `/^https?:\/\/[^\/\s]+(?:\/[^\s]*)?$/i`。

后端调用：

```typescript
import { remote } from "@pc-nexus/network";

const response = await remote.invoke("my-remote", {
    path: "/greeting?name=nexus",
    method: "GET",
});

const post = await remote.invoke("my-remote", {
    path: "/work",
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ team: "nexus" }),
});
```

Nexus 附加到远程请求的头部：

| Header | 说明 |
|---|---|
| `Authorization: Bearer <NIT>` | Nexus Invocation Token（JWT，RS256，TTL 5 分钟） |
| `traceparent` | W3C Trace Context |
| `x-nexus-api-base-url` | 回调 PingCode REST API 的基础 URL |
| `x-nexus-app-token` | 启用 `auth.appToken` 时下发 |
| `x-nexus-user-token` | 启用 `auth.userToken` 且存在用户时下发 |

远程服务必须：

1. 校验 `Authorization` 中的 NIT：验证 `iss === "nexus/invocation-token"`、`aud === "nexus"`、`exp` 与 RS256 签名，公钥来自 `{nexus-host}/api/nexus/nit/.well-known/jwks.json`。
2. NIT 校验通过前不要信任任何其他头部。

错误码：`ERR_REMOTE_KEY_NOT_FOUND`、`ERR_REMOTE_ENDPOINT_NOT_FOUND`、`ERR_REMOTE_EXTENSION_RESOLVER_NOT_FOUND`。

## 8. 校验用户权限

使用 `@pc-nexus/core` 的 `authorize`：

```typescript
import { authorize } from "@pc-nexus/core";

const globalPerms = await authorize.getUserPermissions("global");
const projectPerms = await authorize.getUserPermissions("project", "project-id");
const workitemPerms = await authorize.getUserPermissions("workitem", "INFR-13");

const canEdit =
    workitemPerms.find((p) => p.key === "pca:pjm:requirement:edit")?.has_permission ?? false;
```

API：

```typescript
authorize.getPermissionPoints(): Promise<Record<string, Array<{ key: string; name: string; group: string }>>>;

authorize.getUserPermissions(type: "global", userId?: string): Promise<Array<{ key: string; has_permission: boolean }>>;
authorize.getUserPermissions(
    type: "product" | "project" | "library" | "space" | "idea" | "ticket" | "workitem" | "testcase" | "page",
    id: string,
    userId?: string,
): Promise<Array<{ key: string; has_permission: boolean }>>;
```

要点：

- `userId` 省略时默认取 `context.user.id`。
- `display` 显示条件只在前端生效，NEVER 将其作为安全边界；敏感操作 ALWAYS 在后端使用 `authorize` 或在业务逻辑中再次校验。
- 完整权限点 key 列表（如 `pca:global:pjm:project:create`）参考权限点参考文档。

## 9. 存储

所有托管存储都需要声明 scope：

```yaml
permissions:
  scopes:
    - "pcp:storage:app"
```

```shell
npm install @pc-nexus/storage@0.5.0
```

### 9.1 KVS（键值存储）

适合存储用户偏好、配置等小型数据：

```typescript
import { kvs } from "@pc-nexus/storage";

interface DemoEntity { foo: string; }

await kvs.set<DemoEntity>("key1", { foo: "bar" });
await kvs.set("secret-key", "token", { secret: true, policy: "FAIL_IF_EXISTS" });

const value = await kvs.get<DemoEntity>("key1");
const secret = await kvs.get<string>("secret-key", { secret: true });

await kvs.delete("key1");
```

API：

```typescript
kvs.set<T>(key: string, value: T, options?: { policy?: "OVERRIDE" | "FAIL_IF_EXISTS"; secret?: boolean }): Promise<{ key: string; value: T }>;
kvs.get<T>(key: string, options?: { secret?: boolean }): Promise<T | undefined>;
kvs.delete(key: string): Promise<void>;
```

限制：

- Key 最大长度 `512`。
- 单个 value 最大 `256 KB`，嵌套深度最大 `32`。
- 读取 `secret: true` 写入的数据时必须传 `{ secret: true }`，否则报 `ERR_KVS_GET_OPTIONS_INVALID`。

### 9.2 CES（自定义实体存储）

适合结构化数据。先在 manifest 中声明实体：

```yaml
storage:
  entities:
    - name: employees
      attributes:
        - name: name
          type: string
          required: true
          default: ""
        - name: age
          type: number
      indexes:
        - name: name_age_
          keys: { name: 1, age: 1 }
          options: { unique: true }
```

支持的属性类型：`string`、`number`、`boolean`、`object`、`array`。索引字段只能是标量，`array`/`object` 不能建索引。

```typescript
import { ces, Direction } from "@pc-nexus/storage";

interface EmployeesEntity {
    name: string;
    age: number;
    description?: string;
}

const repo = ces.entity<EmployeesEntity>("employees");

await repo.insert({ name: "Davis", age: 25 });
await repo.insert([
    { name: "a", age: 1 },
    { name: "b", age: 2 },
]);

await repo.update(
    (cb) => { cb.field("name").eq("a"); },
    { age: 10 },
);

const list = await repo.find(
    (cb) => {
        cb.field("name").eq("Davis");
        cb.and((a) => { a.field("age").gt(18); });
        cb.or((o) => {
            o.field("description").eq("engineer");
            o.field("description").eq("manager");
        });
    },
    {
        sort: [{ propertyKey: "age", order: Direction.ascending }],
        limit: 20,
        skip: 0,
    },
);

const total = await repo.count((cb) => { cb.field("age").gte(18); });
await repo.delete((cb) => { cb.field("age").lt(0); });
```

`ConditionBuilder` 操作符：

- 通用：`eq`、`ne`、`exists(boolean)`。
- 数字：`gt`、`gte`、`lt`、`lte`。
- 字符串/数组：`contains`、`notContains`。
- 组合：`and(cb)`、`or(cb)`。

`delete` 为物理删除，不可恢复。

限制：每个应用最多 `32` 个实体，每个实体最多 `64` 个属性、`4` 个索引。

实体迁移限制（已部署到开发/生产后）：

- 不能删除已声明实体。
- 不能删除属性或修改属性类型。
- 不能将可选属性改为必填。

### 9.3 NOS（对象存储/文件）

适合通过预签名 URL 上传下载二进制文件：

```typescript
import { nos } from "@pc-nexus/storage";

const upload = await nos.createUploadUrl(
    { key: "upload-file-1", size: 1024, checksum: "...", checksum_type: "SHA256" },
    { overwrite: false },
);
const uploadUrl = upload.url;

const download = await nos.createDownloadUrl("upload-file-1");
const meta = await nos.getMetadata("upload-file-1");
await nos.delete("upload-file-1");
```

API：

```typescript
nos.createUploadUrl(
    body: { key: string; size: number; checksum: string; checksum_type: "SHA1" | "SHA256" | "CRC32" | "CRC32C" },
    options?: { overwrite?: boolean },
): Promise<{ url: string }>;

nos.createDownloadUrl(key: string): Promise<{ url: string }>;
nos.getMetadata(key: string): Promise<{ key: string; name: string; mime_type?: string; checksum: string; size: number; created_at?: number }>;
nos.delete(key: string): Promise<void>;
```

限制：单文件最大 `1 GB`；预签名 URL 有效期 `1 小时`；上传限流 `5000 req/s/安装`，预签名 URL 限流 `1000 req/s/安装`。

### 9.4 托管数据生命周期

- 应用安装后才会为企业初始化存储。
- 升级会为新实体/索引追加资源，不影响已有数据。
- 卸载后数据软删除并保留 `30 天`，`30 天` 内重新安装可恢复数据，超期永久删除。
- 删除应用前必须先卸载所有安装。

## 10. 异步队列

### 10.1 manifest 声明

```yaml
async:
  queues:
    - key: image-processing
  consumers:
    - key: image-consumer
      queue: image-processing
      handler:
        function: image-consumer-handler
      concurrency: 2
```

- `concurrency` 默认 `8`，为每个队列的最大并行消费者数。
- 队列/消费者 key 在同一 manifest 中必须唯一。

### 10.2 生产者：推送消息

```typescript
import { queue } from "@pc-nexus/async";

const { jobId } = await queue.push("image-processing", { imageId: "img-1" });
const batch = await queue.push("image-processing", [
    { imageId: "img-1" },
    { imageId: "img-2" },
], { delay: 30 });

interface ImageJob { imageId: string; width: number; }
await queue.push<ImageJob>("image-processing", { imageId: "img-1", width: 800 });
```

API：

```typescript
queue.push<T>(key: string, payload: T | T[], options?: { delay?: number }): Promise<{ jobId: string }>;
```

- `delay` 单位为秒，`0` 或省略表示立即投递。
- `push` 只保证入队，不等待消费者执行完成。
- 批量推送共用一个 `jobId`。

限制：单次 `push` 最多 `50` 条，总负载不超过 `256 KB`。

### 10.3 消费者：处理消息

```typescript
import type { ConsumerHandler } from "@pc-nexus/async";

interface ImageJob { imageId: string; width: number; }

export const handler: ConsumerHandler<ImageJob> = async (context, task) => {
    const { imageId, width } = task.payload;
    console.log(task.task_id, task.job_id, task.consumer.key);
};
```

`task` 字段：

| 字段 | 说明 |
|---|---|
| `payload` | `queue.push` 传入的对象，原样透传 |
| `task_id` | 单条任务 ID，用于幂等/去重 |
| `job_id` | 批量任务共享的作业 ID |
| `consumer.key` | 当前消费者的 key |

## 11. 对外暴露自定义 REST API（Exposer）

通过 `exposer` 将后端函数暴露为自定义 REST API，并声明自定义 scope：

```yaml
exposer:
  scopes:
    - name: ncp:read:employee
      displayName: Read Employee Info
      description: Read Employee Info
  routes:
    - key: get-employee
      path: /employeeName
      method: GET
      accept:
        - application/json
      scopes:
        - ncp:read:employee
      handler:
        function: employee-handler

functions:
  - key: employee-handler
    handler: index.employeeHandler
```

自定义 scope 规则：

- 名称必须以 `ncp:` 开头。
- 每个应用最多声明 `16` 个 scope。
- 命名采用「动词+名词」，例如 `ncp:read:employee`、`ncp:write:employee`。

每个应用最多 `32` 条路由；`method` 支持 `GET`、`POST`、`PUT`、`DELETE`、`PATCH`；`accept` 当前仅支持 `application/json`。

## 12. 国际化（服务端）

```typescript
import { i18n } from "@pc-nexus/core";

const { locale, translations } = await i18n.getTranslations("en-US");
const t = await i18n.createTranslator("en-US");
const label = t.translate("app.version", { v: context.app.version });
```

- 翻译文件在 `manifest.yaml` 的 `translations.resources` 中声明，`fallback.default` 指定回退语言。
- `translate(key, params)` 支持点分 key 与 `{{param}}` 占位符。
- 服务端仅支持 `zh-CN` 和 `en-US` 两种语言代码。

## 13. 错误处理

所有 Nexus 错误统一为：

```typescript
interface NexusError {
    code: string;
    message: string;
}
```

处理模式：

```typescript
try {
    // 业务逻辑
} catch (error) {
    const err = error as { code?: string; message: string };
    console.error(`${err.code ?? "UNKNOWN"} : ${err.message}`);
    if (err.code === "ERR_REMOTE_KEY_NOT_FOUND") {
        // 针对特定错误码处理
    }
    throw error;
}
```

后端通用规则：

- 对 PingCode/外部 API 响应 ALWAYS 检查 `response.ok`/`status`，并将 4xx/5xx 转换为有意义的业务错误。
- 操作不存在的资源时返回明确的“未找到”结果，而不是让异常冒泡为 500。
- 对事件与队列任务 ALWAYS 设计幂等处理，避免重复投递产生副作用。
- 未捕获的运行时异常会被平台自动记录为 Error 级别日志并附带堆栈。

## 14. 日志

后端使用标准 `console`：

```typescript
console.log("info message");
console.info("info message");
console.debug("debug message");
console.warn("warn message");
console.error("error message");
```

平台会自动附加：Level、Time、Environment、Invocation ID、Trace ID、Extension、Event Trigger、Function、Version、Site。结构化对象使用 `JSON.stringify(obj, null, 2)`。

查看开发环境日志：

```shell
nexus logs
nexus logs --grouped
nexus logs --invocation <invocation-id>
nexus logs --since 2d
nexus logs --environment development --verbose
```

规则：

- 日志保留 `30 天`。
- 开发环境日志无法关闭；Staging/Production 不支持 CLI 拉取日志，由企业管理员在后台控制是否允许记录。
- NEVER 在日志中输出访问令牌、用户凭证、个人隐私或其他敏感信息。
- 前端 `console` 不会出现在 `nexus logs` 中，只能通过浏览器开发者工具查看。

## 15. 完整示例：一个最小的后端应用

`manifest.yaml`：

```yaml
app:
  id: "466d303d-a2c4-4ec4-ad7c-5435be94583b"
  version: 1.0.0

extensions:
  - key: workitem-page
    title: Work Item Helper
    target: "pcm:pjm:project:page"
    resource: main
    resolver:
      function: resolver

functions:
  - key: resolver
    handler: index.resolver

resources:
  - key: main
    path: web/main/dist

async:
  queues:
    - key: image-processing
  consumers:
    - key: image-consumer
      queue: image-processing
      handler:
        function: image-consumer-handler
      concurrency: 2

event:
  triggers:
    - key: webhook-trigger
      type: webhook
      handler:
        function: webhook-handler

permissions:
  scopes:
    - "pcp:read:pjm:workitem"
    - "pcp:storage:app"
  external:
    fetch:
      backend:
        - "api.example.com"
```

`src/resolvers/index.ts`：

```typescript
import { Resolver } from "@pc-nexus/core";
import { api, fetch } from "@pc-nexus/network";
import { queue } from "@pc-nexus/async";
import { kvs } from "@pc-nexus/storage";

const resolver = new Resolver();

resolver.define<{ workitemId: string }, unknown>("getWorkItem", async (context, payload) => {
    const response = await api.invoke(`/v1/pjm/work_items/${payload.workitemId}`, {
        as: "user",
        userId: context.user?.id ?? "",
    });
    return response.json();
});

resolver.define<{ imageId: string }, { jobId: string }>("enqueueImage", async (_context, payload) => {
    const { jobId } = await queue.push("image-processing", payload);
    return { jobId };
});

resolver.define<{ key: string; value: string }, void>("savePreference", async (_context, payload) => {
    await kvs.set(payload.key, payload.value);
});

resolver.define<void, unknown>("fetchExternal", async () => {
    const response = await fetch.request("https://api.example.com/status", { method: "GET" });
    return response.json();
});

export { resolver };
```

`src/consumers/index.ts`：

```typescript
import type { ConsumerHandler } from "@pc-nexus/async";

interface ImageJob { imageId: string; }

export const handler: ConsumerHandler<ImageJob> = async (_context, task) => {
    console.log(`processing ${task.payload.imageId} (${task.task_id})`);
};
```

`src/handlers/index.ts`：

```typescript
import type { WebhookEventHandler } from "@pc-nexus/event";

export const handler: WebhookEventHandler = async (_context, event) => {
    return {
        statusCode: 200,
        headers: { "Content-Type": "application/json" },
        body: { received: event.payload.path },
    };
};
```

## 16. 不要做的事

- NEVER 使用 `@forge/*` 包或任何 Atlassian Forge API。
- NEVER 编造 scope、事件名、扩展点 target、权限点或 REST 路径。
- NEVER 在未声明 `permissions.scopes` 的情况下调用 PingCode REST API。
- NEVER 调用未在 `permissions.external.fetch.backend` 或 `remotes` 中声明的外部域名。
- NEVER 在 Webhook handler 中假设请求已被鉴权。
- NEVER 依赖前端显示条件（`display`）做安全判断；敏感操作 ALWAYS 在后端校验。
- NEVER 在 UI Invoke 中执行超过 5 秒的工作。
- NEVER 在 `/tmp` 中保存需要跨调用保留的数据。
- NEVER 在日志中输出令牌、凭证或隐私数据。
- NEVER 使用 `any` 或非必要的 `unknown` 逃避前后端契约类型。

## 17. 下一步

- 在 PingCode 事件文档中确认你要订阅的 `pce:*` 事件的精确 payload。
- 在 REST API 文档中确认每个接口所需的 scope 与路径。
- 修改 manifest 后运行 `nexus deploy -e development`，确认 `Manifest is valid.` 和 `Lint passed.`。
- 使用 `nexus serve -e development` 在本地调试 Resolver、事件处理器和消费者，使用 `nexus logs` 查看开发环境日志。
- 权限、外部域名、scope 发生变化后，重新 `nexus deploy` 与 `nexus distribute`，并由企业管理员重新确认安装。
