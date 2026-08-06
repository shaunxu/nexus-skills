---
title: "api"
lastUpdated: 2026-07-28T08:14:26.000Z
---

# api

`api` 模块内置方法可以帮助你在应用中调用 PingCode REST API ，无需手动管理认证信息。

导入：

```typescript
import { api } from "@pc-nexus/network";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>invoke</code></td><td>调用 PingCode REST API</td></tr></tbody></table>

## invoke

使用 `invoke` 函数可以向 PingCode REST API 发起请求，无需手动管理认证信息。

### 函数签名

```typescript
function invoke(path: string, options?: ApiRequestOptions): Promise<Response>

type ApiRequestOptions = RequestInit & {
    as?: "app" | "user";
    userId?: string;
};
```

### 参数

|名称|描述|
|---|---|
|`path`|请求路径|
|`options`|请求选项（见下方详细说明）|

`ApiRequestOptions` 类型定义如下：

|名称|描述|
|---|---|
|`method`|HTTP 请求方法，默认为 `GET`|
|`headers`|自定义请求头|
|`body`|请求体内容|
|`as`|请求的身份上下文（见下方说明）|
|`userId`|当 `as` 为 `"user"` 时，需指定具体用户 ID|

### 身份上下文

通过 `options.as` 指定请求的身份上下文。如果未指定 `as` ，请求将不携带认证信息。

|身份|描述|
|---|---|
|`as: "app"`|以 **应用身份** 发起请求。只要应用拥有相应权限，即可请求对应所有的数据。|
|`as: "user"`|以 **用户身份** 发起请求，表示当前操作者是某个具体用户。需要通过 `userId` 指定目标用户。|

### 声明作用域

作用域定义了应用在调用 PingCode REST APIs 时被允许执行的操作。每个 API 端点可能会要求应用拥有特定的作用域，如果应用未声明所需的作用域，对应的请求将因权限不足而失败。

应用必须在 `manifest.yaml` 文件的 `permissions.scopes` 字段中声明所需的作用域范围：

```yaml
permissions:
  scopes:
    - pcp:read:ship:idea 
    - pcp:write:ship:idea 
    - pcp:read:pjm:workitem 
    - pcp:write:pjm:workitem 
```

关于作用域详情参考： [Permissions](/reference/manifest/permissions)

### 返回值

返回标准的 `Response` 对象，可通过 `response.status` 、 `response.ok` 、 `response.json()` 、 `response.text()` 等标准方法处理响应。

### 示例

#### GET 请求

查询工作项详情：

```typescript
import { api } from "@pc-nexus/network";

const workitemId = "abc123";
const response = await api.invoke(`/v1/project/work_items/${workitemId}`, {
    as: "user",
});

const data = await response.json();
console.log(data);
```

#### POST 请求

创建资源时，通过 `method` 指定 HTTP 方法，通过 `body` 传递请求体：

```typescript
const response = await api.invoke(`/v1/project/work_items`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
    body: JSON.stringify({
        title: "新建工作项",
        type: "story",
    }),
    as: "app",
});

const status = response.status;
const result = await response.json();
```

#### 带查询参数的请求

```typescript
const keyword = "需求";
const params = new URLSearchParams({
    page: "1",
    pageSize: "20",
    keyword: keyword,
});

const response = await api.invoke(`/v1/project/work_items?${params}`, {
    as: "user",
});

const data = await response.json();
```

#### 不携带认证的请求

如果省略 `as` 参数，请求将不附加认证信息：

```typescript
const response = await api.invoke(`/v1/public/info`);
```

### 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.37%" /><col style="width: 57.63%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_REST_API_PATH_INVALID</code></td><td>请求的 API 地址为空</td></tr><tr><td><code>ERR_REST_API_SCOPE_FORBIDDEN</code></td><td>请求权限不足</td></tr></tbody></table>
