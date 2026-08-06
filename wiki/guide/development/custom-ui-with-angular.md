---
title: "使用 Angular 构建界面"
lastUpdated: 2026-07-17T07:59:43.000Z
---

# 使用 Angular 构建界面

本指南详细阐述如何使用 Angular 前端框架开发 Nexus 应用的用户界面。

## 项目结构

在创建应用时，选择 `Angular Custom UI` 模板，系统将自动生成标准的目录结构。所有前端资源存放于  `/web` 目录下，默认包含一个名为  `main` 的示例应用。构建生成的产物将被作为模块资源加载至应用中。

典型目录结构示例如下：

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

## 调用服务端函数

在 `app.ts` 文件中编写业务逻辑，通过 `invoke` 方法调用服务端解析器函数：

```typescript
import { Component, signal } from '@angular/core';
import { invoke } from '@pc-nexus/bridge';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly result = signal<string | null>(null);

  constructor() {
    this.runGreeting();
  }

  protected runGreeting() {
    invoke<string>('greeting', 'Nexus')
      .then((res: string) => this.result.set(res))
      .catch((err: Error) => this.result.set(`Error: ${err}`));
  }
}
```

## 前端界面展示

在 `app.html` 模板中绑定组件数据，渲染服务端返回的内容：

```htmlmixed
<p>{{ result() }}</p>
```

## 配置资源

Angular 应用在部署前首先要构建前端代码，在项目根目录执行如下命令：

```shell
npm run build-web
```

该命令会将静态 Web 应用模板与 Nexus bridge APIs 一起打包。构建产物默认输出到 `web/main/dist` 目录中，将此目录配置为 Nexus 应用 `manifest.yml` 文件中的资源路径：

```yaml
resources:
  - key: main
    path: web/main/dist
```
