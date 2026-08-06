---
title: "事件订阅"
lastUpdated: 2026-07-14T05:10:10.000Z
---

# 事件订阅

Nexus 应用可以订阅事件或设置一个 HTTP 端点，以便在没有用户交互的情况下调用应用内的某个函数，使的应用能够响应 PingCode 产品和 Nexus 平台后台发生的活动，无论这些活动是由用户主动触发的，还是由其他后台处理（例如基于 REST APIs 的脚本对你的项目进行批量更新）触发的.

应用可以监听的 PingCode 产品和平台事件示例包括：

- 新的应用被安装或者卸载
- 应用升级到了最新版本
- 任何用户更新工作项
- 任何用户创建了项目或者空间

## 配置

事件订阅的结构定义：

```yaml
event {}
├─ triggers [] [Optional]
│  ├─ key (string) [Mandatory]
│  ├─ type (string) [Mandatory]
│  ├─ events [] [Optional]
│  └─ handler {} [Mandatory]
└─ registries [] [Optional]
   ├─ key (string) [Mandatory]
   ├─ name (string) [Mandatory]
   └─ allowedRecipients [] [Optional]
```

## 示例

典型的事件订阅配置示例：

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

## 参考

关于事件订阅的详细信息请参考：

- Manifest配置： [Event](/reference/manifest/events)
- 开发指南： [事件订阅](/guide/development/events)
- 参考引用： [Event](/reference/functions/events)
