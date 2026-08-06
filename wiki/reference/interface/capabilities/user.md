---
title: "user"
lastUpdated: 2026-07-03T08:40:25.000Z
---

# user

`user` 支持直接使用选择成员组件。

导入：

```typescript
import { user } from '@pc-nexus/capabilities';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.06%" /><col style="width: 67.94%" /></colgroup><thead><tr><th><strong>API</strong></th><th><strong> 描述</strong></th></tr></thead><tbody><tr><td><code>openDialog</code></td><td>打开模态框选人组件</td></tr><tr><td><code>openPopover</code></td><td>弹窗 popover 选人组件</td></tr></tbody></table>

## openDialog

打开模态框选择成员

### 函数签名

```typescript
function openDialog(options: UserOpenDialogOptions): Promise<UserOpenDialogRef>;

export interface UserOpenDialogOptions {
    title?: string;
    selection?: string[];
    onConfirm: (ids?: string[], users?: UserInfo[]) => Promise<void>;
    onClose?: () => void;
}

export interface UserOpenDialogRef {
    readonly close: () => void;
}

export interface UserInfo {
    id: string;
    display_name?: string;
    name?: string;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.49%" /><col style="width: 67.51%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>options</code></td><td>打开模态框选择成员传入的配置项（见下方详细说明）</td></tr></tbody></table>

`UserOpenDialogOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.49%" /><col style="width: 67.51%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>title</code></td><td style="text-align: left">打开的弹框标题，默认为：“选择成员”</td></tr><tr><td style="text-align: left"><code>selection</code></td><td style="text-align: left">已选择的成员集合</td></tr><tr><td style="text-align: left"><code>onConfirm</code></td><td style="text-align: left">选择完成成员后的回调函数</td></tr><tr><td style="text-align: left"><code>onClose</code></td><td style="text-align: left">选择成员弹框关闭后的回调函数</td></tr></tbody></table>

 `onConfirm` 函数参数如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.49%" /><col style="width: 67.51%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>ids</code></td><td>已选择的成员 id 集合</td></tr><tr><td><code>users</code></td><td>已选择的成员信息集合（提供字段 id、 name 、display_name)</td></tr></tbody></table>

### 返回值

返回值类型为 `UserOpenDialogRef` ，类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.49%" /><col style="width: 67.51%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>close</code></td><td>关闭当前选人组件</td></tr></tbody></table>

### 示例

```typescript
import { user, UserInfo } from '@pc-nexus/capabilities';

user.openDialog({
      selection: [],
      title: '选择企业成员',
      onConfirm: async (ids?: string[], users?: UserInfo[]) => {
        console.log('selected ids:', ids);
        console.log('selected users:',users);
      },
      onClose: () => {
        console.log('onClose called');
      },
});
```

## openPopover

打开 popover 下拉选择成员

### 函数签名

```typescript
function openPopover(options: UserOpenPopoverOptions): Promise<UserOpenPopoverRef>;

export type UserOpenPopoverOptions = MultipleUserOpenPopoverOptions | SingleUserOpenPopoverOptions;

export interface UserOpenPopoverRef {
    readonly close: () => void;
}

export interface UserInfo {
    id: string;
    display_name?: string;
    name?: string;
}

interface MultipleUserOpenPopoverOptions extends SelectUserPopBaseOptions {
    multiple: true;
    selection?: string[];
    onConfirm: (ids?: string[], users?: UserInfo[]) => Promise<void>;
    onClose?: () => void;
}

interface SingleUserOpenPopoverOptions extends SelectUserPopBaseOptions {
    multiple?: false;
    selection?: string;
    onConfirm: (id?: string, user?: UserInfo) => Promise<void>;
    onClose?: () => void;
}

interface SelectUserPopBaseOptions {
    origin: HTMLElement;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.06%" /><col style="width: 67.94%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>options</code></td><td>打开 popover 选择成员传入的配置项（见下方详细说明）</td></tr></tbody></table>

`UserOpenPopoverOptions` 有两种模式：

`MultipleUserOpenPopoverOptions` 和 `SingleUserOpenPopoverOptions` ，类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.78%" /><col style="width: 68.22%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>origin</code></td><td style="text-align: left">锚点元素，用于计算弹出悬浮层位置</td></tr><tr><td style="text-align: left"><code>multiple</code></td><td style="text-align: left">是否支持多选，默认不支持</td></tr><tr><td style="text-align: left"><code>selection</code></td><td style="text-align: left">已选择的成员集合</td></tr><tr><td style="text-align: left"><code>onConfirm</code></td><td style="text-align: left">选择完成成员后的回调函数</td></tr><tr><td style="text-align: left"><code>onClose</code></td><td style="text-align: left">选择成员 popover 框关闭后的回调函数</td></tr></tbody></table>

`MultipleUserOpenPopoverOptions` 下 `onConfirm` 函数参数如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.06%" /><col style="width: 67.94%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>ids</code></td><td>已选择的成员 id 集合</td></tr><tr><td><code>users</code></td><td>已选择的成员信息集合（提供字段 id、 name 、display_name)</td></tr></tbody></table>

`SingleUserOpenPopoverOptions` 下 `onConfirm` 函数参数如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.06%" /><col style="width: 67.94%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>已选择的成员 id</td></tr><tr><td><code>user</code></td><td>已选择的成员信息（提供字段 id、 name 、display_name)</td></tr></tbody></table>

### 返回值

返回值类型为 `UserOpenPopoverRef` ，类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.49%" /><col style="width: 67.51%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>close</code></td><td>关闭当前选人组件</td></tr></tbody></table>

### 示例

```typescript
import { user, UserInfo, UserOpenPopoverRef } from '@pc-nexus/capabilities';

// 单选
let popRef: UserOpenPopoverRef;
popRef = await user.openPopover({
   origin: event.currentTarget as HTMLElement,
   selection: '',
   onConfirm: async (id?: string, user?: UserInfo) => {
       console.log('selected id:', id);
       console.log('selected user:', user);
       popRef.close();
   },
   onClose: () => {
       console.log('onClose called');
   },
});


// 多选
user.openPopover({
   origin: event.currentTarget as HTMLElement,
   multiple: true,
   selection: [],
   onConfirm: async (ids?: string[], users?: UserInfo[]) => {
       console.log('selected ids:', ids);
       console.log('selected users:', users);
   },
   onClose: () => {
       console.log('onClose called');
   },
});
```
