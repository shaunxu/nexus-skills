---
title: "invoke"
lastUpdated: 2026-07-06T03:34:30.000Z
---

# invoke

`invoke` 方法使你的应用能够运行由 Nexus 平台托管的后端 FaaS 函数。

导入：

```typescript
import { invoke } from '@pc-nexus/bridge';
```

## **invoke**

### **函数签名**

```typescript
function invoke<TPayload, TResult>(functionKey: string, payload?: TPayload): Promise<TResult>;
```

### **参数**

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.24%" /><col style="width: 70.76%" /></colgroup><thead><tr><th style="text-align: left">名称</th><th style="text-align: left">描述</th></tr></thead><tbody><tr><td style="text-align: left"><code>functionKey</code></td><td style="text-align: left">后端定义 resolver 函数的唯一标识字符串，该字符串应与 <code>resolver</code> 函数定义中的  <code>functionKey</code>  完全匹配。</td></tr><tr><td style="text-align: left"><code>payload</code></td><td style="text-align: left">传递给 <code>resolver</code> 函数的数据。</td></tr></tbody></table>

### **返回值**

- 调用函数返回的数据，通过  `Promise` 返回。

### **示例**

```typescript
import { invoke } from '@pc-nexus/bridge';

const data = await invoke('getText', { example: 'my-invoke-variable' });
```

### 类型安全调用

使用 TypeScript 时，你可以在后端和前端之间重复使用这些类型使调用类型安全。

通过泛型传递输入参数和返回参数类型：

```typescript
const result = await invoke<{ example: string }, { text: string }>("getText", { example: 'my-invoke-variable' });
console.log(result.text);

// ERROR: 'message' is not defined on the result
console.log(result.message);

// ERROR: 'sample' is not the right parameter
await invoke<{ example: string }, { text: string }>('getText', { sample: 'my-invoke-variable' });
```
