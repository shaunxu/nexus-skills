---
title: "router"
lastUpdated: 2026-07-06T03:38:29.000Z
---

# router

`router` 对象允许你将 PingCode 应用导航到另一个页面。

导入：

```typescript
import { router } from '@pc-nexus/bridge';
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 26.41%" /><col style="width: 73.59%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>navigate</code></td><td>在当前 tab 标签中导航到某个页面</td></tr><tr><td><code>open</code></td><td>根据用户的浏览器配置，会在新的标签页或窗口中打开页面</td></tr><tr><td><code>generateUrl</code></td><td>根据 NavigationLocation 对象生成对应的 Url</td></tr><tr><td><code>reload</code></td><td>重新加载当前页面</td></tr></tbody></table>

## navigate

`navigate` 方法允许你在当前 tab 标签中导航到某个页面。

### **函数签名**

```typescript
function navigate(urlOrLocation: string | NavigationLocation): Promise<void>;
```

### **参数**

|名称|描述|
|---|---|
|`urlOrLocation`|支持传入 `url` 或者 `NavigationLocation` 进行导航|

`NavigationLocation` 定义如下：

|名称|描述|
|---|---|
|`id`|目标对象 `id`|
|`target`|目标对象值， `NavigationTarget` 枚举类型|

`NavigationTarget` 定义如下

```typescript
enum NavigationTarget {
    Workitem = "workitem", // 工作项详情
    Testcase = "testcase", // 测试用例详情
    Page = "page",         // wiki 页面
    Idea = "idea",         // 需求详情
    Ticket = "ticket",     // 工单详情
    Project = "project",   // 项目详情
    Library = "library",   // 测试库详情
    Space = "space",       // 空间详情
    Product = "product",   // 产品详情
}
```

### 返回值

空

### 示例

```typescript
import { router, NavigationTarget } from '@pc-nexus/bridge';

router.navigate('/pjm/workitems/123');

router.navigate('https://www.baidu.com/');

router.navigate({target: NavigationTarget.workItem, id: '123'});
```

## **open**

`open` 方法允许你在新标签页或窗口中打开页面，具体取决于你的浏览器配置。

### **函数签名**

```typescript
function open(urlOrLocation: string | NavigationLocation): Promise<void>;
```

### **参数**

|名称|描述|
|---|---|
|`urlOrLocation`|支持传入 `url` 或者 `NavigationLocation` 打开页面|

### 返回值

空

### 示例

```typescript
import { router, NavigationTarget } from '@pc-nexus/bridge';

router.open('/pjm/workitems/123');

router.open('https://www.baidu.com/');

router.open({target: NavigationTarget.workItem, id: '123'});
```

## **generateUrl**

`generateUrl` 方法允许你检索给定 `NavigationLocation` 对象的 URL。

### **函数签名**

```typescript
function generateUrl(location: NavigationLocation): Promise<URL>;
```

### **参数**

|名称|描述|
|---|---|
|`location`|目标 `url` 的 `NavigationLocation` 对象|

### 返回值

`URL` ，参见 [URL](https://developer.mozilla.org/en-US/docs/Web/API/URL) 规范定义。

### 示例

```typescript
import { router, NavigationTarget } from '@pc-nexus/bridge';

const URL = router.generateUrl({target: NavigationTarget.workItem, id: '123'});
// /pjm/workitems/123
console.log(url.pathname);
// https://<your-team>.pingcode.com/pjm/workitems/123
console.log(url.toString());
```

## **reload**

`reload` 方法允许你重新加载当前页面

### **函数签名**

```typescript
function reload(): Promise<void>
```

### **参数**

空

### **返回值**

空

### 示例

```typescript
import { router } from '@pc-nexus/bridge';

router.reload();
```
