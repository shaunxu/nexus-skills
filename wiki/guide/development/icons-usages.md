---
title: "如何在 UI 添加图标"
lastUpdated: 2026-06-17T09:40:23.000Z
---

# 如何在 UI 添加图标

在 Nexus 平台中，可以为任何带有 `icon` 属性的扩展模块设置图标，图标的设置支持三种方式：

1. 本地资源
1. 图标库
1. 自托管资源

## 本地资源

你可以将图标文件与其他资源一起打包，并将图标图片存储在声明为资源的位置，使用以下语法引用图标：

```yaml
icon: resource:<resource key>/<relative path to resource>
```

在下面的示例中，我们使用位于 `static/hello-world/build/icons/` 下的 `issue-copy.svg` 文件作为工作项操作菜单图标：

```yaml
extensions:
  - key: hello-world-workitem-action
    target: "pcm:pjm:workitem:action"
    title: Custom Menu
    icon: resource:example-resource/icons/issue-copy.svg
    resource: main
    resolver:
      function: resolver
    type: normal
resources:
  - key: example-resource
    path: static/hello-world/build
```

## 图标库

你也可以直接使用 Nexus 平台提供的图标库中的图标，使用以下语法引用图标：

```yaml
icon: nri:icons/<icon key>:<color code>
```

只有使用图标库中的图标时才可以指定颜色，在下面的示例中，我们使用图标库中的 `icon-list-ordered` 图标作为首页导航列表，并指定颜色值为 `#ff9900` ：

```yaml
modules:
  - key: hello-world-project-page
    target: "pcm:pjm:project:hub"
    resolver:
      function: resolver
    pages:
      - key: hub-page
        title: "Page A"
        resource: main_page
        route: "page"
        icon: icons/icon-list-ordered:#ff9900
    section:
      header: Section Title
      enabled: true
```

## 自托管资源

除以上两种方式外， `icon` 属性也支持指向任何自托管图片文件的绝对URL：

```yaml
icon: https://example.com/icon.png
```
