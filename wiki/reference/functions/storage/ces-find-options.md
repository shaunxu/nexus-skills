---
title: "CesFindOptions"
lastUpdated: 2026-07-15T08:33:38.000Z
---

# CesFindOptions

本文档定义了数据库查询操作中使用的核心类型和接口，主要用于类型安全地指定查询的过滤、排序、分页和字段投影等选项。

```typescript
type Projection<TSchema> = (keyof TSchema)[];

enum Direction {
    ascending = 1,
    descending = -1,
}

interface SortProperty<TSchema> {
    propertyKey: keyof TSchema;
    order: Direction;
}

interface CesFindOptions<TSchema> {
    skip?: number;
    limit?: number;
    sort?: SortProperty<TSchema>[];
    hint?: string;
    projection?: Projection<TSchema>;
    includes?: { metadata: boolean };
}
```

## **skip**

限制返回的第一条位置，在所有数据中的位置

```typescript
.find(condition, { skip: 10, limit: 20 })
```

## **limit**

限制返回数量

```typescript
.find(condition, { skip: 10, limit: 20 })
```

## projection

限制返回实体数据，仅包含配置字段。

```typescript
.find(condition, { projection: ["name", "age"] });
```

## **hint**

增加查询效率，可指定索引名。

```typescript
.find(condition, { hint: "name_age_" })
```

## includes

当配置 metadata 为 true 时，数据返回会带上如下元数据字段

- `_created_by`
- `_created_at`
- `_updated_by`
- `_updated_at`
- `_is_deleted`
- `_deleted_by`
- `_deleted_at`

```typescript
.find(condition, { includes: { metadata: true } })
```

## **sort**

自定义字段排序

```typescript
import { Direction } from "@pc-nexus/storage";

.find(condition, {
  sort:[
    {
      propertyKey: "name",
      order: Direction.ascending
    }
  ]
})
```

## 完整示例

完整 find 查询示例

```typescript
import { ces, Direction } from "@pc-nexus/storage";
import type { ConditionBuilder, CesFindOptions } from "@pc-nexus/storage";

const findOptions: CesFindOptions<EmployeesEntity> = {
    skip: 10,
    limit: 20,
    projection: ["name", "age"],
    hint: "name_age_",
    includes: { metadata: true },
    sort: [
        {
            propertyKey: "age",
            order: Direction.ascending
        },
    ],
};
const entities = await ces.entity<EmployeesEntity>("employees").find(
    (cb: ConditionBuilder) => {
        cb.field("name").eq("hello");
        cb.and((andBuilder) => {
            andBuilder.field("age").gt(18);
            andBuilder.field("age").lt(60);
            andBuilder.or((orBuilder) => {
                orBuilder.field("description").eq("engineer");
                orBuilder.field("description").eq("manager");
            });
        });
    },
    findOptions
);
```

在上面的查询示例中，查询的逻辑条件是：

```javascript
name = "hello" && (age > 18 && age < 60 && (description = "engineer" || description = "manager" ) )
```

查询扩展选项配置：

- 从满足条件的第 `11` 条开始返回数据
- 返回 `20` 条数据
- 每条数据，只返回 `name` ”和 `age` 字段
- 使用索引名 `name_age_` 查询数据
- 返回数据，附加上元数据字段
- 按照 `age` 字段数据，升序排序
