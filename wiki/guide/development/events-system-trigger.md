---
title: "订阅系统事件"
lastUpdated: 2026-07-15T13:47:15.000Z
---

# 订阅系统事件

本文档详细阐述如何在 Nexus 应用中订阅系统事件。当用户在 PingCode 产品中执行操作时，系统会生成 PingCode 产品事件，应用可以配置订阅并处理这些事件。典型的示例场景：

- 一个维护并向 Wiki 发布关于工作项活动的最新自定义统计数据的应用，它可能会订阅与工作项相关的事件，并汇总这些信息，并生成内容发布到Wiki 中的页面。
- 将来自 PingCode 产品的新数据和更新数据推送到另一个外部平台，这种方案比在外部平台使用 REST APIs 定期轮询并拉取最新数据的方案更加高效。

## 配置说明

在 `manifest.yaml` 文件中配置想要订阅的系统事件：

- 触发器类型指定为： `system`
- 以创建工作项事件 `pce:pjm:workitem:created` 为例

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

其中 Key名为 `event-handler` 的函数指向处理函数，稍后详细定义。

## 作用域配置

订阅系统事件需要在应用中配置作用域范围，不同的事件对应不同的作用域，详细请参考 [system](/reference/functions/events/system) 。

```yaml
permissions:
  scopes:
    - pcp:read:pjm:workitem
```

上面的示例中配置订阅了事件 `pce:pjm:workitem:created` ，该事件对应的作用域是 `pcp:read:pjm:workitem` 。

## 处理函数

当订阅的事件被触发时，会被定义的处理函数接收到，以便进行详细的逻辑处理：

```typescript
import type { SystemEventHandler } from "@pc-nexus/core";

const handler: SystemEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event.payload));
};

export { handler }
```

如果想要配置事件触发时，被远程服务端点接收并处理，请参考 [远程服务作为事件处理函数](/guide/development/remotes-used-events-handler) 。
