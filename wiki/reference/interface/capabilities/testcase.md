---
title: "testcase"
lastUpdated: 2026-07-06T03:50:28.000Z
---

# testcase

`testcase` 允许你的应用能够直接调用创建测试用例、打开测试用例详情。

导入：

```typescript
import { testcase } from '@pc-nexus/capabilities';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 41.1%" /><col style="width: 58.9%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>openCreate</code></td><td>打开测试用例创建弹窗</td></tr><tr><td><code>openDetail</code></td><td>打开测试用例详情弹窗</td></tr></tbody></table>

## openCreate

`openCreate` 打开测试用例创建弹窗，根据传入的默认值展示数据。

### 函数签名

```typescript
function openCreate: (options: TestcaseOpenCreateOptions): Promise<void>;

export interface TestcaseOpenCreateOptions {
    defaultValues?: {
        title?: string;
        library_id?: string;
    };
    onSuccess?: (payload: Testcase) => void;
}
  
export interface Testcase {
    id: string;
    short_id: string;
    identifier: string;
    title: string;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>options</code></td><td style="text-align: left">打开测试用例创建弹窗的配置项（见下方详细说明）</td></tr></tbody></table>

`TestcaseOpenCreateOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 40.96%" /><col style="width: 59.04%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>defaultValues</code></td><td style="text-align: left">创建测试用例设置一些属性默认值</td></tr><tr><td style="text-align: left"><code>onSuccess</code></td><td style="text-align: left">测试用例创建成功后回调函数</td></tr></tbody></table>

`onSuccess` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 41.24%" /><col style="width: 58.76%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>id</code></td><td style="text-align: left">测试用例的 id</td></tr><tr><td style="text-align: left"><code>title</code></td><td style="text-align: left">测试用例的标题</td></tr><tr><td style="text-align: left"><code>short_id</code></td><td style="text-align: left">测试用例的短 id</td></tr><tr><td style="text-align: left"><code>identifier</code></td><td style="text-align: left">测试用例的编号</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { testcase } from '@pc-nexus/capabilities';

testcase.openCreate({
    defaultValues: {
      title: '新用例',
    },
    onSuccess: (payload) => {
      console.log('create test case success', payload);
    },
});
```

## openDetail

`openDetail` 打开测试用例详情弹窗。

### 函数签名

```typescript
function openDetail: (identifier: string): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 42.09%" /><col style="width: 57.91%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>identifier</code></td><td>测试用例的编号或测试用例 id</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { testcase } from '@pc-nexus/capabilities';

testcase.openDetail('69df016092c2c86322c1890c');
```
