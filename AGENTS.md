# AGENTS.md

面向在本仓库工作的 AI agent 的高信号指引。所有内容均已从仓库现有文件验证。

## 仓库性质

这是一个 **PingCode Nexus 技能插件仓库**（不是 Nexus 应用本身，也没有构建/测试流水线）。产物是 `skills/` 下的 4 个技能目录，每个包含一个 `SKILL.md` 作为入口：

- `nexus-app-builder/` — 脚手架、部署、分发（含 `references/`、`scripts/`、`evals/`）
- `nexus-app-reviewer/` — 发布前就绪审查
- `nexus-debugger/` — 故障诊断
- `nexus-security-reviewer/` — 白盒安全审计（含 `assets/security-rules/`、`scripts/`）

仓库根的 `plugin.json` 声明 `skills: ["./skills/"]` 和 MCP 服务器（`.mcp.json`，指向 `https://mcp.pingcode.com/v1/nexus/mcp`）。

## 关键约束（容易踩坑）

- **没有 build/test/lint/typecheck 命令**。根目录和技能内的 `package.json` 都是空对象 `{}`，仅用于占位；不要尝试 `npm install`、`npm run build` 或 `npm test`。
- **Python 脚本直接运行，无包管理**。例如：
  ```bash
  python3 -m scripts.search_nexus_docs "resolver" --max-pages 3
  ```
  必须在技能目录（如 `skills/nexus-app-builder/`）下运行，以便 `scripts/` 作为模块解析。需要 Python 3。
- **`SKILL.md` frontmatter 字段固定**：`name`、`description`、`license: Apache-2.0`、`labels`、`maintainer: pingcode`、`namespace: nexus`。修改技能时保持这些字段一致。仓库根许可证为 MIT，但每个技能文件头声明 Apache-2.0——不要"统一"它们。
- **技能正文以中文书写**，与现有 4 个 `SKILL.md` 保持一致。
- **`wiki/` 是外部参考资料快照，不是技能内容来源**。`nexus-app-builder` 明确要求 NEVER 引用 `samples/` 或 `wiki/`；回答 Nexus 专属问题时优先查 `references/`，不确定时跑 `scripts/search_nexus_docs.py`（用英文关键词）。
- **`plugin.json` 的 `skills` 字段是目录路径数组**（`["./skills/"]`），不是技能名列表——新增技能放到 `skills/` 下即可被自动发现，无需改此文件。

## 目录约定

| 路径 | 用途 | agent 注意事项 |
| --- | --- | --- |
| `skills/<name>/SKILL.md` | 技能入口，含 YAML frontmatter 和工作流正文 | 修改时遵循 MUST/NEVER 这类大写关键词的现有语气 |
| `skills/<name>/references/` | 技能可引用的长文档（仅 `nexus-app-builder` 有） | 只在该技能工作流中引用；其他技能不读 |
| `skills/<name>/scripts/` | Python 辅助脚本 | 用 `python3 -m scripts.<name>` 调用；`__pycache__/` 已被 gitignore |
| `skills/<name>/assets/` | 规则资产（仅 `nexus-security-reviewer` 有 `security-rules/`） | 安全审查按 manifest 驱动按需加载，不要一次性读全部规则 |
| `skills/<name>/evals/evals.json` | 技能评测用例（仅 `nexus-app-builder` 有） | 是期望行为契约；改技能逻辑时对照检查 expectations |
| `wiki/` | 外部文档镜像 | 只读参考；不要修改，也不要在技能输出里直接引用其路径 |
| `.claude/settings.local.json` | 本地 Claude 配置 | 不要提交本地个人设置变更 |

## 技能内容中反复出现的平台事实（跨技能一致，改动时保持同步）

如果修改任何技能中涉及这些事实的段落，确保 4 个技能口径一致：

- CLI 命令是 `nexus`，npm 包前缀是 `@pc-nexus/*`——**禁止**出现 Atlassian Forge 的 `forge`、`@forge/*`、Jira/Confluence 字样。
- Manifest 文件名固定为 `manifest.yaml`（不是 `.json` 或 `.yml`）。
- Nexus 要求 Node.js ≥ 24。
- Nexus **没有** `nexus install` 命令；应用经 `nexus distribute` 后必须由企业管理员在后台手动安装。
- `nexus deploy` 不自动构建前端；前端改动后必须先 `npm run build-web`。
- Agent 绝不在对话中索要/接收 API 令牌；引导用户在自己的终端执行 `nexus login`。
