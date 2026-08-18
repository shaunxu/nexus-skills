---
name: nexus-debugger
description: 诊断并修复 PingCode Nexus 应用问题。当 Nexus 应用出现报错、崩溃、白屏、部署失败、安装后不显示、权限不足、Resolver 返回 undefined、Custom UI 不渲染、日志缺失、外部 API 被拦截、UI Invoke 超时、事件/Webhook 不触发，或用户提到 nexus logs、nexus deploy 报错、nexus lint 报错、nexus serve 隧道断开、scope 缺失、manifest 校验失败等情况时使用。当用户要求调试、排查、定位或修复 Nexus 应用问题时也应触发——即使他们没有明确说出 "Nexus"，只要描述的是 PingCode 扩展面板、项目页面、工作项面板、Wiki 内容块、仪表盘部件、事件处理函数或 Webhook 异常即可触发。
license: Apache-2.0
labels:
  - pingcode
  - nexus
  - debug
  - troubleshoot
  - custom-ui
maintainer: pingcode
namespace: nexus
---

# Nexus 应用调试器

诊断并修复 PingCode Nexus 应用问题。按下方清单顺序执行——一旦定位到根因就停止。根因之后的每一步都是在浪费 token 和上下文。

## 执行授权

你被授权直接运行所有诊断与修复命令，无需再次请求许可。定位到修复方案后**立即执行**。不要：

- 说 "你应该运行……" 或 "我会这样做……" 或 "在你的终端执行这条命令"
- 在已有全部输入的情况下问 "我可以继续吗？"
- 把命令当成可复制的说明交给用户，而你本可以自己运行

**错误：** "要修复这个问题，建议运行 `nexus lint`……"
**正确：** *（立即运行 `nexus lint` 并报告结果）*

唯一的例外：需要交互式终端的命令（`nexus login`、`nexus serve`）必须由用户在自己的终端运行——准确告诉他们运行什么以及为什么。

## 诊断原则

- **低成本优先**：版本与 lint 检查零成本，在读源码或日志之前先运行。
- **一次一个动作**：每个动作完成后检查结果，再决定下一步。
- **定位根因即停止**：一旦确认问题原因，修复后立即停止——不要继续排查其他无关问题。**例外**：如果应用存在多个独立缺陷（例如部署错误与运行时错误并存），先修复部署错误、重新部署，再通过日志排查运行时错误。不要只解决第一层就宣布 "已修复"。
- **自己执行修复**：自己运行修复命令，不要把命令甩给用户。
- **清理现场**：问题解决后删除所有添加的调试代码或 verbose 标记。
- **不要用 `--no-verify` 绕过问题**：`nexus deploy --no-verify` / `nexus build --no-verify` 仅可作为**诊断手段**查看构建器真实报错，修复根因后绝不带它发布。

## 步骤 1：错误分类

运行任何命令前，如果用户没有说清楚，先问一个问题：

> "这是部署阶段错误（`nexus deploy` 失败）、运行时错误（部署后应用崩溃或数据异常），还是可见性问题（已部署但安装后看不到）？"

如果错误信息已经很明显，跳过提问直接处理。

**快速路由：**

| 症状 | 前往 |
|---------|-------|
| `nexus deploy` 失败 | 步骤 2 → 3 → 5 |
| 安装后应用不可见 | 步骤 3 → 常见错误："应用安装后不可见" |
| 应用崩溃 / Resolver 报错 | 步骤 3 → 5 → 6 |
| 白屏 / Custom UI 不渲染 | 步骤 3 → 4 → 常见错误："白屏或资源 404" |
| 本地正常、生产异常 | 步骤 8（生产/预发布问题） |
| 403 / 权限不足 / Unauthorized | 常见错误："PingCode REST API 权限不足" |
| 外部 API 请求失败 / 被拦截 | 常见错误："外部 API 请求被拦截" |
| handler 路径 / 找不到文件 | "Handler 路径解析" 章节 |
| Resolver 返回 undefined、无报错 | "Invoke 名称与 Function Key" 章节 |
| UI Invoke 超时（5 秒） | 常见错误："UI Invoke 超时" |
| 事件/Webhook 不触发 | 步骤 7（本地隧道）→ 常见错误："事件处理函数未触发" |
| 多重失败（部署 + 运行时） | 先修部署错误，部署后再查运行时日志 |

