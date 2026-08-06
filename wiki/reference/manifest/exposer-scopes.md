---
title: "Scopes"
lastUpdated: 2026-08-04T06:55:29.000Z
---

# Scopes

`scopes` 定义应用支持的自定义作用域。

## 示例

简单配置示例：

```yaml
exposer:
  scopes:
    - name: ncp:read:employee
      displayName: Read Employee Info
      description: Read Employee Info
```

## 属性

属性定义如下：

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 22.91%" /><col style="width: 22.03%" /><col style="width: 55.06%" /></colgroup><thead><tr><th>属性</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td><code>name</code></td><td>Y</td><td>作用域名称，全局唯一，必须符合作用域名称规则</td></tr><tr><td><code>displayName</code></td><td>Y</td><td>作用域展示名称</td></tr><tr><td><code>description</code></td><td></td><td>作用域描述</td></tr></tbody></table>

## 名称规则

开发者自定义的作用域是保证 REST APIs 安全的关键组成部分，请遵循以下原则设计：

- 保持作用域的名称一致：没个作用域必须以 `ncp` 开头
- 必须过度细化：每个应用最多只能声明 `16` 个作用域
- 采用「动词+名词」命名方式：理想情况下，每个作用域名称应包含：
  - 表示动作的动词，例如 `read` 、 `write` 、 `delete`
  - 表示对象的名称，例如 `employee` 、 `user` 、 `customer`
- 作用域示例：
  - `ncp:read:employee` ：用于读取员工数据
  - `ncp:write:employee` ：用于写入员工数据
