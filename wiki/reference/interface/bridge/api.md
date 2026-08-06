---
title: "api"
lastUpdated: 2026-07-06T03:35:44.000Z
---

# api

`api`  提供的桥接方法使 Nexus 应用能够以当前用户的身份调用  [PingCode REST API](https://open.pingcode.com/)  。

导入：

```typescript
import { api } from '@pc-nexus/bridge';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>invoke</code></td><td>调用 PingCode REST API</td></tr></tbody></table>

## **invoke**

### **函数签名**

```typescript
function invoke(path: string, options?: ApiInvokeOptions): Promise<Response>;
```

### **参数**

|名称|描述|
|---|---|
|`path`|PingCode REST API 操作路径 path|
|`options`|调用 PingCode REST API 需要的参数，类型为ApiInvokeOptions（见下方详细说明）|

`ApiInvokeOptions` 定义如下：

```typescript
type ApiInvokeOptions = Omit<RequestInit, "signal">;
```

`RequestInit` 定义参见 WHATWG fetch  [RequestInit 文档](https://fetch.spec.whatwg.org/#requestinit)   


### **返回值**

参见 WHATWG [响应对象](https://fetch.spec.whatwg.org/#response-class) ，通过  `Promise` 返回。

### **示例**

```typescript
import { api } from '@pc-nexus/bridge';

const response = await api.invoke('/v1/myself');
console.log(await response.json());
```
