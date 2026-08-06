---
title: "External permissions"
lastUpdated: 2026-07-15T13:40:33.000Z
---

# External permissions

`external` 部分声明了应用允许访问的外部资源 URL，以及定义的函数允许与之通信的外部网站，包括自定义UI 解析器和其他任何函数。

## 示例

简单配置示例：

```yaml
permissions:
  external:
    fetch:
      backend: 
        - remote: remote-backend
      client:
        - "https://*.example.com"
    fonts:
      - "https://www.example.com/fonts.css"
    styles:
      - "https://www.example.com/stylesheet.css"
    frames:
      - "https://www.example.com/embed/page"
    images:
      - "https://www.example.com/image.png"
    media:
      - "https://www.example.com/media.mp4"
    scripts:
      - "https://www.example.com/script.js"
```

## 属性

包含的属性如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25.99%" /><col style="width: 74.01%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>fetch</code></td><td><code>fetch</code> 列表声明了应用通过前后端可以请求的外部域名</td></tr><tr><td><code>fonts</code></td><td><code>fonts</code> 列表声明了应用的 <code>font-src</code> 指令允许加载哪些外部字体</td></tr><tr><td><code>styles</code></td><td><code>styles</code> 列表声明了应用的 <code>style-src</code> 指令允许加载哪些外部样式</td></tr><tr><td><code>frames</code></td><td><code>frames</code> 列表声明了应用的 <code>frame-src</code> 指令允许加载哪些外部页面</td></tr><tr><td><code>images</code></td><td><code>images</code> 列表声明了应用的 <code>img-src</code> 指令允许加载哪些外部图像</td></tr><tr><td><code>media</code></td><td><code>media</code> 列表声明了应用的 <code>media-src</code> 指令允许加载哪些外部媒体</td></tr><tr><td><code>scripts</code></td><td><code>scripts</code> 列表声明了应用的 <code>script-src</code> 指令允许加载哪些外部脚本</td></tr></tbody></table>

### Fetch

`fetch` 部分声明了应用通过前后端可以请求的外部域名：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 25.99%" /><col style="width: 74.01%" /></colgroup><thead><tr><th>属性</th><th>描述</th></tr></thead><tbody><tr><td><code>backend</code></td><td><code>backend</code> 列表声明了定义的后端函数可以与之通信的外部域名</td></tr><tr><td><code>client</code></td><td><code>client</code> 列表声明了应用的连接源策略允许哪些外部来源，此外，声明在此处的链接在使用 <code>router.navigate</code> 打开时，不会显示外部链接警告弹窗。</td></tr></tbody></table>

在 `fetch` 中声明外部资源时，可以直接给出列表或者使用 `remote` 对象。

直接声明：

```yaml
permissions:
  external:
    fetch:
      backend:
        - "*.example.com"
      client:
        - "*.example.com"
```

支持的域名格式：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 30.08%" /><col style="width: 36.58%" /><col style="width: 33.34%" /></colgroup><thead><tr><th>格式</th><th>示例</th><th>说明</th></tr></thead><tbody><tr><td>HTTPS</td><td><code>https://api.example.com</code></td><td>允许访问指定 URL 下的所有资源</td></tr><tr><td>域名</td><td><code>api.example.com</code></td><td>等价于 HTTPS</td></tr><tr><td>通配符域名</td><td><code>*.example.com</code></td><td>匹配所有子域名，不包含父域名本身</td></tr><tr><td>全部域名</td><td><code>*</code></td><td>允许访问任意域名</td></tr></tbody></table>

使用 `remote` 对象：

```yaml
permissions:
  external:
    fetch:
      backend:
        - remote: remote-backend
remotes:
  - key: remote-backend
    baseUrl: "https://example.com"
    operations:
      - fetch
```

### Fonts

`fonts` 列表声明了应用的 `font-src` 指令允许加载哪些外部字体

示例：

```yaml
permissions:
  external:
    fonts:
      - "https://www.example.com/fonts.css"
```

### Styles

`styles` 列表声明了应用的 `style-src` 指令允许加载哪些外部样式

示例：

```yaml
permissions:
  external:
    styles:
      - "https://www.example.com/stylesheet.css"
```

### Frames

`frames` 列表声明了应用的 `frame-src` 指令允许加载哪些外部页面

示例：

```yaml
permissions:
  external:
    frames:
      - "https://www.example.com/embed/page"
```

### Images

`images` 列表声明了应用的 `img-src` 指令允许加载哪些外部图像

示例：

```yaml
permissions:
  external:
    images:
      - "https://www.example.com/image.png"
```

### Media

`media` 列表声明了应用的 `media-src` 指令允许加载哪些外部媒体

示例：

```yaml
permissions:
  external:
    media:
      - "https://www.example.com/media.mp4"
```

### Scripts

`scripts` 列表声明了应用的 `script-src` 指令允许加载哪些外部脚本

示例：

```yaml
permissions:
  external:
    scripts:
      - "https://www.example.com/script.js"
```

## 限制

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 24.29%" /><col style="width: 24.01%" /><col style="width: 51.7%" /></colgroup><thead><tr><th>限制项</th><th>限制</th><th>描述</th></tr></thead><tbody><tr><td>URL 地址最大长度</td><td><code>1024</code></td><td>每个属性中所描述的外部 URL 的最大长度</td></tr></tbody></table>
