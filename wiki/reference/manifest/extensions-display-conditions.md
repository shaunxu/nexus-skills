---
title: "Display conditions"
lastUpdated: 2026-07-15T05:54:56.000Z
---

# Display conditions

通过显示条件，可以控制扩展模块在用户界面中的可见性。

## 概述

显示条件在客户端执行，无法保证执行结果不会通过浏览器开发者工具被覆盖，不能依赖显示条件作为保护敏感数据的机制。

对于将要操作的任何敏感数据，强烈建议在显示条件的基础上，在代码中进行适当的权限检查。

示例：

```yaml
extensions:
  - key: hello-world-project-page
    resource: main
    target: "pcm:pjm:project:page"
    resolver:
      function: resolver
    title: Hello world
    display:
      and:                                    
        hasPermission: "pca:global:pjm:configuration" 
        project.name: scrum                    
        not:                                    
          project.id: 111111
      or:                                       
        workitem.identifier: TT-2
```

## 条件操作符

显示条件支持以下操作符用于进行多个条件之间的逻辑判断，默认情况下，多个显示条件之间通过 `and` 操作符连接。

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.07%" /><col style="width: 68.93%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>and</code></td><td>所有子条件为 <code>true</code></td></tr><tr><td><code>or</code></td><td>任一子条件为 <code>true</code></td></tr><tr><td><code>not</code></td><td>子条件取反</td></tr></tbody></table>

示例：

```yaml
extensions:
  - key: hello-world-project-page
    resource: main
    target: "pcm:pjm:project:page"
    resolver:
      function: resolver
    title: Hello world
    display:
      or:
        project.type: scrum
        and:                                                       
          project.identifier: PJM                                      
          workitem.type_group: 1
```

## 通用条件

通用条件对所有扩展模块都适用，目前平台支持以下三个通用条件判断：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 31.07%" /><col style="width: 68.93%" /></colgroup><thead><tr><th>名称</th><th>描述</th></tr></thead><tbody><tr><td><code>hasPermission</code></td><td>用户拥有指定权限点，可以指定的权限点参考： <a href="/reference/resource/authorize">权限点参考</a></td></tr><tr><td><code>isTeamOwner</code></td><td>是否为组织所有者</td></tr><tr><td><code>isLoggedIn</code></td><td>当前用户是否已登录</td></tr></tbody></table>

示例：

```yaml
extensions:
  - key: hello-world-project-page
    resource: main
    target: "pcm:pjm:project:page"
    resolver:
      function: resolver
    title: Hello world
    display:
      hasPermission: "pca:global:pjm:configuration"
      isTeamOwner: true
```

## 上下文条件

不同的扩展模块，可以使用扩展模块所能访问的上下文数据进行显示条件的判断，每个扩展模块可以访问的上下文数据定义参考具体模块定义。

示例：

```yaml
extensions:
  - key: hello-world-project-page
    resource: main
    target: "pcm:pjm:project:page"
    resolver:
      function: resolver
    title: Hello world
    display:
      and:
        project.name: scrum                   
        not:                                    
          project.identifier: PJM
      or:                                       
        workitem.type_group: 1
```
