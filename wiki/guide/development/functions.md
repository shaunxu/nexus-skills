---
title: "服务端函数"
lastUpdated: 2026-07-14T10:10:00.000Z
---

# 服务端函数

无服务器函数是 Nexus 平台最核心的组成部分，使开发者能够创建可扩展的自定义应用，并与 PingCode 产品无缝交互和扩展。服务端函数支撑了平台的许多其他基础能力，包括 UI 后端解析器、事件处理函数等。

## 解析器函数

解析器是 Nexus 平台中用于定义和执行后端函数的核心模块，开发者可以通过解析器函数编写服务端逻辑，以响应前端发起的异步调用或处理特定事件。更多详情请参考：

- [解析器函数](/guide/development/functions-resolvers)
- [resolver](/reference/functions/core/resolver)

## 事件处理函数

处理器函数用于监听的事件触发时，进行业务逻辑的处理。更多详情请参考：

- [事件处理函数](/guide/development/functions-events-handler)
- [Event](/reference/functions/events)

## 权限验证

在服务端函数中，如何在执行具体的操作前，验证用户的权限。更多详情请参考：

- [验证用户权限](/guide/development/functions-verify-user-permissions)
- [authorize](/reference/functions/core/authorize)
