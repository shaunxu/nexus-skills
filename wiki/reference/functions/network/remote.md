---
title: "remote"
lastUpdated: 2026-07-28T08:29:51.000Z
---

# remote

`remote` 模块用于向远程服务发起 HTTP 请求，支持应用在 Nexus 函数内与远程后端服务进行集成。

导入：

```typescript
import { remote } from "@pc-nexus/network";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>invoke</code></td><td>向远程服务发起 HTTP 请求，该方法会根据配置决定是否携带 OAuth 令牌</td></tr></tbody></table>

## invoke

使用 `invoke` 方法发起一个 HTTP 请求到配置的远程服务端点。

### 函数签名

```javascript
function invoke(remoteKey: string, options: RemoteInvokeOptions): Promise<Response>

type RemoteInvokeOptions = { path?: string; } & RequestInit;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 43.71%" /><col style="width: 56.29%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>remoteKey</code></td><td><code>manifest</code> 中声明的 remote key</td></tr><tr><td><code>options</code></td><td>请求选项，见下方详细说明</td></tr></tbody></table>

`RemoteInvokeOptions` 类型定义如下：

|名称|描述|
|---|---|
|`path`|请求路由地址|
|`method`|HTTP 请求方法|
|`headers`|自定义请求头|
|`body`|请求体内容|

### 返回值

返回标准的 `Response` 对象，可通过 `response.status` 、 `response.ok` 、 `response.json()` 、 `response.text()` 等标准方法处理响应。

### 示例

#### GET 请求

```javascript
import { remote } from "@pc-nexus/network";

const response = await remote.invoke(`my-remote-key`, {
    path: "/greeting?name=nexus",
    method: "GET"
});

const data = await response.json();
console.log(data);
```

#### POST 请求

```javascript
import { remote } from "@pc-nexus/network";

const response = await remote.invoke(`my-remote-key`, {
    path: "/work",
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
    body: JSON.stringify({
        team: "nexus",
    })
});

const status = response.status;
const result = await response.json();
```

### 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 36.3%" /><col style="width: 63.7%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_REMOTE_EXTENSION_RESOLVER_NOT_FOUND</code></td><td>在 <code>manifest</code> 中，未找到对应的 <code>extension resolver key</code></td></tr><tr><td><code>ERR_REMOTE_ENDPOINT_NOT_FOUND</code></td><td>在 <code>manifest</code> 中，未找到对应的 <code>endpoint key</code></td></tr><tr><td><code>ERR_REMOTE_KEY_NOT_FOUND</code></td><td>在 <code>manifest</code> 中，未找到对应的 <code>remote key</code></td></tr></tbody></table>
