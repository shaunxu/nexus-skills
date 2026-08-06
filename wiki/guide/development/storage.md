---
title: "数据存储"
lastUpdated: 2026-06-23T07:35:56.000Z
---

# 数据存储

Nexus 平台提供了多种存储应用数据的方式：

- 托管存储
- REST APIs 存储
- 远程存储

通过这些存储方式，你可以自由的根据应用需求安全地持久化存储和检索数据。

## 托管存储

推荐使用托管存储方式来保存应用的数据，这样可以专注于解决需求，无需关注基础设施。托管存储支持以下三种数据的存储与检索：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 35.17%" /><col style="width: 64.83%" /></colgroup><thead><tr><th>参考</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/functions/storage/kvs">kvs</a></td><td>键-值对存储，适合存储简单数据，如用户偏好、应用配置等</td></tr><tr><td><a href="/reference/functions/storage/ces">ces</a></td><td>自定义实体存储，适合自定义数据结构，存储结构化数据</td></tr><tr><td><a href="/reference/functions/storage/nos">nos</a></td><td>对象存储，适合存储非结构化数据或者二进制数据，如文件、图片、媒体等</td></tr></tbody></table>

关于使用托管存储的更多详情请参考：

- [使用 KVS 存储偏好数据](/guide/development/storage-kvs-store-preference-data)
- [使用 CES 存储结构化数据](/guide/development/storage-ces-store-structured-data)
- [使用 NOS 上传下载文件](/guide/development/storage-file-upload-and-download)

## REST APIs 存储

应用还可以使用 PingCode 提供的 REST APIs 来存储和检索企业数据，如项目数据、工作项数据等，这些数据可供企业内安装的所有应用以及用户访问。更多详情请参考：

- [前端调用 REST APIs](/guide/development/network-calling-apis-from-frontend)
- [服务端调用 REST APIs](/guide/development/network-calling-apis-from-backend)

## 远程存储

Nexus 允许你将应用与其他平台托管的服务进行集成，这使得 Nexus 应用能够将数据远程存储在自托管数据库或第三方存储服务上。更多详情请参考：

- [前端调用远程服务](/guide/development/remotes-calling-from-frontend)
- [服务端调用远程服务](/guide/development/remotes-calling-from-function)
