---
title: "空间 - 组件页面"
lastUpdated: 2026-07-30T08:45:53.000Z
---

# 空间 - 组件页面

空间组件页面扩展模块，允许在空间一级导航中添加自定义组件页面，该页面的访问地址为：

`/wiki/spaces/{identifier}/apps/{appId}/{envId}/{route}`

![空间｜组件页面.png](../../../assets/7961926820a48f1d98be89e72ef24024fe939404.png)

## 配置

配置结构：

```yaml
extensions []
├─ key (string) [Mandatory]
├─ target (string) [Mandatory]
├─ title (string | i18n) [Mandatory]
├─ resource (string) [Mandatory]
├─ resolver {} [Mandatory]
└─ route (string) [Mandatory]
```

配置示例：

```yaml
extensions:
  - key: hexample-space-page
    target: "pcm:wiki:space:page"
    title: Page title
    resource: main
    resolver:
      function: resolver
    route: route-page
```

## 属性

配置属性：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 16.24%" /><col style="width: 16.95%" /><col style="width: 11.72%" /><col style="width: 55.09%" /></colgroup><thead><tr><th>属性</th><th>类型</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>title</code></td><td><code>string \| i18n</code></td><td>Y</td><td>定义产品组件标题，显示在产品一级导航上</td></tr><tr><td><code>resource</code></td><td><code>string</code></td><td>Y</td><td>定义扩展模块所使用的资源，内容为 <code>resources</code> 节点的资源引用</td></tr><tr><td><code>resolver</code></td><td><code>{ function: string }</code>  或 <code>{ endpoint: string }</code></td><td>Y</td><td>定义扩展模块所使用的处理函数： - 指定后端处理函数时使用 <code>function</code> 属性 - 指定远程服务时使用 <code>endpoint</code> 属性</td></tr><tr><td><code>route</code></td><td><code>string</code></td><td></td><td>定义产品组件页面的路由</td></tr></tbody></table>

## 扩展数据

当前模块可访问的扩展数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.94%" /><col style="width: 70.06%" /></colgroup><thead><tr><th>数据</th><th>说明</th></tr></thead><tbody><tr><td><code>space</code></td><td>空间数据 <a href="/reference/resource/context/space">space</a></td></tr></tbody></table>

## 限制

每个扩展模块对应的数量限制：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.08%" /><col style="width: 24.29%" /><col style="width: 45.63%" /></colgroup><thead><tr><th>限制项</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>扩展模块数量</td><td><code>8</code></td><td>单个应用可以声明的当前扩展模块最大数量</td></tr></tbody></table>

## 桥接方法

当前扩展模块不支持以下桥接方法，详情请参考 [view](/reference/interface/bridge/view) 。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 49.44%" /><col style="width: 50.56%" /></colgroup><thead><tr><th>桥接方法</th><th>支持</th></tr></thead><tbody><tr><td><code>view.refresh</code></td><td>❌</td></tr><tr><td><code>view.submit</code></td><td>❌</td></tr><tr><td><code>view.emitReadyEvent</code></td><td>❌</td></tr></tbody></table>
