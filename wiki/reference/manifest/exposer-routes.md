---
title: "Routes"
lastUpdated: 2026-08-05T03:01:31.000Z
---

# Routes

`routes` 定义应用对外暴露自定义 REST APIs 信息。

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
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.91%" /><col style="width: 22.03%" /><col style="width: 55.06%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>接口的唯一标识</td></tr><tr><td><code>path</code></td><td>Y</td><td>接口暴露的端点地址</td></tr><tr><td><code>method</code></td><td>Y</td><td>接口支持的 HTTP 方法，支持以下方法： - <code>GET</code> - <code>POST</code> - <code>PUT</code> - <code>DELETE</code> - <code>PATCH</code></td></tr><tr><td><code>handler</code></td><td>Y</td><td>接口被调用时的处理函数，使用 <code>function</code> 属性</td></tr><tr><td><code>accept</code></td><td></td><td>接口支持支持请求数据格式，目前只支持： - <code>application/json</code></td></tr><tr><td><code>scopes</code></td><td>Y</td><td>请求接口时需要声明的作用域</td></tr></tbody></table>
