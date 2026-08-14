# Nexus 应用构建技能

引导构建、部署、分发和安装 PingCode Nexus 应用（项目页面、工作项面板、仪表盘部件、Wiki 内容块、事件处理函数、Webhook 等）。构建任何 Nexus 应用时使用。提供自动化的 `nexus create` 工作流、扩展点选择、CLI 命令以及部署脚本。

## 安装

本技能随附于 **[Nexus Skills](https://github.com/shaunxu/nexus-skills)** 插件包中（路径 `skills/nexus-app-builder/`）。建议将该仓库作为插件安装到你的编辑器或 CLI 中，以便同时获得本技能、Nexus CLI 工具链以及配套配置。Cursor、Claude Code、Codex、Copilot CLI 等环境下的具体安装方式，请参考 [nexus-skills README](https://github.com/shaunxu/nexus-skills/blob/main/README.md)。

### 仅使用本技能目录（高级）

如果你的宿主环境支持从任意路径加载技能，可以将其指向 [nexus-skills](https://github.com/shaunxu/nexus-skills) 仓库检出目录中的 `skills/nexus-app-builder`。例如，克隆仓库后将其软链到全局技能目录：

```bash
git clone https://github.com/shaunxu/nexus-skills.git ~/dev/nexus-skills
ln -s ~/dev/nexus-skills/skills/nexus-app-builder ~/.agents/skills/nexus-app-builder
```

根据你使用的工具调整目标路径（`.cursor/skills/`、`.claude/skills/`、`.agents/skills/` 等）。仅做软链不会自动带入仓库根目录的配置文件；如需完整能力，请安装完整插件或自行补齐相应配置。

---

## 本技能提供的能力

- **自动化工作流** —— 校验前置条件，通过 `nexus create` 脚手架应用，并完成部署与分发。
- **扩展点选择** —— 覆盖 PJM、Ship、Wiki、TestHub 以及全局 Platform 的扩展点（项目页面、工作项面板、仪表盘部件、Wiki 内容块、事件/Webhook 等）。
- **辅助脚本** —— 用于创建应用、部署分发，以及在线检索官方文档的 Python 脚本。
- **参考文档** —— 涵盖 CLI 工作流、`manifest.yaml`、后端 Resolver、Custom UI 前端和扩展点列表。

完整技能内容请见 [SKILL.md](SKILL.md)。
