---
title: "workitem"
lastUpdated: 2026-07-15T10:12:18.000Z
---

# workitem

工作项数据。

## 签名

函数签名：

```javascript
export interface WorkItem {
    id: string;
    short_id: string;
    identifier: string;
    title: string;
    type_group: WorkItemTypeGroup;
    type_id: string;
}

export enum WorkItemTypeGroup {
    requirement = 1,
    task = 2,
    bug = 3,
    issue = 4,
    plan = 5
}
```

## 示例

示例数据：

```javascript
{
  "id": "5edca524cad2fa112b06305c",
  "short_id": "Ogf1EYey",
  "identifier": "SCR-1",
  "title": "这是一个史诗",
  "type_group": 1,
  "type_id": "5a86eaf6a72585327ea46fge0",
}
```

## 属性

属性解释：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.93%" /><col style="width: 69.07%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>工作项 ID</td></tr><tr><td><code>short_id</code></td><td>工作项短 ID</td></tr><tr><td><code>identifier</code></td><td>工作项唯一标识</td></tr><tr><td><code>title</code></td><td>工作项名称</td></tr><tr><td><code>type_group</code></td><td>工作项类型分组，取值为 <code>WorkItemTypeGroup</code></td></tr><tr><td><code>type_id</code></td><td>工作项类型 ID</td></tr></tbody></table>
