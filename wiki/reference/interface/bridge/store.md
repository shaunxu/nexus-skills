---
title: "store"
lastUpdated: 2026-07-14T09:59:59.000Z
---

# store

`store` 提供文件上传、下载、获取元数据和删除功能。通过预签名 URL 机制与服务端进行安全的文件传输。

导入:

```typescript
import { store } from '@pc-nexus/store';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.73%" /><col style="width: 64.27%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>upload</code></td><td>将一个或多个文件/Blob 对象上传到对象存储服务</td></tr><tr><td><code>download</code></td><td>根据文件键名从对象存储服务下载文件</td></tr><tr><td><code>getMetadata</code></td><td>获取指定文件的元数据信息</td></tr><tr><td><code>delete</code></td><td>从对象存储服务中删除指定文件</td></tr></tbody></table>

## upload

`upload` 将一个或多个文件/Blob 对象上传到对象存储服务。

### **函数签名**

```typescript
function upload(functionKey: string, objects: (File | Blob)[]): Promise<UploadResult[]>;
  
interface UploadResult {
    success: boolean;
    key: string;
    status?: number;
    error?: string;
}
```

### **参数**

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.08%" /><col style="width: 69.92%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>functionKey</code></td><td>用于获取预签名 URL 的函数标识</td></tr><tr><td><code>objects</code></td><td>待上传的文件或 Blob 对象数组，不能为空</td></tr></tbody></table>

### **返回值**

返回值类型为 `Promise<UploadResult[]>`

`UploadResult` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 34.32%" /><col style="width: 65.68%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>success</code></td><td>上传是否成功</td></tr><tr><td><code>key</code></td><td>文件在存储中的键名</td></tr><tr><td><code>status</code></td><td>HTTP 状态码</td></tr><tr><td><code>error</code></td><td>错误信息（仅失败时存在）</td></tr></tbody></table>

### **示例**

**客户端调用 ：**

```typescript
import { store } from '@pc-nexus/bridge';

async function uploadFiles() {
  const fileInput = document.getElementById('fileInput') as HTMLInputElement;
  const files = Array.from(fileInput.files || []);

  const results = await store.upload(
    'filterAndGenerateUploadUrls',
    files
  )

  console.log(results);
}
```

**服务端 Resolver ：**

```typescript
import {
    GenerateUploadUrlPayload,
    nos,
    PreSignedUrlResult,
    PresignedURLToObjectMetadataMap,
} from "@pc-nexus/storage";

function generateTimestampKey(metadata: GenerateUploadUrlPayload, userId: string): string {
    const timestamp = Date.now();
    return `user-${userId}/${timestamp}`;
}

resolver.define(
    "filterAndGenerateUploadUrls",
    async (context: NexusAppContext, payload: GenerateUploadUrlPayload[]): Promise < PresignedURLToObjectMetadataMap > => {
        const userId = context.user?.id;
        const results = await Promise.all(
            payload.map(async (metadata) => {
                const {
                    checksum,
                    checksum_type,
                    size
                } = metadata;
                const key = generateTimestampKey(metadata, userId as string);
                const presignedUrl: PreSignedUrlResult = await nos.createUploadUrl({
                    key,
                    size,
                    checksum,
                    checksum_type
                }, {
                    overwrite: false,
                });

                return {
                    presignedUrl,
                    metadata: {
                        key,
                        size,
                        checksum,
                        checksum_type,
                        overwrite: false,
                    },
                };
            }),
        );
        const presignedURLsToObjectMetadata: PresignedURLToObjectMetadataMap = {};
        results.forEach((result) => {
            presignedURLsToObjectMetadata[typeof result.presignedUrl === "string" ? result.presignedUrl : result.presignedUrl.url] =
                result.metadata;
        });

        return presignedURLsToObjectMetadata;
    },
);
```

## download

`download` 根据文件键名从对象存储服务下载文件。

### **函数签名**

```typescript
function download(functionKey: string, keys: string[]): Promise<DownloadResult[]>;

interface DownloadResult {
    success: boolean;
    key: string;
    blob?: Blob;
    name?: string;
    status?: number;
    error?: string;
}
```

### **参数**

|名称|描述|
|---|---|
|`functionKey`|用于获取下载 URL 的函数标识|
|`keys`|待下载文件的键名数组，不能为空|

### **返回值**

返回值类型为 `Promise<DownloadResult[]>`

`DownloadResult` 类型定义如下：

|名称|描述|
|---|---|
|`success`|下载是否成功|
|`key`|文件在对象存储中的唯一键名/路径|
|`blob`|下载的文件内容（仅成功时存在）|
|`name`|文件名|
|`status`|HTTP 状态码|
|`error`|错误信息（仅失败时存在）|

### **示例**

**客户端调用 ：**

```typescript
import { store } from '@pc-nexus/bridge';

