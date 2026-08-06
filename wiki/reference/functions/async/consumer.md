---
title: "consumer"
lastUpdated: 2026-07-28T09:21:40.000Z
---

# consumer

本文档介绍如何定义异步队列消费者处理函数。当异步队列中有任务推送时，定义的消费者处理函数会被调用。

导入：

```typescript
import type { ConsumerHandler } from "@pc-nexus/async";
```

## ConsumerHandler

### 示例

定义消费者处理函数：

```typescript
import type { ConsumerHandler } from "@pc-nexus/async";

export const handler: ConsumerHandler = async (context, task) => {
    const { payload, task_id, job_id, consumer } = task;

    console.log(`消费者 ${consumer.key} 处理任务 ${task_id}（job ${job_id}）`);
    console.log(JSON.stringify(payload));
};
```

指定 `payload` 类型：

```typescript
interface ImageJob {
    imageId: string;
    width: number;
}

export const handler: ConsumerHandler<ImageJob> = async (context, task) => {
    const { imageId, width } = task.payload;
};
```

### 参数

处理函数接收 `context` 和 `task` 两个参数：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 36.02%" /><col style="width: 63.98%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>context</code></td><td><code>NexusAppContext</code> 类型，包含应用运行时的上下文信息，详情请参考 <a href="/reference/functions/core/app">app</a> 。</td></tr><tr><td><code>task</code></td><td>任务对象</td></tr></tbody></table>

 `task` 类型为 `QueueTask` ：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 37.15%" /><col style="width: 62.85%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>payload</code></td><td>推送时传入的 <code>payload</code> ，原样带回</td></tr><tr><td><code>task_id</code></td><td>单条任务的标识，幂等去重应当以它为准</td></tr><tr><td><code>job_id</code></td><td>任务所属的 job 标识，一次 <code>push</code> 调用产生一个，批量推送时整批共享</td></tr></tbody></table>
