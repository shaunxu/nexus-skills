---
title: "distribute"
lastUpdated: 2026-07-02T08:22:58.000Z
---

# distribute

分发当前工作区中的应用。

## 使用

```shell
Usage: nexus distribute [options]
```

## 选项

```shell
-v, --verbose                    enable verbose mode
-e, --environment <environment>  environment to distribute to
-s, --siteUrl <siteUrl>          site URL
-h, --help                       display help for command
```

## 示例

执行分发流程

```shell
nexus distribute
```

指定站点和环境执行分发流程

```shell
nexus distribute -s {your-domain}.pingcode.com -e development
```
