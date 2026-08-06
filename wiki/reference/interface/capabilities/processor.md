---
title: "processor"
lastUpdated: 2026-07-06T03:47:14.000Z
---

# processor

`processor` 使你的应用能够弹出进程管理器。

导入：

```typescript
import { processor } from '@pc-nexus/capabilities';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 43.64%" /><col style="width: 56.36%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>add</code></td><td>添加进程，弹出进程管理器</td></tr></tbody></table>

## add

### **函数签名**

```typescript
function add(options: ProcessOptions): Promise<ProcessRef>;

export type ProcessOptions = File | CustomProcessItem;

interface CustomProcessItem {
    name: string;
    icon?: string;
}

export interface ProcessRef {
    readonly id: string;
    readonly setProgress: (progress: number) => void;
    readonly complete: (payload?: { fileUrl?: string }) => void;
    readonly error: (message: string) => void;
    readonly cancel: () => void;
}
```

### **参数**

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.34%" /><col style="width: 67.66%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>options</code></td><td style="text-align: left">弹出进程管理器的配置项（见下方详细说明）</td></tr></tbody></table>

`ProcessOptions` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.34%" /><col style="width: 67.66%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>ProcessOptions</code></td><td style="text-align: left">可传入  <code>File</code>  文件，或自定义文件名称和图标</td></tr></tbody></table>

### **返回值**

`ProcessRef` 该实例的引用对象。类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.78%" /><col style="width: 68.22%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>id</code></td><td style="text-align: left">当前进程的 id</td></tr><tr><td style="text-align: left"><code>setProgress</code></td><td style="text-align: left">设置当前进程的进度</td></tr><tr><td style="text-align: left"><code>complete</code></td><td style="text-align: left">标记进程完成 <code>fileUrl</code> 进程完成后文件下载地址</td></tr><tr><td style="text-align: left"><code>error</code></td><td style="text-align: left">标记进程失败， <code>message</code> 进程失败后的错误信息</td></tr><tr><td style="text-align: left"><code>cancel</code></td><td style="text-align: left">进程取消操作</td></tr></tbody></table>

### **示例**

```typescript
import { processor } from '@pc-nexus/capabilities';

const processRef = await processor.add({
    name: 'export.pdf',
});
processRef.complete({
    fileUrl: 'https://example.com/export.pdf',
});
```
