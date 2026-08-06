---
title: "system"
lastUpdated: 2026-07-27T07:25:25.000Z
---

# system

本文档介绍如何在应用中订阅系统事件。当用户在 PingCode 产品中执行操作时，系统会生成 PingCode 产品事件，如创建工作项，应用可以配置订阅并处理这些事件。

## 配置

`manifest.yml` 文件配置示例：

```yaml
event:
  triggers:
    - key: system_trigger
      type: system
      events:
        - pce:ship:idea:created
        - pce:ship:idea:updated
      handler: 
        function: ship-idea-handler
      filter:
        ignoreSelf: true
```

## 处理函数

当事件触发时，会被你定义的处理函数接收到。

### 示例

```javascript
import type { SystemEventHandler } from "@pc-nexus/event";

export const handler: SystemEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event));
};

```

### 参数

处理函数接收 `context` 和 `event` 两个参数。

#### context

`context` 为 `NexusAppContext` 类型，包含应用运行时的上下文信息，详情请参考 [app](/reference/functions/core/app) ，获取触发的事件信息可以从 `context` 中获取 如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.24%" /><col style="width: 70.76%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>event.trigger.key</code></td><td>触发器在 <code>manifest</code> 中定义的 <code>key</code></td></tr><tr><td><code>event.trigger.type</code></td><td>触发器类型，值为 <code>system</code></td></tr></tbody></table>

#### event

`event` 是订阅事件所传递的数据，其类型定义如下：

```typescript
export interface HandlerFunctionEvent {
    event_type: string;
    self_generated: boolean;
    payload: {
        data: PrincipalInfo;
        changelog?: {
            origin?: originValue;
            target?: targetValue;
            property?: PropertyInfo;
        };
        source?: SystemEventSource;
    };
}
```

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25.71%" /><col style="width: 74.29%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>event_type</code></td><td>订阅事件的类型，例如 <code>pce:pjm:workitem:created</code></td></tr><tr><td><code>self_generated</code></td><td>该事件是否为 <code>Nexus App</code> 的操作触发的，如调用 <code>REST API</code> 创建或者更新工作项；当 <code>Manifest</code> 中对应的 <code>config.filter.ignoreSelf</code> 为 <code>true</code> 且 <code>self_generated = true</code> 的事件不会被触发，反之会被触发。</td></tr><tr><td><code>payload</code></td><td>订阅事件所传递的数据</td></tr></tbody></table>

`payload` 中包含：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25.71%" /><col style="width: 74.29%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>事件主体信息，结构与获取主体信息的 REST API 返回的结构相同； 关于辨别主体的几个例子： - <code>pce:pjm:workitem:created</code> 事件主体为 workitem； - <code>pce:pjm:workitem:link:added</code> 事件主体为 workitem； - <code>pce:pjm:sprint:created</code> 事件主体为 sprint；</td></tr><tr><td><code>source</code></td><td>表明了触发事件的源头，默认为空； 例如当时系统自动操作导致产生的事件时，该字段值是 <code>system</code></td></tr><tr><td><code>changelog</code></td><td>变更日志，通常在事件类型是 updated、added 和 removed 时携带此字段</td></tr><tr><td><code>changelog.origin</code></td><td>变更时的原始值； - 当事件类型是 updated 时，该字段就是变更前的值； - 当事件类型是 removed 时，该字段就是移除的目标对象；</td></tr><tr><td><code>changelog.target</code></td><td>变更时的目标值； - 当事件类型是 updated 时，该字段就是变更后的值； - 当事件类型是 added 时，该字段就是增加的目标对象；</td></tr><tr><td><code>changelog.property</code></td><td>变更的属性，通常在事件类型是 updated 时携带此字段，详细结构可参考获取属性信息的 REST API</td></tr></tbody></table>

### 数据示例

以事件 `pce:pjm:workitem:created` 为例，当事件触发时完整的 `event` 参数如下：

