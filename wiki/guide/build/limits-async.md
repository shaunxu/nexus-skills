---
title: "异步队列限制"
lastUpdated: 2026-07-29T05:53:37.000Z
---

# 异步队列限制

本文档定义应用在使用异步队列时的限制。

## 队列限制

以下限制适用于单个应用

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>队列数量</td><td></td><td>最大可以声明的队列数量</td></tr></tbody></table>

## 推送限制

以下限制适用于单个应用

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>单次推送条数</td><td><code>50</code> 条</td><td>调用 <code>push</code> 方法时单次可以推送的最大条数</td></tr><tr><td>单次推送大小</td><td><code>256 KB</code></td><td>调用 <code>push</code> 方法时单次可以推送的最大数据量</td></tr></tbody></table>

## 消费者限制

以下限制适用于单个应用

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>消费者数量</td><td></td><td>单个队列可以订阅的消费者函数最大数量</td></tr><tr><td>任务并发数</td><td><code>8</code></td><td>消费者处理函数最多同时并发处理的任务数</td></tr></tbody></table>
