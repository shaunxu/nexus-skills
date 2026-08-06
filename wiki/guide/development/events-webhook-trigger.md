---
title: "使用 Webhook 触发器"
lastUpdated: 2026-07-14T09:55:05.000Z
---

# 使用 Webhook 触发器

本文档详细阐述如何在 Nexus 应用中处理 Webhook 触发器。Webhook 触发器是在应用中生成对外的 Webhook URL，当外部服务请求这些 URL 时可以被定义的处理函数接收到，并进行业务逻辑处理。

## 配置说明

在 `manifest.yaml` 文件中配置 Webhook 触发器，类型指定为 `webhook` ：

```yaml
event:
  triggers:
    - key: webhook_trigger
      type: webhook
      handler: 
        function: webhook-handler
        
functions:
  - key: webhook-handler
    handler: index.handler
```

其中 Key 名为 `webhook-handler` 的函数指向处理函数，稍后详细定义。

## 生成 URL

在使用 Webhook 触发器时，需要通过 SDK 提供的方法生成 Webhook URL 提供给外部服务调用，其中 `webhook_trigger` 是在上一步配置中指定的 Web trigger key：

```javascript
import { webhook } from "@pc-nexus/event"

const url = await webhook.getUrl("webhook_trigger");

return url;
```

每个 Web trigger key 可以生成多条不同的 Webhook URL，为不同的外部服务使用，所有的 URL 指向同一个处理函数。

## 处理函数

当外部服务请求生成的 Webhook URL 时，会被处理函数接收到，以便进行详细的逻辑处理：

```typescript
import type { WebhookEventHandler } from "@pc-nexus/event";

const handler: WebhookEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event));
    return {
        statusCode: 200,
        headers: {
            "Content-Type": "application/json",
        },
        body: { payload: {
            name: "Davis",
            age: 25
        } },
    }
};

export { handler };
```

关于使用 Webhook 触发器进行事件订阅详情请参考 [webhook](/reference/functions/events/webhook) 。
