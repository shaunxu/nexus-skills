---
title: "定义实体"
lastUpdated: 2026-07-16T02:48:08.000Z
---

# 定义实体

本文档详细介绍如何在 `manifest.yaml` 文件中定义实体。

## 配置

要使用自定义实体存储，需要在 `manifest.yaml` 文件中使用 `storage` 属性进行定义，其语法格式如下：

```yaml
storage:
    entities:
        - name: employees
          attributes:
              - name: name
                type: string
                required: true
                default: ''
              - name: description
                type: string
              - name: age
                type: number
          indexes:
              - name: 'name_age_'
                keys:
                    name: 1
                    age: 1
                options:
                    unique: true
```

详细的定义请参考 [Storage](/reference/manifest/storage) 。

## 属性

自定义实体的属性限制规则

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.49%" /><col style="width: 67.51%" /></colgroup><thead><tr><th style="text-align: left">分类</th><th style="text-align: left">要求</th></tr></thead><tbody><tr><td style="text-align: left"><code>name</code></td><td style="text-align: left">实体名称必须遵循： - 满足正则表达式： <code>^(?!^\[-\_\])(?!\.$)(?!.\*\.\.)\[a-z0-9\_\\-.\]{3,64}$</code> - 名称不能重复 - 名称长度不能少于 3 个字符，不超过 64 个字符</td></tr><tr><td style="text-align: left"><code>attributes</code></td><td style="text-align: left">属性名称必须遵循： - 满足正则表达式 : <code>^[a-zA-Z][a-zA-Z0-9_]*$</code> - 单个实体内属性名称唯一</td></tr><tr><td style="text-align: left"><code>indexes</code></td><td style="text-align: left">索引名称必须遵循： - 满足正则表达式： <code>^(?!.\*\.)(?!.\*\.\.)\[a-zA-Z0-9:\_\\-\]{3,64}$</code> - 同一实体中的每个索引名称都必须唯一 - 名称长度不能短于 3 个字符，不超过 64 个字符</td></tr></tbody></table>

## 数据类型

自定义实体是带有多个类型化或非类型化属性的 key。你可以使用以下数据类型定义属性：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 50%" /><col style="width: 50%" /></colgroup><thead><tr><th style="text-align: left">类型</th><th style="text-align: left">要求</th></tr></thead><tbody><tr><td style="text-align: left"><code>number</code></td><td style="text-align: left">Int ，Float，Double</td></tr><tr><td style="text-align: left"><code>string</code></td><td style="text-align: left">UTF-8 字符串</td></tr><tr><td style="text-align: left"><code>boolean</code></td><td style="text-align: left">ture 或 false</td></tr><tr><td style="text-align: left"><code>object</code></td><td style="text-align: left">Json 数据类型</td></tr><tr><td style="text-align: left"><code>array</code></td><td style="text-align: left">数组类型支持如下数据类型: - number - string - boolean - object</td></tr></tbody></table>

## 注意事项

- 已经部署在开发/生产环境的实体不能被删除
- 实体中已经声明的属性不能再次删除或者修改类型
- 实体中已经声明的 `required` 不能由选填改为必填
