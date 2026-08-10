---
title: 'Nexus 应用 manifest 开发者指南'
description: '面向 AI 的 PingCode Nexus 应用 manifest.yaml 结构、字段、权限与排错指南。'
platform: platform
product: nexus
category: devguide
subcategory: guides
date: '2026-08-10'
---

# Nexus 应用 manifest 开发者指南

## 相关指南

- nexus-development-guide

`manifest.yaml` 文件是每个 Nexus 应用的配置核心。它定义应用的唯一标识、扩展点、后端函数、静态资源以及权限范围。结构正确是应用能够成功构建、部署、分发并在企业中安装的前提。

## 1. 基本结构

每个 `manifest.yaml` 必须存在于应用根目录，文件名固定为 `manifest.yaml`。NEVER 将其命名为 `manifest.json`、`manifest.yml` 或其他名称。

每个 manifest 必须包含三个顶级部分：`app`、`permissions`，以及 `extensions` 或 `event` 中的至少一个：

```yaml
app:
  id: "466d303d-a2c4-4ec4-ad7c-5435be94583b"
  version: 1.0.0

extensions:
  - key: hello-world-project-page
    title: Hello World
    target: "pcm:pjm:project:page"
    resource: main
    resolver:
      function: resolver

functions:
  - key: resolver
    handler: index.resolver

resources:
  - key: main
    path: web/main/dist

permissions:
  scopes: []
```

所有顶级节点如下：

| 节点 | 必填 | 描述 |
|---|---|---|
| `app` | Y | 应用的基本信息（唯一标识、版本、许可等） |
| `permissions` | Y | 应用所需的权限列表（scopes、外部资源、CSP） |
| `extensions` | Y* | 应用扩展的模块列表，与 `event` 至少包含其一 |
| `event` | Y* | 应用事件订阅与发布列表，与 `extensions` 至少包含其一 |
| `functions` |  | 后端函数列表 |
| `resources` |  | Custom UI 静态资源列表 |
| `endpoints` |  | 远程后端端点列表 |
| `remotes` |  | 远程调用资源列表 |
| `storage` |  | 应用自定义实体存储定义 |
| `async` |  | 异步消息队列与消费者 |
| `exposer` |  | 对外暴露的自定义 REST APIs |
| `translations` |  | 多语言资源列表 |
| `environment` |  | 运行时环境变量声明 |

通用限制：

- Key 必须匹配正则 `^[a-zA-Z][a-zA-Z0-9_-]*$`，以字母开头，最大长度 `256`。
- Manifest 文件大小上限为 `256 KB`。
- 所有 `key` 在同一类型内必须唯一，且被其他节点引用时必须完全一致。

ALWAYS 使用两个空格作为 YAML 缩进，并使用英文直引号。NEVER 复制中文弯引号。

## 2. `app` 节点

### 必填属性

`id`：应用的全局唯一标识，由 `nexus create` 自动生成。NEVER 手动修改。

```yaml
app:
  id: "466d303d-a2c4-4ec4-ad7c-5435be94583b"
```

`version`：语义化版本，格式为 `主版本.次版本.修订号`，例如 `1.0.0`。

```yaml
app:
  id: "466d303d-a2c4-4ec4-ad7c-5435be94583b"
  version: 1.0.0
```

版本升级规则：

- 部署到 `Development`：版本号必须不低于原版本号。
- 部署到 `Production`：版本号必须严格高于原版本号。
- 部署到 `Staging`：没有版本号必须升级的要求。

### 可选属性

`licensing`：启用应用许可状态。启用后，企业安装时必须输入序列号才能使用。

```yaml
app:
  id: "466d303d-a2c4-4ec4-ad7c-5435be94583b"
  version: 1.0.0
  licensing:
    enabled: true
```

`name`、`publisher`、`description`、`avatar`、`links`、`links.support` 等展示属性由 CLI 根据开发者中心的数据在打包时自动写入。NEVER 在源码 manifest 中手动维护这些字段。

## 3. `extensions` 节点

`extensions` 定义应用在 PingCode 产品中出现的位置。每个扩展模块都必须声明 `key` 和 `target`，并根据需要关联静态资源、后端函数和显示条件。

### 基本结构

```yaml
extensions:
  - key: hello-world-project-page
    title: Hello World
    target: "pcm:pjm:project:page"
    resource: main
    resolver:
      function: resolver
    viewport:
      size: medium

resources:
  - key: main
    path: web/main/dist

functions:
  - key: resolver
    handler: index.resolver
```

通用属性：

