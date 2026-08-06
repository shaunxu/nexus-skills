---
title: "useAppContext"
lastUpdated: 2026-08-05T14:45:20.000Z
---

# useAppContext

此 Hook 读取组件当前运行的上下文，请注意，上下文数据是异步加载的，因此在加载过程中，其输出将为 `undefined` 。

## 使用

在你的应用中添加 `useAppContext`

```javascript
import { useAppContext } from "@pc-nexus/react";
```

```javascript
import { useAppContext } from "@pc-nexus/angular";
```

```javascript
import React from "react";
import { NexusReconciler, NxText, useProductContext,} from "@pc-nexus/react";

const App = () => {
  const context = useAppContext();

  return (
    <>
      <NxText>
        Extenstion key from context: {context?.extenstion.key}
      </NxText>
    </>
  );
};

NexusReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

```typescript
import { Component } from "@angular/core";
import { bootstrapNexusApplication, NxText, useProductContext,} from "@pc-nexus/angular";

@Component({
  selector: "app-root",
  template: `
    <nx-text>Extenstion key from context: {context()?.extenstion.key}</nx-text>
`,
  imports: [ NxText ]
})
class App {
  context = useAppContext();
}

bootstrapNexusApplication(App);
```

## 函数签名

```javascript
function useAppContext<T = ExtensionData>(): NexusAppContext<T> | undefined;
```

```javascript
function useAppContext<T = ExtensionData>(): Signal<NexusAppContext<T> | undefined>;
```

## 参数

空

## 返回值

详细数据解释请参考：  [上下文数据](https://developer.alpha.pingcode.live/reference/resource/context)
