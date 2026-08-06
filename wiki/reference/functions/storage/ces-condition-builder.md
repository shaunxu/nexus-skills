---
title: "ConditionBuilder"
lastUpdated: 2026-07-15T09:01:04.000Z
---

# ConditionBuilder

本文档旨在说明查询条件构建器 `ConditionBuilder` 的使用方法。该构建器提供了一种链式、可读性强的 API，用于以编程方式定义数据查询条件。

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>field</code></td><td>指定要进行条件判断的字段</td></tr><tr><td><code>and</code></td><td>将多个条件以 AND（逻辑与）​ 关系进行组合</td></tr><tr><td><code>or</code></td><td>将多个条件以 OR（逻辑或）​ 关系进行组合</td></tr></tbody></table>

## field

指定要进行条件判断的字段，并返回一个条件构建器实例，以便链式调用后续的条件操作符。

### 函数签名

```typescript
function field(fieldName: string): ConditionBuilder;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 48.02%" /><col style="width: 51.98%" /></colgroup><thead><tr><th>名称</th><th>说明</th></tr></thead><tbody><tr><td><code>fieldName</code></td><td>查询字段的名称</td></tr></tbody></table>

### 返回值

返回值为 `ConditionBuilder` 实例本身，可继续链式调用条件操作符

### 示例

```typescript
cb.field("name").eq("zhangsan");
cb.field("name").ne("lisi");

// age >= 18 && age <= 60
cb.field("age").gt(18).lt(60);

// description 包含 "a"
cb.field("description").contains(["a"]);
// description 不包含 "b" 和 "c"
cb.field("description").notContains(["b", "c"]);

// description 字段没有值
cb.field("description").exists(false);
// description 字段有值
cb.field("description").exists(true);
```

### 数据类型操作映射

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 47.46%" /><col style="width: 52.54%" /></colgroup><thead><tr><th>数据类型</th><th>操作符</th></tr></thead><tbody><tr><td><code>string</code></td><td><code>eq</code> ， <code>ne</code> ， <code>exists</code> ， <code>contains</code> ， <code>notContains</code></td></tr><tr><td><code>number</code></td><td><code>eq</code> ， <code>ne</code> ， <code>gt</code> ， <code>gte</code> ， <code>lt</code> ， <code>lte</code> ， <code>exists</code></td></tr><tr><td><code>boolean</code></td><td><code>eq</code> ， <code>ne</code> ， <code>exists</code></td></tr><tr><td><code>array</code></td><td><code>eq</code> ， <code>ne</code> ， <code>exists</code> ， <code>contains</code> ， <code>notContains</code></td></tr><tr><td><code>object</code></td><td><code>eq</code> ， <code>ne</code> ， <code>exists</code></td></tr></tbody></table>

### 条件操作符

所有操作符均在 `field(fieldName)` 后调用，支持链式组合。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 47.32%" /><col style="width: 52.68%" /></colgroup><thead><tr><th>操作符</th><th>说明</th></tr></thead><tbody><tr><td><code>eq</code> ， <code>ne</code></td><td>等于，不等于</td></tr><tr><td><code>gt</code> ， <code>gte</code></td><td>大于，大于等于</td></tr><tr><td><code>lt</code> ， <code>lte</code></td><td>小于，小于等于</td></tr><tr><td><code>contains</code> ， <code>notContains</code></td><td>包含，不包含</td></tr><tr><td><code>exists</code></td><td>字段是否有值（null值，也视为有值）</td></tr></tbody></table>

## and

用于创建一个 AND 逻辑组，其回调函数参数内部定义的所有条件将取逻辑与。

### 函数签名

```javascript
function and(builderCallback: function): ConditionBuilder;
```

### 参数

|名称|说明|
|---|---|
|`builderCallback`|接收 `ConditionBuilder` 实例作为参数的回调函数，用于定义需「与」组合的子条件|

### 返回值

返回值为 `ConditionBuilder` 实例本身，支持链式调用

### 示例

```typescript
//逻辑条件：name = "zhangsan" && (age > 30 || description = "test")
cb.and((andBuilder) => {
    andBuilder.field("name").eq("zhangsan");
    andBuilder.or((orBuilder) => {
        orBuilder.field("age").gt(30);
        orBuilder.field("description").eq("test");
    });
})
```

## or

用于创建一个 OR 逻辑组，其回调函数参数内部定义的所有条件将取逻辑或。

### 函数签名

```javascript
function or(builderCallback: function): ConditionBuilder;
```

### 参数

|名称|说明|
|---|---|
|`builderCallback`|接收 `ConditionBuilder` 实例作为参数的回调函数，用于定义需「或」组合的子条件|

### 返回值

返回值为 `ConditionBuilder` 实例本身，支持链式调用

### 示例

```typescript
//逻辑条件：name = "zhangsan" || (age > 30 && description = "test") || name = "lisi"
cb.or((orBuilder) => {
    orBuilder.field("name").eq("zhangsan");
    orBuilder.and((andBuilder) => {
        andBuilder.field("age").gt(30);
        andBuilder.field("description").eq("test");
    });
    orBuilder.field("name").eq("lisi");
})
```
