---
title: "扩展模块"
lastUpdated: 2026-07-03T09:00:32.000Z
---

# 扩展模块

扩展模块是在应用的 `manifest.yaml` 文件中定义的组件，它通过定义与 PingCode 产品内扩展点相对应的属性和行为，来规定您的应用如何与产品集成。

扩展模块能够：

- 扩展功能：为 PingCode 产品添加自定义功能与集成
- 与 APIs 交互：利用 PingCode REST APIs 来增强应用能力
- 自定义用户界面：修改和扩展 UI 以适应您应用的需求

## 配置

扩展模块的结构定义：

```yaml
extensions []
├─ key (string) [Mandatory]
├─ target (string) [Mandatory]
├─ resource (string) [Optional]
├─ resolver {} [Optional]
└─ title (string | i18n) [Optional]

functions []
├─ key (string) [Mandatory]
└─ handler (string) [Mandatory]

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

## 示例

典型的扩展模块配置示例：

```yaml
extensions:
  - key: hello-world-project-hub
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

## 参考

关于扩展模块的详细信息请参考：

- Manifest配置： [Extensions](/reference/manifest/extensions)
- 扩展模块定义： [扩展模块](/reference/resource/extensions)
