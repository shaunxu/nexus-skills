---
title: "网络请求限制"
lastUpdated: 2026-07-01T09:20:01.000Z
---

# 网络请求限制

本文档定义应用在网络请求时的限制。

## 网络请求限制

以下限制适用于单个应用。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>单个环境请求频率</td><td><code>300000 次/分钟</code></td><td>单个应用在单个环境下的每分钟出站网络请求频率</td></tr><tr><td>单个安装实例请求频率</td><td><code>10000 次/分钟</code></td><td>单个应用在单个安装实例下的每分钟出站网络请求频率</td></tr><tr><td>请求超时时长</td><td><code>60 秒</code></td><td>应用出站网络请求超时时长</td></tr><tr><td>请求负载大小</td><td><code>512 KB</code></td><td>应用前端调用请求负载大小</td></tr><tr><td>响应负载大小</td><td><code>5 MB</code></td><td>应用前端调用响应负载大小</td></tr></tbody></table>
