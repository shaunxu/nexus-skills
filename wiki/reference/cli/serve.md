---
title: "serve"
lastUpdated: 2026-07-10T05:36:05.000Z
---

# serve

启动一个服务，将本地代码与开发环境运行的应用建立实时连接。

## 使用

```shell
Usage: nexus serve [options] [command]
```

## 选项

```shell
-v, --verbose                                          enable verbose mode
--no-verify                                            skip pre-serve validation
-d, --debug                                            enable debugger mode
-f,--debugFunctionHandlers <debugFunctionHandlers...>  function handlers to debug (space-separated, as declared in manifest)
-e, --environment [environment]                        environment to connect to
-h, --help                                             display help for command
```

## 子命令

```shell
bind [options]                                         bind your PingCode account
list [options]                                         list bound PingCode accounts
```

## 示例

启动服务

```shell
nexus serve
```

指定环境启动服务

```shell
nexus serve -e development
```
