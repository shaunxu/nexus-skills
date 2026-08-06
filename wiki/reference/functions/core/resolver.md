---
title: "resolver"
lastUpdated: 2026-07-28T02:03:51.000Z
---

# resolver

`Resolver` 是 Nexus 平台中用于定义和执行后端函数的核心模块，开发者可以通过 Resolver 编写服务端逻辑，以响应前端发起的异步调用或处理特定事件。

导入：

```typescript
import { Resolver } from "@pc-nexus/core";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.74%" /><col style="width: 77.26%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>define</code></td><td>用于定义单个解析器函数</td></tr></tbody></table>

## define

`define` 方法用于定义单个解析器函数， `key` 为唯一性标识。

### 函数签名

```typescript
public define<P, R = unknown>(key: string, fn: ResolverFunction<P, R>): this;

export interface ResolverFunction<P, R> {
    (context: NexusAppContext, payload: P): Promise<R>;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.41%" /><col style="width: 70.59%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>解析器函数的字符串标识符，这个字符串必须与用于在前端资源中调用该函数的 <code>functionKey</code> 完全匹配。</td></tr><tr><td><code>fn</code></td><td>实际要执行的回调函数。当客户端通过匹配的 key发起调用时，此函数将被执行。其返回值将被传递回前端调用方。</td></tr></tbody></table>

`fn` 回调函数将传入两个参数：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 23.59%" /><col style="width: 76.41%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>context</code></td><td>当前解析器函数执行时的上下文数据，详情参考 <a href="/reference/functions/core/app">app</a></td></tr><tr><td><code>payload</code></td><td>从前端 <code>invoke</code> 方法调用时传入的数据</td></tr></tbody></table>

### 返回值

方法返回 `Resolver` 实例自身 ( `this` )，支持链式调用。

### 示例

定义一个 Key 为 `exampleFunctionKey` 的解析器函数：

```typescript
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();
resolver.define<{ name: string }>("exampleFunctionKey", async (context, payload) => {
    return { example: `Hello, ${payload.name}!` };
});

export { resolver };
```

在前端代码中调用此解析器函数，必须使用相同的 Key： `exampleFunctionKey`

```typescript
import { invoke } from '@pc-nexus/bridge';

invoke('exampleFunctionKey', { name: 'lily' }).then((returnedData) => {
    console.log(returnedData.example);
});
```

### 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.62%" /><col style="width: 66.38%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_FUNCTION_EXTENSION_NOT_FOUND</code></td><td>调用  <code>invoke</code>  时所在的扩展，在应用 <code>manifest</code> 的  <code>extensions</code>  中找不到。</td></tr><tr><td><code>ERR_FUNCTION_RESOLVER_INVALID</code></td><td>当前扩展未配置  <code>resolver</code> 。</td></tr><tr><td><code>ERR_FUNCTION_RESOLVER_FUNCTION_INVALID</code></td><td>扩展已配置  <code>resolver</code> ，但缺少必填字段  <code>function</code> 。</td></tr><tr><td><code>ERR_FUNCTION_FUNCTION_NOT_FOUND</code></td><td><code>resolver.function</code>  指向的 key 在  <code>functions</code>  中不存在</td></tr></tbody></table>
