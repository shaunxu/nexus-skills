---
title: "ces"
lastUpdated: 2026-07-15T13:50:03.000Z
---

# ces

`ces` 通过自定义实体，进行结构化数据存储,你可以根据应用需求定义这些数据结构。自定义实体支持为单个键（即实体）分配多个值（即属性），并可定义索引以优化针对这些值的查询效率。

## 使用

安装数据存储包：

```powershell
npm install @pc-nexus/storage
```

导入自定义实体存储：

```javascript
import { ces } from "@pc-nexus/storage";
```

## 作用域

在使用自定义实体存储能力时，需要在 `manifest.yml` 文件中声明作用域：

```yaml
permissions:
    scopes:
        - pcp:storage:app
```

## 示例

自定义实体存储示例， `manifest.yml` 文件定义：

```yaml
storage:
    entities:
        - name: employees
          attributes:
              - name: name
                type: string
                required: true
                default: ''
              - name: description
                type: string
              - name: age
                type: number
          indexes:
              - name: 'name_age_'
                keys:
                    name: 1
                    age: 1
                options:
                    unique: true
permissions:
    scopes:
        - pcp:storage:app
```

实体类型定义：

```typescript
interface EmployeesEntity {
    name: string;
    description: string;
    age: number;
}
```

写入数据示例：

```typescript
import { ces } from "@pc-nexus/storage";

const result:EmployeesEntity[] = ces.entity<EmployeesEntity>("employees").insert(
      [
          { name: `user_name_1`, description: "description_1", age: 0 },
          { name: `user_name_2`, description: "description_2", age: 1 },
          { name: `user_name_3`, description: "description_3", age: 2 },
      ],
      { ordered: true },
);
```
