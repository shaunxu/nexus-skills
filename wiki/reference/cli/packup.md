---
title: "packup"
lastUpdated: 2026-06-29T09:06:52.000Z
---

# packup

构建并保存安装包到本地目录。

## 使用

```shell
Usage: nexus packup [options]
```

## 选项

```shell
-v, --verbose                enable verbose mode
-d, --directory <directory>  directory to save the build package (default: project root)
-t, --tag <tag>              specify a custom build tag
-f, --no-verify              skip pre-build validation
-h, --help                   display help for command
```

## 示例

执行打包，将安装包下载到项目根目录

```shell
nexus packup
```

使用自定义构建标签 `7d392hf` 打包，将安装包下载到当前目录

```shell
nexus packup -t 7d392hf
```
