---
title: "存储实体"
lastUpdated: 2026-07-16T01:47:08.000Z
---

# 存储实体

本文档提供的基本方法，您可以通过自定义的实体，进行数据的存储。

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 34.18%" /><col style="width: 65.82%" /></colgroup><thead><tr><th>方法</th><th>描述</th></tr></thead><tbody><tr><td><code>insert</code></td><td>数据写入</td></tr><tr><td><code>update</code></td><td>数据更新</td></tr><tr><td><code>delete</code></td><td>数据删除</td></tr></tbody></table>

## entity().insert

数据写入，支持单条写入和批量写入。

### 函数签名

```typescript
function insert(value: T): Promise<T>;
function insert(value: T[], options?: CesInsertOptions): Promise<T[]>;
```

### 参数

|名称|描述|
|---|---|
|`value`|需插入的 `Entity` 数据，支持传单个或数组|
|`options`|插入多个 `value` 数据时，可以通过 `options` 来配置插入的顺序|

`CesInsertOptions` 类型说明：

|名称|描述|
|---|---|
|ordered|插入多个 `value` 时是否排序，默认值： `false` 。|

### 返回值

插入成功后，返回已插入的数据，通过 `Promise` 返回。

### 示例

```typescript
import { ces } from "@pc-nexus/storage";

const entity = ces.entity<EmployeesEntity>("employees");

// 批量插入
const entities = await entity.insert([
  { name: "a", age: 1, description: "this is a intro." },
  { name: "b", age: 2, description: "this is b intro." },
  { name: "c", age: 3, description: "this is c intro." }
]);

// 单个插入
const entity = await entity.insert({
  name: "a", 
  age: 1, 
  description: "this is a intro."
});
```

## entity().update

数据更新，支持对已有字段修改值。

### 函数签名

```typescript
function update(condition: (conditionBuilder: ConditionBuilder<T>) => void, value: Partial<T>): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.05%" /><col style="width: 66.95%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>condition</code></td><td>查询条件回调函数，参考 <a href="/reference/functions/storage/ces-condition-builder">ConditionBuilder</a></td></tr><tr><td><code>value</code></td><td>需要更新的实体字段数据</td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { ces } from "@pc-nexus/storage";

await ces.entity<EmployeesEntity>("employees").update(
    (cb) => {
        cb.field("name").eq("a");
    }，
    {
        age: 10,
        description: null
    }
);
```

## entity().delete

删除数据，删除数据时即执行物理删除，不可恢复。

### 函数签名

```typescript
function delete(condition: (conditionBuilder: ConditionBuilder<T>) => void): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.05%" /><col style="width: 66.95%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>condition</code></td><td>查询条件回调函数，参考 <a href="/reference/functions/storage/ces-condition-builder">ConditionBuilder</a></td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { ces } from "@pc-nexus/storage";

await ces.entity<EmployeesEntity>("employees").delete(
    (cb) => {
        cb.field("age").gt(1).lt(2);
    }
);
```
