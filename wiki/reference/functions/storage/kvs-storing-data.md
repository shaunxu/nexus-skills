---
title: "存储数据"
lastUpdated: 2026-07-14T07:02:06.000Z
---

# 存储数据

通过本文档提供的方法，可以非常方便的进行 Key-Value 数据的存储与读取。

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>set</code></td><td>写入存储数据</td></tr><tr><td><code>get</code></td><td>读取存储数据</td></tr><tr><td><code>delete</code></td><td>删除存储数据</td></tr></tbody></table>

## set

### 函数签名

```typescript
function set<T extends KvsValueType>(key: string, value: T, options?: KvsSetOptions): Promise<KvsSetResult<T>>;

type KvsValueType = number | string | boolean | object | unknow[];

interface KvsSetOptions {
  policy?: "OVERRIDE" | "FAIL_IF_EXISTS";
  secret?: boolean;
}

interface KvsSetResult<T> {
  key: string;
  value: T;
}

```

### 参数

|名称|描述|
|---|---|
|`key`|数据存储的 `key` 。|
|`value`|数据存储的 `value` ，类型包含 `KvsValueType` ： - `number` - `string` - `boolean` - `object` - `unknow[]`|
|`options`|数据存储选项|

`KvsSetOptions` 类型说明：

|名称|描述|
|---|---|
|`policy`|数据存储策略，当 `key` 已经存在时： - `OVERRIDE` ：新的 `value` 覆盖旧的，默认值 - `FAIL_IF_EXISTS` ：直接报错，该 `key` 已经存在|
|`secret`|值 `value` 是否加密，默认值： `false` 。|

### 返回值

返回值类型为  `KvsSetResult`  ，通过  `Promise`  返回，类型说明：

|名称|描述|
|---|---|
|`key`|数据存储的 `key` 。|
|`value`|数据存储的值。|

### 示例

```typescript
import { kvs } from "@pc-nexus/storage";
interface DemoEntity {
  foo: string;
}
const result = await kvs.set<DemoEntity>("key1", {foo: "bar"}, { 
  policy: "OVERRIDE",
  secret: true
});
return result;
```

## get

### 函数签名

```typescript
function get<T extends KvsValueType>(key: string, options: KvsGetOptions): Promise<T | undefined>;

interface KvsGetOptions {
  secret?: boolean;
}

type KvsValueType = number | string | boolean | object | unknow[];
```

### 参数

|名称|描述|
|---|---|
|`key`|数据存储的 `key` 。|
|`options`|获取存储数据选项|

`KvsGetOptions` 类型说明

|名称|描述|
|---|---|
|secret|获取的数据是否为加密数据，默认值： `false` 。|

### 返回值

返回值类型为  `T`  或 `undefined` ， `T` 是范型参数，指获取数据的类型，通过  `Promise`  返回。

当传入的 `key` 不存在时会返回 `undefined` 。

### 示例

```typescript
import { kvs } from "@pc-nexus/storage";
interface DemoEntity {
  foo: string;
}
const result = await kvs.get<DemoEntity>("key1");
return result;
```

## delete

### 函数签名

```typescript
function delete(key: string): Promise<void>;
```

### 参数

|名称|描述|
|---|---|
|`key`|数据存储的 `key` 。|

### 返回值

空

### 示例

```typescript
import { kvs } from "@pc-nexus/storage";

await kvs.delete("key1");
```