- `key`：扩展模块的唯一标识。
- `target`：扩展点，例如 `pcm:pjm:project:page`。ALWAYS 从扩展模块参考中复制，NEVER 编造。
- `resource`：Custom UI 静态资源，必须与 `resources[].key` 完全一致。
- `resolver.function`：后端 Resolver 函数，必须与 `functions[].key` 完全一致。
- `title`：用户可见的展示名称，支持字符串或 i18n 对象。
- `display`：显示条件，见下一节。
- 其他扩展模块特定属性（例如 `viewport.size`）参考对应模块文档。

### Display conditions（显示条件）

通过 `display` 控制扩展模块在 UI 中的可见性。显示条件在客户端执行，可以被浏览器开发者工具覆盖。NEVER 将其作为保护敏感数据的唯一手段；ALWAYS 在后端代码中同时做权限校验。

```yaml
extensions:
  - key: hello-world-project-page
    target: "pcm:pjm:project:page"
    resource: main
    resolver:
      function: resolver
    title: Hello World
    display:
      and:
        hasPermission: "pca:global:pjm:configuration"
        project.name: scrum
        not:
          project.id: 111111
      or:
        workitem.identifier: TT-2
```

逻辑操作符：

| 操作符 | 描述 |
|---|---|
| `and` | 所有子条件为 `true` |
| `or` | 任一子条件为 `true` |
| `not` | 子条件取反 |

未显式包裹时，多个条件默认以 `and` 连接。

通用条件对所有扩展模块可用：

| 条件 | 描述 |
|---|---|
| `hasPermission` | 用户拥有指定权限点 |
| `isTeamOwner` | 是否为组织所有者 |
| `isLoggedIn` | 当前用户是否已登录 |

```yaml
display:
  hasPermission: "pca:global:pjm:configuration"
  isTeamOwner: true
```

上下文条件（例如 `project.name`、`workitem.type_group`）因扩展模块而异，ALWAYS 参考具体扩展模块定义中可用的上下文字段。NEVER 编造上下文字段名。

## 4. `functions` 节点

`functions` 定义应用使用的后端函数，供扩展模块、事件触发器、异步消费者和 exposer 路由引用。

```yaml
functions:
  - key: resolver
    handler: index.resolver
```

属性：

- `key`：后端函数唯一标识，在同一 manifest 中必须唯一。
- `handler`：处理函数路径，格式为 `file.function` 或 `dir/file.function`，长度不超过 `1024` 字符，必须匹配正则 `/^([\p{Alpha}\d_-]+(?:\/[\p{Alpha}\d_-]+)*)\.([\p{Alpha}\d_-]+)$/u`。

Custom UI 模板使用的 Resolver 入口通常位于 `src/resolvers/index.ts`，对应 handler 为 `index.resolver` 或 `resolvers/index.resolver`，以模板构建配置为准。

## 5. `resources` 节点

`resources` 定义 Custom UI 静态资源。每个资源目录必须包含 `index.html` 入口点。

```yaml
resources:
  - key: main
    path: web/main/dist
```

属性：

- `key`：资源唯一标识，被 `extensions[].resource` 引用。
- `path`：相对于应用根目录的静态资源目录。React/Angular Custom UI 模板 ALWAYS 指向 `web/main/dist`。

NEVER 在 `path` 中指向未构建的前端源码目录。前端改动后 ALWAYS 运行 `npm run build-web`，否则部署时资源会缺失或过期。

## 6. `permissions` 节点

`permissions` 声明应用所需的 OAuth 2.0 作用域、外部资源访问以及前端 CSP 选项。`scopes` 必填，即使为空数组也必须声明。

### Scopes

```yaml
permissions:
  scopes:
    - "pcp:read:pjm:workitem"
    - "pcp:write:pjm:workitem"
```

不调用任何 PingCode REST API 时：

```yaml
permissions:
  scopes: []
```

Nexus 平台 scope：

| Scope | 描述 |
|---|---|
| `pcp:read:app:token` | 读取以「应用」身份调用 APIs 的令牌 |
| `pcp:read:user:token` | 读取以「当前用户」身份调用 APIs 的令牌 |
| `pcp:storage:app` | 使用应用托管存储 |

调用 PingCode 产品 REST API 时，ALWAYS 在对应接口文档中确认所需 scope 后再声明。NEVER 编造 scope，也NEVER 在未声明 scope 的情况下调用 REST API。

### External permissions（外部资源）

`external` 声明应用允许访问的外部域名与资源类型。

