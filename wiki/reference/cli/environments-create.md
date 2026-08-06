---
title: "environments create"
lastUpdated: 2026-06-29T09:02:16.000Z
---

# environments create

创建一个新的开发环境

## 使用

```shell
Usage: nexus environments create [options]
```

## 选项

```shell
-v, --verbose                    enable verbose mode
--non-interactive                run the command without input prompts
-e, --environment [environment]  specify a name for the environment
-h, --help                       display help for command
```

## 示例

执行环境创建

```shell
nexus environments create
```

创建名称为 `dev1` 的开发环境

```shell
nexus environments create -e dev1
```
