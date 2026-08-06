---
title: "queue"
lastUpdated: 2026-08-03T07:11:22.000Z
---

# queue

本文档介绍异步队列的推送 APIs。异步队列用于把耗时的工作从当前函数里剥离出去，交给消费者函数在后台异步执行。

导入：

```typescript
import { queue } from "@pc-nexus/async";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>push</code></td><td>用于把 payload 推入异步队列</td></tr></tbody></table>

## push

`push` 函数用于把一条或者多条 payload 推入异步队列，调用只保证入队，不等待消费者执行。

### **函数签名**

```typescript
function push<T = unknown>(key: string, payload: T | T[], options?: QueuePushOptions): Promise<QueuePushResult>;

interface QueuePushOptions {
    delay?: number;
}

interface QueuePushResult {
    jobId: string;
}
```

### **参数**

|名称|描述|
|---|---|
|`key`|队列名，必须与 manifest 中某个 `async.queues` 条目的 `key` 一致|
|`payload`|单条 payload，或一个 payload 数组，会原样出现在消费者收到的 `task.payload`|
|`options`|可选，异步队列推送选项设置|

`QueuePushOptions` 类型定义如下：

|名称|描述|
|---|---|
|`delay`|表示延时投递的秒数： - 入队后至少延迟该秒数才可被消费 - 不传或传 0 表示尽快投递 - 批量推送时对本次所有任务生效|

### **返回值**

 返回值类型为 `QueuePushResult` ，通过 `Promise` 返回。

|名称|描述|
|---|---|
|`jobId`|本次推送产生的任务标识，由服务端生成。批量推送时，整批载荷共享同一个 `jobId`|

### **示例**

推送单条：

```typescript
import { queue } from "@pc-nexus/async";

const { jobId } = await queue.push("image-processing", { imageId: "img-1" });
```

批量推送：

```typescript
const { jobId } = await queue.push("image-processing", [{ imageId: "img-1" }, { imageId: "img-2" }]);
```

指定 payload 类型，让入参获得类型检查：

```typescript
interface ImageJob {
    imageId: string;
    width: number;
}

const { jobId } = await queue.push<ImageJob>("image-processing", { imageId: "img-1", width: 800 });
```
