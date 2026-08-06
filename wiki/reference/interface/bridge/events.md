---
title: "events"
lastUpdated: 2026-07-06T03:41:24.000Z
---

# events

`events` API 允许你订阅、取消订阅和触发事件。你可以让同一应用内的不同 UI 之间互相通信。

导入：

```typescript
import { events } from "@pc-nexus/bridge";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>on</code></td><td>订阅一个自定义事件</td></tr><tr><td><code>emit</code></td><td>发送一个自定义事件</td></tr></tbody></table>

## on

订阅一个自定义事件

### 函数签名

```typescript
function on<T = any>(eventName: string, callback: (payload?: T) => any): Promise<Subscription>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 39.69%" /><col style="width: 60.31%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>eventName</code></td><td style="text-align: left">事件名称</td></tr><tr><td style="text-align: left"><code>callback</code></td><td style="text-align: left">收到事件后的回调函数，payload 为事件携带的数据</td></tr></tbody></table>

### 返回值

返回一个 `Promise<Subscription>` 订阅对象，可进行取消订阅：

```typescript
interface Subscription {
  unsubscribe: () => void;
}
```

`Subscription` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 39.69%" /><col style="width: 60.31%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>unsubscribe</code></td><td style="text-align: left">取消订阅函数</td></tr></tbody></table>

### 示例

```typescript
import { events } from "@pc-nexus/bridge";

function eventHandler(payload?: any) {
  console.log("Payload: ", payload);
}

const subscription = await events.on("EVENT_NAME", eventHandler);

// 取消订阅
subscription.unsubscribe();
```

## emit

发送一个自定义事件。

### 函数签名

```typescript
function emit<T = any>(eventName: string, payload: T): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 38.98%" /><col style="width: 61.02%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>eventName</code></td><td style="text-align: left">事件名称</td></tr><tr><td style="text-align: left"><code>payload</code></td><td style="text-align: left">事件数据，可以是对象、数组、字符串等，也支持 Blob</td></tr></tbody></table>

### 返回值

空

### 示例

**on.ts**

```typescript
import { events } from "@pc-nexus/bridge";

function eventHandler(payload?: any) {
  if (payload) {
    console.log(`Payload: ${payload}`);
  }
}

await events.on("EVENT_NAME", eventHandler);
```

**emit.ts**

```typescript
import { events } from "@pc-nexus/bridge";

const payload = "PAYLOAD";

await events.emit("EVENT_NAME", payload);
```

## 发送 Blob 数据

`events` 支持在事件数据中传递 `Blob` 。bridge 会自动将 `Blob` 转换为可传输的数据结构，并在接收端还原为 `Blob` 对象，因此你可以像传递普通数据一样传递文件内容。

**on.ts**

```typescript
import { events } from "@pc-nexus/bridge";

async function eventHandler(payload?: any) {
  if (payload) {
    const text = await payload.file?.text();
    console.log(text);
  }
}

await events.on<{ file: Blob }>("FILE_CHANGE", eventHandler);
```

**emit.ts**

```typescript
import { events } from "@pc-nexus/bridge";

const file = new Blob(["hello world"], { type: "text/plain" });

await events.emit("FILE_CHANGE", { file });
```
