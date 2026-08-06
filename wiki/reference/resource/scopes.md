---
title: "作用域参考"
lastUpdated: 2026-07-15T12:27:15.000Z
---

# 作用域参考

作用域指的是应用能够请求 PingCode 产品数据的访问级别，这里定义的作用域适用于采用OAuth 2.0授权码许可进行授权的应用以及 Nexus 应用。在授权流程中，作用域的描述会显示在用户的授权同意界面上。

设置作用域时，需要：

- 检查您的应用，确定其使用的所有操作
- 查阅 PingCode REST APIs 文档，确定每个操作所需的作用域
- 将所需作用域添加至 `manifest.yaml` 文件中，并记得移除所有过时的作用域。

## 作用域定义

目前系统支持的作用域定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 38.56%" /><col style="width: 61.44%" /></colgroup><thead><tr><th>权限</th><th>说明</th></tr></thead><tbody><tr><td><a href="/reference/resource/scopes/global">全局作用域</a></td><td>定义系统全局作用域</td></tr><tr><td><a href="/reference/resource/scopes/ship">产品管理</a></td><td>定义产品管理作用域</td></tr><tr><td><a href="/reference/resource/scopes/pjm">项目管理</a></td><td>定义项目管理作用域</td></tr><tr><td><a href="/reference/resource/scopes/wiki">知识管理</a></td><td>定义知识管理作用域</td></tr><tr><td><a href="/reference/resource/scopes/testhub">测试管理</a></td><td>定义测试管理作用域</td></tr><tr><td><a href="/reference/resource/scopes/devops">DevOps 数据</a></td><td>定义 DevOps 数据作用域</td></tr></tbody></table>
