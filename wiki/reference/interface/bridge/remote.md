---
title: "remote"
lastUpdated: 2026-07-09T06:54:13.000Z
---

# remote

`remote` 使你的应用能够调用 PingCode 外部平台上的远程后端服务。

导入：

```typescript
import { remote } from '@pc-nexus/bridge';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.33%" /><col style="width: 66.67%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>invoke</code></td><td>允许应用能够与托管在外部的远程服务进行集成，根据配置决定是否携带 OAuth 令牌</td></tr><tr><td><code>request</code></td><td>允许应用在前端代码中直接向远程服务发送请求，不携带 OAuth 令牌</td></tr></tbody></table>

## **invoke**

允许应用能够与托管在外部的远程服务进行集成。在请求被转发到远程服务之前，会先进行验证，并添加必要的认证信息，如果配置了 OAuth 令牌，则会使用 OAuth 令牌。

### **函数签名**

```typescript
function invoke(options: RemoteInvokeOptions): Promise<Response>;

type RemoteInvokeOptions = { path: string; } & Pick<RequestInit, "headers" | "body" | "method">;
```

### **参数**

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.06%" /><col style="width: 67.94%" /></colgroup><thead><tr><th>名称</th><th>说明</th></tr></thead><tbody><tr><td><code>options</code></td><td>调用远程函数传入的选项（见下方详细说明）</td></tr></tbody></table>

`RemoteInvokeOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.34%" /><col style="width: 67.66%" /></colgroup><thead><tr><th>名称</th><th>说明</th></tr></thead><tbody><tr><td><code>path</code></td><td>远程服务的路径， 完整的调用地址为 Remote 配置的 baseUrl + path</td></tr><tr><td><code>method</code></td><td>HTTP 请求方法</td></tr><tr><td><code>headers</code></td><td>自定义请求头</td></tr><tr><td><code>body</code></td><td>请求体内容</td></tr></tbody></table>

### **返回值**

参见 WHATWG [响应对象](https://fetch.spec.whatwg.org/#response-class) ，通过  `Promise` 返回。

### **示例**

```typescript
import { remote } from '@pc-nexus/bridge';

const response = await remote.invoke({
  path: '/my-api',
  method: 'POST',
  headers: {
    'content-type': 'application/json',
  },
  body: {
    message: 'hello',
  },
});

console.log(response.status);

const data = await response.json();
console.log(data);
```

## **request**

允许应用在前端代码中直接向远程服务发送请求，与 `invoke` 方法不同，即使为远程配置了 OAuth 令牌， `request` 方法也不会包含这些令牌。

### **函数签名**

```typescript
function request(remoteKey: string, options?: RemoteRequestOptions): Promise<Response>;

type RemoteRequestOptions = { path: string; } & Omit<RequestInit, "signal">;
```

### **参数**

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 24.58%" /><col style="width: 75.42%" /></colgroup><thead><tr><th>名称</th><th>说明</th></tr></thead><tbody><tr><td><code>remoteKey</code></td><td>远程服务配置的唯一标识字符串，对应 <code>remotes[].key</code></td></tr><tr><td><code>options</code></td><td>调用远程函数传入的选项（见下方详细说明）</td></tr></tbody></table>

`RemoteRequestOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 24.29%" /><col style="width: 75.71%" /></colgroup><thead><tr><th>名称</th><th>说明</th></tr></thead><tbody><tr><td><code>path</code></td><td>远程服务的路径， 完整的调用地址为 Remote 配置的 baseUrl + path</td></tr><tr><td><code>method</code></td><td>HTTP 请求方法</td></tr><tr><td><code>headers</code></td><td>自定义请求头</td></tr><tr><td><code>body</code></td><td>请求体内容</td></tr></tbody></table>

### **返回值**

参见 WHATWG [响应对象](https://fetch.spec.whatwg.org/#response-class) ，通过  `Promise` 返回。

### **示例**

```typescript
import { remote } from '@pc-nexus/bridge';

const response = await remote.request('my-remote', {
  path: '/my-api',
  method: 'POST',
  headers: {
    'content-type': 'application/json',
  },
  body: JSON.stringify({
    message: 'hello',
  }),
});

console.log(response.status);

const data = await response.json();
console.log(data);
```
