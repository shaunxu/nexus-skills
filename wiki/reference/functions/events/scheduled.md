---
title: "scheduled"
lastUpdated: 2026-07-27T07:40:19.000Z
---

# scheduled

本文档介绍如何在应用中配置定时触发器。 `scheduled` 类型的触发器会按照指定的时间间隔周期性地调用一个函数或远程服务端点。触发器首次执行时间基于应用安装时刻计算，后续按配置的间隔持续执行。

## 配置

配置示例：

```yaml
event:
  triggers:
    - key: scheduled-trigger
      type: scheduled
      handler:
        function: scheduled-handler
      interval: hour
functions:
  - key: scheduled-handler
    handler: scheduled.handler
```

每个触发器包含的属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.33%" /><col style="width: 15.49%" /><col style="width: 55.18%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>handler</code></td><td>是</td><td>声明处理该触发器的函数或 endpoint</td></tr><tr><td><code>interval</code></td><td>是</td><td>触发间隔，支持 <code>tenMinute</code> 、 <code>hour</code> 、 <code>day</code> 、 <code>week</code></td></tr><tr><td><code>timeout</code></td><td>否</td><td>函数超时时间（秒），最小值为 <code>60</code></td></tr></tbody></table>

### handler

`handler` 声明定时触发器调用的处理单元， `function` 与 `endpoint` 二选一。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.57%" /><col style="width: 68.43%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>function</code></td><td>引用 <code>functions</code> 中定义的函数 key</td></tr><tr><td><code>endpoint</code></td><td>引用 <code>endpoints</code> 中定义的 endpoint key（用于 Nexus Remote）</td></tr></tbody></table>

使用函数：

```yaml
events:
  triggers:
    - key: my-scheduled-trigger
      type: scheduled
      handler:
        function: my-scheduled-function
      interval: hour
```

使用 endpoint ：

```yaml
events:
  triggers:
    - key: remote-scheduled-trigger
      type: scheduled
      handler:
        endpoint: remote-scheduled-endpoint
      interval: hour
```

### interval

`interval` 声明触发器的执行频率。

|值|描述|
|---|---|
|`tenMinute`|每 10 分钟|
|`hour`|每小时|
|`day`|每天|
|`week`|每周|

## 处理函数

当定时触发时，会调用你定义的处理函数。

### **示例**

```typescript
import type { ScheduledEventHandler } from "@pc-nexus/event";

export const handler: ScheduledEventHandler = async (context, event) => {
    console.log(JSON.stringify(context));
    console.log(JSON.stringify(event));
};
```

### 参数

处理函数接收 `context` 和 `event` 两个参数。

#### **context**

`context` 为 `NexusAppContext` 类型，包含应用运行时的上下文信息，详情请参考 [app](/reference/functions/core/app) ，获取触发的事件信息可以从 `context` 中获取 如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.24%" /><col style="width: 70.76%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>event.trigger.key</code></td><td>触发器在 <code>manifest</code> 中定义的 <code>key</code></td></tr><tr><td><code>event.trigger.type</code></td><td>触发器类型，值为 <code>scheduled</code></td></tr></tbody></table>

#### **event**

定时触发器的 `payload` 为空对象 `{}` , `event_type` 值为 `undefined` 。

## 注意事项

- **执行时机** ：首次触发时间由应用安装时刻和 `interval` 共同计算得出，重新部署后所有定时触发器会被重置。
- **至少执行一次** ：系统保证 at-least-once 语义，服务重启后可能会对同一任务重复触发，处理函数应保证幂等。
- **无用户上下文** ： `context.user` 始终为 `undefined` ，触发器不代表任何登录用户发起。
- **错误不重试** ：函数执行失败不会自动重试，下一次触发仍按正常间隔执行。

::: tip
如需更多自由的触发方式，比如 crontab支持，建议创建 webtrigger 从而通过外部触发来实现。
:::

## 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.62%" /><col style="width: 66.38%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_EVENT_SCHEDULE_UNIT_INVALID</code></td><td>调度时间单位不合法（仅支持 <code>minute</code> / <code>hour</code> / <code>day</code> / <code>week</code> ）。</td></tr><tr><td><code>ERR_EVENT_SCHEDULE_INTERVAL_INVALID</code></td><td>调度间隔不合法（仅支持 <code>tenMinute</code> / <code>hour</code> / <code>day</code> / <code>week</code> ）。</td></tr><tr><td><code>ERR_EVENT_FUNCTION_NOT_FOUND</code></td><td><code>manifest</code> 中找不到该 <code>trigger</code> 声明的 <code>function</code> 。</td></tr></tbody></table>
