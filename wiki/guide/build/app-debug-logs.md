---
title: "日志调试"
lastUpdated: 2026-07-17T03:51:25.000Z
---

# 日志调试

本指南详细阐述如何通过查看日志调试 Nexus 应用。

## 记录日志

开发者可以在代码中增加 `console` 代码日志来调试应用。

```javascript
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();

resolver.define<string, string>("greeting", async (_context, payload) => {
    console.log("Handler invoked: greeting");
    return `Hello, ${payload}!`;
});
```

## **本地启动日志**

通过 `nexus serve` 本地启动时，Nexus 不会记录日志，运行日志会实时显示在执行终端。

```shell
nexus serve     
Starting local server...

✔ Select target environment: development
✓ Connected to development.

Listening for requests...

Info     2026-07-13T06:19:29.105Z    e9d02f80-f7ac-4546-95cd-ba8a1f4ab18b    Handler invoked: greeting.
```

## **查看远程日志**

在远程云端运行时，日志会被 Nexus 自动采集，开发者可以通过开发者中心日志管理或 `nexus logs` 命令查看，详细请参考 [日志记录](/guide/development/logs) 。

```
nexus logs
nexus logs -g                          # 按 Invocation ID 分组
nexus logs -i <invocation-id>          # 查看单次调用
nexus logs -s 2d                       # 最近 2 天
```
