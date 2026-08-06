---
title: "App"
lastUpdated: 2026-07-19T08:41:37.000Z
---

# App

`app` 定义应用的基本信息，包括唯一标识、名称、开发者信息等。

## 结构

结构定义如下：

```yaml
app {}
├─ id (string) [Mandatory]
├─ version (string) [Mandatory]
└─ licensing {} [Optional]
```

## 示例

简单配置示例：

```yaml
app:
  id: “466d303d-a2c4-4ec4-ad7c-5435be94583b”
  version: 1.6.0
  licensing:
    enabled: true
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>id</code></td><td>Y</td><td>应用的全局唯一标识，由 CLI 工具自动生成</td></tr><tr><td><code>version</code></td><td>Y</td><td>定义应用的版本，由开发者指定，格式为： <code>主版本号.次级版本号.修正版本号</code> 举例： <code>1.6.0</code></td></tr><tr><td><code>licensing</code></td><td></td><td>是否为应用启用许可状态，如果启用在应用安装时需要输入序列号才可以使用</td></tr><tr><td><code>name</code></td><td>*</td><td>定义应用的名称，在开发者中心设置</td></tr><tr><td><code>publisher</code></td><td>*</td><td>应用的发布者，在开发者中心设置</td></tr><tr><td><code>description</code></td><td>*</td><td>应用的简单描述，在开发者中心设置</td></tr><tr><td><code>avatar</code></td><td>*</td><td>应用图标，在开发者中心设置</td></tr><tr><td><code>links</code></td><td>*</td><td>应用的相关链接，在开发者中心设置</td></tr><tr><td><code>links.support</code></td><td>*</td><td>应用技术支持链接，在开发者中心设置</td></tr></tbody></table>

以上加 `*` 属性由 CLI 工具根据开发者中心的数据，自动打包完成。
