---
title: "使用定时触发器"
lastUpdated: 2026-07-14T09:55:21.000Z
---

# 使用定时触发器

本文档详细阐述如何在 Nexus 应用中使用定时触发器。定时触发器会按照指定的时间间隔周期性地调用处理器函数或远程服务端点，触发器首次执行时间基于应用安装时刻计算，后续按配置的间隔持续执行。

## 配置说明

在 `manifest.yaml` 文件中配置定时触发器，类型指定为 `scheduled` ：

```yaml
event:
  triggers:
    - key: scheduled-trigger
      type: scheduled
      handler:
        function: scheduled-handler
      interval: hour
        
functions:
  - key: scheduled-handler
    handler: index.handler
```

其中 `interval` 定义定时触发器的间隔， Key 名为 `scheduled-handler` 的函数指向处理函数，稍后详细定义。

## 处理函数

当到达配置的间隔周期时，处理函数会被执行：

```typescript
import type { ScheduledEventHandler } from "@pc-nexus/event";

const handler: ScheduledEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event));
};

export { handler };
```

在编写处理函数时请保证逻辑幂等，有可能应用重新部署后会重复触发，关于定时触发器的使用详情请参考 [scheduled](/reference/functions/events/scheduled) 。
