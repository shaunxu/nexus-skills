---
title: "扩展模块"
lastUpdated: 2026-07-16T07:10:52.000Z
---

# 扩展模块

本文档详细定义 Nexus 平台中支持的扩展模块。扩展模块是在应用的 `manifest.yaml` 文件中定义的组件，它通过定义与 PingCode 产品内扩展点相对应的属性和行为，来规定你的应用如何与产品集成。

扩展模块应用场景：

- 扩展功能：为 PingCode 产品添加自定义功能与集成
- 与 APIs 交互：利用 PingCode APIs 来增强应用能力
- 自定义用户界面：修改和扩展 UI 以适应您应用的需求

## 模块定义

以下为 Nexus 平台目前支持的扩展模块及其详细定义。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 32.2%" /><col style="width: 67.8%" /></colgroup><thead><tr><th>分类</th><th>描述</th></tr></thead><tbody><tr><td><a href="/reference/resource/extensions/global">全局扩展</a></td><td>定义 PingCode 产品中全局扩展模块</td></tr><tr><td><a href="/reference/resource/extensions/ship">产品管理</a></td><td>定义 PingCode 产品中产品管理扩展模块</td></tr><tr><td><a href="/reference/resource/extensions/pjm">项目管理</a></td><td>定义 PingCode 产品中项目管理扩展模块</td></tr><tr><td><a href="/reference/resource/extensions/wiki">知识管理</a></td><td>定义 PingCode 产品中知识管理扩展模块</td></tr><tr><td><a href="/reference/resource/extensions/testhub">测试管理</a></td><td>定义 PingCode 产品中测试管理扩展模块</td></tr></tbody></table>

## 上下文数据

每个扩展模块可以访问的上下文数据如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 33.05%" /><col style="width: 66.95%" /></colgroup><thead><tr><th>上下文数据</th><th>描述</th></tr></thead><tbody><tr><td><code>app</code></td><td>当前应用数据</td></tr><tr><td><code>team</code></td><td>当前应用安装的企业数据</td></tr><tr><td><code>installation</code></td><td>当前应用安装数据</td></tr><tr><td><code>environment</code></td><td>当前应用所在环境数据</td></tr><tr><td><code>user</code></td><td>当前用户数据</td></tr><tr><td><code>extension</code></td><td>扩展模块数据</td></tr></tbody></table>

详细的解释请参考： [上下文数据](/reference/resource/context)
