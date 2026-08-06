---
title: "调用前端业务能力"
lastUpdated: 2026-07-17T08:54:30.000Z
---

# 调用前端业务能力

本指南详细阐述如何在 Nexus 应用中直接调用 PingCode 产品提供的前端业务能力，例如打开选择成员弹窗、打开工作项详情等，而无需重复编写代码。

## 选择成员

通过  `user`  模块打开成员选择器，支持模态弹窗（Dialog）或下拉菜单（Popover）两种形式。

### 调用流程

1. 从  `@pc-nexus/capabilities`  引入  `user`
1. 调用  `user.openDialog()`  或  `user.openPopover()`
1. 在  `onConfirm`  回调中获取选中的成员 ID 和用户信息

### 使用示例

打开模态对话框选择成员，适用于选择成员数量比较多的场景：

```typescript
import { user, UserInfo } from '@pc-nexus/capabilities';

async function openMemberDialog() {
  const ref = await user.openDialog({
    title: '选择成员',
    selection: ['user-id-1'],
    onConfirm: async (ids?: string[], users?: UserInfo[]) => {},
    onClose: () => {},
  });
}
```

打开下拉菜单选择成员，适用于快速选择成员，如分配负责人等场景：

```typescript
import { user, UserInfo } from '@pc-nexus/capabilities';

async function openMemberPopover(event: MouseEvent) {
  await user.openPopover({
    origin: event.currentTarget as HTMLElement,
    multiple: true,
    selection: ['user-id-1', 'user-id-2'],
    onConfirm: async (ids?: string[], users?: UserInfo[]) => {},
  });
}
```

## 工作项详情

通过  `workitem`  模块可以调用工作项详情页。

### 调用流程

1. 从  `@pc-nexus/capabilities`  引入  `workitem`
1. 调用  `workitem.openDetail(identifier)` ，传入 `identifier` 。

### 使用示例

可以使用工作项标识或者 ID 打开详情页：

```typescript
import { workitem } from '@pc-nexus/capabilities';

async function openWorkItemDetail() {
  await workitem.openDetail('GON-24');
}
```

打开 PingCode 中其他业务对象的详情，与打开工作项详情类似，如产品需求、工单等。详情信息请参考 [Capability APIs](/reference/interface/capabilities) 。
