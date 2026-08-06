---
title: "权限点参考"
lastUpdated: 2026-07-15T11:47:48.000Z
---

# 权限点参考

Nexus 平台提供了一些内置方法供开发者在执行某些操作之前检查当前用户对系统、项目、事项的操作权限，系统中每个操作权限都具有唯一标识，开发者可以使用这些标识通过 `REST APIs` 或者 `authorize` 方法进行权限验证。

## 权限点定义

系统全部权限点定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 38.56%" /><col style="width: 61.44%" /></colgroup><thead><tr><th>权限</th><th>说明</th></tr></thead><tbody><tr><td><a href="/reference/resource/authorize/global">全局权限</a></td><td>定义系统全局权限点</td></tr><tr><td><a href="/reference/resource/authorize/ship">产品管理</a></td><td>定义产品管理权限点</td></tr><tr><td><a href="/reference/resource/authorize/pjm">项目管理</a></td><td>定义项目管理权限点</td></tr><tr><td><a href="/reference/resource/authorize/wiki">知识管理</a></td><td>定义知识管理权限点</td></tr><tr><td><a href="/reference/resource/authorize/testhub">测试管理</a></td><td>定义测试管理权限点</td></tr><tr><td><a href="/reference/resource/authorize/insight">效能度量</a></td><td>定义效能度量权限点</td></tr><tr><td><a href="/reference/resource/authorize/teams">协作空间</a></td><td>定义协作空间权限点</td></tr></tbody></table>
