---
title: "Nexus scopes"
lastUpdated: 2026-07-15T13:39:24.000Z
---

# Nexus scopes

本文档定义 Nexus 平台的作用域，如使用数据存储等

## 作用域

作用域定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.32%" /><col style="width: 67.68%" /></colgroup><thead><tr><th>权限</th><th>描述</th></tr></thead><tbody><tr><td><code>pcp:read:app:token</code></td><td>读取以「应用」身份调用 APIs 的令牌</td></tr><tr><td><code>pcp:read:user:token</code></td><td>读取以「当前用户」身份调用 APIs 的令牌</td></tr><tr><td><code>pcp:storage:app</code></td><td>应用使用托管存储数据</td></tr></tbody></table>

## 示例

示例代码如下：

```yaml
permissions:
    scopes:
      - “pcp:storage:app”
      - “pcp:read:app:token”
      - “pcp:read:user:token”
```
