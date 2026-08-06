---
title: "验证用户权限"
lastUpdated: 2026-07-02T08:35:33.000Z
---

# 验证用户权限

本文档详细阐述在 Nexus 应用中如何验证用户权限。

## 安装依赖

在应用的根目录中安装以下依赖项：

```shell
npm install @pc-nexus/core
```

## 使用示例

以下是一个判断用户是否对某个特定工作项拥有编辑权限的示例：

```typescript
import { authorize } from "@pc-nexus/core";

const workitemPermissions = await authorize.getUserPermissions(
    "workitem",
    "INFR-13"
);

const canEdit = workitemPermissions.find(p => p.key === "pca:pjm:requirement:edit")?.has_permission ?? false;

if(canEdit) {
    // Do something...
}
```

## 权限点定义

PingCode 产品中每一个操作都会对应一个权限点的定义，如上面的示例中判断用户对某个工作项的编辑权限，使用 `pca:pjm:requirement:edit` ，完整的权限点定义请参考 [权限点参考](/reference/resource/authorize) 。