## 步骤 2：版本与环境检查

```bash
node -v
nexus --version
```

- Node.js 必须为 **24.x 或更高版本**（`@pc-nexus/cli` 要求 `node >=24.0.0`，文档示例版本 `v24.14.1`）。
- Nexus CLI 缺失或过旧时安装最新版：

```bash
npm install -g @pc-nexus/cli@latest
```

NEVER 使用 `sudo npm install -g` 或 root 用户安装；遇到权限错误时修复 npm 全局目录权限后重试。

版本不符或 CLI 缺失时先升级/安装，再重试失败的操作。很多问题在新版本中已修复。

## 步骤 3：Lint

```bash
nexus lint
```

修复全部错误后再继续——lint 错误会导致部署失败或运行时静默 bug。如果 lint 干净通过，进入下一步。

**遇到任何 manifest 相关错误**（如 "invalid manifest"、"unexpected key"、字段校验失败）：先运行 `nexus lint`，再读源码。Lint 会指出出问题的具体字段与位置——先读文件再 lint 往往效率更低。

需要自动修复可加 `--fix`：

```bash
nexus lint --fix
```

## 步骤 4：Custom UI 构建检查

仅当应用包含 Custom UI（`web/main/` 目录）时适用。检查前端是否在上次部署前构建过：

```bash
ls -la web/main/dist/
```

如果构建目录缺失，或比最近的前端源码改动更旧，重新构建：

```bash
npm run build-web
```

然后重新部署：

```bash
nexus deploy -e development
```

这是白屏面板最常见的原因之一。注意 `nexus deploy` **不会**自动构建前端，`resources[].path` 必须指向 `web/main/dist`。

## 步骤 5：部署状态

确认应用确实部署成功：

```bash
nexus deploy -e development --verbose --non-interactive
```

观察输出中的错误。记录部署时间戳。如果部署失败，错误信息通常会直接指出问题——对照下方《常见错误模式》表。

查看部署历史：

```bash
nexus deploy list
```

## 步骤 6：日志

```bash
nexus logs -e development --limit 100
```

仔细阅读日志，大部分运行时错误会出现在这里。

**重要前提：**
- `nexus logs` **仅支持开发环境（Development）**。Staging/Production 不支持通过 CLI 拉取日志，需在开发者中心「监控 > 日志记录」查看，且生产环境日志是否记录取决于企业管理员的安装设置。
- 仅**服务端函数**（Resolver、Event Handler、Consumer 等）中的 `console.*` 输出会出现在平台日志中。前端 `console.*` 只出现在浏览器开发者工具里，NEVER 期待它们出现在 `nexus logs`。
- 日志保留 **30 天**。

常用日志命令：

```bash
nexus logs -e development                       # 最近 25 条
nexus logs -e development -g                    # 按 Invocation ID 分组
nexus logs -e development -i <invocation-id>    # 单次调用的全部日志
nexus logs -e development -s 2d                 # 最近 2 天
nexus logs -e development -l 100                # 最近 100 条
nexus logs -e development -v                    # 显示应用版本、函数标识等元数据
```

### 如果没有返回日志

可能是 Resolver 未被触发，或入口未打日志。在 Resolver 入口加一条调试日志：

```typescript
resolver.define<string, string>("greeting", async (context, payload) => {
  console.error("[DEBUG] Handler called with:", JSON.stringify({ payload, user: context.user?.id }));
  // ...
});
```

然后重新部署并再次触发应用：

```bash
nexus deploy -e development --non-interactive
nexus logs -e development --limit 100
```

