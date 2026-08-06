---
title: "管理对象"
lastUpdated: 2026-07-14T07:17:20.000Z
---

# 管理对象

通过本文档提供的基本方法，您可以持久化存储非结构化数据或者二进制数据，如文件、图片、媒体等。主要包括：

|方法|描述|
|---|---|
|`createUploadUrl`|创建上传文件的 URL 地址。|
|`createDownloadUrl`|创建下载文件的 URL 地址。|
|`getMetadata`|获取对象的基本信息。|
|`delete`|删除对象。|

## createUploadUrl

创建上传文件的 URL 地址。

### 函数签名

```typescript
function createUploadUrl(body: UploadUrlBody, options?: NosUploadUrlOptions): Promise<PresignedUrlResponse>;

interface UploadUrlBody {
    key: string;
    size: number;
    checksum: string;
    checksum_type: "SHA1" | "SHA256" | "CRC32" | "CRC32C";
}

interface NosUploadUrlOptions {
    overwrite?: boolean; // 是否覆盖旧文件
}

interface PreSignedUrlResult {
    url: string;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 48.38%" /><col style="width: 51.62%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>body</code></td><td>创建上传 URL 对象</td></tr><tr><td><code>options</code></td><td>创建上传 URL 额外参数</td></tr></tbody></table>

`UploadUrlBody` 类型说明：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 41.81%" /><col style="width: 58.19%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>该对象的 <code>key</code> ，不同对象 <code>key</code> 的值不能相同。</td></tr><tr><td><code>size</code></td><td>该对象文件的大小。</td></tr><tr><td><code>checksum</code></td><td>该对象文件的签名字符串。</td></tr><tr><td><code>checksum_type</code></td><td>该对象文件的签名方式。</td></tr></tbody></table>

`NosUploadUrlOptions` 类型说明：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 41.81%" /><col style="width: 58.19%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>overwrite</code></td><td>如果 <code>key</code> 已经存在，新上传的对象是否覆盖原有的对象文件，默认值： <code>false</code> 1. <code>true</code> 会覆盖 1. <code>false</code> 会报错： <code>key</code> 已经存在</td></tr></tbody></table>

### 返回值

返回值类型为 `PreSignedUrlResult` ，通过 `Promise` 返回，类型说明：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 48.38%" /><col style="width: 51.62%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>url</code></td><td>该对象准备上传文件的上传地址。</td></tr></tbody></table>

### 示例

```typescript
import { nos } from "@pc-nexus/storage";

const urlResult = await nos.createUploadUrl({
  key: "upload-file-1",
  size: 1024,
  checksum: "Cniua8PqLHwzRN7BGWWg7YpFDVVOJAToT9l8LQ2uysw=",
  checksum_type: "SHA256"
}, { overwrite: false });
const url = urlResult.url;
return url;
```

## createDownloadUrl

创建文件下载的 URL 地址。

### 函数签名

```typescript
function createDownloadUrl(key: string): Promise<PreSignedUrlResult>;

export interface PreSignedUrlResult {
    url: string;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 49.01%" /><col style="width: 50.99%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>对象的 <code>key</code></td></tr></tbody></table>

### 返回值

返回值类型为 `PreSignedUrlResult` ，通过 `Promise` 返回，类型说明：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 48.38%" /><col style="width: 51.62%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>url</code></td><td>该对象文件下载的 URL 地址。</td></tr></tbody></table>

### 示例

```javascript
import { nos } from "@pc-nexus/storage";

const urlResult = await nos.createDownloadUrl("upload-file-1");
const url = urlResult.url;
return url;
```

## getMetadata

获取对象的基本信息。

### 函数签名

```typescript
function getMetadata(key: string): Promise<ObjectMetadata>;

interface ObjectMetadata {
    key: string;
    name: string;
    mime_type?: string;
    checksum: string;
    size: number;
    created_at?: number;
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 49.01%" /><col style="width: 50.99%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>对象的 <code>key</code></td></tr></tbody></table>

### 返回值

返回值类型为 `ObjectMetadata` ，通过 `Promise` 返回，类型说明：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 48.38%" /><col style="width: 51.62%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>对象的 <code>key</code> 。</td></tr><tr><td><code>name</code></td><td>对象的文件名。</td></tr><tr><td><code>mime_type</code></td><td>对象的文件类型。</td></tr><tr><td><code>checksum</code></td><td>对象的文件签名。</td></tr><tr><td><code>size</code></td><td>对象的文件大小。</td></tr><tr><td><code>created_at</code></td><td>对象的创建时间戳。</td></tr></tbody></table>

### 示例

```typescript
import { nos } from "@pc-nexus/storage";

const metadata = await nos.getMetadata("upload-file-1");
return metadata;
```

## delete

删除对象。

### 函数签名

```typescript
function delete(key: string): Promise<void>;
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 49.01%" /><col style="width: 50.99%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>对象的 <code>key</code></td></tr></tbody></table>

### 返回值

空

### 示例

```typescript
import { nos } from "@pc-nexus/storage";

await nos.delete("upload-file-1");
```
