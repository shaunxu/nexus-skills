---
title: "dialog"
lastUpdated: 2026-07-06T03:35:17.000Z
---

# dialog

`dialog` 使你的应用能够打开包含指定资源的模态框。

导入：

```typescript
import { dialog } from "@pc-nexus/bridge";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 41.81%" /><col style="width: 58.19%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>open</code></td><td>打开包含指定资源的模态框</td></tr><tr><td><code>confirm</code></td><td>打开确认弹窗</td></tr></tbody></table>

## open

### **函数签名**

```typescript
function open<T>(options: DialogOpenOptions): Promise<DialogRef<T>>;

export interface DialogOpenOptions {
    resource: string;
    size?: ViewportSize;
    context?: Record<string, unknown>;
    backdropClosable?: boolean;
    onClose?: (payload?: unknown) => void;
    title?: string;
    icon?: string;
}

export interface DialogRef<T = unknown> {
   readonly close: (payload?: T) => void;
}

type ViewportSize = "small" | "medium" | "large" | "xlarge" | "max" | "fullscreen";
```

### **参数**

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>options</code></td><td>打开模态框传入的配置项（见下方详细说明）</td></tr></tbody></table>

`DialogOpenOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.31%" /><col style="width: 64.69%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>resource</code></td><td style="text-align: left">在模态框中打开的静态资源 key</td></tr><tr><td style="text-align: left"><code>size</code></td><td style="text-align: left">模态框大小，ViewportSize 可选值为： • small • medium • large • xlarge • max • fullscreen</td></tr><tr><td style="text-align: left"><code>context</code></td><td style="text-align: left">可添加到模态资源上下文中的自定义模态框上下文对象，会以模态框资源 <code>view.getContext()</code>  返回对象的  <code>extension.data.dialog</code>  返回</td></tr><tr><td style="text-align: left"><code>backdropClosable</code></td><td style="text-align: left">遮罩是否可关闭，默认为 <code>true</code> 。当设置为 <code>true</code> 时，点击遮罩或按 ESC 可关闭模态框，否则只能显示调用 close 关闭</td></tr><tr><td style="text-align: left"><code>onClose</code></td><td style="text-align: left">模态框关闭时的回调函数，接受可选的 <code>payload</code> 参数，在模态框资源内调用 <code>view.close(payload)</code> 时传入</td></tr><tr><td style="text-align: left"><code>title</code></td><td style="text-align: left">模态框头部标题，当标题有值时，模态框会显示头部组件，头部组件的标题为 title</td></tr><tr><td style="text-align: left"><code>icon</code></td><td style="text-align: left">模态框头部标题图标，只有 title 设置了值才会起作用</td></tr></tbody></table>

### 返回值

返回模态框的引用 DialogRef<T = unknown>

`DialogRef` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>close</code></td><td>关闭当前模态框</td></tr></tbody></table>

### **示例**

```typescript
import { dialog } from "@pc-nexus/bridge";

const dialogRef = await dialog.open({
  resource: 'dialog-resource',
  size: 'max',
  context: { message: 'from dialog context' },
  title: 'Dialog Title',
  icon: 'icons/bell-fill:#ff4d4f',
});
```

`dialog-resource` 示例：

```typescript
import { view } from '@pc-nexus/bridge';

const isDialog = await view.isDialog();

if (isDialog) {
  const context = await view.getContext();
  const message = context.extension.dialog.message;
  await view.close();
}
```

## confirm

### 函数签名

```typescript
function confirm<T>(options: DialogConfirmOptions): Promise<void>;
  
interface DialogConfirmOptions {
    content: string;
    title?: string;
    operationType?: "danger" | "primary";
    onConfirm: () => Promise<void>;
    onCancel?: () => void;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.03%" /><col style="width: 64.97%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>options</code></td><td>打开确认框传入的配置项（见下方详细说明）</td></tr></tbody></table>

`DialogConfirmOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 36.16%" /><col style="width: 63.84%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>title</code></td><td style="text-align: left">标题</td></tr><tr><td style="text-align: left"><code>content</code></td><td style="text-align: left">确认框提示内容</td></tr><tr><td style="text-align: left"><code>operationType</code></td><td style="text-align: left">确认按钮类型， <code>primary</code>  展示主色， <code>danger</code> 显示红色，默认为  <code>danger</code></td></tr><tr><td style="text-align: left"><code>onConfirm</code></td><td style="text-align: left">确认回调函数，点击确认后调用，异步函数结束后自动关闭确认框</td></tr><tr><td style="text-align: left"><code>onCancel</code></td><td style="text-align: left">取消回调函数，点击取消后调用</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { dialog } from '@pc-nexus/bridge';

dialog.confirm({
  title: 'Confirm',
  content: 'Are you sure you want to confirm?',
  onConfirm: async () => {
    console.log('onConfirm callback', payload);
  }
});
```
