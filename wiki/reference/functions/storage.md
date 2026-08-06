---
title: "Storage"
lastUpdated: 2026-07-15T15:15:43.000Z
---

# Storage

Nexus 平台提供托管式数据存储能力，支持在您的应用安装实例中持久化存储数据。每个应用安装实例均需遵循 Nexus 平台托管式存储的限制规定。数据存储功能适用于长期存储数据，直到您需要删除或覆盖数据为止。

## 安装

```powershell
npm install @pc-nexus/storage
```

导入：

```javascript
import { kvs } from "@pc-nexus/storage";

import { ces } from "@pc-nexus/storage";
```

## APIs

Storage APIs 提供的能力如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 37.78%" /><col style="width: 62.22%" /></colgroup><thead><tr><th>APIs</th><th>说明</th></tr></thead><tbody><tr><td><a href="/reference/functions/storage/kvs">kvs</a></td><td>为键-值对数据提供简单的存储功能，如用户偏好设置或应用配置等数据</td></tr><tr><td><a href="/reference/functions/storage/ces">ces</a></td><td>通过自定义实体，进行结构化数据存储</td></tr><tr><td><a href="/reference/functions/storage/nos">nos</a></td><td>存储非结构化数据或者二进制数据，如文件、图片、媒体等</td></tr></tbody></table>

## 数据生命周期

使用托管式存储（ `kvs` 、 `ces` 、 `nos` ）的应用，其数据的保留与删除遵循统一规则，详情请参考 [托管数据生命周期](/guide/development/hosted-data-lifecycle) 。
