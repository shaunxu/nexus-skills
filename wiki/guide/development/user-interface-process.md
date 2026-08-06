---
title: "前端界面构建流程"
lastUpdated: 2026-07-17T09:23:24.000Z
---

# 前端界面构建流程

本指南详细阐述如何使用 Nexus 平台构建用户界面的基本要素，如何声明和使用资源与解析器函数，这是前端界面 UI 开发中的关键概念。

## 静态资源

资源允许你使用静态资源（如 HTML、CSS、JavaScript 和图片）来自定义自己的用户界面。现代 Web 应用程序 `/src` 为前端源代码， `/dist` 为构建后的目录：

```javascript
├── web
│   └── main
│       ├── dist
│       └── src
├── manifest.yaml
```

在执行构建时会将静态 Web 应用模板与 Nexus bridge APIs 一起打包到 `web/main/dist` 目录中，随后将此目录配置为 Nexus 应用 `manifest.yml` 文件中的资源路径：

```yaml
resources:
  - key: main
    path: web/main/dist
```

path 配置的目录下确保必须存在 `index.html` ，这是当前资源的入口文件，关于 Javascript、CSS 都是通过该文件去加载，当扩展应用渲染时会通过 iframe 加载该文件。

## 解析器函数

在 `/src/resolvers/index.ts` 文件中，使用 `Resolver` 定义解析器函数：

```typescript
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<string, string>("greeting", async (context, payload) => {
    return `Hello, ${payload}`;
});

export { resolver };
```

在 `manifest.yaml` 文件中声明函数：

```yaml
functions:
  - key: resolver
    handler: index.resolver
```

## 调用函数

在前端代码 `/web/main/src/app/app.ts` 中通过 `invoke` 调用解析器函数，其中 `greeting` 为自定义的函数标识：

```typescript
import { invoke } from '@pc-nexus/bridge';

const data = await invoke('greeting', { example: 'my-invoke-variable' });
```

## 扩展模块

前面定义的静态资源和后端解析器函数，需要在 `manifest.yaml` 文件中将其附加到扩展模块上：

```yaml
extensions:
  - key: hello-world-project-hub
    title: Hello World
    target: "pcm:pjm:project:page"
    resource: main
    resolver:
      function: resolver
      
functions:
  - key: resolver
    handler: index.resolver
    
resources:
  - key: main
    path: web/main/dist
```
