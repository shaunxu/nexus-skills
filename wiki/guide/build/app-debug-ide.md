---
title: "IDE 断点调试"
lastUpdated: 2026-07-17T03:50:13.000Z
---

# IDE 断点调试

本指南详细阐述如何在可视化 IDE 中进行 Nexus 应用调试。

## VS Code

### **启动调试**

使用 `nexus serve` 命令并指定 `--debug` 参数在项目根目录启动本地调试：

```shell
nexus serve --debug
```

### **创建配置文件**

在应用根目录创建 `.vscode/launch.json` 。

```javascript
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Nexus Serve",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "restart": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

### **连接调试器**

按下快捷键 `Cmd+Shift+D` （Windows / Linux 为 `Ctrl+Shift+D` ）打开 **Run and Debug** 面板，在下拉菜单中选中 `Nexus Serve` 配置，点击 **Start Debugging (F5)** 绿色箭头开始挂载。 

## IntelliJ IDEA / WebStorm

### **启动调试**

使用 `nexus serve` 命令并指定 `--debug` 参数在项目根目录启动本地调试：

```shell
nexus serve --debug
```

### **添加运行配置**

1. 点击右上角运行配置下拉框，选择  `Edit Configurations... ` 打开配置窗口
1. 在 Run/Debug Configurations 窗口左上角点击 +，从列表中选择  **Attach to Node.js/Chrome** 。
1. 填写配置后点击 **OK** 保存配置

- **Name** ： `Nexus Serve`
- **Host** ： `localhost`
- **Port** ： `9229`
- 勾选 `Reconnect automatically`

### **连接调试器**

点击右上角 Debug `Nexus Serve` 运行调试器。
