---
title: "解析器函数"
lastUpdated: 2026-07-02T08:30:39.000Z
---

# 解析器函数

本文档详细阐述如何在 Nexus 应用中使用解析器函数。解析器是 Nexus 平台中用于定义和执行后端函数的核心模块，开发者可以通过解析器函数编写服务端逻辑，以响应前端发起的异步调用或处理特定事件。

## 安装依赖

在应用的根目录中安装以下依赖项：

```shell
npm install @pc-nexus/core
```

## 文件结构

在应用的 `/src` 目录中，添加以下目录和函数入口文件：

```shell
/src
  /resolvers
    /index.ts
```

## 定义函数

在 `/src/resolvers/index.ts` 文件中，使用 `Resolver` 定义解析器函数：

```typescript
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<string, string>("greeting", async (context, payload) => {
    return `Hello, ${payload}`;
});

export { resolver };
```

## 配置函数

在应用 `manifest.yaml` 文件中声明函数：

```yaml
functions:
  - key: resolver
    handler: index.resolver
```

## 附加到扩展模块

要使定义的函数能够运行，需要通过 `manifest.yaml` 文件将其附加到扩展模块上：

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
```
