---
title: "系统事件"
lastUpdated: 2026-07-15T10:10:12.000Z
---

# 系统事件

当用户在 PingCode 产品中执行操作时，系统会生成 PingCode 产品事件，如创建工作项，应用可以配置订阅并处理这些事件。

本文档详细定义 Nexus 平台中支持的系统事件。

## 事件定义

以下为 Nexus 平台目前支持的系统事件及其详细定义。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.2%" /><col style="width: 67.8%" /></colgroup><thead><tr><th>分类</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/resource/events/global">全局事件</a></td><td>定义 PingCode 产品中全局系统事件</td></tr><tr><td><a href="/reference/resource/events/ship">产品管理</a></td><td>定义 PingCode 产品中产品管理系统事件</td></tr><tr><td><a href="/reference/resource/events/pjm">项目管理</a></td><td>定义 PingCode 产品中项目管理系统事件</td></tr><tr><td><a href="/reference/resource/events/wiki">知识管理</a></td><td>定义 PingCode 产品中知识管理系统事件</td></tr><tr><td><a href="/reference/resource/events/testhub">测试管理</a></td><td>定义 PingCode 产品中测试管理系统事件</td></tr></tbody></table>

关于系统事件的更多信息请参考 [system](/reference/functions/events/system) 。

## 数据格式

在订阅事件时返回的实体数据格式，如工作项、评论等，与 PingCode APIs 返回的数据格式保持一致。
