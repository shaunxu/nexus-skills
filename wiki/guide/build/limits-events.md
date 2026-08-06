---
title: "事件限制"
lastUpdated: 2026-07-01T08:47:24.000Z
---

# 事件限制

本文档定义应用中事件订阅的限制。

## 事件通用限制

以下限制适用于单个应用：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.21%" /><col style="width: 16.81%" /><col style="width: 51.98%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>事件触发器数量</td><td><code>128</code></td><td>单个应用中可以声明的事件触发器总数，即 <code>events</code> 下的节点数量</td></tr></tbody></table>

## 定时触发器

以下限制适用于单个应用：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.21%" /><col style="width: 16.81%" /><col style="width: 51.98%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>定时触发器数量</td><td><code>8</code></td><td>单个应用中可以声明的定时触发器数量</td></tr><tr><td>频率 <code>tenMinute</code> 数量</td><td><code>1</code></td><td>单个应用中可以声明执行频率为 <code>tenMinute</code> 的触发器数量</td></tr></tbody></table>

## Webhook 触发器

以下限制适用于单个应用：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.21%" /><col style="width: 16.81%" /><col style="width: 51.98%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>Web Trigger 数量</td><td><code>8</code></td><td>单个应用中可以声明的 Webhook 触发器数量</td></tr><tr><td>Webhook URL 数量</td><td><code>32</code></td><td>单个应用中同一个 Web trigger key 所能创建的 Webhook URL 数量</td></tr><tr><td>超时限制</td><td><code>60 秒</code></td><td>Web trigger 处理函数响应最长时间</td></tr></tbody></table>
