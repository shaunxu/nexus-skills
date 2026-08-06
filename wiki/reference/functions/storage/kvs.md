---
title: "kvs"
lastUpdated: 2026-07-15T13:49:50.000Z
---

# kvs

`kvs` 为 Key-Value 数据提供简单的存储功能，如用户偏好设置或应用配置等数据。

## 使用

安装数据存储包：

```powershell
npm install @pc-nexus/storage
```

导入键-值对存储：

```javascript
import { kvs } from "@pc-nexus/storage";
```

## 作用域

在使用键-值对存储能力时，需要在 `manifest.yml` 文件中声明作用域：

```yaml
permissions:
    scopes:
        - pcp:storage:app
```

## 示例

简单存储数据示例：

```typescript
import { kvs } from "@pc-nexus/storage";
interface DemoEntity {
  foo: string;
}
const result = await kvs.set<DemoEntity>("key1", {foo: "bar"}, { 
  policy: "OVERRIDE",
  secret: true
});
return result;
```
