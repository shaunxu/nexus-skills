---
title: "Translations"
lastUpdated: 2026-07-15T03:10:43.000Z
---

# Translations

`translations` 定义应用使用的多语言信息。

## 结构

结构定义如下：

```yaml
translations {}
├─ resources [] [Mandatory]
│  ├─ key (string) [Mandatory]
│  └─ path (string) [Mandatory]
└─ fallback {} [Mandatory]
   └─ default (string) [Mandatory]
```

## 示例

简单配置示例：

```yaml
translations:
    resources:
      - key: en-US
        path: locales/en-US.json
      - key: zh-CN
        path: locales/zh-CN.json
      - key: de-DE
        path: locales/de-DE.json
    fallback:
      default: zh-CN
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>resources</code></td><td>Y</td><td>定义应用中使用的多语言资源，每个资源的 Key 必须是系统当前支持的语言代码。</td></tr><tr><td><code>fallback</code></td><td>Y</td><td>指定找不到对应的语言资源时，默认使用的语言</td></tr></tbody></table>

资源的 Key 是标准化的标识符，用于在 `manifest.yml` 文件中定义应用支持的语言类型，采用 BCP-47 格式，由两个字母的语言代码和两个字母的地区代码组成，中间以短横线分隔。当前支持的语言类型为：

|名称|语言|支持代码|
|---|---|---|
|Chinese (Simplified)|中文（简体）|`zh-CN`|
|English (United States)|English（US）|`en-US`|