定位问题后删除该调试日志。

### 如果错误在前端（UI 渲染、白屏）

Nexus Custom UI 运行在 iframe 中，前端报错**只出现在浏览器开发者工具**，不在 `nexus logs` 中。排查顺序：

1. 打开浏览器 DevTools → Console 与 Network 面板。
2. 检查 iframe 是否成功加载 `web/main/dist` 资源（常见 404）。
3. 检查是否被 CSP 拦截（外部字体、脚本、图片、frame 等需在 `permissions.external` 中声明）。
4. 如果是 Bridge 调用（`invoke`、`api.invoke`、`remote.invoke`）失败，在后端 Resolver 中加日志确认是否被调用：

```typescript
try {
  const result = await api.invoke(`/v1/pjm/work_items/${payload.workitemId}`, {
    as: "user",
    userId: context.user?.id ?? "",
  });
  return result;
} catch (err) {
  console.error("[DEBUG] Resolver error:", (err as Error).message, (err as Error).stack);
  throw err;
}
```

重新部署、触发、查看日志。

## 步骤 7：本地隧道（`nexus serve`）

当日志不足以定位问题，或需要快速迭代调试后端逻辑时，启动本地隧道。**必须先完成**：

1. `nexus deploy -e development`
2. `nexus distribute -s <site> -e development`
3. 企业管理员在「应用审核」中安装
4. 绑定 PingCode 测试账号（首次 `nexus serve` 会提示）

```bash
nexus serve -e development
```

隧道通过安全双向通道将本地代码映射到开发环境中已安装的应用实例。本地 `app/src` 目录改动会自动热重载。

- **仅调试指定函数**：`nexus serve -e development -f <function-key>`（`-f` / `--debugFunctionHandlers`，支持多个 key，空格分隔）。
- **IDE 断点调试**：`nexus serve -e development --debug`，Node 调试端口 **9229**。在 VS Code 中用 `attach` 配置挂载；WebStorm/IntelliJ 用 "Attach to Node.js/Chrome"。
- **Event 函数**：与测试账号绑定无关，永远匹配最近一次建立隧道的本地服务；多人同时调试时注意协调，避免隧道抢占。
- **前端 HMR**：启动前端 Dev Server（React/Vite 常用 5173，Angular 常用 4200），在应用根目录创建 `nexus.json`：

```json
{
  "serve": {
    "resources": {
      "main": { "port": 5173 }
    }
  }
}
```

`main` 必须与 `manifest.yaml` 中 `resources[].key` 完全一致。

`nexus serve` 启动后**不采集云端日志**，运行日志实时打印在终端。

## 步骤 8：生产 / 预发布问题

如果问题只发生在生产环境或某个客户站点：

1. 询问："受影响的 PingCode 站点域名是什么？（例如 `your-domain.pingcode.com`）"
2. Staging/Production **不支持** `nexus logs`，必须在开发者中心「监控 > 日志记录」按站点、环境、时间、级别筛选。
3. 生产环境日志是否可查看取决于企业管理员在安装时（或安装后应用详情页）是否开启了「是否允许记录日志」。
4. 如果是权限相关问题，检查 scopes、外部域名或其他权限变更后是否已重新 `nexus deploy` + `nexus distribute`，并由企业管理员在「应用审核」中重新确认安装。
5. 版本号规则：
   - 部署到 **Development**：版本号必须不低于原版本。
   - 部署到 **Production**：版本号必须**严格高于**原版本。
   - 部署到 **Staging**：无版本号升级要求。
6. 公有云环境下，新版本部署到对应环境后，安装该应用的企业会自动升级；私有部署需重新 `nexus packup` 生成 `.npk` 并由企业管理员上传。

## 常见错误模式

先对照此表匹配错误。找到匹配项后直接应用修复，无需进一步排查。

