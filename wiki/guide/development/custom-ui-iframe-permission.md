---
title: "Custom UI iframe 权限"
lastUpdated: 2026-07-15T08:15:31.000Z
---

# Custom UI iframe 权限

所有使用 Custom UI 开发的应用都在 iframe 中运行，这为自定义用户界面提供了安全且隔离的托管环境。本文档详细描述了 iframe 的预设权限，默认情况下，以下权限会应用于 iframe，且 Nexus 应用的开发者无法修改这些权限。

## 功能策略

Custom UI iframe 指定了一系列功能策略，这些策略根据请求的来源定义了 iframe 可用的功能。下表列出了为 Custom UI iframe 配置的功能策略：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 34.6%" /><col style="width: 65.4%" /></colgroup><thead><tr><th>功能策略</th><th>描述</th></tr></thead><tbody><tr><td><code>camera</code></td><td>允许使用视频输入设备</td></tr><tr><td><code>clipboard-write</code></td><td>允许向剪贴板写入数据</td></tr><tr><td><code>display-capture</code></td><td>允许使用屏幕捕获 API</td></tr><tr><td><code>fullscreen</code></td><td>允许使用 <code>Element.requestFullscreen()</code> 函数</td></tr><tr><td><code>microphone</code></td><td>允许使用音频输入设备</td></tr></tbody></table>

## 沙箱限制

Custom UI iframe 还包含一组沙箱属性，用于对 iframe 中的内容施加额外限制。下表列出了应用于Custom UI iframe 的沙箱属性：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 34.6%" /><col style="width: 65.4%" /></colgroup><thead><tr><th>沙箱属性</th><th>描述</th></tr></thead><tbody><tr><td><code>allow-downloads</code></td><td>允许通过用户手势启动下载</td></tr><tr><td><code>allow-forms</code></td><td>允许资源提交表单</td></tr><tr><td><code>allow-modals</code></td><td>允许资源打开模态窗口</td></tr><tr><td><code>allow-pointer-lock</code></td><td>允许资源使用指针锁定 API</td></tr><tr><td><code>allow-same-origin</code></td><td>允许将 iframe 内容视为与其父页面同源</td></tr><tr><td><code>allow-scripts</code></td><td>允许资源运行脚本，但不得创建弹出窗口</td></tr></tbody></table>
