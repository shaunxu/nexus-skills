---
title: "订阅生命周期事件"
lastUpdated: 2026-07-14T09:54:40.000Z
---

# 订阅生命周期事件

本文档详细阐述如何在 Nexus 应用中订阅应用生命周期事件。应用生命周期事件是在应用进行安装、卸载、升级等事件发生时，由系统自动进行触发，开发者可以订阅这些事件并提供自定义的事件处理函数，以实现自己的业务逻辑。典型的示例场景：

- 当应用被安装时，进行一些初始化的操作
- 当应用版本升级时，进行数据一致性的处理

## 配置说明

在 `manifest.yaml` 文件中配置想要订阅的生命周期事件：

- 触发器类型指定为： `lifecycle`
- 以应用升级事件 `pce:nexus:app:upgrade` 为例

```yaml
event:
  triggers:   
    - key: lifecycle_trigger
      type: lifecycle
      events:
        - pce:nexus:app:upgrade
      handler: 
        function: lifecycle-handler
        
functions:
  - key: lifecycle-handler
    handler: index.handler
```

其中 Key 名为 `lifecycle-handler` 的函数指向处理函数，稍后详细定义。

## 处理函数

当订阅的事件被触发时，会被定义的处理函数接收到，以便进行详细的逻辑处理：

```typescript
import type { LifecycleEventHandler } from "@pc-nexus/event";

const handler: LifecycleEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event));
};

export { handler }
```

关于订阅生命周期事件详情请参考 [lifecycle](/reference/functions/events/lifecycle) 。

## 注意事项

注意不要在生命周期事件中执行长时间的任务。
