---
title: "Registries"
lastUpdated: 2026-08-04T05:51:05.000Z
---

# Registries

`registries` 属性用于定义应用声明的事件列表，在此处声明的事件可以被其他应用订阅处理。

## 示例

简单配置示例：

```yaml
event:
  registries:
    - key: event-key
      name: Event name
      allowedRecipients:
        - app:466d303d-a2c4-4ec4-ad7c-5435be94583b
```

## 属性

`registries` 中声明的事件需要指定以下三个属性：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.96%" /><col style="width: 16.54%" /><col style="width: 56.5%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>定义事件的唯一标识</td></tr><tr><td><code>name</code></td><td>Y</td><td>定义事件的名称</td></tr><tr><td><code>allowedRecipients</code></td><td></td><td>定义允许哪些应用可以订阅该事件，使用如下格式通过应用唯一标识指定： <code>app:466d303d-a2c4-4ec4-ad7c-5435be94583b</code></td></tr></tbody></table>

## 限制接收者

默认情况下，仅允许发布应用接收该应用事件，允许的接收者列表可通过 `allowedRecipients` 属性进行控制。

若允许任何接收者接收事件，可在值列表中添加特殊的*通配符：

```yaml
event:
  registries:
     - key: event-key
       name: Event name
       allowedRecipients: ['*']
```

也可以通过应用的唯一标识，仅允许特定的一组应用接收事件：

```yaml
event:
  registries:
     - key: event-key
       name: Event name
       allowedRecipients:
          - app:466d303d-a2c4-4ec4-ad7c-5435be94583b
```
