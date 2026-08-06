---
title: "environments delete"
lastUpdated: 2026-06-29T09:02:34.000Z
---

# environments delete

删除应用的一个或多个开发环境

## 使用

```shell
Usage: nexus environments delete [options]
```

## 选项

```shell
-v, --verbose                        enable verbose mode
--non-interactive                    run the command without input prompts
-e, --environment [environments...]  specify the environments to delete
-h, --help                           display help for command
```

## 示例

执行环境删除

```shell
nexus environments delete
```

指定删除 `env1` 、 `env2` 开发环境

```shell
nexus environments delete -e env1 env2
```
