---
title: "ticket"
lastUpdated: 2026-07-15T10:12:11.000Z
---

# ticket

工单数据。

## 签名

函数签名：

```javascript
export interface Ticket {
    id: string;
    short_id: string;
    identifier: string;
    title: string;
}
```

## 示例

示例数据：

```javascript
{
   "id": "6948e5e4b1b23bf6de9c8bc0",
   "short_id": "Q0mOWC8g",
   "identifier": "CPCWU-T1",
   "title": "示例工单",
}
```

## 属性

属性解释：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.93%" /><col style="width: 69.07%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>工单 ID</td></tr><tr><td><code>short_id</code></td><td>工单短 ID</td></tr><tr><td><code>identifier</code></td><td>工单唯一标识</td></tr><tr><td><code>title</code></td><td>工单名称</td></tr></tbody></table>
