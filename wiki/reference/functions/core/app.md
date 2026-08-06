---
title: "app"
lastUpdated: 2026-07-28T06:38:05.000Z
---

# app

`app` 模块内置的方法可以获取应用的上下文详情，包括函数运行时所处的应用环境及版本

导入：

```typescript
import { app } from "@pc-nexus/core";
```

内置方法：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.74%" /><col style="width: 77.26%" /></colgroup><thead><tr><th>API</th><th>描述</th></tr></thead><tbody><tr><td><code>getContext</code></td><td>获取 Nexus 函数的上下文详情</td></tr></tbody></table>

## getContext

`getContext`  函数可获取 Nexus 函数的上下文详情，包括该函数运行时所处的应用环境及版本。

### 函数签名

```typescript
export declare function getContext(): NexusAppContext;

export interface NexusAppContext {
    app: {
        id: string;
        version: string;
    };
    environment: {
        id: string;
        type: EnvironmentType;
    };
    team: Team;
    installation: {
        id: string;
    };
    invocation: {
        id: string;
    };
    user?: User;
    extension?: Extension;
    event?: {
        trigger: {
          key: string; 
          type: string
        };
    };
}

export enum EnvironmentType {
    development = "development",
    production = "production",
}

export interface Team {
    id: string;
    url: string;
    locale: string;
    timezone: string;
}

export interface User {
    id: string;
    locale: string;
    timezone: string;
}

export interface Extension {
    key: string;
    local_id: string;
    target: string;
    location: string;
    data?: Record<string, unknown>;
}
```

### 参数

空

### 返回值

返回值类型为 `NexusAppContext` ，包含应用当前运行环境上下文信息的对象，可用的数据取决于应用所使用的模块。

#### app

定义当前应用数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前应用 ID</td></tr><tr><td><code>version</code></td><td>当前应用版本</td></tr></tbody></table>

#### team

定义当前应用安装的企业数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前应用安装的企业 ID</td></tr><tr><td><code>url</code></td><td>当前应用安装的企业访问地址</td></tr><tr><td><code>locale</code></td><td>当前应用安装的企业设置的语言</td></tr><tr><td><code>timezone</code></td><td>当前应用安装的企业设置的时区</td></tr></tbody></table>

#### installation

定义当前应用安装数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前应用安装时的唯一标识</td></tr></tbody></table>

#### invocation

定义当前调用的数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前调用的唯一标识</td></tr></tbody></table>

#### environment

定义当前应用所在环境数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前应用所在的环境 ID</td></tr><tr><td><code>type</code></td><td>当前应用所在的环境类型， <code>development</code> 还是 <code>production</code></td></tr></tbody></table>

#### user

定义当前用户数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前帐户所对应的用户 ID</td></tr><tr><td><code>locale</code></td><td>当前用户设置的语言</td></tr><tr><td><code>timezone</code></td><td>当前用户设置的时区</td></tr></tbody></table>

#### extension

定义扩展模块数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>扩展模块唯一标识，在 <code>manifest.yml.yaml</code>  文件定义</td></tr><tr><td><code>local_id</code></td><td>应用在当前页面的唯一 ID</td></tr><tr><td><code>target</code></td><td>扩展模块对应扩展点目标，即扩展模块在产品中出现的位置</td></tr><tr><td><code>location</code></td><td>当前页面的位置</td></tr><tr><td><code>data</code></td><td>扩展模块能够访问的上下文数据，与前端获取的上下文数据一致，详情参考 <a href="/reference/resource/context">上下文数据</a></td></tr></tbody></table>

#### event

定义事件订阅数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>trigger.key</code></td><td>触发器在 <code>manifest.yaml</code> 中定义的 <code>key</code></td></tr><tr><td><code>trigger.type</code></td><td>触发器类型</td></tr></tbody></table>

### 示例

以下是一段使用 `getContext` 方法获取的数据示例：

```typescript
{
    "app": {
        "id": "fe85a6b3-4073-4fd2-89e0-481a38ca5958",
        "version": "1.3.0"
    },
    "environment": {
        "id": "375cc666-98a7-4bf0-a85e-28085fe1772f",
        "type": "development"
    },
    "team": {
        "id": "5db7a0ed77c86b2d749605ad",
        "url": "https://your-domain.pingcode.com",
        "locale": "en-us",
        "timezone": "Asia/Shanghai"
    },
    "installation": {
        "id": "63dd9483-7652-4a2a-9fd7-15783380467b"
    },
    "invocation": {
        "id": "1a538371-7aea-4943-969b-d9c759a80baf"
    },
    "user": {
        "id": "52b9af20da8a4969aab88092d1fa64ce",
        "locale": "zh-cn",
        "timezone": "Asia/Shanghai"
    },
    "extension": {
        "key": "my-ship-page",
        "local_id": "fe85a6b3-4073-4fd2-89e0-481a38ca5958/375cc666-98a7-4bf0-a85e-28085fe1772f/my-ship-page",
        "target": "pcm:ship:product:page",
        "location": "https://your-domain.pingcode.com/ship/products/CPCWU/apps/fe85a6b3-4073-4fd2-89e0-481a38ca5958/375cc666-98a7-4bf0-a85e-28085fe1772f",
        "data": {
            "product": {
                "id": "68d4983fcd51c2d6113d79c6",
                "identifier": "CPCWU",
                "name": "产品测试"
            }
        }
    }
}
```