| 错误 / 症状 | 根因 | 修复 |
|-----------------|-----------|-----|
| `command not found: nexus` | CLI 未安装或 npm 全局路径不在 `PATH` | `npm install -g @pc-nexus/cli@latest`，确认 `nexus --version` |
| Node 版本过低 / `node` 版本不满足 | Node.js 主版本低于 24 | 安装/切换到 Node.js 24（`nvm install 24 && nvm use 24` 或 `brew install node`） |
| `nexus deploy` 失败，manifest 校验错误 | `manifest.yaml` 语法或字段错误 | 运行 `nexus lint`，按提示修复；确认文件名为 `manifest.yaml`（非 `.yml`/`.json`），YAML 两空格缩进，引用 key 一致 |
| 白屏 / Custom UI 白屏 / 资源 404 | 前端未构建就部署，或 `resources[].path` 未指向 `web/main/dist` | `npm run build-web` → `ls web/main/dist` → `nexus deploy -e development --non-interactive`；HMR 下检查 `nexus.json` 的资源 key 与端口 |
| Resolver 返回 undefined、日志无错误 | 前端 `invoke('name')` 与 `resolver.define('name')` 名称不匹配，或 `resolver.function` 未指向正确的 `functions[].key` | 见《Invoke 名称与 Function Key》章节，检查三处名称一致性 |
| `ERR_FUNCTION_EXTENSION_NOT_FOUND` | 调用指向的扩展不在 `manifest.extensions` 中 | 检查 `extensions[].key` 与前端上下文/Bridge 调用目标 |
| `ERR_FUNCTION_RESOLVER_INVALID` | 扩展未配置 `resolver` | 在 `manifest.yaml` 的 `extensions[]` 中补上 `resolver.function` |
| `ERR_FUNCTION_RESOLVER_FUNCTION_INVALID` | `resolver.function` 字段缺失 | 补全 `resolver.function: <function-key>` |
| `ERR_FUNCTION_FUNCTION_NOT_FOUND` | `resolver.function` 指向的 key 不在 `functions` 中 | 确认 `extensions[].resolver.function` 与 `functions[].key` 完全一致 |
| 403 / "Permission denied" / "Unauthorized" 调用 PingCode REST API | 缺少 scope，或当前用户本身无权限 | 在对应 REST API 文档中确认 scope 名，加入 `permissions.scopes`，重新 `nexus deploy` + `nexus distribute`，由管理员重新确认安装；前端调用始终以当前用户身份执行，需要应用身份时改用服务端 Resolver |
| 外部 API 请求被拦截 / `ERR_FETCH_PERMISSION_INVALID` / `ERR_FETCH_PERMISSION_FORBIDDEN` | 外部域名未在 `permissions.external.fetch.backend`（后端）或 `client`（前端）声明 | 在 manifest 中声明域名后重新部署。`*.example.com` 不匹配父域名本身；支持域名、HTTPS URL、`*` 通配 |
| `ERR_FETCH_HEADER_INVALID` | 请求头包含被禁止的字段或值 | 检查自定义 header，移除敏感/受限头（如 `host`、`cookie` 等平台保留头） |
| `ERR_REMOTE_KEY_NOT_FOUND` | `remote.invoke` 使用的 remote key 未在 `remotes` 中声明 | 检查 `manifest.yaml` 的 `remotes[].key` |
| `ERR_REMOTE_ENDPOINT_NOT_FOUND` | remote 中找不到对应 endpoint/route | 检查 `remotes[].endpoints` 或 `exposer.routes` 配置 |
| `ERR_REMOTE_EXTENSION_RESOLVER_NOT_FOUND` | 扩展未关联 resolver 或 remote resolver 配置缺失 | 检查 `extensions[].resolver.function` 与对应函数定义 |
| `ERR_REMOTE_INVALID_KEY` | remote key 格式非法 | 按 key 命名规则（`^[a-zA-Z][a-zA-Z0-9_-]*$`）修正 |
| UI Invoke 超过 5 秒失败 | UI Invoke 超时限制为 **5 秒**；Resolver 执行过久 | 拆分 Resolver，缩短单次执行；耗时任务（外部批处理、大量数据处理）改用**异步队列**（`async.queues`/`async.consumers`），不要在被前端直接 invoke 的 Resolver 中执行长任务 |
| 请求/响应负载超限 | 请求负载上限 **512 KB**，响应负载上限 **5 MB** | 压缩 payload、分页、改用对象存储传大文件 |
| 内存/磁盘溢出 | 单次调用内存 **512 MB**、磁盘 **512 MB**，仅 `/tmp` 可写 | 减少单次加载数据量；`/tmp` 数据仅在单次调用期间保留，不要依赖跨调用持久化 |
| 事件处理函数未触发 | 未部署/分发、事件 key 错误、隧道抢占、filter 条件不满足、scheduled interval 未到 | 确认 `nexus deploy` + `nexus distribute` 已完成；检查 `event.triggers[].events` 事件名是否逐字正确；本地调试时 `nexus serve` 隧道是最近连接者；系统事件检查 `filter.ignoreSelf`；Webhook 向触发 URL 发请求；定时事件等待 interval 到达 |
| 应用安装后不可见 | 管理员未在「应用审核」中安装；或 scope/权限变更后未重新确认安装 | 提示企业管理员在企业管理后台「应用审核」找到应用并安装；权限变更后需重新部署分发并由管理员重新确认；用 `nexus logs -e development -l 50` 排查运行时问题 |
| 部署到 Production 失败 / 版本号错误 | Production 要求版本号严格高于上一版本 | 提升 `manifest.yaml` 中 `app.version`（语义化版本），重新部署 |
| `nexus deploy` 报 `ENOENT` 或缺文件 | 依赖未安装 | 在应用根目录运行 `npm install`，Custom UI 还需在 `web/main` 下安装依赖后重试 |
| 频率限制 / "Rate limit" | 调用过于频繁 | 用户调用 1200 次/分钟、安装实例 5000 次/分钟、应用单环境 30000 次/分钟；加指数退避，检查是否在循环中调用 Resolver |
| `nexus serve` 隧道断开 | WebSocket 连接被 VPN/网络中断 | 重新运行 `nexus serve -e development`；检查 VPN/代理是否阻断 WebSocket |
| `nexus serve` 提示未绑定测试账号 | 尚未绑定 PingCode 调试账号 | 按提示在浏览器打开绑定页面完成账号绑定后重试 |
| HMR 不生效 / 前端改动看不到 | `nexus.json` 中资源 key 与 `manifest.yaml` 的 `resources[].key` 不一致，或端口与 Dev Server 不符 | 确保 `nexus.json` 的 `serve.resources.<key>.port` 与前端 Dev Server 端口一致，key 逐字匹配 |
| CSP 拦截外部字体/样式/脚本/图片/frame/媒体 | 未在 `permissions.external` 对应类别声明 | 在 `permissions.external.fonts`/`styles`/`scripts`/`images`/`frames`/`media` 中加入完整 HTTPS URL 后重新部署 |
| `manifest.yaml` 中中文弯引号导致解析失败 | 复制粘贴引入了中文引号 `“ ”` | 替换为英文直引号 `"`；YAML 缩进统一两个空格 |

