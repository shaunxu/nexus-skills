---
title: "Event"
lastUpdated: 2026-07-18T05:46:40.000Z
---

# Event

应用通过订阅事件或设置 HTTP 端点，无需任何用户交互即可调用应用内的函数，无论这些事件是由用户通过界面操作引起，还是通过其他方式（如 REST APIs调用）引用。

典型的事件如：

- 应用被某个企业安装
- 任意用户更新了工作项状态
- 任意用户创建了新的文档页面

## 安装

```powershell
npm install @pc-nexus/event
```

导入：

```typescript
import { webhook } from "@pc-nexus/event";
```

## APIs

目前 Nexus 平台支持以下五种类型的事件：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.65%" /><col style="width: 69.35%" /></colgroup><thead><tr><th>事件</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/functions/events/system">system</a></td><td>系统事件，PingCode 产品内的事件，如创建工作项</td></tr><tr><td><a href="/reference/functions/events/lifecycle">lifecycle</a></td><td>应用生命周期事件，如安装、卸载</td></tr><tr><td><a href="/reference/functions/events/webhook">webhook</a></td><td>Webhook 触发器，通过注册的一个 HTTP 请求端点，触发调用</td></tr><tr><td><a href="/reference/functions/events/scheduled">scheduled</a></td><td>定时触发器，根据配置定时调用，如每天一次</td></tr><tr><td><a href="/reference/functions/events/app">app</a></td><td>应用自定义事件，其他应用发布的事件</td></tr></tbody></table>
