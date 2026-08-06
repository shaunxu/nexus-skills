---
title: "ticket"
lastUpdated: 2026-07-06T03:49:59.000Z
---

# ticket

`ticket` 允许你的应用能够直接调用创建工单、打开工单详情。

导入：

```typescript
import { ticket } from '@pc-nexus/capabilities';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.94%" /><col style="width: 57.06%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>openCreate</code></td><td>打开工单创建弹窗</td></tr><tr><td><code>openDetail</code></td><td>打开工单详情弹窗</td></tr></tbody></table>

## openCreate

`openCreate` 打开工单创建弹窗，根据传入的默认值展示数据。

### 函数签名

```typescript
function openCreate: (options: TicketOpenCreateOptions): Promise<void>;

export interface TicketOpenCreateOptions {
    defaultValues?: {
        title?: string;
        product_id?: string;
    };
    onSuccess?: (payload: Ticket) => void;
}

export interface Ticket {
    id: string;
    short_id: string;
    identifier: string;
    title: string;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>options</code></td><td style="text-align: left">打开工单创建弹窗的配置项（见下方详细说明）</td></tr></tbody></table>

`TicketOpenCreateOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 39.55%" /><col style="width: 60.45%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>defaultValues</code></td><td style="text-align: left">创建工单设置一些属性默认值</td></tr><tr><td style="text-align: left"><code>onSuccess</code></td><td style="text-align: left">工单创建成功后回调函数</td></tr></tbody></table>

`onSuccess`  类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 39.83%" /><col style="width: 60.17%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>id</code></td><td style="text-align: left">工单的 id</td></tr><tr><td style="text-align: left"><code>title</code></td><td style="text-align: left">工单的标题</td></tr><tr><td style="text-align: left"><code>short_id</code></td><td style="text-align: left">工单的短 id</td></tr><tr><td style="text-align: left"><code>identifier</code></td><td style="text-align: left">工单的编号</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { ticket } from '@pc-nexus/capabilities';

ticket.openCreate({
    defaultValues: {
      title: '新工单',
    },
    onSuccess: (payload) => {
      console.log('create ticket success', payload);
    },
});
```

## openDetail

`openDetail` 打开工单详情弹窗。

### 函数签名

```typescript
function openDetail: (identifier: string): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.8%" /><col style="width: 57.2%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>identifier</code></td><td>工单的编号或工单 id</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { ticket } from '@pc-nexus/capabilities';

ticket.openDetail('683eaaa1cbb4a4e340e2e92a');
```
