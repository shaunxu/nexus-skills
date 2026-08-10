---
title: 'List Nexus Extensions'
description: '' # A short summary for search engines to display, max 120 chars
platform: platform
product: nexus
category: devguide
subcategory: guides
date: '2026-08-10'
---

# Nexus extensions by product

## Related tools

- nexus-development-guide
- nexus-app-manifest-guide

Once you find the extension you want, look up its `target` and properties in the corresponding extension reference under `wiki/reference/resource/extensions/`. ALWAYS copy the `target` string verbatim from that reference; NEVER invent a target.

Each extension is declared under the top-level `extensions` array of `manifest.yaml`. Every extension requires at minimum `key` and `target`. UI extensions additionally reference a Custom UI bundle via `resource` (matching a `resources[].key`) and a backend handler via `resolver.function` (matching a `functions[].key`) or `resolver.endpoint` (matching an `endpoints[].key`). See `nexus-app-manifest-guide` for the full manifest schema, including `display` conditions, permissions, and the distinction between `function` and `endpoint` resolvers.

## Global extensions (Platform)

Available across PingCode products:

### 全局

- 全局｜顶部公告 `pcm:global:header:banner`: 在系统顶部添加自定义公告。
- 全局｜独立应用 `pcm:global:app:hub`
- 全局｜应用设置 `pcm:global:app:setting`
- 全局｜新建菜单 `pcm:global:create:action`: 在全局「新建」菜单中添加自定义操作入口。

### 工作台

- 工作台｜首页导航 `pcm:global:workspace:page`
- 工作台｜仪表盘部件 `pcm:global:dashboard:widget`: 在工作台仪表盘中添加自定义部件。

### 帐号

- 帐号｜个人设置 `pcm:global:personal:setting`: 在用户帐号的个人设置中添加自定义配置页面。

## 项目管理 (PJM) extensions

### 项目

- 项目 - 首页导航 `pcm:pjm:project:hub`
- 项目 - 组件页面 `pcm:pjm:project:page`: 在项目一级导航中添加自定义组件页面，访问路径 `/pjm/projects/{identifier}/apps/{appId}/{envId}/{route}`。
- 项目 - 设置页面 `pcm:pjm:project:setting`
- 项目 - 首页后台脚本 `pcm:pjm:project:background`: 在项目首页运行不可见的后台脚本容器。

### 工作项

- 工作项 - 详情导航 `pcm:pjm:workitem:area`
- 工作项 - 详情面板 `pcm:pjm:workitem:panel`: 在工作项详情页右侧添加可展开面板，点击进入二级页。
- 工作项 - 详情上下文 `pcm:pjm:workitem:context`
- 工作项 - 详情菜单 `pcm:pjm:workitem:action`: 在工作项详情页的更多操作菜单中添加自定义菜单项。
- 工作项 - 详情后台脚本 `pcm:pjm:workitem:background`: 在工作项详情页运行不可见的后台脚本容器。

### 迭代

- 迭代 - 详情导航 `pcm:pjm:sprint:page`
- 迭代 - 详情菜单 `pcm:pjm:sprint:action`: 在迭代详情页的更多操作菜单中添加自定义菜单项。

### 发布

- 发布 - 详情导航 `pcm:pjm:release:page`
- 发布 - 详情菜单 `pcm:pjm:release:action`: 在发布详情页的更多操作菜单中添加自定义菜单项。

### 基线

- 基线 - 详情导航 `pcm:pjm:baseline:page`
- 基线 - 详情菜单 `pcm:pjm:baseline:action`: 在基线详情页的更多操作菜单中添加自定义菜单项。

## 产品管理 (Ship) extensions

### 产品

- 产品 - 首页导航 `pcm:ship:product:hub`
- 产品 - 组件页面 `pcm:ship:product:page`
- 产品 - 产品设置 `pcm:ship:product:setting`
- 产品 - 首页后台脚本 `pcm:ship:product:background`: 在产品首页运行不可见的后台脚本容器。

