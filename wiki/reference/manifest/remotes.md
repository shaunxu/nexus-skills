---
title: "Remotes"
lastUpdated: 2026-07-15T03:09:46.000Z
---

# Remotes

当使用外部认证服务，或者使用远程调用模块时，远程服务的域名需要在 `remotes` 属性中列出，并在其他地方通过 `key` 进行引用。

## 结构

结构定义如下：

```yaml
remotes []
├─ key (string) [Mandatory]
├─ baseUrl (string) [Mandatory]
└─ auth {} [Optional]
   ├─ userToken (boolean) [Optional]
   └─ appToken (boolean) [Optional]
```

## 示例

简单配置示例：

```yaml
remotes:
   - key: remote-backend
     baseUrl: "https://backend.example.com"
     auth:
        userToken: true
        appToken: false
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>远程资源的唯一标识，其他模块可以引用该远程资源，在同一个 manifest 文件中必须唯一</td></tr><tr><td><code>baseUrl</code></td><td>Y</td><td>指定远程资源的基础 URL，满足以下要求： - 长度不能超过 2048 字符； - 满足正则 <code>/^https?:\/\/[^\/\s]+(?:\/[^\s]*)?$/i</code> ；</td></tr><tr><td><code>auth.userToken</code></td><td></td><td>如启用，远程端点是在用户的登录会话内被调用，Nexus 会在发送给远程应用的调用令牌中包含一个 <code>userToken</code> 。 如果端点选择启用远程用户令牌访问，则必须在 <code>manifest</code> 文件的 <code>permissions</code> 部分同时指定 <code>pcp:read:user:token</code> 权限范围。</td></tr><tr><td><code>auth.appToken</code></td><td></td><td>如启用，Nexus 会在发送给远程应用的调用令牌中包含一个 <code>appToken</code> 。 如果端点选择启用远程系统令牌访问，则必须在 <code>manifest</code> 文件的 <code>permissions</code> 部分同时指定 <code>pcp:read:app:token</code> 权限范围。</td></tr></tbody></table>
