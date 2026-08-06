---
title: "autocomplete"
lastUpdated: 2026-06-11T10:43:26.000Z
---

# autocomplete

为命令行工具配置自动补全功能

## 使用

```shell
Usage: nexus autocomplete [options] [command]
```

## 选项

```shell
-h, --help           display help for command
```

## 子命令

```shell
install [options]    install shell completion for the Nexus CLI
uninstall [options]  uninstall shell completion for the Nexus CLI
help [command]       display help for command
```

## 示例

安装自动补全功能，执行后需要重启命令行工具

```shell
nexus autocomplete install
```

卸载自动补全功能，执行后需要重启命令行工具

```shell
nexus autocomplete uninstall
```
