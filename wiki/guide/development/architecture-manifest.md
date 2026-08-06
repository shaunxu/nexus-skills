---
title: "Manifest"
lastUpdated: 2026-07-14T09:34:48.000Z
---

# Manifest

Manifest 文件是每个扩展应用的核心配置文件，使用 YAML 格式描述，负责描述应用的元数据、扩展点以及访问权限，定义应用的唯一标识，必须存在于每个应用的根目录下且文件名不能修改。

```javascript
my-first-app
├── src/
│   ├── resolvers/
│   │   └── index.ts
│   └── index.ts
├── web/
│   └── main/
│       ├── src/
│       │   ├── app/
│       │   │   ├── app.config.ts
│       │   │   ├── app.html
│       │   │   ├── app.scss
│       │   │   └── app.ts
│       │   ├── index.html
│       │   ├── main.ts
│       │   └── styles.scss
│       ├── angular.json
│       ├── package.json
│       ├── tsconfig.app.json
│       ├── tsconfig.json
│       └── tsconfig.spec.json
├── manifest.yaml
├── package.json
└── tsconfig.json
```

## 结构

每个 `manifest.yaml` 文件必须包含三个顶级属性： `app` 、 `permissions` 以及 `extensions` 和 `event` 其中之一，完整的结构如下：

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
translations {}
```

## 示例

以下是一个简单的 `manifest.yaml` 文件示例：

```yaml
app:
  id: "466d303d-a2c4-4ec4-ad7c-5435be94583b"
  version: 1.6.0

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

permissions:
  scopes:
    - "pcp:read:ship:idea"
    - "pcp:write:ship:idea"
```

## 参考

关于 `manifest.yaml` 文件的详细定义请参考 [概述](/reference/manifest/overview)
