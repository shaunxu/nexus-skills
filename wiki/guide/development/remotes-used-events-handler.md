---
title: "远程服务作为事件处理函数"
lastUpdated: 2026-07-14T05:18:36.000Z
---

# 远程服务作为事件处理函数

Nexus 应用中可以配置事件触发时，直接发送到远程服务进行处理，平台会自动路由这些事件，并附带一个Nexus 调用令牌和可选的 OAuth 令牌。

## 配置说明

配置事件发送到远程服务，请在 `manifest.yaml` 文件中进行如下配置。

### Step 1：event

定义一个 `event` 项，指定将要订阅的事件：

- 指定应用将向其发送远程请求的端点，通过事件触发器的 `endpoint` 属性完成。使用 `endpoint` 而非 `function` 是告诉平台你的应用将调用远程端点
- 在 `permissions` 中配置事件对应的权限范围

```yaml
event:
  triggers:
    - key: system_trigger
      type: system
      events:
        - pce:pjm:workitem:created
      handler:
        endpoint: my-remote-endpoint
        
permissions:
  scopes:
    - pcp:read:pjm:workitem
```

### Step 2：endpoints

定义一个 `endpoints` 项，其 `key` 与上一步指定的端点名称相匹配：

- 将 `remote` 属性设置为唯一标识该端点将要通信的远程服务的 `key`
- 将 `route` 设置为要附加到远程服务 `baseUrl` 之后的 REST APIs 操作路径，以调用所需的 REST APIs
- 如果需要在远程服务中使用 OAuth 令牌，在 `auth` 属性中指定，并且在 `permissions` 中指定权限范围

```yaml
endpoints:
  - key: my-remote-endpoint
    remote: my-remote-key
    route: /nexus-trigger
    auth:
      appToken: true

permissions:
  scopes:
    - pcp:read:app:token
    - pcp:read:pjm:workitem
```

### Step 3：remotes

定义一个 `remotes` 项，其 `key` 与你在 `endpoint` 中指定的远程服务名称相匹配：

- 将 `baseUrl` 设置为站点 URL 前缀，该前缀将预先添加到应用中 `route` 所指定的路由之前

```yaml
remotes:
  - key: my-remote-key
    baseUrl: https://api.example.com
```

## 配置示例

以下是一个完整示例 `manifest.yaml` ，展示了在新建工作项时将事件路由到远程服务：

```yaml
event:
  triggers:
    - key: system_trigger
      type: system
      events:
        - pce:pjm:workitem:created
      handler:
        endpoint: my-remote-endpoint
        
endpoints:
  - key: my-remote-endpoint
    remote: my-remote-key
    route: /nexus-trigger
    auth:
      appToken: true

remotes:
  - key: my-remote-key
    baseUrl: https://api.example.com

permissions:
  scopes:
    - pcp:read:app:token
    - pcp:read:pjm:workitem
```
