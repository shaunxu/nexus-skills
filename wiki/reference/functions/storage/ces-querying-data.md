---
title: "查询数据"
lastUpdated: 2026-07-15T08:53:19.000Z
---

# 查询数据

本文档提供的基本方法，您可以通过自定义的实体，进行数据的查询。

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 34.18%" /><col style="width: 65.82%" /></colgroup><thead><tr><th>方法</th><th>描述</th></tr></thead><tbody><tr><td><code>find</code></td><td>查询实体列表</td></tr><tr><td><code>count</code></td><td>查询实体数量</td></tr></tbody></table>

## find

查询实体列表。

### 函数签名

```typescript
function find(condition?: (conditionBuilder: ConditionBuilder<T>) => void, options?: CesFindOptions<T>): Promise<T[]>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.05%" /><col style="width: 66.95%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>condition</code></td><td>查询条件回调函数，参考 <a href="/reference/functions/storage/ces-condition-builder">ConditionBuilder</a></td></tr><tr><td><code>options</code></td><td>查询选项对象，参考 <a href="/reference/functions/storage/ces-find-options">CesFindOptions</a></td></tr></tbody></table>

### 返回值

返回查询到的自定义实体列表，通过 `Promise` 返回。

### 示例

```typescript
import { ces, Direction } from "@pc-nexus/storage";

// 逻辑条件：name = "hello" && (age > 18 && age < 60) && (description = "engineer" || description = "manager")
const entities = await ces.entity<EmployeesEntity>("employees").find(
    (cb) => {
        cb.field("name").eq("hello");
        cb.and((andBuilder) => {
            andBuilder.field("age").gt(18);
            andBuilder.field("age").lt(60);
        });
        cb.or((orBuilder) => {
            orBuilder.field("description").eq("engineer");
            orBuilder.field("description").eq("manager");
        });
    },
    {
        sort: [
            {
                propertyKey: "age",
                order: Direction.ascending
            },
        ],
    },
);
```

## count

查询实体数量。

### 函数签名

```typescript
function count(condition?: (conditionBuilder: ConditionBuilder<T>) => void): Promise<number>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.05%" /><col style="width: 66.95%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>condition</code></td><td>查询条件回调函数，参考 <a href="/reference/functions/storage/ces-condition-builder">ConditionBuilder</a></td></tr></tbody></table>

### 返回值

返回查询到的数量，通过 `Promise` 返回。

### 示例

```typescript
import { ces } from "@pc-nexus/storage";

// 逻辑条件：age > 18 && age < 60
const nums = await ces.entity<EmployeesEntity>("employees").count(
    (cb) => {
        cb.field("age").gt(18).lt(60);
    }
);
```
