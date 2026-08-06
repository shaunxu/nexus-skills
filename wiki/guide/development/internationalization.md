---
title: "多语言开发"
lastUpdated: 2026-06-24T09:39:30.000Z
---

# 多语言开发

Nexus 平台提供了完整的多语言（i18n）支持，允许开发者为应用提供多语言版本。本指南详细介绍如何在 Nexus 应用中使用多语言功能。

## 配置说明

在 `manifest.yaml` 中通过 `translations` 字段配置多语言资源：

```yaml
translations:
  resources:
    - key: en-US
      path: locales/en-US.json
    - key: zh-CN
      path: locales/zh-CN.json
  fallback:
    default: zh-CN
```

支持的语言列表：

|语言标识|语言名称|
|---|---|
|`zh-CN`|简体中文|
|`en-US`|美式英语|

## 资源定义

在应用代码包中提供多语言资源定义。

### 目录结构

推荐的项目目录结构如下，多语言资源放在 `/locales` 目录下：

```typescript
your-app/
├── locales/
│   ├── en-US.json
│   └── zh-CN.json
├── src/
├── web/
└── manifest.yaml
```

### JSON 结构

翻译文件采用标准 JSON 格式，并支持嵌套结构以实现模块化管理。

示例 `locales/zh-CN.json` ：

```typescript
{
  "checklist": {
    "loading": "加载中...",
    "addItemPlaceholder": "添加检查项",
    "saveAsTemplateSuccess": "模板保存成功"
  },
  "common": {
    "ok": "确定",
    "cancel": "取消",
    "delete": "删除"
  }
}
```

示例 `locales/en-US.json` ：

```typescript
{
  "common": {
    "welcome": "Welcome back",
    "loading": "Loading..."
  },
  "page": {
    "title": "Page Title"
  },
  "checklist": {
    "loading": "Loading checklist..."
  }
}
```

### 变量替换

支持使用 `{{变量名}}` 语法进行动态变量替换：

```typescript
{
  "setting": {
    "currentProject": "当前项目：{{projectId}}",
    "numOfItems": "{{count}} 个检查项"
  }
}
```

### 最佳实践

- **统一命名规范** ：使用驼峰命名。
- **模块划分** ：按功能模块组织翻译键，例如 `checklist.*` 、 `setting.*` 。
- **公共词汇提取** ：将通用词汇统一放置在 `common.*` 中。
- **保持结构一致** ：所有语言文件应保持相同的 JSON 结构，避免出现缺失或冗余字段。

## Manifest 使用

在 `manifest.yaml` 文件中，支持通过 `i18n` 字段声明多语言资源 key，用于动态解析不同语言下的展示内容：

```javascript
extensions:
  - key: hello-world-project-hub
    title: 
      i18n: page.title
    target: "pcm:pjm:project:page"
    resource: main
    resolver:
      function: resolver
```

运行时系统会根据当前语言环境自动将 `i18n` 对应的 key 解析为具体文案，例如：

- `zh-CN` → `页面标题`
- `en-US` → `Page Title`

## 服务端使用

服务端提供 `i18n` 模块，用于获取翻译资源和进行服务端文案翻译。适用于消息通知、日志输出、模板渲染等需要根据语言环境动态生成文本的场景。

```javascript
import { i18n } from "@pc-nexus/core";

// 获取指定语言的所有翻译资源
const translations = await i18n.getTranslations("zh-CN");

// 基础翻译
const result = await i18n.translate("checklist.loading");
```

## 前端使用

前端提供 `i18n` 模块，用于获取当前语言的翻译资源和创建翻译器。推荐通过创建翻译器的方式进行文案翻译，避免频繁调用接口并获得更好的开发体验。

```javascript
import { i18n } from '@pc-nexus/bridge';

// 或直接获取翻译资源
const result = await i18n.getTranslations();

// 创建翻译器（推荐方式）
const translator = await i18n.createTranslator();
const greeting = translator.translate('common.welcome', { name: '张三' });
```
