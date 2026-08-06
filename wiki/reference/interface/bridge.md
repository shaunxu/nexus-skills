---
title: "Bridge APIs"
lastUpdated: 2026-07-29T06:18:20.000Z
---

# Bridge APIs

桥接方法是一种 JavaScript APIs，它提供了一系列 APIs 允许 Nexus 应用与 PingCode 产品能够进行安全的集成。如调用后端函数、获取当前视图的上下文信息、使用模态框等。

## 安装

```powershell
npm install @pc-nexus/bridge
```

使用

```typescript
import { invoke } from '@pc-nexus/bridge';

import { view } from '@pc-nexus/bridge';
```

## APIs

目前提供的桥接方法 APIs 如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.15%" /><col style="width: 66.85%" /></colgroup><thead><tr><th>APIs</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/interface/bridge/view">view</a></td><td>获取当前视图的上下文数据</td></tr><tr><td><a href="/reference/interface/bridge/invoke">invoke</a></td><td>调用服务端函数</td></tr><tr><td><a href="/reference/interface/bridge/dialog">dialog</a></td><td>打开包含指定资源的模态框</td></tr><tr><td><a href="/reference/interface/bridge/api">api</a></td><td>调用 PingCode REST API</td></tr><tr><td><a href="/reference/interface/bridge/i18n">i18n</a></td><td>操作多语言</td></tr><tr><td><a href="/reference/interface/bridge/router">router</a></td><td>控制应用路由</td></tr><tr><td><a href="/reference/interface/bridge/events">events</a></td><td>订阅处理事件</td></tr><tr><td><a href="/reference/interface/bridge/remote">remote</a></td><td>调用远程函数</td></tr><tr><td><a href="/reference/interface/bridge/store">store</a></td><td>对象存储</td></tr></tbody></table>
