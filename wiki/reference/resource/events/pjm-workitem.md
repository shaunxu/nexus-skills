---
title: "工作项"
lastUpdated: 2026-07-15T13:48:43.000Z
---

# 工作项

本文档定义项目管理中的工作项事件。

|事件|描述|
|---|---|
|`pce:pjm:workitem:created`|创建工作项|
|`pce:pjm:workitem:updated`|更新工作项|
|`pce:pjm:workitem:viewed`|查看工作项详情|
|`pce:pjm:workitem:deleted`|删除工作项|
|`pce:pjm:workitem:link:added`|工作项增加关联|
|`pce:pjm:workitem:link:removed`|工作项移除关联|
|`pce:pjm:workitem:comment:created`|新增工作项评论|
|`pce:pjm:workitem:comment:updated`|更新工作项评论|
|`pce:pjm:workitem:comment:deleted`|删除工作项评论|

## 创建工作项

创建工作项时，会触发 `pce:pjm:workitem:created` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项信息</td></tr></tbody></table>

## 更新工作项

更新工作项时，会触发 `pce:pjm:workitem:updated` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
- pcp:read:pjm:configuration
- pcp:read:pjm:sprint
- pcp:read:pjm:release
- pcp:read:pjm:board
- pcp:read:pjm:board
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项信息</td></tr><tr><td><code>changlog</code></td><td>变更日志</td></tr><tr><td><code>changlog.origin</code></td><td>变更前的值，变更属性的类型决定了值的类型</td></tr><tr><td><code>changlog.target</code></td><td>变更后的值，变更属性的类型决定了值的类型</td></tr><tr><td><code>changlog.property</code></td><td>变更的属性</td></tr></tbody></table>

## 查看工作项详情

查看工作项时，会触发 `pce:pjm:workitem:viewed` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项信息</td></tr></tbody></table>

## 删除工作项

删除工作项时，会触发 `pce:pjm:workitem:deleted` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项信息</td></tr></tbody></table>

## 工作项增加关联

在工作项上增加关联时，会触发 `pce:pjm:workitem:deleted` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项信息</td></tr><tr><td><code>changelog</code></td><td>变更日志</td></tr><tr><td><code>changelog.target</code></td><td>关联信息</td></tr><tr><td><code>source</code></td><td>如果是系统触发的关联动作，值为 <code>system</code></td></tr></tbody></table>

## 工作项移除关联

在工作项上移除关联时，会触发 `pce:pjm:workitem:link:removed` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项信息</td></tr><tr><td><code>changelog</code></td><td>变更日志</td></tr><tr><td><code>changelog.origin</code></td><td>关联信息</td></tr><tr><td><code>source</code></td><td>如果是系统触发的关联动作，值为 <code>system</code></td></tr></tbody></table>

## 新增工作项评论

在工作项上新增评论时，会触发 `pce:pjm:workitem:comment:created` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td><code>data</code></td><td>工作项信息</td></tr><tr><td><code>changelog</code></td><td>变更日志</td></tr><tr><td><code>changelog.target</code></td><td>工作项评论</td></tr></tbody></table>

## 更新工作项评论

在工作项上更新评论时，会触发 `pce:pjm:workitem:comment:created` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td></td><td></td></tr></tbody></table>

## 删除工作项评论

在工作项上删除评论时，会触发 `pce:pjm:workitem:comment:deleted` 事件。

### 作用域

订阅此事件需要配置如下作用域：

```yaml
- pcp:read:pjm:workitem
```

### 数据

`payload` 中提供的数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>数据</th><th>描述</th></tr></thead><tbody><tr><td></td><td></td></tr></tbody></table>
