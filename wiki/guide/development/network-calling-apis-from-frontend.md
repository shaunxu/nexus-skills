---
title: "前端调用 REST APIs"
lastUpdated: 2026-07-15T13:43:37.000Z
---

# 前端调用 REST APIs

本指南详细阐述如何在 Nexus 应用内通过前端代码直接向 PingCode REST APIs 发起请求，无须手动管理认证信息，该请求将始终以当前与应用交互的用户身份调用。

## 配置说明

在 `manifest.yaml` 文件中配置对应的作用域范围，没有声明作用域范围的接口调用将因权限不足而失败。如通过工作项标识查询工作项详情信息和更新工作项信息，在接口文档中查询到所要调用接口的作用域，在 `scopes` 中声明：

```yaml
permissions:
  scopes:
    - “pcp:read:pjm:workitem”
    - “pcp:write:pjm:workitem”
```

## 安装依赖

安装前端桥接方法模块依赖：

```
npm install @pc-nexus/bridge
```

## 使用示例

以下示例展示了在前端代码中，调用查询工作项 API 的典型流程：

```typescript
import { api } from "@pc-nexus/bridge";

const response = await api.invoke('/v1/pjm/work_items/{workitem_id}');
console.log(await response.json());
```

## 注意事项

从前端代码发起的 REST APIs 请求始终以当前用户的权限调用，没有与服务端 `{as: "app"}` 等效的选项，这意味着除了应用在 `manifest.yaml` 文件中声明正确的权限范围外，当前用户还必须具备所调用的 REST APIs 操作所需的 PingCode 权限。如果用户没有这些权限，即使应用的权限范围配置正确，请求也会失败。

如果需要应用以自身的身份调用 REST APIs，请使用服务端函数进行调用，参考 [服务端调用 REST APIs](/guide/development/network-calling-apis-from-backend) 。
