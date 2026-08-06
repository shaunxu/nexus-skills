---
title: "fetch"
lastUpdated: 2026-07-28T08:22:36.000Z
---

# fetch

`fetch` 模块内置方法用于向外部资源发起 HTTP 请求，适用于访问第三方服务（如 GitHub、Slack、自建服务等）。

导入：

```typescript
import { fetch } from "@pc-nexus/network";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>request</code></td><td>向外部资源发起 HTTP 请求</td></tr></tbody></table>

## request

`request` 函数用于向外部资源发起 HTTP 请求。

### 函数签名

```typescript
function request(url: string, options?: RequestInit): Promise<Response>
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 50%" /><col style="width: 50%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>url</code></td><td>请求的完整 URL</td></tr><tr><td><code>options</code></td><td>请求选项 - 目前不支持 dispatcher 属性设置 - 其余见下方详细说明</td></tr></tbody></table>

`RequestInit` 类型部分属性定义如下：

|名称|描述|
|---|---|
|`method`|HTTP 请求方法|
|`headers`|自定义请求头。 - 支持标准的 HTTP 请求头字段，如 `Content-Type` 、 `Accept` 、 `Authorization` 等 - 以 `x-nexus-` 开头的请求头为 Nexus 系统内部使用，用户不可定义使用，如果用户尝试设置此类请求，系统将自动覆盖其值。|
|`body`|请求体内容|

要了解完整的实现细节，请参阅 `undici` 文档中的在 [Node.js 中使用 Fetch API 与 Undici](https://nodejs.org/learn/getting-started/fetch#using-the-fetch-api-with-undici-in-nodejs) 这一章节。

### 返回值

返回标准的 `Response` 对象，可通过 `response.status` 、 `response.ok` 、 `response.json()` 、 `response.text()` 等标准方法处理响应。

### 权限声明

使用 `fetch` 访问外部资源前，需要在 `manifest.yaml` 中通过声明允许访问的域名。未声明的域名请求将被运行时拦截，同时抛出错误。

```yaml
permissions:
  scopes: []
  external:
    fetch:
      backend:
        - "api.example.com"        # 允许访问的域名
        - "*.example-dev.com"       # 支持通配符匹配子域名
```

关于权限声明详情请参考： [External permissions](/reference/manifest/permissions-external)

### 示例

#### GET 请求

```typescript
import { fetch } from "@pc-nexus/network";

const response = await fetch.request("https://api.example.com/users", {
    method: "GET",
    headers: {
        "Accept": "application/json",
    },
});

const data = await response.json();
console.log(data);
```

#### POST 请求

```typescript
import { fetch } from "@pc-nexus/network";

const response = await fetch.request("https://api.example.com/users", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
    body: {
        name: "张三",
        email: "zhangsan@example.com",
    },
});

const result = await response.json();
```

### 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 43.36%" /><col style="width: 56.64%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_FETCH_HEADER_INVALID</code></td><td><code>fetch header</code> 格式错误或者缺少 <code>url</code> 字段</td></tr><tr><td><code>ERR_FETCH_PERMISSION_INVALID</code></td><td><code>manifest</code> 未定义 <code>fetch backend</code> 权限</td></tr><tr><td><code>ERR_FETCH_PERMISSION_FORBIDDEN</code></td><td><code>fetch permission</code> 权限不足</td></tr></tbody></table>
