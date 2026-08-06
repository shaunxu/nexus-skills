---
title: "管理索引"
lastUpdated: 2026-07-08T05:49:05.000Z
---

# 管理索引

本文档介绍如何通过基于实体的属性键（Attribute Key）自定义索引，提高数据查询效率。

## 配置

在实体配置的 `indexes` 部分声明索引，语法如下：

```yaml
indexes:
  - name: <value>
    keys:
        - <attribute_key>: 1 ｜ -1
    options:
        unique: true ｜ false
```

## 属性

针对每条索引，可以进行如下属性设置：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td></td><td>索引的唯一标识，在查询 hit 中使用，如果不设置 ，系统会默认按照 Key 的顺序生成索引</td></tr><tr><td><code>keys</code></td><td>Y</td><td>索引的属性列表，以及索引顺序，不支持在类型为 <code>array</code> 和 <code>object</code> 的属性上建立索引 <code>key</code> 的值只能是 1 或者 -1， 1 代表升序，-1 代表降序</td></tr><tr><td><code>options</code></td><td></td><td>索引设置，当前支持： - <code>unique</code> 是否为唯一索引</td></tr></tbody></table>

## 说明

- 在你的应用代码部署期间，存储服务会根据需要创建或更新索引
- 索引过程的耗时会随数据集大小增加而变长
- 索引过程与部署的其他环节相互独立，因此部署命令通常会在索引仍在进行时就执行完成。在索引过程完成之前，你无法在任何站点安装应用
- 部署中检查上一次部署中 `manifest.yml` 文件中相同名字，或者相同内容的索引，在当前部署中不存在就会自动删除
