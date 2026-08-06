---
title: "使用 React 构建界面"
lastUpdated: 2026-07-17T07:59:48.000Z
---

# 使用 React 构建界面

本指南详细阐述如何使用 React 前端框架开发 Nexus 应用的用户界面。

## 项目结构

在创建应用时，选择 `React Custom UI` 模板，系统将自动生成标准的目录结构。所有前端资源存放于 `/web` 目录下，默认包含一个名为 `main` 的示例应用。构建生成的产物将被作为模块资源加载至应用中。

典型目录结构示例如下：

```
my-first-app
├── src/
│   ├── resolvers/
│   │   └── index.ts
│   └── index.ts
├── web/
│   └── main/
│       ├── src/
│       │   ├── App.tsx
│       │   └── main.tsx
│       ├── index.html
│       ├── package.json
│       ├── tsconfig.app.json
│       ├── tsconfig.json
│       ├── tsconfig.node.json
│       └── vite.config.ts
├── manifest.yaml
├── package.json
└── tsconfig.json
```

## 调用服务端函数

在 `App.tsx` 文件中编写业务逻辑，通过 `invoke` 方法调用服务端解析器函数：

```typescript
import { useEffect, useState } from 'react'
import { invoke } from '@pc-nexus/bridge'

function App() {
  const [result, setResult] = useState<string | null>(null)

  useEffect(() => {
    runGreeting()
  }, [])

  function runGreeting() {
    invoke<string>('greeting', 'Nexus')
      .then((res: string) => setResult(res))
      .catch((err: Error) => setResult(`Error: ${err}`))
  }
}
```

## 前端界面展示

在 `App.tsx` 组件返回值中绑定组件数据，渲染服务端返回的内容：

```jsx
return <p>{result}</p>
```

## 配置资源

React 应用在部署前首先要构建前端代码，在项目根目录执行如下命令：

```shell
npm run build-web
```

该命令会将静态 Web 应用模板与 Nexus bridge APIs 一起打包。构建产物默认输出到 `web/main/dist` 目录中，将此目录配置为 Nexus 应用 `manifest.yml` 文件中的资源路径：

```yaml
resources:
  - key: main
    path: web/main/dist
```
