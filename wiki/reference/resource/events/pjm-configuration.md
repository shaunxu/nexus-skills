---
title: "配置中心"
lastUpdated: 2026-07-15T13:49:15.000Z
---

# 配置中心

本文档定义项目管理中的配置事件。

|事件|描述|
|---|---|
|`pce:pjm:configuration:workitemtype:created`|创建工作项类型|
|`pce:pjm:configuration:workitemtype:updated`|更新工作项类型|
|`pce:pjm:configuration:workitemtype:deleted`|删除工作项类型|
|`pce:pjm:configuration:field:created`|创建工作项属性|
|`pce:pjm:configuration:field:updated`|更新工作项属性|
|`pce:pjm:configuration:field:deleted`|删除工作项属性|

## 创建工作项类型

创建新的工作项类型时，会触发 `pce:pjm:configuration:workitemtype:created` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:configuration
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项类型信息</td></tr></tbody></table>

## 创建工作项属性

创建新的工作项属性时，会触发 `pce:pjm:configuration:field:created` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:configuration
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项属性信息</td></tr></tbody></table>
