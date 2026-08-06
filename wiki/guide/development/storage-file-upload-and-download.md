---
title: "使用 NOS 上传下载文件"
lastUpdated: 2026-07-15T14:06:07.000Z
---

# 使用 NOS 上传下载文件

本文档将详细介绍如何在 Nexus 应用中使用 `nos` 进行文件的上传和下载操作， `nos` 是Nexus 平台提供的对象存储服务，用于存储和管理应用的文件资源。

## 配置说明

使用 `nos` 时需要在 `manifest.yaml` 文件中添加数据存储作用域：

```yaml
permissions:
  scopes:
    - pcp:storage:app
```

## 文件上传

`nos` 采用预签名 URL 机制上传文件，流程如下：

**前端：**

1. 准备好上传的文件
1. 调用 SDK 上传 API 上传文件
1. 核心 API： `store.upload()`

**服务端：**

1. 提供获取上传预签名 URL的 Resolver 函数
1. 调用生成上传 URL 的方法，返回可直接访问的上传地址
1. 核心 API: `nos.createUploadUrl()`

### 前端实现

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

### 服务端实现

定义解析器函数，返回文件上传预签名 URL：

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
                            );

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
                        }), );
                    const presignedURLsToObjectMetadata: PresignedURLToObjectMetadataMap = {}; results.forEach((result) => {
                        presignedURLsToObjectMetadata[typeof result.presignedUrl === "string" ? result.presignedUrl : result.presignedUrl.url] =
                            result.metadata;
                    });

                    return presignedURLsToObjectMetadata;
                },
        );
```

## 文件下载

`nos` 采用预签名 URL 机制下载文件，流程如下：

**前端：**

1. 调用 SDK 下载 API 获取文件
1. 核心 API： `store.download()`

**服务端：**

1. 提供获取下载预签名 URL 的 Resolver 函数
1. 调用生成下载 URL 的方法，返回可直接访问的下载地址
1. 核心 API: `nos.createDownloadUrl()`

### 前端实现

```typescript
import { store } from '@pc-nexus/bridge';

async function downloadFiles() {
    const fileKeys = [
        'shared/documents/invoice-001.pdf',
        'shared/documents/invoice-002.pdf',
        'shared/documents/invoice-003.pdf'
    ];

    const results = await store.download(
        'filterAndGenerateDownloadUrls',
        fileKeys
    );

    console.log(results);
}
```

### 服务端实现

定义解析器函数，返回文件下载 URL：

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

关于对象存储详情请参考 [nos](/reference/functions/storage/nos) 。