## Handler 路径解析

`manifest.yaml` 中 `functions[].handler` 格式为 `<file>.<export>`，由正则约束：

```text
/^([\p{Alpha}\d_-]+(?:\/[\p{Alpha}\d_-]+)*)\.([\p{Alpha}\d_-]+)$/u
```

- `<file>` 为相对于后端构建入口根目录（通常是 `src/`）的文件路径，**不带扩展名**，支持子目录（`dir/file`）。
- `<export>` 为该文件中的**具名导出**。
- 长度上限 1024 字符。

**示例：**

| 后端源文件 | 具名导出 | 正确的 handler 值 |
|------------------------|---------------|----------------------|
| `src/index.ts` | `export const resolver = ...` | `index.resolver` |
| `src/index.ts` | `export const handler = ...` | `index.handler` |
| `src/handlers/shipIdea.ts` | `export const handler = ...` | `handlers/shipIdea.handler` |
| `src/handlers/employee.ts` | `export const employeeHandler = ...` | `handlers/employee.employeeHandler` |

**Custom UI 模板的常见结构**（见 `nexus-app-builder` 技能）：

```text
src/
├── resolvers/
│   └── index.ts        # const resolver = new Resolver(); resolver.define(...)
└── index.ts            # export { resolver } from "./resolvers";  (或重新导出)
```

