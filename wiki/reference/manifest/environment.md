---
title: "Environment"
lastUpdated: 2026-07-24T06:38:34.000Z
---

# Environment

`environment` 定义应用环境相关的信息，如环境变量等。

## 结构

结构定义如下：

```javascript
environment {}
└─ variables [] [Mandatory]
   ├─ key (string) [Mandatory]
   ├─ default (string) [Mandatory]
   └─ description (string) [Optional]
```

## 示例

简单配置示例：

```yaml
environment:
  variables:
    - key: REMOTE_PREFIX  
      default: "https://remote.example.com"  
      description: "Prefix used to identify remote services."
```

## 属性

`environment` 属性包含 `variables` 节点：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>variables</code></td><td>Y</td><td>定义应用运行时的环境变量</td></tr></tbody></table>

`variables` 的属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 17.51%" /><col style="width: 18.64%" /><col style="width: 63.85%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>key</code></td><td>Y</td><td>环境变量标识</td></tr><tr><td><code>default</code></td><td>Y</td><td>环境变量默认值</td></tr><tr><td><code>description</code></td><td></td><td>环境变量说明</td></tr></tbody></table>