```javascript
{
    "event_type": "pce:pjm:workitem:created",
    "self_generated": false,  
    "payload": {
        "data": {
            "id": "6a06d7954cd222a3dad91d45",
            "url": "https://open.pingcode.com/v1/project/work_items/6a06d7954cd222a3dad91d45",
            "project": {
                "id": "68c24404b2ae15e123c9e60c",
                "url": "https://open.pingcode.com/v1/project/projects/68c24404b2ae15e123c9e60c",
                "name": "test-hybrid",
                "type": "hybrid",
                "identifier": "H20020",
                "is_archived": 0,
                "is_deleted": 0
            },
            "identifier": "H20020-59",
            "title": "TEST",
            "type": "story",
            "start_at": null,
            "end_at": null,
            "parent_id": null,
            "short_id": "JoP34lQM",
            "html_url": "https://xxx.pingcode.com/pjm/workitems/JoP34lQM",
            "parent": null,
            "assignee": null,
            "state": {
                "id": "62d8f23c461c1ccf22123314",
                "url": "https://open.pingcode.com/v1/project/work_item_states/62d8f23c461c1ccf22123314",
                "name": "打开",
                "type": "pending",
                "color": "#56ABFB"
            },
            "priority": null,
            "board": {
                "id": "68c24404b2ae15e123c9e63b",
                "url": "https://open.pingcode.com/v1/project/projects/68c24404b2ae15e123c9e60c/boards/68c24404b2ae15e123c9e63b",
                "name": "默认看板",
                "work_item_types": [
                    "62d8f240461c1ccf221235d7",
                    "646b58929f3ece3cfda66c8c",
                    "636ca7d543350c333e49c3d0",
                    "62d8f23c461c1ccf22123309",
                    "636ca7f643350c333e49c3e1"
                ]
            },
            "entry": {
                "id": "68c24404b2ae15e123c9e635",
                "url": "https://open.pingcode.com/v1/project/projects/68c24404b2ae15e123c9e60c/boards/68c24404b2ae15e123c9e63b/entries/68c24404b2ae15e123c9e635",
                "name": "需求池"
            },
            "swimlane": {
                "id": "68c24404b2ae15e123c9e63a",
                "url": "https://open.pingcode.com/v1/project/projects/68c24404b2ae15e123c9e60c/boards/68c24404b2ae15e123c9e63b/swimlanes/68c24404b2ae15e123c9e63a",
                "name": "默认泳道"
            },
            "version": null,
            "versions": null,
            "sprint": null,
            "phase": null,
            "story_points": null,
            "estimated_workload": null,
            "remaining_workload": null,
            "description": null,
            "completed_at": null,
            "properties": {
                "risk": null,
                "backlog_type": null,
                "backlog_from": null,
                "schedule_mode": null,
                "dangechengyuan": null,
                "duogechengyuan": null,
                "workload": {
                    "reported_total": 0,
                    "remaining": 0,
                    "estimated": {
                        "duration": 0,
                        "estimated_at": 1778833301,
                        "estimated_by": null
                    }
                },
                "operation_time": 1778833301,
                "entry_status": 1,
                "entry_position": 16384
            },
            "tags": [],
            "participants": [
                {
                    "id": "c1ecd63e5af2461e810d402767e78fc8",
                    "url": "https://open.pingcode.com/v1/participants/c1ecd63e5af2461e810d402767e78fc8?principal_type=work_item&principal_id=6a06d7954cd222a3dad91d45",
                    "type": "user",
                    "user": {
                        "id": "c1ecd63e5af2461e810d402767e78fc8",
                        "url": "https://open.pingcode.com/v1/directory/users/c1ecd63e5af2461e810d402767e78fc8",
                        "name": "xxx",
                        "display_name": "xxx",
                        "avatar": null
                    }
                }
            ],
            "created_at": 1778833301,
            "created_by": {
                "id": "c1ecd63e5af2461e810d402767e78fc8",
                "url": "https://open.pingcode.com/v1/directory/users/c1ecd63e5af2461e810d402767e78fc8",
                "name": "xxx",
                "display_name": "xxx",
                "avatar": null
            },
            "updated_at": 1778833301,
            "updated_by": {
                "id": "c1ecd63e5af2461e810d402767e78fc8",
                "url": "https://open.pingcode.com/v1/directory/users/c1ecd63e5af2461e810d402767e78fc8",
                "name": "xxx",
                "display_name": "xxx",
                "avatar": null
            },
            "is_archived": 0,
            "is_deleted": 0
        }
    }
}
```

## 事件

目前 Nexus 平台支持的系统事件如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 36.72%" /><col style="width: 63.28%" /></colgroup><thead><tr><th>事件</th><th>说明</th></tr></thead><tbody><tr><td><a href="/reference/resource/events/global">全局事件</a></td><td>定义 PingCode 中全局系统事件</td></tr><tr><td><a href="/reference/resource/events/ship">产品管理</a></td><td>定义 PingCode 中产品管理系统事件</td></tr><tr><td><a href="/reference/resource/events/pjm">项目管理</a></td><td>定义 PingCode 中项目管理系统事件</td></tr><tr><td><a href="/reference/resource/events/wiki">知识管理</a></td><td>定义 PingCode 中知识管理系统事件</td></tr><tr><td><a href="/reference/resource/events/testhub">测试管理</a></td><td>定义 PingCode 中测试管理系统事件</td></tr></tbody></table>

## 作用域范围

订阅事件需要在应用 `manifest.yaml` 中申请相应的作用域范围，不同事件需要不同的作用域。如果权限不足，应用将无法接收到事件或获取完整数据。

```yaml
event:
  triggers:
    - key: system_trigger
      type: system
      events:
        - pce:ship:idea:created
        - pce:ship:idea:updated
      handler: 
        function: ship-idea-handler
permissions:
  scopes:
    - “pcp:read:ship:idea”
```

## 事件循环

在 `manifest.yml` 的触发器配置中，建议设置 `filter.ignoreSelf: true` 。这可以确保应用自身通过 APIs 触发的操作所产生的事件不会被自己再次订阅到，从而避免无限循环。

```yaml
event:
  triggers:
    - key: system_trigger
      type: system
      events:
        - pce:ship:idea:created
        - pce:ship:idea:updated
      handler: 
        function: ship-idea-handler
      filter:
        ignoreSelf: true
```

## 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.62%" /><col style="width: 66.38%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_EVENT_FUNCTION_NOT_FOUND</code></td><td><code>manifest</code> 中找不到该 <code>trigger</code> 声明的 <code>function</code> 。</td></tr></tbody></table>
