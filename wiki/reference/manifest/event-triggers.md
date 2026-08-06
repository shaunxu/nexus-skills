---
title: "Triggers"
lastUpdated: 2026-08-04T05:50:55.000Z
---

# Triggers

`triggers` 属性定义当订阅的指定事件触发时，通知应用。

## 示例

简单配置示例：

```yaml
event:
  triggers:
    - key: system-trigger
      type: system
      events:
        - pce:ship:idea:created
        - pce:ship:idea:updated
      handler: 
        function: ship-idea-handler
functions:
  - key: ship-idea-handler
    handler: shipIdea.handler
```

## 属性

`triggers` 中每一项需要定义如下属性：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.96%" /><col style="width: 16.54%" /><col style="width: 56.5%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>事件订阅的唯一标识</td></tr><tr><td><code>type</code></td><td>Y</td><td>指定订阅的事件类型，取值为如下几个： - <code>system</code> ：PingCode 产品内的事件，如创建工作项 - <code>app</code> ：应用自定义事件，其他应用通过 <code>registries</code> 声明的事件 - <code>lifecycle</code> ：应用生命周期事件，如安装、卸载 - <code>webhook</code> ：通过注册的一个 HTTP 请求端点，触发调用 - <code>scheduled</code> ：定时触发调用应用，如每天一次</td></tr><tr><td><code>config</code></td><td>Y</td><td>不同类型的事件订阅，所需要的配置信息，详情见下面</td></tr></tbody></table>

## 事件

当前支持5种事件类型。

### system

`system` 类型指定订阅 PingCode 产品内的事件，如创建工作项等

```yaml
event:
  triggers:
    - key: system-trigger
      type: system
      events:
        - pce:ship:idea:created
        - pce:ship:idea:updated
      handler: 
        function: ship-idea-handler
      filter:
        ignoreSelf: true
```

`config` 需要配置的属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.96%" /><col style="width: 16.54%" /><col style="width: 56.5%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>events</code></td><td>Y</td><td>订阅的事件列表，可以同时声明多个事件，使用相同的处理函数 事件以 <code>pce</code> 开头声明，如 <code>pce:ship:idea:updated</code></td></tr><tr><td><code>handler</code></td><td>Y</td><td>事件被触发时的后端处理函数： - 指定后端处理函数时使用 <code>function</code> 属性 - 指定远程服务时使用 <code>endpoint</code> 属性</td></tr><tr><td><code>filter</code></td><td></td><td>用于定义事件的过滤器</td></tr><tr><td><code>filter.ignoreSelf</code></td><td></td><td>指定忽略应用本身触发的事件，默认为 <code>false</code> ，如果不指定，则应用自身触发的事件将会被再次分发。</td></tr></tbody></table>

### app

`app` 类型指定应用自定义事件，其他应用通过 `registries` 声明的事件。

```yaml
event:
  triggers:   
    - key: app-trigger
      type: app
      events:
        - nae:app:466d303d-a2c4-4ec4-ad7c-5435be94583b:event-key
      handler: 
        function: ship-idea-handler
```

`config` 需要配置的属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.96%" /><col style="width: 16.54%" /><col style="width: 56.5%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>events</code></td><td>Y</td><td>订阅的事件列表，可以同时声明多个事件，使用相同的处理函数 事件以 <code>nae</code> 开头声明，如 <code>nae:app:466d303d-a2c4-4ec4-ad7c-5435be94583b:event-key</code></td></tr><tr><td><code>handler</code></td><td>Y</td><td>事件被触发时的后端处理函数： - 指定后端处理函数时使用 <code>function</code> 属性 - 指定远程服务时使用 <code>endpoint</code> 属性</td></tr></tbody></table>

### lifecycle

`lifecycle` 类型指定应用生命周期事件，如安装、卸载。

```yaml
event:
  triggers:   
    - key: lifecycle-trigger
      type: lifecycle
      events:
        - pce:nexus:app:install
      handler: 
        function: lifecycle-handler
```

`config` 需要配置的属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.96%" /><col style="width: 16.54%" /><col style="width: 56.5%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>events</code></td><td>Y</td><td>订阅的事件列表，可以同时声明多个事件，使用相同的处理函数 事件以 <code>pce</code> 开头声明，如 <code>pce:nexus:app:install</code></td></tr><tr><td><code>handler</code></td><td>Y</td><td>事件被触发时的后端处理函数： - 指定后端处理函数时使用 <code>function</code> 属性 - 指定远程服务时使用 <code>endpoint</code> 属性</td></tr></tbody></table>

### webhook

`webhook` 类型指定通过注册的一个 HTTP 请求端点，触发调用。

```yaml
event:
  triggers:   
    - key: webhook-trigger
      type: webhook
      handler:
        function: webhook-handler
```

`config` 需要配置的属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.96%" /><col style="width: 16.54%" /><col style="width: 56.5%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>handler</code></td><td>Y</td><td>事件被触发时的后端处理函数： - 指定后端处理函数时使用 <code>function</code> 属性</td></tr></tbody></table>

### scheduled

`scheduled` 类型指定定时触发调用应用，如每天一次。

```yaml
event:
  triggers:   
    - key: scheduled-trigger
      type: scheduled
      handler:
        function: scheduled-handler
      interval: hour
      timeout: 60
```

`config` 需要配置的属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.96%" /><col style="width: 16.54%" /><col style="width: 56.5%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>handler</code></td><td>Y</td><td>事件被触发时的后端处理函数： - 指定后端处理函数时使用 <code>function</code> 属性 - 指定远程服务时使用 <code>endpoint</code> 属性</td></tr><tr><td><code>interval</code></td><td>Y</td><td>事件定时触发的频率： - <code>tenMinute</code> ：每10分钟触发一次 - <code>hour</code> ：每小时触发一次 - <code>day</code> ：每天触发一次 - <code>week</code> ：每周触发一次</td></tr><tr><td><code>timeout</code></td><td></td><td>允许的最大超时时间，单位为秒</td></tr></tbody></table>
