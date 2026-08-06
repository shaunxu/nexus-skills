---
title: "上下文数据"
lastUpdated: 2026-07-15T11:40:56.000Z
---

# 上下文数据

本文档详细定义了上下文数据的格式。通过桥接方法中的 `view.getContext` 方法可以让你在扩展应用中获取上下文信息，同时也可以使用这些上下文数据中的属性，对扩展模块的显示设置条件。

## 数据示例

上下文示例数据：

```javascript
{
  "app": {
    "id": "4abd2038-a42c-49a1-b98c-ae04e29bf57a",
    "version": "1.0.0"
  },
  "team": {
    "id": "5db7a0ed77c86b2d749605ad",
    "url": "http://at.alpha.pingcode.live",
    "locale": "en-us",
    "timezone": "Asia/Shanghai"
  },
  "installation": {
    "id": "8158c947-a68e-4276-9b13-45f67bea4e05"
  },
  "environment": {
    "id": "adc783ac-4b53-4f9b-a7b4-a6bc5d2c99ff",
    "type": "development"
  },
  "user": {
    "id": "52b9af20da8a4969aab88092d1fa64ce",
    "locale": "zh-cn",
    "timezone": "Asia/Shanghai"
  },
  "extension": {
    "key": "my-first-hello-world",
    "local_id": "4abd2038-a42c-49a1-b98c-ae04e29bf57a/adc783ac-4b53-4f9b-a7b4-a6bc5d2c99ff/my-first-hello-world",
    "target": "pcm:pjm:project:page",
    "location": "http://your-domain.pingcode.com/pjm/projects/GON/apps/4abd2038-a42c-49a1-b98c-ae04e29bf57a/adc783ac-4b53-4f9b-a7b4-a6bc5d2c99ff/page1",
    "data": {
      "project": {
        "id": "69266c6db410a5e2b9eacf3f",
        "identifier": "NEXUS",
        "name": "NEXUS 开发项目",
        "type": "scrum"
      }
    }
  }
}
```

## 属性

返回的数据中包含应用当前运行环境上下文信息的对象，可用的数据取决于应用所使用的模块。

### app

定义当前应用数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前应用 ID</td></tr><tr><td><code>version</code></td><td>当前应用版本</td></tr></tbody></table>

### team

定义当前应用安装的企业数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前应用安装的企业 ID</td></tr><tr><td><code>url</code></td><td>当前应用安装的企业访问地址</td></tr><tr><td><code>locale</code></td><td>当前应用安装的企业设置的语言</td></tr><tr><td><code>timezone</code></td><td>当前应用安装的企业设置的时区</td></tr></tbody></table>

### installation

定义当前应用安装数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前应用安装时的唯一标识</td></tr></tbody></table>

### environment

定义当前应用所在环境数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前应用所在的环境 ID</td></tr><tr><td><code>type</code></td><td>当前应用所在的环境类型， <code>development</code> 还是 <code>production</code></td></tr></tbody></table>

### user

定义当前用户数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>当前帐户所对应的用户 ID</td></tr><tr><td><code>locale</code></td><td>当前用户设置的语言</td></tr><tr><td><code>timezone</code></td><td>当前用户设置的时区</td></tr></tbody></table>

### extension

定义扩展模块数据

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.52%" /><col style="width: 70.48%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>扩展模块唯一标识，在 <code>manifest.yml</code>  文件定义</td></tr><tr><td><code>local_id</code></td><td>应用在当前页面的唯一 ID</td></tr><tr><td><code>target</code></td><td>扩展模块对应扩展点目标，即扩展模块在产品中出现的位置</td></tr><tr><td><code>location</code></td><td>当前页面的位置</td></tr><tr><td><code>data</code></td><td>扩展模块能够访问的上下文数据，详见下节「扩展数据」</td></tr></tbody></table>

## 扩展数据

`extension.data` 属性中根据扩展模块的不同，会提供不同的扩展数据：

```javascript
{
  "extension": {
    "data": {
      "project": {
         "id": "69266c6db410a5e2b9eacf3f",
         "identifier": "NEXUS",
         "name": "NEXUS 开发项目",
         "type": "scrum"
      }
    }
  }
}
```

扩展数据的定义如下，每个扩展模块可以使用哪些扩展数据请参考详细的扩展模块说明：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.32%" /><col style="width: 40.11%" /><col style="width: 37.57%" /></colgroup><thead><tr><th>数据</th><th>描述</th><th>参考</th></tr></thead><tbody><tr><td><code>project</code></td><td>项目数据</td><td><a href="/reference/resource/context/project">project</a></td></tr><tr><td><code>product</code></td><td>产品数据</td><td><a href="/reference/resource/context/product">product</a></td></tr><tr><td><code>space</code></td><td>空间数据</td><td><a href="/reference/resource/context/space">space</a></td></tr><tr><td><code>library</code></td><td>测试库数据</td><td><a href="/reference/resource/context/library">library</a></td></tr><tr><td><code>idea</code></td><td>需求数据</td><td><a href="/reference/resource/context/idea">idea</a></td></tr><tr><td><code>ticket</code></td><td>工单数据</td><td><a href="/reference/resource/context/ticket">ticket</a></td></tr><tr><td><code>workitem</code></td><td>工作项数据</td><td><a href="/reference/resource/context/workitem">workitem</a></td></tr><tr><td><code>page</code></td><td>页面数据</td><td><a href="/reference/resource/context/page">page</a></td></tr><tr><td><code>testcase</code></td><td>测试用例数据</td><td><a href="/reference/resource/context/testcase">testcase</a></td></tr><tr><td><code>testplan</code></td><td>测试计划数据</td><td><a href="/reference/resource/context/testplan">testplan</a></td></tr><tr><td><code>sprint</code></td><td>迭代数据</td><td><a href="/reference/resource/context/sprint">sprint</a></td></tr><tr><td><code>baseline</code></td><td>基线数据</td><td><a href="/reference/resource/context/baseline">baseline</a></td></tr><tr><td><code>release</code></td><td>发布数据</td><td><a href="/reference/resource/context/release">release</a></td></tr><tr><td><code>plan</code></td><td>产品计划</td><td><a href="/reference/resource/context/plan">plan</a></td></tr><tr><td><code>widget</code></td><td>部件数据</td><td><a href="/reference/resource/context/widget">widget</a></td></tr><tr><td><code>dashboard</code></td><td>仪表盘数据</td><td><a href="/reference/resource/context/dashboard">dashboard</a></td></tr><tr><td><code>entry</code></td><td>资源入口数据</td><td><a href="/reference/resource/context/entry">entry</a></td></tr></tbody></table>
