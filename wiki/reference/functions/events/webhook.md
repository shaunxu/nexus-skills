---
title: "webhook"
lastUpdated: 2026-07-14T09:51:47.000Z
---

# webhook

本文档介绍如何在应用中配置 Webhook 触发器。Web trigger 事件是通过 HTTPS 传入的调用请求来触发后端处理函数执行，如来自于第三方的 Webhook 服务。

## 配置

`manifest.yml` 文件配置示例：

```yaml
event:
  triggers:   
    - key: web_trigger
      type: webhook
      handler:
        function: egress-function
functions:
    - key: egress-function
      handler: index.egressFunction
```

`config` 包含的属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 15.69%" /><col style="width: 26.96%" /><col style="width: 57.35%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>handler</code></td><td>Y</td><td>事件被触发时的后端处理函数： - 指定后端处理函数时使用 <code>function</code> 属性</td></tr></tbody></table>

## 管理 URL

提供给外部调用的 Webhook URL 地址需要开发者自行通过 SDK 生成，并提供给用户，参考 [管理 URLs](/reference/functions/events/webhook-url) ，生成的 URL 格式如下：

`https://{appid}.webhook.pingcodex.com/x1/{webhook_id}`

- `https://` ：协议
- `4f94fb6cc-e162-44f4-a936-996a9ce032e0` 子域名应用 ID
-  `webhook.pingcodex.com` 域名
- `/x1/` ：固定路径前缀
- `uuid` ：Web trigger UUID

示例：

```javascript
https://4abd2038-a42c-49a1-b98c-ae04e29bf57a.webhook.pingcodex.com/x1/9f70b33d-04ad-4e28-a189-07f54b974176
```

## 处理函数

当外部服务通过 Webhook URL 发起请求时会被处理函数接收到，并进行处理：

### 示例

```typescript
import { WebhookEventHandler } from "@pc-nexus/event";

export const handler: WebhookEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event));
    return {
        statusCode: 200,
        headers: {
            "Content-Type": "application/json",
        },
        body: { payload: event.payload },
    }
};
```

注意： Nexus 平台不会对请求的 URL 做任何认证处理，开发者如有需要可以自行在处理函数进行认证。

### 参数

处理函数接收 `context` 和 `event` 两个参数。

#### **context**

`context` 为 `NexusAppContext` 类型，包含应用运行时的上下文信息，详情请参考 [app](/reference/functions/core/app) ，获取触发的事件信息可以从 `context` 中获取 如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.24%" /><col style="width: 70.76%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>event.trigger.key</code></td><td>触发器在 <code>manifest</code> 中定义的 <code>key</code></td></tr><tr><td><code>event.trigger.type</code></td><td>触发器类型，值为 <code>webhook</code></td></tr></tbody></table>

#### **event**

`event` 是订阅事件所传递的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.24%" /><col style="width: 70.76%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>payload</code></td><td>定义 Webhook 请求的原始数据，包括： <code>method</code> , <code>path</code> , <code>headers</code> , <code>body</code> , <code>queryParameters</code></td></tr><tr><td><code>event_type</code></td><td>定义事件类型，在Web trigger 事件类型中该属性值为 <code>undefined</code></td></tr></tbody></table>

`payload` 中包含Webhook 请求的原始数据：

```javascript
{
            "method": "GET",
            "path": "/4abd2038-a42c-49a1-b98c-ae04e29bf57a.webhook.pingcodex.com/x1/d8da6df4-9a98-4387-845f-85556c11880d/hello/world",
            "headers": {
                "content-type": "application/json",
                "accept": "*/*",
                "cache-control": "no-cache",
                "host": "localhost:30003",
                "accept-encoding": "gzip, deflate, br",
                "connection": "keep-alive"
            },
            "body": "",
            "queryParameters": {}
}
```

### 返回结果

```javascript
export interface WebhookEventResult {
    statusCode: number;
    headers?: OutgoingHttpHeaders;
    body?: unknown;
}
```

如上示例代码， `WebhookEventHandler` 必须返回指定 `WebhookEventResult` 类型的结果。

`WebhookEventResult` 类型说明：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.17%" /><col style="width: 70.83%" /></colgroup><thead><tr><th>属性</th><th>说明</th></tr></thead><tbody><tr><td><code>statusCode</code></td><td><code>http</code> 响应的状态码，如：200，400 等</td></tr><tr><td><code>headers</code></td><td><code>http</code> 响应的 <code>headers</code> 信息，如： ``<code>javascript { "content-length": 128, "content-type": "application/json" } </code>``</td></tr><tr><td><code>body</code></td><td><code>http</code> 响应体，可以是纯文本， <code>json</code> 对象等</td></tr></tbody></table>

## 请求

