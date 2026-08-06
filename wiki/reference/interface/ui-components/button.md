---
title: "Button"
lastUpdated: 2026-08-05T14:33:21.000Z
---

# Button

## 介绍

按钮会触发一个事件或动作，它让用户知道接下来会发生什么。

## 使用

::: code-group

``` []
import { NxButton } from "@pc-nexus/react";
```

``` []
import { NxButton } from "@pc-nexus/angular";
```

:::

## 属性

<table style="width: 100%; table-layout: fixed"><colgroup><col style="width: 20.76%" /><col style="width: 26.27%" /><col style="width: 12.01%" /><col style="width: 40.96%" /></colgroup><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th></tr></thead><tbody><tr><td>type</td><td>'primary' \| 'info' \| 'warning' \| 'danger '\| 'success'</td><td>否</td><td>按钮类型。</td></tr><tr><td>size</td><td>'xs' \| 'sm' \| 'md' \| 'default' \| 'lg'</td><td>否</td><td>按钮大小。</td></tr></tbody></table>

## 示例

**默认**

```javascript
import { NxButton } from "@pc-nexus/react";

const ButtonDefaultExample = () => {
  return <NxButton>Default</NxButton>;
};
```

```typescript
import { NxButton } from "@pc-nexus/angular";

@Component({
  template: `<nx-button>Default</nx-button>`,
  imports: [ NxButton ]
})
class ButtonDefaultExample { }
```

**类型**

```javascript
import { NxButton } from "@pc-nexus/react";

const ButtonPrimaryExample = () => {
  return <NxButton type="primary">Primary</NxButton>;
};
```

```typescript
import { NxButton } from "@pc-nexus/angular";

@Component({
  template: `<nx-button type="primary">Default</nx-button>`,
  imports: [ NxButton ]
})
class ButtonPrimaryExample { }
```
