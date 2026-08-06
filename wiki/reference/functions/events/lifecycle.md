---
title: "lifecycle"
lastUpdated: 2026-07-27T07:52:53.000Z
---

# lifecycle

本文档介绍如何在应用中订阅生命周期事件。应用生命周期事件是在应用进行安装、卸载、升级等事件发生时，由系统自动进行触发，开发者可以提供自定义的事件处理函数，以实现自己的业务逻辑。

## 配置

`manifest.yml` 文件配置示例：

```yaml
event:
  triggers:   
    - key: life_trigger
      type: lifecycle
      events:
        - pce:nexus:app:install
      handler: 
        function: install-handler
```

## 处理函数

当事件触发时，会被你定义的处理函数接收到。

### 示例

```javascript
import type { LifecycleEventHandler } from "@pc-nexus/event";

export const handler: LifecycleEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event));
};
```

### 参数

处理函数接收 `context` 和 `event` 两个参数。

#### context

`context` 为 `NexusAppContext` 类型，包含应用运行时的上下文信息，详情请参考 [app](/reference/functions/core/app) ，获取触发的事件信息可以从 `context` 中获取 如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.24%" /><col style="width: 70.76%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>event.trigger.key</code></td><td>触发器在 <code>manifest</code> 中定义的 <code>key</code></td></tr><tr><td><code>event.trigger.type</code></td><td>触发器类型，值为 <code>lifecycle</code></td></tr></tbody></table>

#### event

`event` 是订阅事件所传递的数据，其类型定义如下：

```javascript
export interface EventPayload {}

export interface LifecycleEventPayload extends EventPayload {
    installation_id: string;
    app: {
        id: string;
        version: string;
        name: string;
        publisher: string;
    };
    environment: {
        id: string;
        type: string;
        name: string;
    };
    operated_by: string;
}
export interface HandlerFunctionEvent<T = unknown> {
    event_type?: string;
    payload: T;
}
```

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.31%" /><col style="width: 76.69%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>event_type</code></td><td>订阅事件的类型，例如: <code>pce:nexus:app:install</code></td></tr><tr><td><code>payload</code></td><td>订阅事件所传递的数据</td></tr></tbody></table>

`payload` 在应用生命周期事件中，所有事件通用属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.31%" /><col style="width: 76.69%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>installation_id</code></td><td>当前应用安装时的唯一标识</td></tr><tr><td><code>app</code></td><td>当前应用数据</td></tr><tr><td><code>environment</code></td><td>当前应用所在环境数据</td></tr><tr><td><code>operated_by</code></td><td>当前事件操作的用户 ID</td></tr></tbody></table>

`app` 定义当前应用数据：

|名称|描述|
|---|---|
|`id`|应用 ID|
|`version`|应用版本号|
|`name`|应用名|
|`publisher`|应用发布者|

`environment` 当前应用所在环境数据：

|名称|描述|
|---|---|
|`id`|应用部署环境 ID|
|`type`|当前应用所在的环境类型， `development` 还是 `production`|
|`name`|应用部署环境名称|

## 事件

目前 Nexus 平台的应用支持以下几个事件：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 48.45%" /><col style="width: 51.55%" /></colgroup><thead><tr><th>事件名</th><th>描述</th></tr></thead><tbody><tr><td><code>pce:nexus:app:install</code></td><td>应用安装后触发</td></tr><tr><td><code>pce:nexus:app:uninstall</code></td><td>应用卸载前触发</td></tr><tr><td><code>pce:nexus:app:upgrade</code></td><td>应用升级时触发</td></tr></tbody></table>

### install

当应用程序在站点中完成安装后，系统会发送名为 `pce:nexus:app:install` 的事件。

数据示例：

```javascript
{
        "event_type": "pce:nexus:app:install",
        "payload": {
            "installation_id": "d2b9c438-c0ee-4f4d-86dc-d6b263d83eff",
            "app": {
                "id": "33b0bb1b-429b-40eb-b4d5-5418584faa04",
                "version": "1.0.0",
                "name": "nexus-lifecycle-event",
                "publisher": "69f16a4bd200465a6826a6c0"
            },
            "environment": {
                "id": "879b2014-6d56-4beb-9610-34a17dc7355b",
                "type": "development",
                "name": "development"
            },
            "operated_by": "631fec198a984680b564b2104ff79ce9"
        }
    }
```

### uninstall

通过用户界面触发卸载操作时，系统会发送名为 `pce:nexus:app:uninstall` 的事件。

数据示例：

```javascript
{
        "event_type": "pce:nexus:app:uninstall",
        "payload": {
            "installation_id": "d2b9c438-c0ee-4f4d-86dc-d6b263d83eff",
            "app": {
                "id": "33b0bb1b-429b-40eb-b4d5-5418584faa04",
                "version": "1.0.0",
                "name": "nexus-lifecycle-event",
                "publisher": "69f16c1ad200465a6826a6c6"
            },
            "environment": {
                "id": "879b2014-6d56-4beb-9610-34a17dc7355b",
                "type": "development",
                "name": "development"
            },
            "operated_by": "631fec198a984680b564b2104ff79ce9"
        }
    }
```

### upgrade

对已安装应用升级至新版本时，会触发名为 `pce:nexus:app:upgrade` 的事件。

数据示例：

```javascript
{
        "event_type": "pce:nexus:app:upgrade",
        "payload": {
            "installation_id": "d2b9c438-c0ee-4f4d-86dc-d6b263d83eff",
            "app": {
                "id": "33b0bb1b-429b-40eb-b4d5-5418584faa04",
                "version": "1.0.0",
                "name": "nexus-lifecycle-event",
                "publisher": "69f16c1ad200465a6826a6c6"
            },
            "environment": {
                "id": "879b2014-6d56-4beb-9610-34a17dc7355b",
                "type": "development",
                "name": "development"
            },
            "operated_by": "631fec198a984680b564b2104ff79ce9"
        }
    }
```

## 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.62%" /><col style="width: 66.38%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_EVENT_LIFECYCLE_HANDLER_INVALID</code></td><td><code>Lifecycle trigger</code> 缺少有效的  <code>handler.function</code>  或  <code>handler.endpoint</code></td></tr><tr><td><code>ERR_EVENT_FUNCTION_NOT_FOUND</code></td><td><code>manifest</code> 中找不到该 <code>trigger</code> 声明的 <code>function</code> 。</td></tr></tbody></table>
