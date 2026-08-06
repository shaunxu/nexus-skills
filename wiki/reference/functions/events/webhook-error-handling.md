---
title: "错误处理"
lastUpdated: 2026-07-27T07:36:28.000Z
---

# 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.62%" /><col style="width: 66.38%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_EVENT_WEBHOOK_PATH_INVALID</code></td><td><code>Incoming Webhook</code> 请求路径格式不正确。</td></tr><tr><td><code>ERR_EVENT_WEBHOOK_METHOD_INVALID</code></td><td><code>HTTP</code> 方法不被支持（仅允许 <code>GET</code> 、 <code>PUT</code> 、 <code>POST</code> 、 <code>DELETE</code> 、 <code>PATCH</code> ）。</td></tr><tr><td><code>ERR_EVENT_WEBHOOK_CONTENT_TYPE_INVALID</code></td><td>缺少 <code>Content-Type</code> ，或不在支持的媒体类型列表中。</td></tr><tr><td><code>ERR_EVENT_WEBHOOK_NOT_FOUND</code></td><td>根据 <code>hook id</code> 找不到对应的 <code>Webhook</code> 配置。</td></tr><tr><td><code>ERR_EVENT_WEBHOOK_APP_NOT_FOUND</code></td><td>请求域名中的应用与该 <code>Webhook</code> 所属应用不匹配。</td></tr><tr><td><code>ERR_EVENT_WEBHOOK_URL_INVALID</code></td><td>提供的 <code>Webhook URL</code> 格式无效。</td></tr><tr><td><code>ERR_EVENT_WEBHOOK_URL_PATH_INVALID</code></td><td><code>Webhook URL</code> 路径不符合 <code>Incoming</code> 约定（ <code>/x1/{hookId}</code> ）</td></tr><tr><td><code>ERR_EVENT_WEBHOOK_TRIGGER_NOT_FOUND</code></td><td>当前安装的 <code>manifest</code> 中找不到与该 <code>Webhook key</code> 对应的 <code>webhook trigger</code> 。</td></tr><tr><td><code>ERR_EVENT_WEBHOOK_HANDLER_INVALID</code></td><td><code>Webhook trigger</code> 已声明，但缺少有效的  <code>handler.function</code> 。</td></tr><tr><td><code>ERR_EVENT_FUNCTION_NOT_FOUND</code></td><td><code>manifest</code> 中找不到该 <code>trigger</code> 声明的 <code>function</code> 。</td></tr></tbody></table>
