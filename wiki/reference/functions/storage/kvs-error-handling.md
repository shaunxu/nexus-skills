---
title: "错误处理"
lastUpdated: 2026-07-28T07:15:30.000Z
---

# 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.62%" /><col style="width: 66.38%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_KVS_VALUE_INVALID</code></td><td><code>set</code> 时 <code>value</code> 参数输入不符合规范。</td></tr><tr><td><code>ERR_KVS_KEY_CONFLICT</code></td><td><code>key</code> 已经存在。</td></tr><tr><td><code>ERR_KVS_GET_OPTIONS_INVALID</code></td><td>获取加密数据时 <code>options.secret</code> 的值必须为 <code>True</code> 。</td></tr><tr><td><code>ERR_KVS_VALUE_LIMIT</code></td><td><code>set</code> 的 <code>value</code> 值超出限制。</td></tr><tr><td><code>ERR_KVS_KEY_LIMIT</code></td><td><code>key</code> 长度超出限制。</td></tr></tbody></table>
