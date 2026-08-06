---
title: "事件处理函数"
lastUpdated: 2026-07-14T10:11:16.000Z
---

# 事件处理函数

本文档详细阐述如何使用事件处理函数，事件处理函数用于监听的事件触发时，进行业务逻辑的处理。

## 安装依赖

在应用的根目录中安装以下依赖项：

```shell
npm install @pc-nexus/event
```

## 文件结构

在应用的 `/src` 目录中，添加以下目录和函数入口文件：

```shell
/src
  /handlers
    /index.ts
```

## 定义函数

在 `/src/handlers/index.ts` 文件中定义事件处理函数：

```typescript
import type { SystemEventHandler } from "@pc-nexus/event";

const handler: SystemEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event.payload));
};

export { handler }
```

## 配置函数

在应用 `manifest.yaml` 文件中声明函数：

```yaml
functions:
  - key: event-handler
    handler: index.handler
```

## 附加到事件

要使定义的函数能够运行，需要通过 `manifest.yaml` 文件将其附加到具体的事件触发器上：

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
