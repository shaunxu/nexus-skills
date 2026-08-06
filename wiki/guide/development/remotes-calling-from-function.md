---
title: "服务端调用远程服务"
lastUpdated: 2026-07-09T06:26:36.000Z
---

# 服务端调用远程服务

本指南详细阐述如何在 Nexus 服务端函数中调用远程服务。

## 配置说明

从服务端函数中调用远程服务，需要在 `manifest.yaml` 定义一个远程端点，配置示例如下：

```yaml
permissions:
  scopes:
    - pcp:read:user:token

remotes:
  - key: my-remote-key
    baseUrl: https://example.com
    auth:
      userToken: true
      appToken: false
```

如果需要向远程服务发送 OAuth 令牌，需要在 `scopes` 中添加对应的权限，详情请参考 [Permissions](/reference/manifest/permissions)

## 安装依赖

安装服务端网络请求模块依赖：

```
npm install @pc-nexus/network
```

## 使用示例

从服务端函数中调用远程服务，可以使用 `remote.invoke()` 方法，该方法允许你向远程服务发起 HTTP 请求。一个典型的 GET 请求示例如下：

```javascript
import { remote } from "@pc-nexus/network";

const response = await remote.invoke("my-remote-key", {
    path: "/greeting?name=nexus",
    method: "GET"
});

const data = await response.json();
console.log(data);
```

在远程服务端接收到的 Request Headers 如下：

```javascript
{
  "authorization": "Bearer eyJhbGciOiJ...",
  "traceparent": "892c7ede-9fe1-4d8d-9e2c-ac50e0c97c52",
  "x-nexus-api-base-url": "https://open.pingcode.com/ex",
  "x-nexus-user-token": "eyJhbGciO..."
}
```

在远程服务中获取 NIT 信息验证请求来源，以及获取令牌信息在回调 PingCode REST APIs 时使用，详情请参考 [远程服务](/guide/development/remotes) 。