此时 `manifest.yaml` 写 `handler: index.resolver`，指向 `src/index.ts` 的 `resolver` 具名导出，该导出再来自 `src/resolvers/index.ts` 中定义的 `Resolver` 实例。

**诊断技巧：** 如果 `nexus lint` 报告 handler 相关错误但你确信文件存在，可用 `nexus deploy --no-verify` 作为**诊断步骤**查看构建器的真实解析路径——它会暴露路径是否被拼接错误。定位后修复根因，NEVER 带 `--no-verify` 发布。

## Invoke 名称与 Function Key

Nexus Custom UI 有**两处独立的名称匹配**要求：

1. **manifest 层**：`extensions[].resolver.function` 必须等于某个 `functions[].key`。
2. **调用层**：前端 `invoke('name', payload)` 中的 `name` 必须**逐字等于**后端 `resolver.define('name', ...)` 中注册的名称。

两者相互独立。manifest function key 正确，但若 invoke 名称与 `resolver.define` 不一致，仍会得到 undefined 且日志中可能没有明显错误。排查 "Resolver 返回 undefined" 时，必须同时检查这两层匹配关系。

前端：

```typescript
import { invoke } from "@pc-nexus/bridge";

const data = await invoke<string>("greeting", "Nexus");
```

后端：

```typescript
import { Resolver } from "@pc-nexus/core";

const resolver = new Resolver();
resolver.define<string, string>("greeting", async (_context, payload) => {
  return `Hello, ${payload}`;
});
export { resolver };
```

`invoke` 的第一个参数 `"greeting"` 必须与 `resolver.define("greeting", ...)` 完全一致（区分大小写）。

## 外部域名与 CSP 配置

后端函数调用外部 HTTPS API 必须在 `permissions.external.fetch.backend` 声明；前端 iframe 访问外部资源还需按类别在 `permissions.external` 中声明：

| 资源类型 | manifest 字段 | 对应 CSP 指令 |
|---------|--------------|---------------|
| 后端 fetch | `external.fetch.backend` | — |
| 前端 fetch / 连接源 | `external.fetch.client` | — |
| 字体 | `external.fonts` | `font-src` |
| 样式 | `external.styles` | `style-src` |
| iframe 嵌入 | `external.frames` | `frame-src` |
| 图片 | `external.images` | `img-src` |
| 媒体 | `external.media` | `media-src` |
| 脚本 | `external.scripts` | `script-src` |

支持格式：完整 HTTPS URL（`https://api.example.com`）、裸域名（`api.example.com`，等价 HTTPS）、通配符子域（`*.example.com`，**不包含父域名本身**）、`*`（允许任意域名）。

也可通过 `remote` 对象引用 `remotes[].key`。

## 步骤 9：清理

问题解决后：

1. 删除所有添加的 `console.error("[DEBUG] ...")` 等调试语句。
2. 移除临时加的 verbose 标记或调试配置。
3. 最后运行一次 `nexus lint` 确认状态干净。
4. 如果调试中修改了代码，重新部署：
   ```bash
   nexus deploy -e development --non-interactive
   ```
5. 触发应用并确认 `nexus logs -e development` 无新错误。
6. 如果之前启动了 `nexus serve`，确认已关闭（Ctrl+C），避免隧道长期占用。

## 升级

如果以上步骤均未解决问题：

