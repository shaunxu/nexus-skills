---
title: "使用 CES 存储结构化数据"
lastUpdated: 2026-07-15T14:05:21.000Z
---

# 使用 CES 存储结构化数据

本文档详细阐述如何使用 `ces` 存储结构化数据， `ces` 存储允许你根据应用需求自定义数据结构并进行存储。

## 定义实体

在 `manifest.yaml` 文件中通过 `storage` 属性定义实体的结构：

```yaml
storage:
  entities:
    - name: employees
      attributes:
        - name: name
          type: string
          required: true
          default: ''
        - name: gender
          type: string
        - name: age
          type: number
```

## 配置作用域

使用 `ces` 存储需要在 `manifest.yaml` 文件中声明作用域：

```yaml
permissions:
    scopes:
        - pcp:storage:app
```

## 安装依赖

安装数据存储模块依赖：

```
npm install @pc-nexus/storage
```

## 写入数据

下面是一个写入单条实体数据的示例：

```typescript
import { ces } from "@pc-nexus/storage";

interface EmployeesEntity {
  name: string;
  age: number;
  gender: string;
}

const entity = ces.entity<EmployeesEntity>("employees");

const result = await entity.insert({
    name: "Davis", 
    age: 25, 
    gender: "male"
});
```

## 查询数据

下面是一个查询实体数据的示例：

```typescript
import { ces } from "@pc-nexus/storage";

const entities = await ces.entity<EmployeesEntity>("employees").find(
    (cb) => {
        cb.field("name").eq("Davis");
    }
);
```

完整的使用请参考 [ces](/reference/functions/storage/ces) 。
