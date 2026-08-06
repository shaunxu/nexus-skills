---
title: "deploy"
lastUpdated: 2026-07-10T02:52:55.000Z
---

# deploy

部署应用到环境

## 使用

```shell
Usage: nexus deploy [options] [command]
```

## 选项

```shell
-v, --verbose                    enable verbose mode
--non-interactive                run the command without input prompts
-f, --no-verify                  skip pre-build validation
-e, --environment <environment>  specify the environment to deploy to
-t, --tag <tag>                  specify a build tag to deploy (from nexus build)
-h, --help                       display help for command
```

## 子命令

```shell
list [options]                   list deployments for your app
```

## 示例

执行构建并部署

```shell
nexus deploy
```

将应用构建部署到 `development` 环境

```shell
nexus deploy -e development
```

部署已有构建  `7d392hf`

```shell
nexus deploy -t 7d392hf
```

**Tag 约束**

- 必须在此应用中是唯一的
- 长度最多可达 64 个字符
- 不区分大小写 
- 必须以字母数字字符开头
- 只能包含字母 `A-Z` 或 `a-z` 、数字 `0-9` 、连字符 `-` 、下划线 `_` 和句号 `.`
