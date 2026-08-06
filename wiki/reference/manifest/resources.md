---
title: "Resources"
lastUpdated: 2026-07-15T03:09:59.000Z
---

# Resources

`resources` 定义应用使用的资源信息。

## 结构

结构定义如下：

```yaml
resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

## 示例

简单配置示例：

```yaml
resources: 
  - key: main
    path: src/index
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>资源的唯一标识，其他模块可以引用该资源，在同一个 manifest 文件中必须唯一</td></tr><tr><td><code>path</code></td><td>Y</td><td>从应用程序根目录到包含您的静态资源的目录的相对路径，该目录必须包含一个 <code>index.html</code> 入口点。</td></tr></tbody></table>
