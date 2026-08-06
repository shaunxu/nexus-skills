---
title: "release"
lastUpdated: 2026-07-15T10:13:04.000Z
---

# release

发布数据。

## 签名

函数签名：

```javascript
export interface Release {
    id: string;
    short_id: string;
    identifier: string;
    name: string;
}
```

## 示例

示例数据：

```javascript
{
   "id": "6a27c01aadb5a1cc90d9af3d",
   "short_id": "3AQ_oqj7",
   "identifier": "1",
   "name": "发布一",
}
```

## 属性

属性解释：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.93%" /><col style="width: 69.07%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>发布 ID</td></tr><tr><td><code>short_id</code></td><td>发布短 ID</td></tr><tr><td><code>identifier</code></td><td>发布唯一标识</td></tr><tr><td><code>name</code></td><td>发布名称</td></tr></tbody></table>
