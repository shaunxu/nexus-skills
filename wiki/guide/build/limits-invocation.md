---
title: "调用限制"
lastUpdated: 2026-07-03T09:01:03.000Z
---

# 调用限制

本文档定义应用中函数可被调用的次数，以及调用的最大运行时长等。

## 频率限制

用户发起的调用具有以下频率限制。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.9%" /><col style="width: 51.98%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>用户调用次数</td><td><code>1200 次/分钟</code></td><td>单个安装实例中单个用户的最大调用次数</td></tr><tr><td>安装实例调用次数</td><td><code>5000 次/分钟</code></td><td>单个安装实例中所有用户的最大调用次数</td></tr><tr><td>应用调用次数</td><td><code>30000 次/分钟</code></td><td>单个应用单个环境中所有安装实例的最大调用次数</td></tr></tbody></table>

## 超时限制

调用超时时长限制。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.68%" /><col style="width: 20.34%" /><col style="width: 51.98%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>UI Invoke 超时时长</td><td><code>5 秒</code></td><td>通过 UI Invoke 调用时超时时长</td></tr><tr><td>其他调用超时时长</td><td><code>60 秒</code></td><td>其他调用超时时长，如网络请求</td></tr></tbody></table>

## 负载限制

调用请求负载和响应负载大小限制。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 28.53%" /><col style="width: 19.49%" /><col style="width: 51.98%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>请求负载</td><td><code>512 KB</code></td><td>前端调用的最大请求负载大小</td></tr><tr><td>响应负载</td><td><code>5 MB</code></td><td>前端调用的最大响应负载大小</td></tr></tbody></table>

## 存储限制

应用可访问的存储资源限制。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 28.39%" /><col style="width: 19.63%" /><col style="width: 51.98%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>内存</td><td><code>512 MB</code></td><td>单个应用每次调用可用内存</td></tr><tr><td>磁盘</td><td><code>512 MB</code></td><td>单个应用每次调用可用的磁盘空间</td></tr><tr><td>磁盘可写目录</td><td><code>/tmp</code></td><td>仅 <code>/tmp</code> 目录可以读写，其他文件都只读。写入此目录的数据仅在单次调用期间保留，两次执行之间可能会被清空。</td></tr></tbody></table>
