---
title: "管理 URLs"
lastUpdated: 2026-07-14T10:01:18.000Z
---

# 管理 URLs

Web trigger 运行时 API 可以编程方式管理 Webhook URL。

导入：

```typescript
import { webhook } from "@pc-nexus/event";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>getUrl</code></td><td>根据指定的 Web trigger key，获取对应 Webhook URL</td></tr><tr><td><code>queryUrls</code></td><td>获取指定键的所有 Webhook URL</td></tr><tr><td><code>deleteUrl</code></td><td>删除传入的 Webhook URL</td></tr></tbody></table>

## getUrl

根据指定的 Web trigger key，获取对应 Webhook URL。

### 函数签名

```typescript
function getUrl(webTriggerKey: string, options?: WebhookGetUrlOptions): Promise<string>

export interface WebhookGetUrlOptions {
    forceCreate?: boolean;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.94%" /><col style="width: 57.06%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>webTriggerKey</code></td><td><code>manifest.yaml</code> 文件中配置的 Web trigger key</td></tr><tr><td><code>options</code></td><td>创建 Webhook URL 可配置的参数</td></tr></tbody></table>

`WebhookGetUrlOptions` 类型定义：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.94%" /><col style="width: 57.06%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>options.forceCreate</code></td><td>- <code>true</code> ：始终创建新的 Webhook URL - <code>false</code> ：返回已经存在的 Webhook URL 或者创建新的 Webhook URL</td></tr></tbody></table>

### 返回值

返回 Webhook URL，通过 `Promise<string>` 返回

```javascript
// 返回值示例
"http://4abd2038-a42c-49a1-b98c-ae04e29bf57a.webhook.pingcodex.com/x1/webhookId1"
```

### 示例

```typescript
await webhook.getUrl("example-web-trigger-key");
```

## queryUrls

获取指定 Web trigger key 下的所有 Webhook URL，若未指定则返回当前应用的所有有效 Webhook URL。

### 函数签名

```typescript
function queryUrls(webTriggerKey?: string): Promise<WebhookQueryUrlResult[]> 

export interface WebhookQueryUrlResult {
    webTriggerKey: string;
    url: string;
}

```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 38.21%" /><col style="width: 61.79%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>webTriggerKey</code></td><td>要查询 URL 的 Web trigger key，如果不指定，则返回应用在当前环境下所有的 Webhook URL。</td></tr></tbody></table>

### 返回值

返回值为查询到的 Webhook URL ，以数组的形式返回，返回值类型为 ` Promise<WebhookQueryUrlResult[]> `

`WebhookQueryUrlResult ` 类型说明

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 37.57%" /><col style="width: 62.43%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>webTriggerKey</code></td><td>Manifest 中声明的 Web trigger key</td></tr><tr><td><code>url</code></td><td>可供第三方调用的完整的 Webhook URL</td></tr></tbody></table>

```javascript
// 返回值示例
[
  {
    "webTriggerKey": "example-web-trigger-key",
    "url": "http://4abd2038-a42c-49a1-b98c-ae04e29bf57a.webhook.pingcodex.com/x1/webhookId1"
  },
  {
    "webTriggerKey": "example-web-trigger-key",
    "url": "http://4abd2038-a42c-49a1-b98c-ae04e29bf57a.webhook.pingcodex.com/x1/webhookId2"
  }
]
```

### 示例

```typescript
await webhook.queryUrls("example-web-trigger-key"); // 返回指定 Webhook URL

await webhook.queryUrls(); // 返回应用所有的有效 Webhook URL
```

## deleteUrl

删除指定的 Webhook URL

### 函数签名

```typescript
function deleteUrl(webhookUrl: string): Promise<void>
```

### 参数

|名称|描述|
|---|---|
|`webhookUrl`|要删除的 Webhook URL|

### 返回值

空

### 示例

```typescript
await webhook.deleteUrl("http://4abd2038-a42c-49a1-b98c-ae04e29bf57a.webhook.pingcodex.com/x1/xxxx");
```
