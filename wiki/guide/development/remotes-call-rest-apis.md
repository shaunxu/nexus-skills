---
title: "远程服务调用 REST APIs"
lastUpdated: 2026-07-06T08:57:08.000Z
---

# 远程服务调用 REST APIs

本文档详细阐述如何在远程服务中调用 PingCode APIs 和 Nexus APIs。 Nexus 应用可以配置向远程端点发送身份验证令牌，使得远程端点可以使用身份令牌向 PingCode 平台发起经过身份验证的回调。

## 调用流程

在远程服务中回调 PingCode APIs 时可以遵循以下流程：

- 获取 Nexus 调用令牌（NIT），并进行验证，确保上下文是可信任的
- 提取身份令牌，用于回调时的身份验证
- 向指定的 PingCode APIs 发起请求

## 使用示例

以下是一个使用 TypeScript 语言编写的远程服务示例，在该示例中获取来自 Nexus 平台的令牌信息，并回调创建工作项接口：

```javascript
import express, { Request, Response } from 
import fetch from 'node-fetch';          
import jwt, { JwtPayload } from 'jsonwebtoken';
import { createRemoteJWKSet, jwtVerify } from 'jose';

const app = express();
app.use(express.json());

// 1. 配置：Nexus JWKS 端点（替换为实际域名）
const JWKS_URL = 'https://your-nexus-host/api/nexus/nit/.well-known/jwks.json';
const JWKS = createRemoteJWKSet(new URL(JWKS_URL));

/**
 * 验证 Nexus 调用令牌（NIT）
 */
async function verifyNIT(authHeader: string): Promise<JwtPayload> {
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    throw new Error('Missing or invalid Authorization header');
  }

  const token = authHeader.slice(7); // 去掉 "Bearer "

  // 使用 jose 验证 RS256 签名、aud、iss、exp
  const { payload } = await jwtVerify(token, JWKS, {
    audience: 'nexus',
    issuer: 'nexus/invocation-token',
  });

  return payload as JwtPayload;
}

// 2. 远程服务端点示例
app.post('/compute', async (req: Request, res: Response) => {
  // 步骤 A：验证 NIT，确保请求来自 Nexus
  const context = await verifyNIT(req.headers.authorization || '');
  console.log('NIT verified, context:', context);

  // 步骤 B：提取用于调用 PingCode REST API 的令牌
  const appToken = req.headers['x-nexus-app-token'] as string | undefined;

  // 步骤 C：构造 PingCode REST API 请求
  const pingcodeBaseUrl = req.headers['x-nexus-api-base-url'] as string;
  const apiUrl = `${pingcodeBaseUrl}/v1/pjm/work_items`;

  // 创建工作项的请求体（示例）
  const workitemPayload = {
    title: '新任务',
    description: '由 Nexus 远程服务创建',
    type_id: 'some-type-id',
  };

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${appToken}`, 
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(workItemPayload),
  });

  const result = await response.json();
  res.json({ success: true, data: result });
});
```
