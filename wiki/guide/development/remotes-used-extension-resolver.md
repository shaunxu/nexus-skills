---
title: "远程服务作为模块解析器"
lastUpdated: 2026-07-09T06:28:51.000Z
---

# 远程服务作为模块解析器

本指南详细阐述如何在 Nexus 应用中使用远程服务，作为扩展模块解析器。

## 配置说明

配置远程服务作为扩展模块解析器，在 `manifest.yaml` 文件中进行如下配置。

### Step 1：extensions

定义一个 `extensions` 项，配置扩展模块，指定应用将向其发送远程请求的端点，通过扩展模块的 `resolver.endpoint` 属性完成。使用 `endpoint` 而非 `function` 是告诉平台你的应用将调用远程端点：

```yaml
extensions:
  - key: remote-project-page
    target: pcm:pjm:project:page
    title: Remote Project Page
    resolver:
      endpoint: remote-project-page-endpoint
    resource: main
```

### Step 2：endpoints

定义一个 `endpoints` 项，其 `key` 与上一步指定的端点名称相匹配：

- 将 `remote` 属性设置为唯一标识该端点将要通信的远程服务的 `key`
- 如果需要在远程服务中使用 OAuth 令牌，在 `auth` 属性中指定，并且在 `permissions` 中指定权限范围

```yaml
endpoints:
  - key: remote-project-page-endpoint
    remote: my-remote-key
    auth:
      userToken: true
      appToken: true
      
permissions:
  scopes:
    - pcp:read:app:token
    - pcp:read:user:token
```

### Step 3：remotes

定义一个 `remotes` 项，其 `key` 与你在 `endpoint` 中指定的远程服务名称相匹配：

- 将 `baseUrl` 设置为站点 URL 前缀，该前缀将预先添加到应用中 `route` 所指定的路由之前

```yaml
remotes:
  - key: my-remote-key
    baseUrl: https://api.example.com
```

## 配置示例

完整的 `manifest.yaml` 文件配置示例如下：

```yaml
permissions:
  scopes:
    - pcp:read:app:token
    - pcp:read:user:token

extensions:
  - key: remote-project-page
    target: pcm:pjm:project:page
    title: Remote Project Page
    resolver:
      endpoint: remote-project-page-endpoint
    resource: main

remotes:
  - key: my-remote-key
    baseUrl: https://example.com

endpoints:
  - key: remote-project-page-endpoint
    remote: my-remote-key
    auth:
      userToken: true
      appToken: true
```

## 安装依赖

安装前端桥接方法模块依赖：

```shell
npm install @pc-nexus/bridge
```

## 使用示例

在前端代码中，使用 `remote.invoke()` 方法调用当前扩展模块关联的远程服务，使用 `path` 参数指定请求的具体路径：

```typescript
import { remote } from "@pc-nexus/bridge";

const response = await remote.invoke({
    path: "/greeting?name=nexus",
    method: "GET"
});

const data = await response.json();
console.log(data);
```

在远程服务端接收到的 Request Headers 如下：

```
{
  "authorization": "Bearer eyJhbGciOiJ...",
  "traceparent": "892c7ede-9fe1-4d8d-9e2c-ac50e0c97c52",
  "x-nexus-api-base-url": "https://open.pingcode.com/ex",
  "x-nexus-app-token": "eyJhbGciO...",
  "x-nexus-user-token": "eyJhbGciO..."
}
```

在远程服务中获取 NIT 信息验证请求来源，以及获取令牌信息在回调 PingCode REST APIs 时使用，详情请参考 [远程服务](/guide/development/remotes) 。
