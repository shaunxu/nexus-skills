---
title: "测试用例 - 详情后台脚本"
lastUpdated: 2026-07-15T16:25:44.000Z
---

# 测试用例 - 详情后台脚本

允许在测试用例详情页增加后台脚本，支持统一处理数据、状态和事件逻辑

## 配置

配置结构：

```yaml
extensions []
├─ key (string) [Mandatory]
├─ target (string) [Mandatory]
└─ resource (string) [Mandatory]
```

配置示例：

```yaml
extensions:
  - key: example-testcase-background
    target: "pcm:testhub:testcase:background"
    resource: main
```

## 属性

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 16.24%" /><col style="width: 16.95%" /><col style="width: 11.72%" /><col style="width: 55.09%" /></colgroup><thead><tr><th>属性</th><th>类型</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>resource</code></td><td><code>string</code></td><td>Y</td><td>定义扩展模块所使用的资源，内容为 <code>resources</code> 节点的资源引用</td></tr></tbody></table>

## 扩展数据

当前模块可访问的扩展数据：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.4%" /><col style="width: 72.6%" /></colgroup><thead><tr><th>数据</th><th>说明</th></tr></thead><tbody><tr><td><code>library</code></td><td>测试库数据 <a href="/reference/resource/context/library">library</a></td></tr><tr><td><code>testcase</code></td><td>测试用例数据 <a href="/reference/resource/context/testcase">testcase</a></td></tr></tbody></table>

## 限制

每个扩展模块对应的数量限制：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 27.12%" /><col style="width: 20.06%" /><col style="width: 52.82%" /></colgroup><thead><tr><th>资源</th><th>限制</th><th>说明</th></tr></thead><tbody><tr><td>扩展模块数量</td><td><code>8</code></td><td>单个应用可以声明的当前扩展模块最大数量</td></tr></tbody></table>

## 桥接方法

当前扩展模块不支持以下桥接方法，详情请参考 [view](/reference/interface/bridge/view) 。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 49.44%" /><col style="width: 50.56%" /></colgroup><thead><tr><th>桥接方法</th><th>支持</th></tr></thead><tbody><tr><td><code>view.setWindowTitle</code></td><td>❌</td></tr><tr><td><code>view.refresh</code></td><td>❌</td></tr><tr><td><code>view.createHistory</code></td><td>❌</td></tr><tr><td><code>view.submit</code></td><td>❌</td></tr></tbody></table>
