---
title: "richtext"
lastUpdated: 2026-07-24T09:31:13.000Z
---

# richtext

`richtext` 通过 iframe 方式嵌入富文本内容，提供富文本渲染器和编辑器的创建能力。

导入：

```typescript
import { richtext } from '@pc-nexus/capabilities';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 50%" /><col style="width: 50%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>createRenderer</code></td><td>用于创建富文本渲染器</td></tr><tr><td><code>createEditor</code></td><td>用于创建富文本编辑器</td></tr></tbody></table>

## createRenderer

`createRenderer` 创建富文本渲染器。

### 函数签名

```typescript
function createRenderer(iframe: HTMLIFrameElement, options?: RichtextRendererOptions): Promise<RichtextRendererRef>;

interface RichtextRendererOptions {
    content?: RichtextContent;
}

interface RichtextRendererRef {
    iframe: HTMLIFrameElement;
    update: (content: RichtextContent) => void;
}

type RichtextContent = Descendant[] | string;

type Descendant = RichtextElement | RichtextText;

interface RichtextText {
    text: string;
    [key: string]: unknown;
}

interface RichtextElement {
    type: string;
    children: Descendant[];
    [key: string]: unknown;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.59%" /><col style="width: 76.41%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>iframe</code></td><td>用于承载富文本内容的 iframe 元素</td></tr><tr><td><code>options</code></td><td>初始化选项，类型为 <code>RichtextRendererOptions</code> (见下方详细说明)</td></tr></tbody></table>

 `RichtextRendererOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.59%" /><col style="width: 76.41%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>content</code></td><td>初始渲染内容</td></tr></tbody></table>

### 返回值

返回值类型为 `RichtextRendererRef` ，表示渲染器的引用对象：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.59%" /><col style="width: 76.41%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>iframe</code></td><td>渲染器所在的 iframe 元素</td></tr><tr><td><code>update</code></td><td>更新渲染内容的方法</td></tr></tbody></table>

### 示例

```typescript
import { richtext, type RichtextContent } from "@pc-nexus/capabilities";

const content: RichtextContent = [
  {
    type: "paragraph",
    children: [{ text: "Hello, this is a sample richtext document." }],
  },
];

const iframe = document.getElementById("richtext-renderer") as HTMLIFrameElement;

const rendererRef = await richtext.createRenderer(iframe, { content });

// 更新渲染内容
rendererRef.update(newContent);
```

## createEditor

`createEditor` 创建富文本编辑器。

### 函数签名

```typescript
function createEditor(iframe: HTMLIFrameElement, options?: RichtextEditorOptions): Promise<RichtextEditorRef>;
  
interface RichtextEditorOptions extends RichtextRendererOptions {
    onContentChange?: (content: RichtextContent) => void;
}

interface RichtextEditorRef extends RichtextRendererRef {
    destroy: () => void;
}

```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.59%" /><col style="width: 76.41%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>iframe</code></td><td>用于承载富文本编辑器的 iframe 元素</td></tr><tr><td><code>options</code></td><td>初始化选项，类型为 <code>RichtextEditorOptions</code> (见下方详细说明)</td></tr></tbody></table>

`RichtextEditorOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25.42%" /><col style="width: 74.58%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>content</code></td><td>初始编辑内容</td></tr><tr><td><code>onContentChange</code></td><td>内容变更回调函数</td></tr></tbody></table>

### 返回值

返回值类型为 `RichtextEditorRef` ，表示编辑器的引用对象：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.59%" /><col style="width: 76.41%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>iframe</code></td><td>编辑器所在的 iframe 元素</td></tr><tr><td><code>update</code></td><td>更新编辑内容的方法</td></tr><tr><td><code>destroy</code></td><td>销毁编辑器实例，清理资源</td></tr></tbody></table>

### 示例

```typescript
import { richtext, type RichtextContent } from "@pc-nexus/capabilities";

let content: RichtextContent = [
  {
    type: "paragraph",
    children: [{ text: "Editable document" }],
  },
];

const iframe = document.getElementById("richtext-editor") as HTMLIFrameElement;

const editorRef = await richtext.createEditor(editorIframe, {
  content,
  onContentChange: (doc) => {
    content = doc ?? [];
  },
});

// 组件卸载或页面离开时销毁编辑器
editorRef.destroy();
```

## toHtml

`toHtml` 转换为 HTML 格式的文本内容。

### 函数签名

```typescript
function toHtml(content: RichtextContent): Promise<string>
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25.85%" /><col style="width: 74.15%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td>content</td><td>富文本内容</td></tr></tbody></table>

### 返回值

返回 `Promise<string>` 。

### 示例

```typescript
import { richtext, type RichtextContent } from "@pc-nexus/capabilities";

const content: RichtextContent = [
  {
    type: "paragraph",
    children: [{ text: "Hello, this is a sample richtext document." }],
  },
];

richtext.toHtml(content);
// <p>Hello, this is a sample richtext document for testing.</p>


```

## toPlainText

`toPlainText` 转换为纯文本内容。

### 函数签名

```typescript
function toPlainText(content: RichtextContent): Promise<string>
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25.85%" /><col style="width: 74.15%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td>content</td><td>富文本内容</td></tr></tbody></table>

### 返回值

返回 `Promise<string>` 。

### 示例

```typescript
import { richtext, type RichtextContent } from "@pc-nexus/capabilities";

const content: RichtextContent = [
  {
    type: "paragraph",
    children: [{ text: "Hello, this is a sample richtext document." }],
  },
];

richtext.toPlainText(content);
// Hello, this is a sample richtext document for testing.

```
