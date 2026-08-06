---
title: "Content permissions"
lastUpdated: 2026-06-15T08:55:05.000Z
---

# Content permissions

`content` 部分声明了前端用户界面所需的内容安全策略（CSP）选项。当前端资源需要使用内联脚本、内联样式或动态代码执行等浏览器特性时，需要在此处显式声明，否则浏览器的默认 CSP 将阻止这些行为。

## 示例

简单配置示例：

```yaml
permissions:
  content:
    scripts:
      - unsafe-inline
    styles:
      - unsafe-inline
```

## 属性

包含的属性如下：

|属性|描述|
|---|---|
|`scripts`|`scripts` 列表声明了应用的 `script-src` 指令允许的内联脚本来源|
|`styles`|`styles` 列表声明了应用的 `style-src` 指令允许的内联样式来源|

### Scripts

`scripts` 列表声明了应用的 `script-src` 指令允许的内联脚本来源。

可用值如下：

|值|描述|
|---|---|
|`unsafe-inline`|允许使用内联脚本（如 `<script>` 标签内的代码）|
|`unsafe-hashes`|允许使用特定内联事件处理器（如 `onclick="..."` ）|
|`unsafe-eval`|允许使用 `eval()` 及类似的动态代码执行方法|
|`blob:`|允许通过 `blob:` URI 加载脚本|
|`sha256-/sha384-/sha512-`|通过哈希值精确允许特定的内联脚本内容|

示例：

```yaml
permissions:
  content:
    scripts:
      - unsafe-hashes
```

### Styles

`styles` 列表声明了应用的 `style-src` 指令允许的内联样式来源。

可用值如下：

|值|描述|
|---|---|
|`unsafe-inline`|允许使用内联样式（如 `style` 属性或 `<style>` 标签）|

示例：

```yaml
permissions:
  content:
    styles:
      - unsafe-inline
```
