---
title: "Endpoints"
lastUpdated: 2026-07-15T03:08:42.000Z
---

# Endpoints

`endpoints` 用于定义端点的属性，如其授权方式、承载该端点的远程后端，以及相对于远程后端基础 URL 的路由。

## 结构

结构定义如下：

```yaml
endpoints []
├─ key (string) [Mandatory]
├─ remote (string) [Mandatory]
├─ route (string) [Mandatory]
└─ auth {} [Optional]
   ├─ userToken (boolean) [Mandatory]
   └─ appToken (boolean) [Mandatory]
```

## 示例

简单配置示例：

```yaml
endpoints:
  - key: remote-trigger-boot
    remote: remote-backend
    route: /nexus-trigger
    auth:
      userToken: true
      appToken: false
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>端点的唯一标识，其他模块可以引用该端点，在同一个 manifest 文件中必须唯一</td></tr><tr><td><code>remote</code></td><td>Y</td><td>定义此端点路径基础部分的 <code>key</code></td></tr><tr><td><code>route</code></td><td></td><td>定义调用此端点时，将附加到远程对象 <code>baseUrl</code> 属性后的路径，此属性仅对后端模块端点是必需的 UI 模块远程解析器端点的路径，始终在应用前端的 <code>remote.invoke</code> 请求中指定</td></tr><tr><td><code>auth</code></td><td></td><td>定义远程端点在调用函数时可使用的认证选项的对象，可以指定是否启用： - <code>userToken</code> ：用户令牌 - <code>appToken</code> ：应用令牌</td></tr><tr><td><code>auth.userToken</code></td><td></td><td>如启用，Nexus 会在发送给远程端点的调用令牌中包含一个 <code>userToken</code> 如果端点选择启用远程用户令牌访问，则必须在 <code>manifest</code> 文件的 <code>permissions</code> 部分同时指定 <code>read:user:token</code> 权限范围</td></tr><tr><td><code>auth.appToken</code></td><td></td><td>如启用，Nexus 会在发送给远程端点的调用令牌中包含一个 <code>appToken</code> 如果端点选择启用远程系统令牌访问，则必须在 <code>manifest</code> 文件的 <code>permissions</code> 部分同时指定 <code>read:app:token</code> 权限范围</td></tr></tbody></table>
