---
title: "Capability APIs"
lastUpdated: 2026-07-14T07:36:27.000Z
---

# Capability APIs

业务能力提供了一系列 APIs，能够帮助开发者直接调用 PingCode 产品能力，而无需重复开发，包括发送通知消息、选择企业成员、打开进程管理器等。

## 安装

```powershell
npm install @pc-nexus/capabilities
```

使用

```typescript
import { notify } from '@pc-nexus/capabilities';

import { user } from '@pc-nexus/capabilities';
```

## APIs

目前提供的业务能力 APIs 如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.15%" /><col style="width: 66.85%" /></colgroup><thead><tr><th>APIs</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/interface/capabilities/notify">notify</a></td><td>提供应用能够打开与 PingCode 风格一致的通知信息</td></tr><tr><td><a href="/reference/interface/capabilities/user">user</a></td><td>提供选择企业成员组件</td></tr><tr><td><a href="/reference/interface/capabilities/processor">processor</a></td><td>提供应用打开进程管理器组件</td></tr><tr><td><a href="/reference/interface/capabilities/workitem">workitem</a></td><td>提供应用打开工作项创建、详情弹窗组件</td></tr><tr><td><a href="/reference/interface/capabilities/idea">idea</a></td><td>提供应用打开需求创建、详情弹窗组件</td></tr><tr><td><a href="/reference/interface/capabilities/ticket">ticket</a></td><td>提供应用打开工单创建、详情弹窗组件</td></tr><tr><td><a href="/reference/interface/capabilities/testcase">testcase</a></td><td>提供应用打开测试用例创建、详情弹窗组件</td></tr><tr><td><a href="/reference/interface/capabilities/page">page</a></td><td>提供应用打开页面创建、详情弹窗组件</td></tr><tr><td><a href="/reference/interface/capabilities/richtext">richtext</a></td><td>提供富文本展示和编辑组件</td></tr></tbody></table>
