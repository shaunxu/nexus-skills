---
title: "view"
lastUpdated: 2026-07-20T08:05:54.000Z
---

# view

`view` 视图对象指向当前加载资源的上下文。

导入：

```typescript
import { view } from "@pc-nexus/bridge";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>getContext</code></td><td>在扩展应用中获取上下文信息</td></tr><tr><td><code>setWindowTitle</code></td><td>在扩展应用中更改当前 document 的标题</td></tr><tr><td><code>refresh</code></td><td>再次刷新父页面的数据，而无需进行整个页面加载</td></tr><tr><td><code>close</code></td><td>关闭当前视图</td></tr><tr><td><code>onClose</code></td><td>注册一个回调函数，当 Dialog 关闭时执行该回调函数</td></tr><tr><td><code>isDialog</code></td><td>判断当前资源是否在 Dialog 中运行</td></tr><tr><td><code>createHistory</code></td><td>扩展应用能够操作当前页面 URL，以便在全页面应用内进行路由</td></tr><tr><td><code>submit</code></td><td>在上下文配置视图上提交表单</td></tr><tr><td><code>emitReadyEvent</code></td><td>通知 Nexus 当前扩展的业务内容已加载完成</td></tr></tbody></table>

## getContext

 `getContext` 方法可以让你在扩展应用中获取上下文信息。

### **函数签名**

```typescript
function getContext(): Promise<NexusAppContext>;

export type ExtensionData = Record<string, any>;

export interface NexusAppContext<T = ExtensionData> {
    app: {
        id: string;
        version: string;
    };
    environment: {
        id: string;
        type: NexusAppEnvironment;
    };
    team: {
        id: string;
        url: string;
        locale: SupportedLocaleCode;
        timezone: string;
    };
    installation: {
        id: string;
    };
    account: {
        id: string;
        locale: SupportedLocaleCode;
        timezone: string;
    };
    extension: {
        key: string;
        local_id: string;
        target: string;
        location: string;
        data: T;
    };
}
```

### 参数

空

### **返回值**

详细数据解释请参考： [上下文数据](/reference/resource/context)

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

const context = await view.getContext();
```

## setWindowTitle

`setWindowTitle`  方法允许更改当前 `document` 的标题，该方法只支持部分扩展模块。

### **函数签名**

```typescript
function setWindowTitle(newTitle: string): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.9%" /><col style="width: 70.1%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>newTitle</code></td><td style="text-align: left">浏览器 document 标题，完整的标题会在 newTitle 后追加 <code>- {产品名}</code> ，产品名默认是 "PingCode"，企业购买了 Access 产品后可以自定义产品名。</td></tr></tbody></table>

### 返回值

空

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

await view.setWindowTitle("New Title");
```

## refresh

`refresh` 方法允许你再次刷新父页面的数据，而无需进行整个页面加载。该方法只支持部分扩展模块。

### **函数签名**

```typescript
function refresh(): Promise<void>;
```

### 参数

空

### 返回值

空

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

view.refresh();
```

## close

`close` 方法允许你关闭当前视图。例如: 关闭一个 dialog 模态框或者动态菜单打开的视图。

### **函数签名**

```typescript
function close(payload?: unknown): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.23%" /><col style="width: 69.77%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>payload</code></td><td style="text-align: left">主动触发 Dialog（或其他视图）的关闭行为时，携带的 payload 数据将作为入参，分发给 Dialog 打开时注册的 onClose 回调函数。</td></tr></tbody></table>

### 返回值

空

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

view.close({ formValue: '' });
```

## onClose

`onClose` 方法允许你注册一个回调，当 Dialog（或其他视图）关闭时执行该回调函数。

### **函数签名**

```typescript
function onClose(callback: () => Promise<void>): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.81%" /><col style="width: 66.19%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>callback</code></td><td style="text-align: left">注册的回调函数，当 Dialog（或其他视图）关闭时调用。</td></tr></tbody></table>

### 返回值

空

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

view.onClose(async () => {
  // do somethings
});
```

## isDialog

`isDialog` 方法用于判断当前资源是否在 Dialog 中运行。

### **函数签名**

```typescript
function isDialog(): Promise<boolean>;
```

### 参数

空

### 返回值

返回 `Promise<boolean>` 表示是否是一个 Dialog。

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

const isDialog = await view.isDialog();
```

