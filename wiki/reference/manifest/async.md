---
title: "Async"
lastUpdated: 2026-07-29T02:09:22.000Z
---

# Async

`async` 定义异步消息队列和消费者处理函数。

## 结构

结构定义如下：

```javascript
async {}
├─ queues [] [Mandatory]
│  └─ key (string) [Mandatory]
└─ consumers [] [Mandatory]
   ├─ key (string) [Mandatory]
   ├─ queue (string) [Mandatory]
   ├─ handler {} [Mandatory]
   └─ concurrency (number) [Optional]
```

## 示例

简单配置示例：

```yaml
async:
  queues:
    - key: my-queue
  consumers:
    - key: my-consumer
      queue: my-queue
      handler:
        function: my-consumer-handler
      concurrency: 2
```

## 属性

`async` 属性定义异步队列和消费者，包含两个数组：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>queues</code></td><td>Y</td><td>队列声明列表</td></tr><tr><td><code>consumers</code></td><td>Y</td><td>消费者声明列表</td></tr></tbody></table>

`queues` 属性声明应用拥有的异步队列，属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>队列的唯一标识，在同一个 <code>manifest</code> 文件中必须唯一</td></tr></tbody></table>

`consumers` 属性下定义每个异步队列的消费者，属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>消费者唯一标识，在同一个 <code>manifest</code> 文件中必须唯一</td></tr><tr><td><code>queue</code></td><td>Y</td><td>异步队列名称</td></tr><tr><td><code>handler</code></td><td>Y</td><td>接收到队列的消息时的后端处理函数： - 指定后端处理函数时使用 <code>function</code> 属性</td></tr><tr><td><code>concurrency</code></td><td></td><td>允许最大并行执行的消费者函数，默认值为 <code>8</code></td></tr></tbody></table>
