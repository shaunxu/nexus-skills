---
title: "URI 定义"
lastUpdated: 2026-07-06T10:12:24.000Z
---

# URI 定义

Nexus APIs 遵循 REST 规范，采用层级化、标准化的 URI 路径定位业务资源。路径中通过 {参数名} 标记动态路径参数，接口调用时需替换为实际业务数值。

## 规则

所有接口统一遵循以下通用路径格式：

```
https://{rest_api_root}/v1[/{area}]/{resource}[/{action}]
```

路径参数说明：

```
- rest_api_root：API 根路径
  - 公有云环境：open.pingcode.com/ex
  - 私有部署环境：{自定义域名}/open/ex
  - 其他环境：{在上下文中提供的地址}
- area：资源所属子区域（可空）
- resource：资源路径
- action：特殊操作（可空）
```

## 示例

接口路径示例：

```
https://open.pingcode.com/ex/v1/nexus/ces/insert 
https://open.pingcode.com/ex/v1/nexus/ces/find
```
