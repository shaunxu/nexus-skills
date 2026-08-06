---
title: "存储限制"
lastUpdated: 2026-07-01T08:15:01.000Z
---

# 存储限制

本文档定义应用中使用存储的限制。

## 键-值对存储

以下限制适用于单个应用。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>Key 长度</td><td><code>512</code></td><td>使用的 Key 最大长度限制</td></tr><tr><td>Value 深度</td><td><code>32</code></td><td>Value 值类型为对象或数组时，最大深度限制</td></tr><tr><td>Value 大小</td><td><code>256 KB</code></td><td>单条 Value 值的大小限制，RAW 原始字节数</td></tr></tbody></table>

## 自定义实体存储

以下限制适用于单个应用。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>实体数量</td><td><code>32</code></td><td>单个应用中可以声明的实体最大数量</td></tr><tr><td>索引数量</td><td><code>4</code></td><td>单个实体中可以声明的索引最大数量</td></tr><tr><td>实体属性数量</td><td><code>64</code></td><td>单个实体中可以声明的实体属性最大数量</td></tr></tbody></table>

## 对象存储

以下限制适用于单个应用。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>上传频率</td><td><code>5000 次/秒</code></td><td>单个应用中单个安装实例上传文件每秒请求最大数量</td></tr><tr><td>文件大小</td><td><code>1 GB</code></td><td>单个应用中支持上传文件的大小</td></tr><tr><td>URL 请求频率</td><td><code>1000 次/秒</code></td><td>单个应用中单个安装实例 URL 每秒请求频率</td></tr><tr><td>URL 有效期</td><td><code>1 小时</code></td><td>单个应用中单个安装实例 URL 有效时间</td></tr></tbody></table>