### 需求

- 需求 - 详情导航 `pcm:ship:idea:area`
- 需求 - 详情面板 `pcm:ship:idea:panel`
- 需求 - 详情上下文 `pcm:ship:idea:context`
- 需求 - 详情菜单 `pcm:ship:idea:action`: 在需求详情页的更多操作菜单中添加自定义菜单项。
- 需求 - 详情后台脚本 `pcm:ship:idea:background`: 在需求详情页运行不可见的后台脚本容器。

### 工单

- 工单 - 详情导航 `pcm:ship:ticket:area`
- 工单 - 详情面板 `pcm:ship:ticket:panel`
- 工单 - 详情上下文 `pcm:ship:ticket:context`
- 工单 - 详情菜单 `pcm:ship:ticket:action`: 在工单详情页的更多操作菜单中添加自定义菜单项。
- 工单 - 详情后台脚本 `pcm:ship:ticket:background`: 在工单详情页运行不可见的后台脚本容器。

### 计划

- 计划 - 详情导航 `pcm:ship:plan:page`
- 计划 - 详情菜单 `pcm:ship:plan:action`: 在计划详情页的更多操作菜单中添加自定义菜单项。

### 基线

- 基线 - 详情导航 `pcm:ship:baseline:page`
- 基线 - 详情菜单 `pcm:ship:baseline:action`: 在基线详情页的更多操作菜单中添加自定义菜单项。

## 知识管理 (Wiki) extensions

### 空间

- 空间 - 首页导航 `pcm:wiki:space:hub`
- 空间 - 组件页面 `pcm:wiki:space:page`
- 空间 - 空间设置 `pcm:wiki:space:setting`
- 空间 - 首页后台脚本 `pcm:wiki:space:background`: 在空间首页运行不可见的后台脚本容器。

### 页面

- 页面 - 上下文操作 `pcn:wiki:context:action`: 在页面中选中文本时的上下文菜单中添加操作入口。
- 页面 - 详情菜单 `pcm:wiki:page:action`: 在页面详情页的更多操作菜单中添加自定义菜单项。
- 页面 - 文档内容块 `pcm:wiki:document:block`: 在 Wiki 文档中插入自定义内容块。
- 页面 - 详情后台脚本 `pcm:wiki:page:background`: 在页面详情页运行不可见的后台脚本容器。

### 基线

- 基线 - 详情导航 `pcm:wiki:baseline:page`
- 基线 - 详情菜单 `pcm:wiki:baseline:action`: 在基线详情页的更多操作菜单中添加自定义菜单项。

## 测试管理 (TestHub) extensions

### 测试库

- 测试库 - 首页导航 `pcm:testhub:library:hub`
- 测试库 - 组件页面 `pcm:testhub:library:page`
- 测试库 - 设置页面 `pcm:testhub:library:setting`
- 测试库 - 首页后台脚本 `pcm:testhub:library:background`: 在测试库首页运行不可见的后台脚本容器。

### 测试用例

- 测试用例 - 详情导航 `pcm:testhub:testcase:area`
- 测试用例 - 详情面板 `pcm:testhub:testcase:panel`
- 测试用例 - 详情上下文 `pcm:testhub:testcase:context`
- 测试用例 - 详情菜单 `pcm:testhub:testcase:action`: 在测试用例详情页的更多操作菜单中添加自定义菜单项。
- 测试用例 - 详情后台脚本 `pcm:testhub:testcase:background`: 在测试用例详情页运行不可见的后台脚本容器。

### 测试计划

- 测试计划 - 详情导航 `pcm:testhub:plan:page`
- 测试计划 - 详情菜单 `pcm:testhub:plan:action`: 在测试计划详情页的更多操作菜单中添加自定义菜单项。

### 基线

- 基线 - 详情导航 `pcm:testhub:baseline:page`
- 基线 - 详情菜单 `pcm:testhub:baseline:action`: 在基线详情页的更多操作菜单中添加自定义菜单项。
