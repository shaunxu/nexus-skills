---
title: "Functions"
lastUpdated: 2026-07-15T03:09:21.000Z
---

# Functions

`functions` 定义应用使用的后端函数。

## 结构

结构定义如下：

```yaml
functions []
├─ key (string) [Mandatory]
└─ handler (string) [Mandatory]
```

## 示例

简单配置示例：

```yaml
functions:
  - key: resolver
    handler: index.handler
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>后端函数的唯一标识，其他模块可以引用该资源，在同一个 manifest 文件中必须唯一</td></tr><tr><td><code>handler</code></td><td>Y</td><td>指定后端处理函数，满足以下要求： - 长度不能超过 1024 字符； - 期望的格式:  <code>file.function</code> 或 <code>dir/file.function</code> - 满足正则 <code>/^([\p{Alpha}\d_-]+(?:\/[\p{Alpha}\d_-]+)*)\.([\p{Alpha}\d_-]+)$/u</code> ；</td></tr></tbody></table>
