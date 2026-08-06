---
title: "Indexes"
lastUpdated: 2026-05-26T07:25:00.000Z
---

# Indexes

`indexes` 节点指定为自定义实体哪些属性创建索引，拥有索引的属性会针对查询进行优化，因此，您应根据计划使用的查询模式来创建索引。

## 示例

简单配置示例：

```yaml
storage:
  entities:
      indexes:
        - name: "name_age_"
          keys:
            - name: 1
            - age: 1
          options:
            unique: true
        - name: "name_sex_"
          keys:
            - name: 1
            - sex: 1
```

## 属性

针对每条索引，可以通过以下属性进行设置：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td></td><td>索引的唯一标识</td></tr><tr><td><code>keys</code></td><td>Y</td><td>索引的属性列表，以及索引顺序，不支持在类型为 <code>array</code> 和 <code>object</code> 的属性上建立索引</td></tr><tr><td><code>options</code></td><td></td><td>索引设置，当前支持： - <code>unique</code> 是否为唯一索引</td></tr></tbody></table>
