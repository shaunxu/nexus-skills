---
title: "Event"
lastUpdated: 2026-07-15T03:09:03.000Z
---

# Event

`events` 属性用于定义应用的事件订阅列表。

## 结构

结构定义如下：

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

简单配置示例：

```yaml
event:
  triggers:
    - key: ship-trigger
      events:
        - pce:ship:idea:created
        - pce:ship:idea:updated
      handler: 
        function: ship-idea-handler
functions:
  - key: ship-idea-handler
    handler: shipIdea.handler
```

## 属性

支持两个次级属性，分别用于定义事件订阅和发布：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.91%" /><col style="width: 22.03%" /><col style="width: 55.06%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>triggers</code></td><td></td><td>当订阅的指定事件触发时，通知应用程序</td></tr><tr><td><code>registries</code></td><td></td><td>应用声明的事件列表，在此处声明的事件可以被其他应用订阅处理</td></tr></tbody></table>
