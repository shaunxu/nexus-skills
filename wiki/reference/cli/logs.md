---
title: "logs"
lastUpdated: 2026-06-29T09:05:56.000Z
---

# logs

查看应用日志信息

## 使用

```shell
Usage: nexus logs [options]
```

## 选项

```shell
-v, --verbose                    enable verbose mode
-i, --invocation [invocation]    view logs for a given invocation ID
-g, --grouped                    group logs by invocation ID
-s, --since [since]              view logs since the specified time. Valid formats:
                                 YYYY-MM-DD, ISO 8601 timestamp, or a relative time
                                 (e.g. 5m, 10h, 2d)
-l, --limit [limit]              specify the number of logs to show (default: 25)
-e, --environment [environment]  specify the environment
-h, --help                       display help for command
```

## 示例

查看最近 25 条运行日志

```shell
nexus logs
```

查看运行日志并以调用 id 分组

```shell
nexus logs -g
```

查看指定环境的运行日志

```shell
nexus logs -e development
```

查看指定时间内的运行日志

```shell
nexus logs -s 2d
nexus logs -s 2026-5-17
```

查看指定调用的运行日志

```shell
nexus logs --invocation ab7e72cd-k8293-4244-9b39-567141b084ee
```