```yaml
permissions:
  scopes: []
  external:
    fetch:
      backend:
        - "api.example.com"
        - "*.example-dev.com"
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

`fetch` 分为：

- `backend`：后端函数可访问的外部域名。
- `client`：前端允许连接的外部来源；在此声明的链接通过 `router.navigate` 打开时不会出现外部链接警告弹窗。

支持的域名格式：

| 格式 | 示例 | 说明 |
|---|---|---|
| HTTPS URL | `https://api.example.com` | 允许访问指定 URL 下的所有资源 |
| 域名 | `api.example.com` | 等价于 HTTPS |
| 通配符域名 | `*.example.com` | 匹配所有子域名，不包含父域名本身 |
| 全部域名 | `*` | 允许访问任意域名 |

也可以通过 `remotes` 引用远程资源：

```yaml
permissions:
  external:
    fetch:
      backend:
        - remote: remote-backend

remotes:
  - key: remote-backend
    baseUrl: "https://backend.example.com"
    operations:
      - fetch
```

其他 CSP 资源类型（`fonts`、`styles`、`frames`、`images`、`media`、`scripts`）分别声明浏览器对应指令允许加载的外部 URL，每个 URL 最大长度 `1024`。

NEVER 调用未在 `permissions.external.fetch.backend` 中声明的后端外部域名；未声明域名会被运行时拦截。

### Content permissions（CSP）

`content` 声明前端 Custom UI 所需的内联脚本和样式策略。

```yaml
permissions:
  content:
    scripts:
      - unsafe-inline
      - unsafe-hashes
    styles:
      - unsafe-inline
```

`scripts` 可用值：

| 值 | 描述 |
|---|---|
| `unsafe-inline` | 允许内联脚本（如 `<script>` 标签内代码） |
| `unsafe-hashes` | 允许特定内联事件处理器（如 `onclick="..."`） |
| `unsafe-eval` | 允许 `eval()` 及类似动态代码执行 |
| `blob:` | 允许通过 `blob:` URI 加载脚本 |
| `sha256-/sha384-/sha512-` | 通过哈希值精确允许特定内联脚本内容 |

`styles` 当前仅支持 `unsafe-inline`。

## 7. 可选顶级节点

### `remotes`

定义远程服务，供 `fetch.backend`、`endpoints` 和事件 handler 引用。

```yaml
remotes:
  - key: remote-backend
    baseUrl: "https://backend.example.com"
    auth:
      userToken: true
      appToken: false
```

属性：

- `key`：远程资源唯一标识。
- `baseUrl`：远程服务基础 URL，长度不超过 `2048`，必须匹配 `/^https?:\/\/[^\/\s]+(?:\/[^\s]*)?$/i`。
- `auth.userToken`：启用后调用令牌中包含当前用户令牌，必须同时声明 `pcp:read:user:token`。
- `auth.appToken`：启用后调用令牌中包含应用令牌，必须同时声明 `pcp:read:app:token`。

### `endpoints`

定义基于远程后端的端点。

```yaml
endpoints:
  - key: remote-trigger-boot
    remote: remote-backend
    route: /nexus-trigger
    auth:
      userToken: true
      appToken: false
```

`route` 会附加到 `remotes[].baseUrl` 之后。UI 模块的远程解析器端点路径由前端 `remote.invoke` 请求指定，不强制要求 `route`。

### `event`

声明事件订阅（`triggers`）和自定义事件发布（`registries`）。

```yaml
event:
  triggers:
    - key: ship-trigger
      type: system
      events:
        - pce:ship:idea:created
        - pce:ship:idea:updated
      handler:
        function: ship-idea-handler
      filter:
        ignoreSelf: true
  registries:
    - key: event-key
      name: Event name
      allowedRecipients:
        - app:466d303d-a2c4-4ec4-ad7c-5435be94583b

functions:
  - key: ship-idea-handler
    handler: shipIdea.handler
```

`triggers[].type` 支持以下类型：

| 类型 | 描述 |
|---|---|
| `system` | PingCode 产品事件，事件以 `pce:` 开头 |
| `app` | 其他应用通过 `registries` 声明的自定义事件，以 `nae:` 开头 |
| `lifecycle` | 应用生命周期事件，例如 `pce:nexus:app:install` |
| `webhook` | 通过 HTTP 请求端点触发 |
| `scheduled` | 定时触发，需配置 `interval`，可选 `timeout` |

`scheduled.interval` 取值：`tenMinute`、`hour`、`day`、`week`。

`system` 类型支持 `filter.ignoreSelf`，默认为 `false`；设置为 `true` 可忽略应用自身触发的事件，避免循环。

`registries` 定义应用对外发布的事件：

- `allowedRecipients` 默认为仅发布应用自身。
- 使用 `['*']` 允许所有应用订阅。
- 使用 `app:<app-id>` 仅允许指定应用订阅。

