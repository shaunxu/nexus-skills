---
title: "register"
lastUpdated: 2026-06-29T09:05:13.000Z
---

# register

将当前应用注册为一个新的 Nexus 应用

::: info
此命令会将应用所有者设置为当前执行注册命令的开发者平台账户 id，并使用新的应用 id 更新 manifest 清单文件

如果该应用此前已使用 
`nexus create`
 或 
`nexus register`
 命令在 PingCode 开发者平台注册过，那么再次运行 
`nexus register`
 时，将会使用一个新的应用 ID 来更新 manifest 清单文件，并将您的账户设置为该新 ID 应用的所有者。此操作不会影响该应用之前的记录。
:::

## 使用

```shell
Usage: nexus register [options] [name]
```

## 参数

```shell
name           specify the app name
```

## 选项

```shell
-v, --verbose  enable verbose mode
-h, --help     display help for command
```

## 示例

注册当前应用为新应用

```shell
nexus register
```

指定应用名称注册

```shell
nexus register my-app
```
