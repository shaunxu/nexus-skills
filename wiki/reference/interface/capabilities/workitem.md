---
title: "workitem"
lastUpdated: 2026-07-06T03:48:17.000Z
---

# workitem

`workitem` 允许你的应用能够直接调用创建工作项、打开工作项详情。

导入：

```typescript
import { workitem } from '@pc-nexus/capabilities';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 44.21%" /><col style="width: 55.79%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>openCreate</code></td><td>打开工作项创建弹窗</td></tr><tr><td><code>openDetail</code></td><td>打开工作项详情弹窗</td></tr></tbody></table>

## openCreate

`openCreate` 打开工作项创建弹窗，根据传入的默认值展示数据。

### 函数签名

```typescript
function openCreate: (options: WorkitemOpenCreateOptions): Promise<void>;
  
export interface WorkitemOpenCreateOptions {
  defaultValues?: {
    title?: string;
    project_id?: string;
  };
  onSuccess?: (payload: Workitem) => void;
}

export interface Workitem {
  id: string;
  short_id: string;
  identifier: string;
  title: string;
  type_group: WorkitemTypeGroup;
  type_id: string;
}

export enum WorkitemTypeGroup {
  Requirement = 1,
  Task = 2,
  Bug = 3,
  Issue = 4,
  Plan = 5,
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>options</code></td><td style="text-align: left">打开工作项创建弹窗的配置项（见下方详细说明）</td></tr></tbody></table>

`WorkitemOpenCreateOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>defaultValues</code></td><td style="text-align: left">创建工作项时设置的部分属性默认值</td></tr><tr><td style="text-align: left"><code>onSuccess</code></td><td style="text-align: left">工作项创建成功后的回调函数</td></tr></tbody></table>

`onSuccess` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>id</code></td><td style="text-align: left">工作项 id</td></tr><tr><td style="text-align: left"><code>title</code></td><td style="text-align: left">工作项标题</td></tr><tr><td style="text-align: left"><code>short_id</code></td><td style="text-align: left">工作项短 id</td></tr><tr><td style="text-align: left"><code>identifier</code></td><td style="text-align: left">工作项编号</td></tr><tr><td style="text-align: left"><code>type_group</code></td><td style="text-align: left">工作项类型</td></tr><tr><td style="text-align: left"><code>type_id</code></td><td style="text-align: left">工作项类型 id</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { workitem } from '@pc-nexus/capabilities';

workitem.openCreate({
    defaultValues: {
      title: '新工作项',
    },
    onSuccess: (payload) => {
      console.log('create workitem success', payload);
    },
});
```

## openDetail

`openDetail` 打开工作项详情弹窗。

### 函数签名

```typescript
function openDetail: (identifier: string): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>identifier</code></td><td style="text-align: left">工作项的编号或工作项 id</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { workitem } from '@pc-nexus/capabilities';

workitem.openDetail('CSKBL-21');
```