### `async`

定义异步消息队列和消费者。

```yaml
async:
  queues:
    - key: my-queue
  consumers:
    - key: my-consumer
      queue: my-queue
      handler:
        function: my-consumer-handler
      concurrency: 2
```

- `queues[].key`：队列唯一标识。
- `consumers[].queue`：必须引用已声明的队列。
- `consumers[].handler.function`：消息处理函数，引用 `functions[].key`。
- `consumers[].concurrency`：最大并行执行数，默认 `8`。

### `storage`

定义应用自定义实体存储。使用托管存储需要声明 `pcp:storage:app` scope。

```yaml
storage:
  entities:
    - name: employees
      attributes:
        - name: name
          type: string
          required: true
          default: ""
        - name: age
          type: integer
      indexes:
        - name: name_age
          keys:
            - name: 1
            - age: 1
          options:
            unique: true
```

实体命名规则：

- 只允许小写字母 `a-z`、数字 `0-9`、连接符 `-`、下划线 `_` 和点号 `.`。
- 不能以 `-` 或 `_` 开头。
- 开头和结尾不能是 `.`，不能包含连续的 `..`。
- 单个应用内实体名称不可重复。

### `exposer`

定义应用对外暴露的自定义 REST APIs 及其自定义作用域。

```yaml
exposer:
  routes:
    - key: get-employee-api
      path: /employeeName
      method: GET
      handler:
        function: employee-handler
      accept:
        - application/json
      scopes:
        - ncp:read:employee
  scopes:
    - name: ncp:read:employee
      displayName: Read Employee Info
      description: Read Employee Info
```

`routes[].method` 支持 `GET`、`POST`、`PUT`、`DELETE`、`PATCH`。`accept` 当前只支持 `application/json`。

自定义 scope 规则：

- 必须以 `ncp` 开头。
- 每个应用最多声明 `16` 个自定义 scope。
- 采用「动词+名词」命名，例如 `ncp:read:employee`、`ncp:write:employee`。

### `translations`

定义多语言资源。

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

`resources[].key` 使用 BCP-47 格式，当前支持：

| 语言 | 代码 |
|---|---|
| 中文（简体） | `zh-CN` |
| English (US) | `en-US` |

### `environment`

声明运行时环境变量。环境变量在部署时由平台注入，NEVER 在 manifest 或源码中硬编码密钥。

```yaml
environment:
  variables:
    - key: REMOTE_PREFIX
      default: "https://remote.example.com"
      description: "Prefix used to identify remote services."
```

属性：

- `key`：环境变量标识，必填。
- `default`：默认值，必填。
- `description`：变量说明，可选。

## 8. 完整示例

```yaml
app:
  id: "466d303d-a2c4-4ec4-ad7c-5435be94583b"
  version: 1.0.0

extensions:
  - key: workitem-status-panel
    title: Work Item Status
    target: "pcm:pjm:workitem:panel"
    resource: main
    resolver:
      function: resolver
    display:
      hasPermission: "pca:global:pjm:configuration"

functions:
  - key: resolver
    handler: index.resolver

resources:
  - key: main
    path: web/main/dist

permissions:
  scopes:
    - "pcp:read:pjm:workitem"
  external:
    fetch:
      backend:
        - "api.example.com"
    images:
      - "https://cdn.example.com"
  content:
    styles:
      - unsafe-inline

remotes:
  - key: example-api
    baseUrl: "https://api.example.com"
```

## 9. 关键提示

1. 校验引用一致性：`extensions[].resource` 必须等于 `resources[].key`；`extensions[].resolver.function` 必须等于 `functions[].key`。
2. 使用最小权限：只声明实际使用的 scopes，并在接口文档中确认每个 scope。
3. 外部域名：`*.example.com` 不匹配父域名 `example.com`，需要父域名时单独声明。
4. 前端资源：任何前端改动后 ALWAYS 运行 `npm run build-web`，再执行 `nexus deploy -e development`。
5. 显示条件仅用于 UI：敏感操作必须在后端做权限校验，NEVER 只依赖 `display`。
6. 变更 manifest 后 ALWAYS 重新部署；NEVER 假设 `nexus serve` 会让所有 manifest 变更立即生效。

## 10. 下一步

- 在扩展模块参考中查找具体 `target` 的完整属性。
- 在 PingCode REST API 文档中确认每个接口所需的 scope。
- 修改 manifest 后运行 `nexus deploy -e development`，确认输出包含 `Manifest is valid.` 和 `Lint passed.`。
- 如果 scopes、外部域名或其他权限发生变化，重新分发应用并由企业管理员重新确认安装。
