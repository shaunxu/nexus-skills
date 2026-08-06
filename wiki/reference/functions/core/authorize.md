---
title: "authorize"
lastUpdated: 2026-07-14T02:53:05.000Z
---

# authorize

`authorize` 模块可以帮助你在执行具体的操作前，验证用户的权限。

导入：

```typescript
import { authorize } from "@pc-nexus/core";
```

内置方法：

|API|描述|
|---|---|
|`getPermissionPoints`|获取系统中所有可用的权限点定义|
|`getUserPermissions`|获取指定用户在全局或某个具体资源上的权限列表|

## getPermissionPoints

`getPermissionPoints` 函数返回系统预定义的全部权限点，即各子产品中用户可被授予的操作许可的完整列表。

### 函数签名

```typescript
function getPermissionPoints(): Promise<PermissionPointsResult>;

type PermissionPointsResult = Record<string, PermissionPoint[]>

interface PermissionPoint {
    key: string;
    name: string;
    group: string;
}
```

### 参数

空

### 返回值

返回以分组名为 key 的 `PermissionPointsResult` 对象，每个 key 对应该分组下的权限点数组：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 24.29%" /><col style="width: 75.71%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>权限点唯一标识</td></tr><tr><td><code>name</code></td><td>权限点的展示名称</td></tr><tr><td><code>group</code></td><td>权限点在所属分组内的子分类</td></tr></tbody></table>

### 示例

```typescript
import { authorize } from "@pc-nexus/core";

const allPoints = await authorize.getPermissionPoints();
console.log(allPoints);
```

## getUserPermissions

`getUserPermissions` 函数返回指定用户在全局或某个具体资源上拥有的权限列表。

- 传入 `"global"` 作为类型时，返回不依附于任何具体资源的全局权限（如"创建项目"、"管理成员"等）。
- 传入具体资源类型（如 `"project"` 、 `"library"` 等）时，返回该用户在指定资源上的权限。资源类型涵盖 Pilot 资源（产品、项目、测试库、知识库）和 Principal 资源（需求、工单、工作项、测试用例、页面）。

### 函数签名

```typescript
// 获取全局权限
function getUserPermissions(type: "global", userId?: string): Promise<UserPermission[]>;

// 获取权限
function getUserPermissions(type: ResourceType, id: string, userId?: string): Promise<UserPermission[]>;

type PilotType    = "product" | "project" | "library" | "space";
type PrincipalType = "idea" | "ticket" | "workitem" | "testcase" | "page";
type ResourceType  = PilotType | PrincipalType;

interface UserPermission {
    key: string;           
    has_permission: boolean; 
}
```

### 参数

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.4%" /><col style="width: 72.6%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>type</code></td><td><code>"global"</code> 表示全局权限；或具体资源类型：Pilot 类型（ <code>product</code> / <code>project</code> / <code>library</code> / <code>space</code> ）或 Principal 类型（ <code>idea</code> / <code>ticket</code> / <code>workitem</code> / <code>testcase</code> / <code>page</code> ）。</td></tr><tr><td><code>id</code></td><td>资源的唯一 ID。仅在 <code>type</code> 为资源类型时需要传入。</td></tr><tr><td><code>userId</code></td><td>目标用户的 ID。不传时默认使用当前调用上下文中的登录用户。</td></tr></tbody></table>

### 返回值

返回 `UserPermission[]` 数组，每项表示该用户对某个权限点的拥有情况：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.26%" /><col style="width: 72.74%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>权限点唯一标识</td></tr><tr><td><code>has_permission</code></td><td><code>true</code> 表示用户拥有该权限， <code>false</code> 表示没有</td></tr></tbody></table>

### 示例

```typescript
import { authorize } from "@pc-nexus/core";

// 获取当前登录用户的全局权限
const myPermissions = await authorize.getUserPermissions("global");
console.log(myPermissions);

// 获取指定用户的全局权限
const permissions = await authorize.getUserPermissions("global", "user-id-123");
const canCreateProject = permissions.find(p => p.key === "pca:global:pjm:project:create")?.has_permission ?? false;
console.log(canCreateProject); 

// 获取当前登录用户在指定项目上的权限
const projectPermissions = await authorize.getUserPermissions("project", "project-id-abc");
console.log(projectPermissions);

// 获取指定用户在某个工作项上的权限
const workitemPermissions = await authorize.getUserPermissions(
    "workitem",
    "workitem-id-xyz",
    "user-id-123",
);
const canEdit = workitemPermissions.find(p => p.key === "pca:pjm:task:edit")?.has_permission ?? false;
console.log(canEdit);
```

## 错误处理

发生错误时响应都会附带一个包含更多信息的错误代码，下面列出了所有可能的错误代码、它们的含义以及可以采取哪些措施来解决。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.62%" /><col style="width: 66.38%" /></colgroup><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td><code>ERR_</code></td><td></td></tr></tbody></table>
