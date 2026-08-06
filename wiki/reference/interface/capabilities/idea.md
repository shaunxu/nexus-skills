---
title: "idea"
lastUpdated: 2026-07-06T03:49:14.000Z
---

# idea

`idea` 允许你的应用能够直接调用创建产品需求、打开产品需求详情。

导入：

```typescript
import { idea } from '@pc-nexus/capabilities';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 41.67%" /><col style="width: 58.33%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>openCreate</code></td><td>打开产品需求创建弹窗</td></tr><tr><td><code>openDetail</code></td><td>打开产品需求详情弹窗</td></tr></tbody></table>

## openCreate

`openCreate` 打开产品需求创建弹窗，根据传入的默认值展示数据。

### 函数签名

```typescript
function openCreate: (options: IdeaOpenCreateOptions): Promise<void>;

export interface IdeaOpenCreateOptions {
    defaultValues?: {
        title?: string;
        product_id?: string;
    };
    onSuccess?: (payload: Idea) => void;
}

export interface Idea {
    id: string;
    short_id: string;
    identifier: string;
    title: string;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>options</code></td><td style="text-align: left">打开产品需求创建弹窗的配置项（见下方详细说明）</td></tr></tbody></table>

`IdeaOpenCreateOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 40.4%" /><col style="width: 59.6%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>defaultValues</code></td><td style="text-align: left">创建产品需求设置一些属性默认值</td></tr><tr><td style="text-align: left"><code>onSuccess</code></td><td style="text-align: left">产品需求创建成功后回调函数</td></tr></tbody></table>

`onSuccess`  类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 40.54%" /><col style="width: 59.46%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>id</code></td><td style="text-align: left">产品需求的 id</td></tr><tr><td style="text-align: left"><code>title</code></td><td style="text-align: left">产品需求的标题</td></tr><tr><td style="text-align: left"><code>short_id</code></td><td style="text-align: left">产品需求的短 id</td></tr><tr><td style="text-align: left"><code>identifier</code></td><td style="text-align: left">产品需求的编号</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { idea } from '@pc-nexus/capabilities';

idea.openCreate({
    defaultValues: {
      title: '新需求',
    },
    onSuccess: (payload) => {
      console.log('create idea success', payload);
    },
});
```

## openDetail

`openDetail` 打开产品需求详情弹窗。

### 函数签名

```typescript
function openDetail: (identifier: string): Promise<void>
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 43.79%" /><col style="width: 56.21%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>identifier</code></td><td>产品需求的编号或产品需求 id</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { idea } from '@pc-nexus/capabilities';

idea.openDetail('66da99b3f5075970efbe7492');
```
