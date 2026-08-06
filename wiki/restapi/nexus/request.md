---
title: "调用方式"
lastUpdated: 2026-07-06T10:27:19.000Z
---

# 调用方式

Nexus APIs 支持使用标准的 HTTP 方法请求：

- `GET` / `DELETE` 方法：通过 `querystring` 传递参数
- `POST` / `PUT` / `PATCH` 方法：需要在 `headers` 中添加 `"content-type": "application/json"` ，然后通过 `body` 传递参数。

Nexus APIs 使用 [HTTP状态码](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml) 指示已执行操作的状态，使用 `response body` 传递数据。

## 数据结构

Nexus APIs 使用 `JSON` 作为通讯格式。

## 认证方式

调用接口时，需在 HTTP 请求的请求头中添加 `Authorization: Bearer {access_token}` 。

`access_token` 由 Nexus 平台随请求上下文 Headers 发送至 Remote 服务，可直接从请求 Headers 中读取。

## 响应格式

Nexus APIs 使用 [HTTP 状态码](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml) 指示已执行操作的状态；使用 `response.body` 传递数据。

### 成功

当请求成功时，会返回 `JSON` 格式的数据。

```
HTTP状态码：200
Body：
{
     "name": "名称",
     "created_at": 1578897962
}
```

### 错误

当请求失败时，会返回错误码和错误信息。

```
HTTP状态码：500
Body：
{
     "code": "100000",
     "message": "Internal Server Error"
}
```
