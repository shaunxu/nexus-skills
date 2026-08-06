---
title: "构建限制"
lastUpdated: 2026-07-02T03:41:25.000Z
---

# 构建限制

本文档定义应用在构建过程中的限制。

## 应用限制

以下限制适用于单个应用。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>相同环境同时部署数</td><td><code>1</code></td><td>单个应用在同一个环境中，可以同时执行部署的数量</td></tr><tr><td>安装包保留时长</td><td><code>30 天</code></td><td>单个应用的安装包，未在任何环境中使用，或者使用后被新的安装包替换，在保留特定时长后，会被清理</td></tr></tbody></table>

## 用户限制

以下限制适用于单个开发者用户。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>执行构建并行数</td><td><code>2</code></td><td>单个开发者用户可以同时并行执行的构建部署操作数量</td></tr></tbody></table>
