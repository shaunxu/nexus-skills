---
title: "notify"
lastUpdated: 2026-07-06T06:42:06.000Z
---

# notify

`notify` 使你的应用能够打开和 PingCode 风格一致的通知信息。

导入：

```typescript
import { notify } from "@pc-nexus/capabilities";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.88%" /><col style="width: 77.12%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>show</code></td><td>用于显示自定义配置的系统消息</td></tr><tr><td><code>success</code></td><td>用于显示「成功」类的系统消息</td></tr><tr><td><code>info</code></td><td>用于显示「消息」类的系统消息</td></tr><tr><td><code>warning</code></td><td>用于显示「警告」类的系统消息</td></tr><tr><td><code>error</code></td><td>用于显示「错误」类的系统消息</td></tr></tbody></table>

## show

`show` 方法可以显示自定义配置的系统消息。

### 函数签名

```typescript
function show(options: NotifyOptions): Promise<NotifyRef>;
  
interface NotifyOptions {
    type?: NotifyType;
    title?: string;
    description?: string;
    detail?: string | NotifyDetail;
    actions?: NotifyAction[];
    isAutoClose?: boolean;
}

interface NotifyRef {
    readonly close: () => void;
}

enum NotifyType {
    Success = "success",
    Error = "error",
    Warning = "warning",
    Info = "info",
}

interface NotifyDetail {
    link?: string;
    content?: string;
}

interface NotifyAction {
    text: string;
    icon?: string;
    onClick: (event?: Event) => void;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 28.67%" /><col style="width: 71.33%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>options</code></td><td>通知的配置选项，类型是 <code>NotifyOptions</code> （见下方详细说明）</td></tr></tbody></table>

`NotifyOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 28.67%" /><col style="width: 71.33%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>type</code></td><td>通知类型，可选值： <code>success</code> 、 <code>error</code> 、 <code>warning</code> 、 <code>info</code></td></tr><tr><td><code>title</code></td><td>通知标题</td></tr><tr><td><code>description</code></td><td>通知的简要描述</td></tr><tr><td><code>detail</code></td><td>通知的详细内容说明，用于补充描述信息，类型是 <code>string \| NotifyDetail</code> （见下方详细说明）</td></tr><tr><td><code>isAutoClose</code></td><td>是否自动关闭通知，默认为 <code>true</code> ，4.5 秒后关闭</td></tr><tr><td><code>actions</code></td><td>通知操作按钮数组，类型是 <code>NotifyAction</code> （见下方详细说明）</td></tr></tbody></table>

`NotifyDetail` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 28.53%" /><col style="width: 71.47%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>link</code></td><td>链接名称</td></tr><tr><td><code>content</code></td><td>详情描述内容</td></tr></tbody></table>

`NotifyAction` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.97%" /><col style="width: 72.03%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>text</code></td><td>按钮文本</td></tr><tr><td><code>icon</code></td><td>按钮图标</td></tr><tr><td><code>onClick</code></td><td>按钮点击事件回调</td></tr></tbody></table>

### 返回值

返回值类型为 `NotifyRef` ，表示通知实例的引用对象：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.59%" /><col style="width: 76.41%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>close</code></td><td>关闭当前通知。调用该方法后，将立即关闭对应的通知实例</td></tr></tbody></table>

### 示例 

```typescript
import { notify, NotifyOptions } from "@pc-nexus/capabilities";

const options: NotifyOptions = {
  type: NotifyType.success,
  title: 'Notify show success',
  description: 'Hello World',
  isAutoClose: false,
  detail: {
      link: 'View',
      content: 'View content',
  },
  actions: [
      {
        text: 'Close',
        icon: 'close',
        onClick: () => this.closeNotify(),
      },
      {
        text: 'Confirm',
        icon: 'check',
        onClick: () => this.closeNotify(),
      },
    ],
}

this.notifyRef = await notify.show(options)
```

## success

`success` 方法可以显示「成功」类的系统消息。

### 函数签名

```typescript
function success(options: Omit<NotifyOptions, "type">): Promise<NotifyRef>;
```

### 参数

类型为 `Omit<NotifyOptions, "type">` 同上方 `show` 方法参数。

### 返回值

类型为 `NotifyRef` ，同上方 `show` 方法返回值。

### 示例

```typescript
import { notify, NotifyOptions } from "@pc-nexus/capabilities";

const options: NotifyOptions = {
      title: 'Success title',
      description: 'Success description',
      detail: {
        link: 'View',
        content: 'View content',
      },
    };

const notifyRef = await notify.success(options);
```

## info

`info` 方法可以显示「信息」类的系统消息。

### 函数签名

```typescript
function info(options: Omit<NotifyOptions, "type">): Promise<NotifyRef>;
```

### 参数

类型为 `Omit<NotifyOptions, "type">` 同上方 `show` 方法参数。

### 返回值

类型为 `NotifyRef` ，同上方 `show` 方法返回值。

###  示例

```typescript
import { notify, NotifyOptions } from "@pc-nexus/capabilities";

const options: NotifyOptions = {
  title: 'Info title',
  description: 'Info description',
  detail: {
    link: 'View',
    content: 'View content',
  },
};

const notifyRef = await notify.info(options);
```

## warning

`warning` 方法可以显示「警告」类的系统消息。

### 函数签名

```typescript
function warning(options: Omit<NotifyOptions, "type">): Promise<NotifyRef>;
```

### 参数

类型为 `Omit<NotifyOptions, "type">` 同上方 `show` 方法参数。

### 返回值

类型为 `NotifyRef` ，同上方 `show` 方法返回值。

### 示例

```typescript
import { notify, NotifyOptions } from "@pc-nexus/capabilities";

const options: NotifyOptions = {
  title: 'Warning title',
  description: 'Warning description',
  detail: {
    link: 'View',
    content: 'View content',
  },
};

const notifyRef = await notify.warning(options);
```

## error

`error` 方法可以显示「错误」类的系统消息。

### 函数签名

```typescript
function error(options: Omit<NotifyOptions, "type">): Promise<NotifyRef>;
```

### 参数

类型为 `Omit<NotifyOptions, "type">` 同上方 `show` 方法参数。

### 返回值

类型为 `NotifyRef` ，同上方 `show` 方法返回值。

### 示例

```typescript
import { notify, NotifyOptions } from "@pc-nexus/capabilities";

const options: NotifyOptions = {
  title: 'Error title',
  description: 'Error description',
  detail: {
    link: 'View',
    content: 'View content',
  },
};

const notifyRef = await notify.error(options);
```
