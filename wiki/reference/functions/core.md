---
title: "Core"
lastUpdated: 2026-07-15T09:18:55.000Z
---

# Core

Core APIs 提供了一系列 APIs，用于帮助开发者进行服务端函数定义、获取上下文、权限验证、日志记录或者多语言设置等操作。

## 安装

```shell
npm install @pc-nexus/core
```

使用

```javascript
import { Resolver } from "@pc-nexus/core";

import { i18n } from "@pc-nexus/core";
```

## APIs

目前 Core APIs 提供的能力如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.15%" /><col style="width: 66.85%" /></colgroup><thead><tr><th>APIs</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/functions/core/resolver">resolver</a></td><td>定义服务端解析器函数</td></tr><tr><td><a href="/reference/functions/core/app">app</a></td><td>获取当前应用上下文信息</td></tr><tr><td><a href="/reference/functions/core/authorize">authorize</a></td><td>获取当前用户的权限信息</td></tr><tr><td><a href="/reference/functions/core/i18n">i18n</a></td><td>应用多语言设置</td></tr></tbody></table>
