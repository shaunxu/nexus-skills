---
title: "服务端调用 REST APIs"
lastUpdated: 2026-07-15T13:43:52.000Z
---

# 服务端调用 REST APIs

本指南详细阐述如何在 Nexus 应用内通过服务端函数向 PingCode REST APIs 发起请求，无须手动管理认证信息。

## 配置说明

在 `manifest.yaml` 文件中配置对应的作用域范围，没有声明作用域范围的接口调用将因权限不足而失败。如通过工作项标识查询工作项详情信息和更新工作项信息，在接口文档中查询到所要调用接口的作用域，在 `scopes` 中声明：

```yaml
permissions:
  scopes:
    - “pcp:read:pjm:workitem”
    - “pcp:write:pjm:workitem”
```

## 安装依赖

安装服务端网络请求模块依赖：

```
npm install @pc-nexus/network
```

## 使用示例

以下示例展示了在服务端函数中，调用查询工作项 APIs 的典型流程：

```typescript
import { api } from "@pc-nexus/network";

const response = await api.invoke(`/v1/pjm/work_items/${payload.workitemId}`, {
    as: "user",
    userId: context.user?.id ?? ''
});

console.log(await response.json());
```
