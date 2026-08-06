---
title: "create"
lastUpdated: 2026-07-10T05:36:41.000Z
---

# create

创建一个新的应用

## 使用

```shell
Usage: nexus create [options] [name]
```

## 参数

```shell
name                              specify the app name
```

## 选项

```shell
-v, --verbose                     enable verbose mode
-d, --directory <directory name>  specify the directory to create (default: app name in
                                  kebab-case)
-t, --template <template name>    specify the template to use
-h, --help                        display help for command
```

## 示例

执行应用创建流程

```shell
nexus create
```

指定应用名称创建

```shell
nexus create hello-world
```

指定应用名称、模板调用

```shell
nexus create hello-world -t angular-custom-ui
```

**支持模板列表**

- angular-custom-ui
- vue-custom-ui
- react-custom-ui
- javascript-custom-ui
- event-typescript
- webhook-typescript
