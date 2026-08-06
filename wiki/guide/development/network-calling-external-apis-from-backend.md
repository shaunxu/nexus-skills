---
title: "服务端调用外部 APIs"
lastUpdated: 2026-07-02T05:47:37.000Z
---

# 服务端调用外部 APIs

本指南详细阐述如何使用 `fetch` 模块在 Nexus 应用服务端函数中调用外部 APIs。

## 配置说明

在 Nexus 服务端函数中调用外部 APIs 时，调用的 URL 地址需要在 `manifest.yaml ` 文件中配置权限，未声明的域名在请求时会被运行时拦截：

```yaml
permissions:
  scopes: []
  external:
    fetch:
      backend:
        - "api.example.com"    
        - "*.example-dev.com"
```

## 安装依赖

安装服务端网络请求模块依赖：

```
npm install @pc-nexus/network
```

## 使用示例

`fetch` 模块本质上就是提供了一个简单的 HTTP 请求客户端，以下示例展示了如何在服务端函数中调用外部 APIs：

```typescript
import { fetch } from "@pc-nexus/network";

const response = await fetch.request("https://api.example.com", {
    method: "GET",
    headers: {
        "Accept": "application/json",
    },
});

const data = await response.json();
console.log(data);
```
