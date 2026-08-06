---
title: "使用 KVS 存储偏好数据"
lastUpdated: 2026-07-15T14:05:05.000Z
---

# 使用 KVS 存储偏好数据

本指南详细阐述如何使用 `kvs` 进行 Key-Value 类型数据存储，如用户偏好设置或应用配置等数据。

## 配置说明

使用 `kvs` 存储数据时需要在 `manifest.yaml` 文件中声明作用域：

```yaml
permissions:
    scopes:
        - pcp:storage:app
```

## 安装依赖

安装数据存储模块依赖：

```
npm install @pc-nexus/storage
```

## 存储数据

以下示例展示了对 Key-Value 数据的基本操作：

```typescript
import { kvs } from "@pc-nexus/storage";

await kvs.set("foo", "bar");
await kvs.get("foo");

await kvs.delete("foo");
```

## 加密存储

使用 `kvs` 进行数据存储时，可以对敏感数据进行加密存储，通过指定 `secret` 属性实现，加密数据在读取时会自动解密：

```typescript
import { kvs } from "@pc-nexus/storage";

await kvs.set("foo", "bar", {
    secret: true    
});
    
await kvs.get("foo");
```

完整的使用请参考 [kvs](/reference/functions/storage/kvs) 。
