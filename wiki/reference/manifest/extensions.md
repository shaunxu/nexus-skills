---
title: "Extensions"
lastUpdated: 2026-07-15T05:48:03.000Z
---

# Extensions

`extensions` 节点作为顶级属性，定义应用扩展的模块列表。

## 结构

结构定义如下：

```yaml
extensions []
├─ key (string) [Mandatory]
├─ target (string) [Mandatory]
├─ resource (string) [Optional]
├─ resolver {} [Optional]
├─ title (string | i18n) [Optional]
└─ display {} [Optional]
```

## 示例

简单配置示例：

```yaml
extensions:
  - key: hello-world-project-page
    title: Hello World
    target: "pcm:pjm:project:page"
    resource: main
    resolver:
      function: resolver
    viewport:
      size: medium

resources: 
  - key: main
    path: src/index

functions:
  - key: resolver
    handler: index.handler
```

## 属性

每个 `extensions` 节点下，部分属性是通用属性，即所有扩展模块都可以定义的属性，扩展模块的特定属性在每个模块的页面定义。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 21.89%" /><col style="width: 17.37%" /><col style="width: 60.74%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>定义扩展模块的唯一标识</td></tr><tr><td><code>target</code></td><td>Y</td><td>定义扩展模块的目标，即扩展模块在产品中出现的位置。如： <code>pcm:pjm:project:page</code></td></tr><tr><td><code>display</code></td><td></td><td>定义扩展模块的显示条件，参考： <a href="/reference/manifest/extensions-display-conditions">Display conditions</a></td></tr></tbody></table>

完整的属性定义请参考： [扩展模块](/reference/resource/extensions)
