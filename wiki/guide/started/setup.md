---
title: "环境配置"
lastUpdated: 2026-07-16T05:32:56.000Z
---

# 环境配置

在进行开发具体应用之前，需要做一些环境上的准备。

## 准备工作

Nexus 应用基于 TypeScript 语言编写，因此你需要熟悉 TypeScript，熟悉 Angular 也会对 Nexus 应用开发有所帮助。当然你也可以使用自己熟悉的前端框架编写应用界面，如 React、Vue等，或者直接使用原生 JavaScript。

开发 Nexus 应用需要 Node.js 环境，推荐安装 `Node.js 24.x (LTS)` 及以上版本。你可以使用以下命令进行版本验证：

```shell
% node -v
v24.14.1
```

## 安装 CLI

Nexus CLI 是用于构建和部署 Nexus 应用的命令行界面工具，帮助开发者快速创建、打包、构建、部署以及分发应用。

安装命令：

```shell
npm install -g @pc-nexus/cli@latest
```

安装完成后，你可以使用 `--version` 选项来验证是否安装正确以及获取版本信息。

```shell
nexus --version
```

如果无法识别命令，请检查 npm 环境变量配置。你可以运行 `nexus --help` 查看所有可用指令。

## 注册帐号

在开发 Nexus 应用时，需要拥有一个开发者帐号，来进行应用的环境、构建及部署管理等，访问 [PingCode 开放平台](https://developer.pingcode.com/console/signup) 完成帐号注册。在使用 Nexus CLI 之前需要先登录，以获得相应的操作权限。

进入开发者中心/个人设置页面，创建个人访问令牌并复制。在终端输入以下命令：

```shell
nexus login
```

根据提示粘贴输入令牌：

```shell
Log in to your PingCode Developer account.
Press Ctrl+C to cancel.

? Enter your PingCode API token: [input is masked]
```

出现如下提示，表示成功登录 CLI：

```javascript
✔ Logged in as yourname.

Now try running 'nexus create' to start a new app.
```

下一步使用 CLI 来创建第一个应用。