## createHistory

`createHistory`  方法使你的应用能够操作当前页面 URL，以便在全页面应用内进行路由，使用时 `to` 属性始终相对于应用的 URL。该方法只支持部分扩展模块。

### **函数签名**

```typescript
function createHistory(): Promise<NexusHistory>;

export interface NexusHistory {
    action: HistoryAction;
    location: HistoryLocation;
    push(to: HistoryTo, state?: HistoryState): void;
    replace(to: HistoryTo, state?: HistoryState): void;
    go(delta: number): void;
    back(): void;
    forward(): void;
    listen(listener: HistoryListener): Promise<UnlistenCallback>;
}


export enum HistoryAction {
    Pop = "POP",
    Push = "PUSH",
    Replace = "REPLACE",
}

export type HistoryTo = string | Partial<HistoryPath>;

export type HistoryState = unknown;

export interface HistoryLocation extends HistoryPath {
    state: HistoryState;
}

export interface HistoryUpdate {
    action: HistoryAction;
    location: HistoryLocation;
}

export interface HistoryListener {
    (update: HistoryUpdate): void;
}

export type UnlistenCallback = () => void;

interface HistoryPath {
    pathname: string;
    search: string;
    hash: string;
}

```

### 参数

空

### 返回值

`Promise<NexusHistory>` 是一个 History 对象引用。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.49%" /><col style="width: 67.51%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>action</code></td><td>当前的历史操作类型，枚举值： <code>POP</code> 、 <code>PUSH</code> 、 <code>REPLACE</code> 。</td></tr><tr><td><code>location</code></td><td>当前的位置描述对象，包含 <code>pathname</code> （路径）、 <code>search</code> （查询参数）、 <code>hash</code> （哈希值）、 <code>state</code> （状态数据）。</td></tr><tr><td><code>push</code></td><td>导航到新的 URL，向历史栈添加一条新记录。支持传入路径字符串或 <code>HistoryPath</code> 对象，支持传入 <code>HistoryState</code> 状态数据。</td></tr><tr><td><code>replace</code></td><td>替换当前 URL，不添加新的历史记录。支持传入路径字符串或 <code>HistoryPath</code> 对象，支持传入 <code>HistoryState</code> 状态数据。</td></tr><tr><td><code>go</code></td><td>在历史栈中前进或后退 <code>delta</code> 步，传入负数表示后退，正数表示前进。</td></tr><tr><td><code>back</code></td><td>后退一步，相当于调用 <code>go(-1)</code> 。</td></tr><tr><td><code>forward</code></td><td>前进一步，相当于调用 <code>go(1)</code> 。</td></tr><tr><td><code>listen</code></td><td>注册一个监听器，当历史变化（如路由跳转）时触发回调。返回一个 <code>Promise&lt;UnlistenCallback&gt;</code> ，调用该回调可取消监听。</td></tr></tbody></table>

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

const history = await view.createHistory();

// e.g. URL begins as http://example.pingcode.com/apps/abc/123

const to: HistoryTo = '/page-1';
history.push(to);
// this updates the URL to http://example.pingcode.com/apps/abc/123/page-1


const to: HistoryTo = {
  pathname: '/page-2',
  search: '?fruit=apple&color=blue',
  hash: '#section',
};
const state = { from: 'pushLocation' };
history.push(to, state);
// this updates the URL to http://example.pingcode.com/apps/abc/123/page-2?fruit=apple&color=blue#section

history.go(-2);
// this updates the URL to http://example.pingcode.com/apps/abc/123
```

## submit

`submit` 方法允许你在上下文配置视图上提交表单。该方法只支持部分扩展模块。

### **函数签名**

```typescript
function submit<T = any>(payload?: T): Promise<boolean>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.23%" /><col style="width: 69.77%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>payload</code></td><td style="text-align: left">有效负载参数由视图的要求定义。</td></tr></tbody></table>

### 返回值

空

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

view.submit({ config: { name: 'lily' } });
```

## emitReadyEvent

### **函数签名**

```typescript
function emitReadyEvent(): Promise<void>;
```

### 参数

空

### 返回值

空

### **示例**

```typescript
import { view } from "@pc-nexus/bridge";

await view.emitReadyEvent();
```
