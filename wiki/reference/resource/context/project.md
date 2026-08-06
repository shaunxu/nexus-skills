---
title: "project"
lastUpdated: 2026-07-15T10:11:33.000Z
---

# project

项目数据。

## 签名

函数签名：

```javascript
export interface Project {
    id: string;
    identifier: string;
    name: string;
    type: "scrum" | "kanban" | "waterfall" | "hybrid";
}
```

## 示例

示例数据：

```javascript
{
  "id": "5eb623f6a70571487ea47000",
  "type": "scrum",
  "name": "Scrum 项目",
  "identifier": "SCR"
}
```

## 属性

属性解释：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.93%" /><col style="width: 69.07%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>项目 ID</td></tr><tr><td><code>type</code></td><td>项目类型，取值为： <code>scrum</code> 、 <code>kanban</code> 、 <code>waterfall</code> 、 <code>hybrid</code></td></tr><tr><td><code>name</code></td><td>项目名称</td></tr><tr><td><code>identifier</code></td><td>项目唯一标识</td></tr></tbody></table>
