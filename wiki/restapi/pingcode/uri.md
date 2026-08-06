---
title: "URI 定义"
lastUpdated: 2026-07-06T10:12:10.000Z
---

# URI 定义

PingCode APIs 通过 URI 路径提供对资源的访问，使用 `{}` 将 URI 路径的一部分标记为可使用参数替换的部分。

## 规则

URI 路径遵循以下规则：

```
https://rest_api_root/v1[/{area}]/{resource}
```

`rest_api_root` 表示REST API的根路径，在不同的环境中rest_api_root值有所不同：

```
公有云环境的rest_api_root值为：https://open.pingcode.com
私有部署环境的rest_api_root值为：https://xxxxxx/open
```

`oauth2_root` 表示OAuth2页面的根路径，在不同的环境中oauth2_root值也有所不同：

```
公有云环境的oauth2_root值为：https://open.pingcode.com/oauth2
私有部署环境的oauth2_root值为：https://xxxxxx/oauth2
```

## 示例

接口路径示例：

```
https://open.pingcode.com/v1/scm/products
https://open.pingcode.com/v1/scm/products/{product_id}/repositories
https://open.pingcode.com/v1/release/environments
```
