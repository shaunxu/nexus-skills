---
title: "前端调用远程服务"
lastUpdated: 2026-07-09T05:22:06.000Z
---

# 前端调用远程服务

本指南详细阐述如何在 Nexus 应用前端代码中调用远程服务。

## 配置说明

从应用前端调用远程服务，需要在 `manifest.yaml` 定义一个远程端点，配置示例如下：

```yaml
remotes:
  - key: my-remote
    baseUrl: https://remote.example.com
```

## 安装依赖

安装前端桥接方法模块依赖：

```shell
npm install @pc-nexus/bridge
```

## 使用示例

从应用前端调用远程服务，可以使用 `remote.request()` 方法，该方法发起请求时不会携带 OAuth 令牌，下面分别是两种请求内容的示例。

### 普通请求

一个典型的 GET 请求示例如下：

```typescript
import { remote } from "@pc-nexus/bridge";

const response = await remote.request("my-remote-key", {
    path: "/greeting?name=nexus",
    method: "GET"
});

const data = await response.json();
console.log(data);
```

### 文件上传

`remote.request()` 支持通过 `FormData` 上传文件，使用时不要手动设置 `content-type` ，浏览器会自动生成包含 `boundary` 的请求头。

```typescript
import { remote } from "@pc-nexus/bridge";

async function uploadFile(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("description", "remote request upload");

    const response = await remote.request("my-remote-key", {
        path: "/upload",
        method: "POST",
        body: formData
    });

    const result = await response.json();
    console.log(result);
}
```

## 注意事项

远程服务需要允许应用所在 PingCode 域名跨域访问，并允许 `Authorization` 请求头， `remote.request` 方法会在请求头中携带 NIT token：

```javascript
Authorization: Bearer <NIT token>
```
