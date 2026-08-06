---
title: "帐号 - 个人设置"
lastUpdated: 2026-07-30T08:37:23.000Z
---

# 帐号 - 个人设置

个人帐号设置页面扩展模块，允许在个人帐号设置页面左侧添加自定义组件页面，该页面的访问地址为：

`/account/apps/{appId}/{envId}/{route}`

![image.png](../../../assets/726a4d53c16c9876f0826f7a23f93e9c24720312.png)

## 配置

配置结构：

```yaml
extensions []
├─ key (string) [Mandatory]
├─ target (string) [Mandatory]
├─ resolver {} [Mandatory]
├─ pages {} [Mandatory]
│  ├─ key (string) [Mandatory]
│  ├─ title (string | i18n) [Mandatory]
│  ├─ resource (string) [Mandatory]
│  └─ route (string) [Mandatory]
└─ section {} [Optional]
   ├─ header (string) [Mandatory]
   └─ enabled (boolean) [Optional]
```

配置示例：

```yaml
extensions:
  - key: example-personal-setting
    target: "pcm:global:personal:setting"
    resolver:
      function: resolver
    pages:
      - key: example-page
        title: Page title
        resource: main
        route: route-page
    section:
      header: Section Title
      enabled: true
```

## 属性

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 18.41%" /><col style="width: 17.76%" /><col style="width: 8.69%" /><col style="width: 55.14%" /></colgroup><thead><tr><th>属性</th><th>类型</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>resolver</code></td><td><code>{ function: string }</code>  或 <code>{ endpoint: string }</code></td><td>Y</td><td>定义扩展模块所使用的处理函数： - 指定后端处理函数时使用 <code>function</code> 属性 - 指定远程服务时使用 <code>endpoint</code> 属性</td></tr><tr><td><code>pages</code></td><td><code>array[]</code></td><td>Y</td><td>定义扩展模块所包括的页面</td></tr><tr><td><code>pages·key</code></td><td><code>string</code></td><td>Y</td><td>定义扩展模块所包括的页面的唯一标识</td></tr><tr><td><code>pages.title</code></td><td><code>string｜ i18n</code></td><td>Y</td><td>定义扩展模块所包括的页面的标题</td></tr><tr><td><code>pages.resource</code></td><td><code>string</code></td><td>Y</td><td>定义扩展模块所包括的页面使用的资源，内容为 <code>resources</code> 节点的资源引用</td></tr><tr><td><code>pages.route</code></td><td><code>string</code></td><td>Y</td><td>定义扩展模块具体页面的路由</td></tr><tr><td><code>section</code></td><td><code>object</code></td><td></td><td>定义扩展模块分组</td></tr><tr><td><code>section·header</code></td><td><code>string</code></td><td></td><td>定义扩展模块分组名称，如果不启用分组，则页面展示在默认分组 <code>应用</code> 下</td></tr><tr><td><code>section·enabled</code></td><td><code>boolean</code></td><td></td><td>定义扩展模块分组是否启用，默认 <code>false</code></td></tr></tbody></table>

## 扩展数据

当前模块可访问的扩展数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 29.94%" /><col style="width: 70.06%" /></colgroup><thead><tr><th>数据</th><th>说明</th></tr></thead><tbody><tr><td>无</td><td></td></tr></tbody></table>

## 限制

每个扩展模块对应的数量限制：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>扩展模块数量</td><td><code>1</code></td><td>单个应用可以声明的当前扩展模块最大数量</td></tr><tr><td>页面数量</td><td><code>8</code></td><td>单个当前模块下可以声明的页面数量</td></tr></tbody></table>

## 桥接方法

当前扩展模块不支持以下桥接方法，详情请参考 [view](/reference/interface/bridge/view) 。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 49.44%" /><col style="width: 50.56%" /></colgroup><thead><tr><th>桥接方法</th><th>支持</th></tr></thead><tbody><tr><td><code>view.refresh</code></td><td>❌</td></tr><tr><td><code>view.submit</code></td><td>❌</td></tr><tr><td><code>view.emitReadyEvent</code></td><td>❌</td></tr></tbody></table>
