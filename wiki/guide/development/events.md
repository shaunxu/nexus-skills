---
title: "事件订阅"
lastUpdated: 2026-07-14T09:53:54.000Z
---

# 事件订阅

你的应用可以订阅事件或设置一个 HTTP 端点，以便在没有用户交互的情况下调用应用内的某个函数。这使得你的应用能够响应 PingCode 产品和 Nexus 平台后台发生的活动，无论这些活动是由用户主动触发的，还是由其他后台处理（例如基于 REST APIs 的脚本对你的项目进行批量更新）触发的。

应用可以监听的 PingCode 产品和平台事件示例包括：

- 新的应用被安装或者卸载
- 应用升级到了最新版本
- 任何用户更新工作项
- 任何用户创建了项目或者空间

## 开发事件订阅

事件订阅应用时：

- 配置 Manifest
- 定义处理函数
- 配置权限

### 配置 Manifest

在 `manifest.yaml` 文件中添加 `events` 属性，指定你的应用将要响应的事件，以及在收到这些事件时要执行的操作：

```yaml
event:
  triggers:
    - key: system-trigger
      type: system
      events:
        - pce:pjm:workitem:created
        - pce:pjm:workitem:viewed
      handler:
        function: event-handler
             
functions:
  - key: event-handler
    handler: index.handler
```

### 处理函数

根据具体事件的参考引用内容，为你的应用添加处理事件的功能：

```typescript
import type { SystemEventHandler } from "@pc-nexus/event";

const handler: SystemEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event.payload));
};

export { handler }
```

### 配置权限

订阅系统事件时，需要在 `manifest.yaml` 中声明对应的权限：

```yaml
permissions:
  scopes:
    - pcp:read:pjm:workitem
```

### 注意事项

开发订阅事件的应用时，有一些特殊的注意事项：

- 订阅事件的 Nexus 应用代码无法访问 PingCode 产品的用户界面，并且不与任何用户的会话关联
- 订阅事件的应用代码是以系统用户的身份运行的，而不是 PingCode 产品交互式用户帐户，如果你为某个资源设定了特定用户帐户访问权限，那么你的应用在处理接收到的事件时可能无法访问该资源，因为系统用户可能没有相应的权限。

## 开发指南

关于事件订阅应用开发，更多详情请参考：

- [订阅系统事件](/guide/development/events-system-trigger)
- [订阅生命周期事件](/guide/development/events-lifecycle-trigger)
- [使用定时触发器](/guide/development/events-scheduled-trigger)
- [使用 Webhook 触发器](/guide/development/events-webhook-trigger)

## 参考引用

Nexus 平台支持的事件类型及其参考引用：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 43.83%" /><col style="width: 56.17%" /></colgroup><thead><tr><th>参考</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/functions/events/system">system</a></td><td>PingCode 产品内的事件，如创建工作项</td></tr><tr><td><a href="/reference/functions/events/lifecycle">lifecycle</a></td><td>应用生命周期事件，如安装、卸载</td></tr><tr><td><a href="/reference/functions/events/webhook">webhook</a></td><td>通过注册的一个 HTTP 请求端点，触发调用</td></tr><tr><td><a href="/reference/functions/events/scheduled">scheduled</a></td><td>定时触发调用应用，如每天一次</td></tr><tr><td><a href="/reference/functions/events/app">app</a></td><td>应用自定义事件，其他应用发布的事件</td></tr></tbody></table>
