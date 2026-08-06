---
title: "前端界面构建"
lastUpdated: 2026-07-18T02:02:07.000Z
---

# 前端界面构建

本指南详细阐述如何在 Nexus 平台中开发应用前端界面。

## 前端界面

Nexus 平台提供了两种构建前端界面的方式：

1. **Native UI** ：基于 React / Angular 的框架，让开发者能够通过使用 React / Angular 基本组件在 PingCode 产品中原生渲染应用组件，开发出与 PingCode 产品风格一致的应用。

 详情请参考 [Native UI 构建前端界面](/guide/development/user-interface-native-ui) 。

1. **Custom UI** ：赋予开发者完全控制权来构建应用的用户界面。Custom UI 在 iframe 内运行，为应用的界面显示提供了一个隔离环境。

 详情请参考 [Custom UI 构建前端界面](/guide/development/user-interface-custom-ui) 。

## 桥接方法

桥接方法是 Nexus 平台前端开发的核心组件，它是一种 JavaScript APIs，提供了一系列 APIs 允许 Nexus 应用与 PingCode 产品能够进行安全的集成。如调用后端函数、获取当前视图的上下文信息、使用模态框等。更多详情请参考：

- [Bridge APIs](/reference/interface/bridge)

## 业务能力

业务能力提供了一系列 JavaScript APIs，能够帮助开发者直接调用 PingCode 产品能力，而无需重复开发，包括发送通知消息、选择企业成员、打开进程管理器等。更多详情请参考：

- [调用前端业务能力](/guide/development/ui-capabilities)
- [Capability APIs](/reference/interface/capabilities)
