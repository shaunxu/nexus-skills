---
title: "nos"
lastUpdated: 2026-07-15T13:50:17.000Z
---

# nos

`nos` 对象存储用于持久化存储非结构化数据或者二进制数据，如文件、图片、媒体等。

## 使用

安装数据存储包：

```powershell
npm install @pc-nexus/storage
```

导入对象存储：

```javascript
import { nos } from "@pc-nexus/storage";
```

## 作用域

在使用对象存储能力时，需要在 `manifest.yml` 文件中声明作用域：

```yaml
permissions:
    scopes:
        - pcp:storage:app
```

## 示例

获取上传文件的 URL 地址：

```typescript
import { nos } from "@pc-nexus/storage";

const urlResult = await nos.createUploadUrl({
  key: "upload-file-1",
  size: 1024,
  checksum: "Cniua8PqLHwzRN7BGWWg7YpFDVVOJAToT9l8LQ2uysw=",
  checksum_type: "SHA256"
});
const url = urlResult.url;
return url;
```
