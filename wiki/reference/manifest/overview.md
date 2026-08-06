---
title: "概述"
lastUpdated: 2026-07-15T05:47:32.000Z
---

# 概述

Manifest 文件是每个扩展应用的核心配置文件，使用 YAML 格式描述，负责描述应用的元数据、扩展点以及访问权限，定义应用的唯一标识，必须存在于每个应用的根目录下且文件名不能修改。

## 结构

每个 `manifest.yaml` 文件必须包含三个顶级属性： `app` 、 `permissions` 以及 `extensions` 和 `event` 其中之一，结构定义如下：

```yaml
app {}
├─ id (string) [Mandatory]
└─ version (string) [Mandatory]
permissions {}
└─ scopes [] [Mandatory]
extensions []
event {}
functions []
resources []
endpoints []
remotes []
storage {}
queue {}
translations {}
```

## 示例

简单配置示例：

```yaml
app:
  id: "466d303d-a2c4-4ec4-ad7c-5435be94583b"
  version: 1.6.0

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

permissions:
  scopes:
    - "pcp:read:ship:idea"
    - "pcp:write:ship:idea"
```

## 属性

Manifest 文件中顶级节点属性的定义如下表所示，每个属性的详细信息请参考具体属性文档。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.74%" /><col style="width: 13.42%" /><col style="width: 63.84%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>app</code></td><td>Y</td><td>定义应用的基本信息，包括唯一标识、名称、开发者信息等</td></tr><tr><td><code>permissions</code></td><td>Y</td><td>定义应用所需要的权限列表</td></tr><tr><td><code>extensions</code></td><td>Y*</td><td>定义应用扩展的模块列表，和 <code>event</code> 节点至少要包含其中之一</td></tr><tr><td><code>event</code></td><td>Y*</td><td>定义应用事件订阅列表，和 <code>extensions</code> 节点至少要包含其中之一</td></tr><tr><td><code>functions</code></td><td></td><td>定义应用的后端函数列表</td></tr><tr><td><code>endpoints</code></td><td></td><td>定义应用所使用的端点列表</td></tr><tr><td><code>remotes</code></td><td></td><td>定义远程调用资源列表</td></tr><tr><td><code>resources</code></td><td></td><td>定义应用中所用的资源列表</td></tr><tr><td><code>storage</code></td><td></td><td>定义应用存储的实体信息</td></tr><tr><td><code>queue</code></td><td></td><td>定义异步消息队列</td></tr><tr><td><code>translations</code></td><td></td><td>定义应用翻译资源列表</td></tr></tbody></table>

## 限制

在 Manifest 文件定义时，有一些通用的规则需要注意：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>限制项</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>Key 组成规则</td><td><code>^[a-zA-Z][a-zA-Z0-9_-]*$</code></td><td>每个 Key 都必须满足该正则表达式 - 使用大小写字母、数字以及下划线、连接线组成 - 以字母 <code>a-z A-Z</code> 开头</td></tr><tr><td>Key 最大长度</td><td><code>256</code></td><td>每个 Key 的最大长度</td></tr><tr><td>Manifest 文件大小</td><td><code>256KB</code></td><td>Manifest 文件最大 <code>256KB</code></td></tr></tbody></table>
