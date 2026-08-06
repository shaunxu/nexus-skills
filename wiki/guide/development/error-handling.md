---
title: "错误处理"
lastUpdated: 2026-07-10T09:50:02.000Z
---

# 错误处理

本文档详细阐述如何在 Nexus 平台中进行错误处理。

## 错误格式

发生错误时响应都会附带一个包含更多信息的错误代码，结构如下：

```typescript
interface NexusError {
  code: string;
  message: string;
}
```

示例：

```javascript
{
  "code": "ERR_REMOTE_INVALID_KEY",
  "message": "Invalid remote key format"
}
```

属性说明：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 28.39%" /><col style="width: 71.61%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>code</code></td><td>错误码，通过错误码可以在参考引用中查看详细的含义及解决方法</td></tr><tr><td><code>message</code></td><td>错误消息，用一句话描述当前是什么错误及可能的解决方法</td></tr></tbody></table>

更详细的错误码及其含义，请查看相关模块 SDK 的参考引用。

## 错误处理

下面是一个错误处理的示例：

```typescript
try { 
  // 处理业务逻辑
} 
catch (error) { 
  
  console.error(`${error.code} : ${error.message}`);
  
  if (error.code === "ERR_REMOTE_INVALID_KEY") { 
    // Handling error.
  } 
}
```
