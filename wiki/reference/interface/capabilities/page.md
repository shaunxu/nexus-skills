---
title: "page"
lastUpdated: 2026-07-06T05:48:57.000Z
---

# page

`page` 允许你的应用能够直接调用创建页面、打开页面详情。

导入：

```typescript
import { page } from '@pc-nexus/capabilities';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>openCreate</code></td><td>打开页面创建弹窗</td></tr><tr><td><code>openDetail</code></td><td>打开页面详情弹窗</td></tr></tbody></table>

## openCreate

`openCreate` 打开页面创建弹窗，根据传入的默认值展示数据。

### 函数签名

```typescript
function openCreate: (options?: PageOpenCreateOptions): Promise<void>;

export interface PageOpenCreateOptions {
    onSuccess?: (payload: Page) => void;
}

export interface Page {
    id: string;
    short_id: string;
    name: string;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>options</code></td><td style="text-align: left">打开页面创建弹窗的配置项（见下方详细说明）</td></tr></tbody></table>

`PageOpenCreateOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 40.4%" /><col style="width: 59.6%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>onSuccess</code></td><td style="text-align: left">页面创建成功后回调函数</td></tr></tbody></table>

`onSuccess` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 38.7%" /><col style="width: 61.3%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>id</code></td><td style="text-align: left">页面 的 id</td></tr><tr><td style="text-align: left"><code>name</code></td><td style="text-align: left">页面 的 标题</td></tr><tr><td style="text-align: left"><code>short_id</code></td><td style="text-align: left">页面 的 短 id</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { page } from '@pc-nexus/capabilities';

page.openCreate({
    onSuccess: (payload) => {
      console.log('create page success', payload);
    }
});
```

## openDetail

`openDetail` 打开页面详情弹窗。

### 函数签名

```typescript
function openDetail: (identifier: string): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 40.11%" /><col style="width: 59.89%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>identifier</code></td><td>页面 id 或页面短 id</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { page } from '@pc-nexus/capabilities';

page.openDetail('6502db48a32bb45fc0d41b8d');
```
