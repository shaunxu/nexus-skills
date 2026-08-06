---
title: "概述"
lastUpdated: 2026-07-17T10:53:38.000Z
---

# 概述

Nexus 平台提供的前端、服务端 SDK 详细说明。

## 前端

Nexus 平台提供了多个前端开发包来简化用户界面的构建。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.33%" /><col style="width: 66.67%" /></colgroup><thead><tr><th>参考</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/interface/ui-components">UI Components</a></td><td>提供了大量预构建且可定制的组件，这些组件符合 PingCode 的设计标准</td></tr><tr><td><a href="/reference/interface/react-hooks">React Hooks</a></td><td>提供了一组预构建的自定义 React Hooks，用于辅助完成常见任务</td></tr><tr><td><a href="/reference/interface/bridge">Bridge APIs</a></td><td>支持 Nexus 应用与 PingCode 产品进行安全的集成</td></tr><tr><td><a href="/reference/interface/capabilities">Capability APIs</a></td><td>支持 Nexus 应用直接调用 PingCode 产品能力，而无需重复开发</td></tr></tbody></table>

## 服务端

无服务器函数是 Nexus 平台的核心组成部分，使开发者能够创建可扩展的自定义应用，并与 PingCode 产品实现无缝交互和功能扩展。该功能支撑着平台的诸多核心能力，包括 UI后端解析器、应用事件处理等。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.05%" /><col style="width: 66.95%" /></colgroup><thead><tr><th>参考</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/functions/core">Core</a></td><td>服务端核心开发包，帮助开发者进行服务端函数定义、获取上下文等操作</td></tr><tr><td><a href="/reference/functions/network">Network</a></td><td>网络请求模块，在 Nexus 应用中实现 APIs 访问、外部网络请求及跨应用通信能力</td></tr><tr><td><a href="/reference/functions/storage">Storage</a></td><td>数据存储模块，提供托管式数据存储能力，支持在应用安装实例中持久化存储数据</td></tr><tr><td><a href="/reference/functions/events">Event</a></td><td>事件订阅模块，通过订阅事件或 HTTP 端点，无需任何用户交互调用应用内的函数</td></tr><tr><td><a href="/reference/functions/async">Async</a></td><td>异步消息模块，在 Nexus 应用中实现异步消息队列</td></tr><tr><td><a href="/reference/functions/realtime">Realtime</a></td><td>实时更新模块，在 Nexus 应用中实现实时消息推送</td></tr></tbody></table>
