---
title: "Permissions"
lastUpdated: 2026-07-15T13:40:04.000Z
---

# Permissions

`permissions` 定义应用使用的权限信息。

## 结构

结构定义如下：

```yaml
permissions {}
├─ scopes [] [Mandatory]
├─ external {} [Optional]
│  ├─ fetch {} [Optional]
│  │  ├─ backend [] [Optional]
│  │  └─ client [] [Optional]
│  ├─ fonts [] [Optional]
│  ├─ styles [] [Optional]
│  ├─ frames [] [Optional]
│  ├─ images [] [Optional]
│  ├─ media [] [Optional]
│  └─ scripts [] [Optional]
└─ content {} [Optional]
```

## 示例

简单配置示例：

```yaml
permissions:
  scopes:
    - “pcp:storage:app”
    - “pcp:read:app-system-token”
    - “pcp:read:app-user-token”
    - “pcp:read:pjm:workitem”
    - “pcp:write:pjm:workitem”
  external:
    fetch:
      backend: 
        - remote: remote-backend
      client:
        - "https://*.example.com"
  content:
    scripts:
      - unsafe-hashes
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>scopes</code></td><td>Y</td><td>声明应用使用的 OAuth 2.0 的作用域，包括 Nexus 平台的作用域和 PingCode 产品的作用域，详情参考 <a href="/reference/resource/scopes">作用域参考</a> 。</td></tr><tr><td><code>external</code></td><td></td><td>声明应用访问外部资源的地址</td></tr><tr><td><code>content</code></td><td></td><td>声明前端用户界面所需的内容安全策略（CSP）选项</td></tr></tbody></table>