async function download() {
    const fileKeys = [
        'shared/documents/invoice-001.pdf',
        'shared/documents/invoice-002.pdf',
        'shared/documents/invoice-003.pdf',
    ];
    const result = await store.download('filterAndGenerateDownloadUrls', fileKeys);
    console.log('download result', result);
}


```

**服务端 Resolver ：**

```typescript
import {
    nos,
    PreSignedUrlResult,
    PresignedURLToObjectKeyMap
} from "@pc-nexus/storage";

resolver.define(
    "filterAndGenerateDownloadUrls",
    async (context: NexusAppContext, payload: string[]): Promise < PresignedURLToObjectKeyMap > => {
        const userId = context.user?.id;
        const results = await Promise.all(
            payload
            .filter((key) => key.startsWith(`user-${userId}/`) || key.startsWith("shared/"))
            .map(async (key) => {
                const downloadUrl: PreSignedUrlResult = await nos.createDownloadUrl(key);
                return {
                    downloadUrl,
                    key
                };
            }),
        );
        const downloadUrlsToKeys: PresignedURLToObjectKeyMap = {};
        results.forEach((result) => {
            downloadUrlsToKeys[result.downloadUrl.url] = result.key;
        });
        return downloadUrlsToKeys;
    },
);
```

## getMetadata 

`getMetadata` 获取指定文件的元数据信息。

### **函数签名**

```typescript
function getMetadata(functionKey: string, keys: string[]): Promise<GetMetadataResult[]>;

export interface GetMetadataResult {
    key: string;
    name: string;
    mime_type: string;
    checksum: string;
    size: number;
    created_at: string;
    error?: string;
}
```

### **参数**

|名称|描述|
|---|---|
|`functionKey`|用于获取元数据的函数标识|
|`keys`|待查询的文件键名数组，不能为空|

### **返回值**

返回值类型为 `Promise<GetMetadataResult[]>`

`GetMetadataResult` 类型定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.31%" /><col style="width: 64.69%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>文件在对象存储中的唯一键名/路径</td></tr><tr><td><code>name</code></td><td>文件名</td></tr><tr><td><code>mime_type</code></td><td>文件的 MIME 类型（如 image/jpeg 、 application/pdf ）</td></tr><tr><td><code>checksum</code></td><td>文件的校验和值（通常为 SHA256 编码）</td></tr><tr><td><code>size</code></td><td>文件大小</td></tr><tr><td><code>created_at</code></td><td>文件创建时间</td></tr><tr><td><code>error</code></td><td>错误信息（仅失败时存在）</td></tr></tbody></table>

### **示例**

**客户端调用 ：**

```typescript
import { store } from '@pc-nexus/bridge';

async function getObjectMetadata() {
    const fileKeys = [
        'shared/documents/report-2025.pdf',
        'shared/documents/invoice-001.pdf',
        'shared/images/logo.png',
        'shared/videos/tutorial.mp4',
        'shared/data/export.json',
    ];

    const result = await store.getMetadata('getObjectMetadata', fileKeys);
    console.log('get metadata result', result);
}
```

**服务端 Resolver ：**

```typescript
import { nos, ObjectMetadata } from "@pc-nexus/storage";

resolver.define < string > ("getObjectMetadata", async (context: NexusAppContext, payload: string): Promise < ObjectMetadata > => {
    const object: ObjectMetadata = await nos.getMetadata(payload);
    return object;
});
```

## delete

`delete` 从对象存储服务中删除指定文件。

### **函数签名**

```typescript
function delete(functionKey: string, keys: string[]): Promise<void>;
```

### **参数**

|名称|描述|
|---|---|
|`functionKey`|用于删除文件的函数标识|
|`keys`|待删除文件的键名数组，不能为空|

### **返回值**

空

### **示例**

**客户端调用 ：**

```typescript
import { store } from '@pc-nexus/bridge';

async function delete() {
    const fileKeys = [
        'shared/documents/report-2025.pdf',
        'shared/documents/invoice-001.pdf',
        'shared/images/logo.png',
        'shared/videos/tutorial.mp4',
        'shared/data/export.json',
    ];
    const result = await store.delete('deleteObject', fileKeys);
    console.log('delete result', result);
}

```

**服务端 Resolver ：**

```typescript
import { nos } from "@pc-nexus/storage";

resolver.define < string > ("deleteObject", async (context: NexusAppContext, payload: string) => {
    await nos.delete(payload);
    return null;
});
```