当外部服务调用 Webhook URL 时，你定义的处理函数将收到一个结构化的 `event` 对象，其中 `event.payload` 包含原始的 HTTP 请求信息。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25%" /><col style="width: 41.81%" /><col style="width: 8.19%" /><col style="width: 25%" /></colgroup><thead><tr><th style="text-align: left">属性</th><th style="text-align: left">类型</th><th style="text-align: left">必填</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>body</code></td><td style="text-align: left"><code>string</code> <code>Json</code> <code>Xml</code> <code>x-www-form-urlencoded</code></td><td style="text-align: left"></td><td style="text-align: left">HTTP 请求体，内容格式遵循请求头的内容类型，支持 JSON、XML、表单编码格式</td></tr><tr><td style="text-align: left"><code>headers</code></td><td style="text-align: left"><code>object</code></td><td style="text-align: left">是</td><td style="text-align: left">调用方发送的 HTTP 请求头，格式为请求头名称对应字符串数组 <strong>例子</strong> <code>"Content-Type”: ["application/json”]</code></td></tr><tr><td style="text-align: left"><code>method</code></td><td style="text-align: left"><code>string</code></td><td style="text-align: left">是</td><td style="text-align: left">客户端使用的 HTTP 请求方式，如 GET、POST、PUT、DELETE、PATCH</td></tr><tr><td style="text-align: left"><code>path</code></td><td style="text-align: left"><code>string</code></td><td style="text-align: left">是</td><td style="text-align: left">调用方发起请求的访问路径</td></tr><tr><td style="text-align: left"><code>queryParameters</code></td><td style="text-align: left"><code>{ [key: string]:string\|string[]}</code></td><td style="text-align: left"></td><td style="text-align: left">从请求链接中解析出的查询参数</td></tr></tbody></table>

### 带路径参数的请求

以下示例展示对 `/x1/XUBR5WnG2Hk2V52APDdGaRSDm/hello/world?apples=green,red&grapes=green` 的请求，其中 `/hello/world` 是调用方提供的路径参数

```javascript
{
  "method": "POST",
  "headers": {
    "Accept": ["*/*"],
    "accept-encoding": ["gzip, deflate"],
    "content-length": ["71"],
    "Connection": ["keep-alive"],
    "Host": ["localhost:8080"],
    "Cache-Control": ["no-cache"],
    "Content-Type": ["text/plain"]
  },
  "body": "{\n\t\"hello\": 1,\n\t\"test\": [\"foo\", \"bar\"],\n\t\"foo\": {\n\t\t\"bar\": \"hello\"\n\t}\n}",
  "path": "/x1/XUBR5WnG2Hk2V52APDdGaRSDm/hello/world",
  "queryParameters": {
    "apples": ["red", "green"],
    "grapes": ["green"]
  }
}
```

在本示例中：

- 完整 URL 路径： `/x1/XUBR5WnG2Hk2V52APDdGaRSDm/hello/world`
- `path` 字段内容： `/x1/XUBR5WnG2Hk2V52APDdGaRSDm/hello/world` （调用方发送的请求）

### 无路径参数的请求

以下示例展示对 `/x1/XUBR5WnG2Hk2V52APDdGaRSDm?apples=green,red&grapes=green` 的请求，无额外路径片段

```javascript
{
  "method": "POST",
  "headers": {
    "Accept": ["*/*"],
    "accept-encoding": ["gzip, deflate"],
    "content-length": ["71"],
    "Connection": ["keep-alive"],
    "Host": ["localhost:8080"],
    "Cache-Control": ["no-cache"],
    "Content-Type": ["text/plain"]
  },
  "body": "{\n\t\"hello\": 1,\n\t\"test\": [\"foo\", \"bar\"],\n\t\"foo\": {\n\t\t\"bar\": \"hello\"\n\t}\n}",
  "path": "/x1/XUBR5WnG2Hk2V52APDdGaRSDm",
  "queryParameters": {
    "apples": ["red", "green"],
    "grapes": ["green"]
  }
}
```

## 响应

处理函数需要返回一个对象，用于构建发送给调用方的 HTTP 响应。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25%" /><col style="width: 36.3%" /><col style="width: 13.7%" /><col style="width: 25%" /></colgroup><thead><tr><th style="text-align: -webkit-left">属性</th><th style="text-align: -webkit-left">类型</th><th style="text-align: -webkit-left">必填</th><th style="text-align: -webkit-left">说明</th></tr></thead><tbody><tr><td style="text-align: -webkit-left"><code>body</code></td><td style="text-align: -webkit-left"><code>string</code> <code>Json</code> <code>Xml</code></td><td style="text-align: -webkit-left">否</td><td style="text-align: -webkit-left">返回给调用方的 HTTP 响应体</td></tr><tr><td style="text-align: -webkit-left"><code>headers</code></td><td style="text-align: -webkit-left"><code>object</code></td><td style="text-align: -webkit-left">否</td><td style="text-align: -webkit-left">返回给调用方的 HTTP 响应头 格式： <code>响应头名称: 字符串数组</code> 示例： <code>"Content-Type": ["application/json"]</code></td></tr><tr><td style="text-align: -webkit-left"><code>statusCode</code></td><td style="text-align: -webkit-left"><code>integer</code></td><td style="text-align: -webkit-left">是</td><td style="text-align: -webkit-left">返回给调用方的 HTTP 状态码</td></tr></tbody></table>

## 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.62%" /><col style="width: 66.38%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_</code></td><td></td></tr></tbody></table>
