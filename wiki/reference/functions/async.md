---
title: "Async"
lastUpdated: 2026-07-16T09:57:24.000Z
---

# Async

本文档介绍如何在 Nexus 应用中实现异步消息队列。异步消息队列的一个典型场景是，某个应用包含一个运行时间超过 Nexus 函数上限的函数，如导入功能。该应用可以使用异步消息队列 APIs 将事件发送到具有更长运行时间的消费者函数，从而在后台异步执行它们。

## 安装

```powershell
npm install @pc-nexus/async
```

导入：

```javascript
import { queue } from "@pc-nexus/async";
```

## APIs

Async APIs 提供的能力如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 37.78%" /><col style="width: 62.22%" /></colgroup><thead><tr><th>APIs</th><th>说明</th></tr></thead><tbody><tr><td><a href="/reference/functions/async/queue">queue</a></td><td>提供异步消息队列的操作</td></tr><tr><td><a href="/reference/functions/async/consumer">consumer</a></td><td>提供异步消息队列消费者函数</td></tr></tbody></table>
