---
title: "build"
lastUpdated: 2026-06-29T08:59:25.000Z
---

# build

构建并上传你的应用程序

## 使用

```shell
Usage: nexus build [options] [command]
```

## 选项

```shell
-v, --verbose    enable verbose mode
-t, --tag <tag>  specify a custom build tag
-f, --no-verify  skip pre-build validation
-h, --help       display help for command
```

## 子命令

```shell
list [options]   list builds for your app
```

## 示例

执行构建，打包应用程序代码，并上传到 PingCode 开发者平台

```shell
nexus build
```

执行构建，并指定自定义构建标签  `7d392hf`

```shell
nexus build --tag 7d392hf
```

**Tag 约束**

- 必须在此应用中是唯一的
- 长度最多可达 64 个字符
- 不区分大小写 
- 必须以字母数字字符开头
- 只能包含字母 `A-Z` 或 `a-z` 、数字 `0-9` 、连字符 `-` 、下划线 `_` 和句号 `.`
