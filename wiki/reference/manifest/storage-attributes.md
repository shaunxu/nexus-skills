---
title: "Attributes"
lastUpdated: 2026-05-26T07:24:43.000Z
---

# Attributes

`attributes` 节点指定自定义实体的属性列表。

## 示例

简单配置示例：

```yaml
storage:
  entities:
    - name: employees
      attributes:
        - name: name
          type: string
          required: true
          default: ""
        - name: age
          type: integer
```

## 属性

实体的每个属性，都可以指定以下参数：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td>Y</td><td>指定属性的名称</td></tr><tr><td><code>type</code></td><td>Y</td><td>指定属性的类型，支持： - <code>number</code> - <code>string</code> - <code>boolean</code> - <code>array</code> - <code>object</code></td></tr><tr><td><code>required</code></td><td></td><td>指定属性是否不能为空</td></tr><tr><td><code>default</code></td><td></td><td>指定属性的默认值</td></tr></tbody></table>
