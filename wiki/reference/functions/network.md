---
title: "Network"
lastUpdated: 2026-07-15T15:09:52.000Z
---

# Network

Network APIs 是 Nexus 平台运行时的网络请求模块，为应用提供 PingCode REST API 访问、外部网络请求及跨应用通信能力。

## 安装

```
npm install @pc-nexus/network
```

导入

```javascript
import { api } from "@pc-nexus/network";

import { fetch } from "@pc-nexus/network";
```

## APIs

Network APIs 提供的能力如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.72%" /><col style="width: 68.28%" /></colgroup><thead><tr><th>APIs</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/functions/network/api">api</a></td><td>调用 PingCode REST API，运行时自动处理认证</td></tr><tr><td><a href="/reference/functions/network/fetch">fetch</a></td><td>向外部服务发起 HTTP 请求</td></tr><tr><td><a href="/reference/functions/network/remote">remote</a></td><td>调用远程服务端点</td></tr></tbody></table>