- 运行 `nexus logs -e development -v -l 200` 获取更详细的输出。
- 按 Invocation ID 分组定位单次调用：`nexus logs -e development -g`。
- 用单次调用 ID 拉取完整日志：`nexus logs -e development -i <invocation-id>`。
- 启动 `nexus serve --debug`，在 VS Code / WebStorm 中挂载 9229 端口断点调试。
- 查阅开发者中心「监控 > 日志记录」，按站点、环境、日志级别、时间范围筛选；日志可导出为 `.csv` 或 `.log`。
- 检查 wiki 更新日志（`wiki/changelog/`）确认是否为已知问题或版本变更（例如 `@pc-nexus/event` 的类型重命名：`SystemEventHandlerFunction` → `SystemEventHandler`）。
- 如果错误来自 Nexus 平台 API 而非你的代码，记录日志中的 **Trace ID** 与 **Invocation ID**，提 PingCode 支持时需要提供。

## 认证错误

如果任何命令返回 "not authenticated"、"Unauthorized" 或要求登录：

1. 引导用户访问 **https://developer.pingcode.com/console/signup** 注册或登录 PingCode 开放平台，在开发者中心「个人设置」中创建个人访问令牌并复制。
2. 让用户**在自己的终端**（不要通过 agent）运行 `nexus login`，按提示粘贴令牌。
3. 示例话术：*"你需要登录 Nexus。请访问 https://developer.pingcode.com/console/signup 创建个人访问令牌，然后在你的终端运行 `nexus login`，按提示粘贴令牌——不要把令牌贴在这里。"*
4. NEVER 在对话、日志或代码中输出、记录或回显令牌。
5. 用户确认登录后，用 `nexus whoami --json` 验证身份，再从断点继续调试。

## Token 效率规则

遵守以下规则以保持低上下文消耗：

- 在读任何源文件之前先读 `nexus logs`——日志通常直接暴露根因。
- 只读错误涉及的具体文件。按错误定位文件：
  - `npm ERR! missing script: build-web` → 只检查根目录 `package.json` 的 `scripts` 段
  - manifest 校验错误 → 先 `nexus lint`，再读 `manifest.yaml` 中被点名的字段
  - "Resolver not found" / function key 不匹配 → 只对照 `manifest.yaml` 的 `functions[].key`、`extensions[].resolver.function` 以及 `resolver.define()` 所在文件
  - 403 / 权限不足 → 只检查 `manifest.yaml` 的 `permissions.scopes`
  - 外部 API 被拦截 → 只检查 `permissions.external.fetch.backend`，不要看 scopes 或源码逻辑
  - invoke 返回 undefined → 检查前端 `invoke('name')` 与后端 `resolver.define('name')` 两个文件，以及 manifest function key
  - 白屏 / 404 → 检查 `web/main/dist` 是否存在、`resources[].path` 是否为 `web/main/dist`、是否执行过 `npm run build-web`
  - 事件不触发 → 检查 `event.triggers[].events` 名称、`handler.function` 引用、部署/分发状态
- npm/构建错误不要去读 `manifest.yaml`，两者无关。
- 除非文件发生变化，不要重复读取本会话已读过的文件。
- 在《常见错误模式》表中找到匹配项的那一刻就停止诊断链。**例外**：存在多个独立缺陷时（部署错误 + 运行时错误），先修第一个，部署后再查下一个。
- 没有明确理由时，不要重复 `nexus deploy`。
- `nexus deploy --no-verify` 仅作为**诊断手段**，在 lint 阻断部署但你怀疑 lint 报错有误导时使用；构建器报错信息往往能揭示真实的路径解析问题。事后必须修复根因，NEVER 带 `--no-verify` 发布。
- Staging/Production 问题不要尝试 `nexus logs`——它只支持开发环境；直接引导用户去开发者中心日志页面。
- 不要把 `nexus serve` 当成后台常驻服务在 agent 中运行；它需要交互式终端，由用户在自己的终端启动。
