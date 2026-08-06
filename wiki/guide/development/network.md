---
title: "网络请求"
lastUpdated: 2026-07-15T13:43:07.000Z
---

# 网络请求

Nexus 平台提供了一系列方法，用于进行网络请求相关的开发，包括：

- 调用 REST APIs
- 调用外部 APIs
- 调用远程服务

在开发中可以根据应用的实际需要，灵活的选择这些网络请求方式来实现应用的需求。

## 调用 REST APIs

在 Nexus 应用中，无论是在前端界面代码还是服务端函数中，都可以非常方便的请求 PingCode REST APIs，而无需手动管理认证信息。

应用在调用 REST APIs 时需要在 `manifest.yaml` 文件中声明作用域范围，每个 API 端点都拥有特定的作用域，如果应用未声明，对应的请求将因权限不足而失败：

```yaml
permissions:
  scopes:
    - pcp:read:ship:idea 
    - pcp:write:ship:idea 
    - pcp:read:pjm:workitem 
    - pcp:write:pjm:workitem 
```

更多详情请参考：

- [前端调用 REST APIs](/guide/development/network-calling-apis-from-frontend)
- [服务端调用 REST APIs](/guide/development/network-calling-apis-from-backend)

## 调用外部 APIs

使用 `fetch` 模块可以向外部资源发起 HTTP 请求，适用于访问第三方服务（如 GitHub、Slack、自建服务等），在最基本的用法中， `fetch` 是一个简单的 HTTP 客户端。

在使用 `fetch` 访问外部资源时，需要在 `manifest.yaml` 中声明允许访问的域名，未声明的域名请求将被运行时拦截，同时抛出错误：

```yaml
permissions:
  external:
    fetch:
      backend:
        - "api.example.com"
        - "*.example-dev.com"
```

更多详情请参考：

- [服务端调用外部 APIs](/guide/development/network-calling-external-apis-from-backend)

## 调用远程服务

Nexus 允许你将应用与其他平台托管的服务进行集成，支持在应用内向远程服务发起请求。

远程服务的请求地址，需要在 `manifest.yaml` 中声明，否则请求将会被拦截：

```yaml
permissions:
  external:
    fetch:
      backend: 
        - remote: remote-backend
remotes:
   - key: remote-backend
     baseUrl: "https://backend.example.com"
```

更多详情请参考：

- [前端调用远程服务](/guide/development/remotes-calling-from-frontend)
- [服务端调用远程服务](/guide/development/remotes-calling-from-function)
- [远程服务作为模块解析器](/guide/development/remotes-used-extension-resolver)
- [远程服务作为事件处理函数](/guide/development/remotes-used-events-handler)
- [远程服务调用 REST APIs](/guide/development/remotes-call-rest-apis)
