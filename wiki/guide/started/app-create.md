---
title: "创建第一个应用"
lastUpdated: 2026-07-16T05:33:02.000Z
---

# 创建第一个应用

现在准备好创建开发你的第一个应用，对 PingCode 产品功能进行扩展。

## 创建应用

进入你的工作目录，创建一个名为 `my-first-app` 的应用，执行命令：

```javascript
nexus create my-first-app
```

根据提示，选择模板 `Angular Custom UI` ，出现如下提示后应用创建成功：

```shell
Created app my-first-app successfully.

┌ Created successfully. ─────────────────────────────────────────────────────────┐
│                                                                                │
│   Your app is ready to work on, deploy, and install.                           │
│                                                                                │
│   We created 2 environments you can deploy to: production, development.        │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
```

CLI 会为你默认创建好应用目录结构，切换到应用查看：

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

现在我们成功创建了一个使用 `Angular` 进行前端界面开发的应用：

- `src/` 服务端函数源码目录，在这里编写你的解析器函数及后端逻辑
- `web/` 前端资源目录，默认包含一个示例 Web 应用，构建后产物用于作为模块资源被加载
- `manifest.json` 应用的元数据描述文件，定义应用的扩展模块及权限

## 开发应用

当前创建的应用使用了名为 `pcm:pjm:project:page` 的扩展模块，此扩展模块用于在项目管理中增加一个新的项目组件，让我们将这个页面改为自定义名称。

1. 在应用的顶层目录打开  `manifest.yml`  文件
1. 在 `extensions` 下找到 `pcm:pjm:project:page` 扩展模块配置
1. 修改扩展模块配置中的 `title` 属性为 `New Title`

更新后的  `manifest.yml`  文件应如下所示，其中包含修改的标题和应用 ID 的值：

```yaml
app:
  version: 1.0.0
  id: e481d841-e3dc-4b4d-907a-7d7954acee57
extensions:
  - key: my-first-app-project-page
    resource: main
    target: pcm:pjm:project:page
    resolver:
      function: resolver
    title: New title
functions:
  - key: resolver
    handler: index.resolver
resources:
  - key: main
    path: web/main/dist
permissions:
  scopes: []
```

下一步使用CLI部署应用，并安装到 PingCode 产品中使用。
