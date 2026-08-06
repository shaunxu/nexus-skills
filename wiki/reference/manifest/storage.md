---
title: "Storage"
lastUpdated: 2026-06-29T10:31:11.000Z
---

# Storage

`storage` 属性用于定义应用自定义实体数据存储。

## 结构

结构定义如下：

```yaml
storage {}
└─ entities [] [Mandatory]
   ├─ name (string) [Mandatory]
   ├─ attributes [] [Mandatory]
   │  ├─ name (string) [Mandatory]
   │  ├─ type (string) [Mandatory]
   │  ├─ required (boolean) [Optional]
   │  └─ default {} [Optional]
   └─ indexes [] [Optional]
      ├─ name (string) [Mandatory]
      ├─ keys (string) [Mandatory]
      └─ options (string) [Optional]
```

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

实体在 `entities` 属性下定义，每个实体至少包含以下属性：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td>Y</td><td>指定自定义实体的名字，必须符合以下规则： - 只能包含以下字符：小写字母a-z、数字0-9以及连接符、下划线 - 必须符合正则表达式 <code>[_a-z0-9-.]</code> - 不能以连接符（-）或下划线（_）开头 - 开头和结尾不能是点号（.） - 不能包含连续的两个点号（..） - 单个应用内实体名称不可重复</td></tr><tr><td><code>attributes</code></td><td>Y</td><td>定义实体的属性列表</td></tr><tr><td><code>indexes</code></td><td></td><td>定义实体的索引列表</td></tr></tbody></table>
