---
title: "Exposer"
lastUpdated: 2026-08-05T02:20:29.000Z
---

# Exposer

`exposer` 定义应用对外暴露自定义 REST APIs 信息。

## 结构

结构定义如下：

```yaml
exposer {}
├─ routes [] [Mandatory]
│  ├─ key (string) [Mandatory]
│  ├─ path (string) [Mandatory]
│  ├─ method (string) [Mandatory]
│  ├─ accept [] [Optional]
│  ├─ scopes [] [Mandatory]
│  └─ handler {} [Mandatory]
└─ scopes [] [Mandatory]
   ├─ name (string) [Mandatory]
   ├─ displayName (string) [Mandatory]
   └─ description (string) [Optional]
```

## 示例

简单配置示例：

```yaml
exposer:
  routes:
    - key: get-employee-api
      path: /employeeName
      method: GET
      handler: 
        function: employee-handler
      accept:
        - application/json 
      scopes:
        - ncp:read:employee
  scopes:
    - name: ncp:read:employee
      displayName: Read Employee Info
      description: Read Employee Info
```

## 属性

支持两个次级属性，分别用于自定义作用域和定义接口路由：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.91%" /><col style="width: 22.03%" /><col style="width: 55.06%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>routes</code></td><td>Y</td><td>应用对外暴露的 REST APIs</td></tr><tr><td><code>scopes</code></td><td>Y</td><td>应用支持的自定义作用域</td></tr></tbody></table>
