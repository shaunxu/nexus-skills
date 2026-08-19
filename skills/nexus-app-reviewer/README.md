# Nexus 应用审查 Skill

对 PingCode Nexus 应用执行轻量级发布前就绪审查。在部署或交接前，用作广泛的"这个应用能发布了吗？"检查。

本 skill 是审查入口。它检查 Nexus 应用是否看起来可以 lint、构建、部署、安装和维护，然后将更深层的问题路由到专业 skill，而不是复制它们的规则手册。

## 适用场景

- 通用 Nexus 应用审查
- 部署前或发布就绪检查
- Manifest/模块/函数/资源连线
- 架构与可维护性审查
- 依赖、运行时、脚本与验证健全性检查
- 发现需要专业跟进的明显安全或调试信号

## 不适用场景

- 完整 SAST、可利用性分析、CVSS 评分或密钥/授权/租户隔离审计
- 已知故障，如白屏、部署/安装失败、Resolver 错误或具体堆栈跟踪

Nexus 目前没有成本优化相关的 skill，平台也没有公开的计费规则；如关心资源消耗，本 skill 仅作为代码模式观察记录，不做具体成本估算。

## 专业 skill 交接

- 使用 `nexus-security-reviewer` 进行深度安全审计、SAST、授权、密钥、租户隔离、可利用性和 CVSS 报告。
- 使用 `nexus-debugger` 处理已知故障、错误信息、白屏、部署/安装问题、Resolver 错误、隧道/日志诊断以及停止工作的应用。
- 使用 `nexus-app-builder` 进行应用创建、部署与分发流程。

## 检查内容

- Manifest 引用：extensions、functions、resources、handlers、permissions（scopes、external.fetch、content/CSP）、event.triggers、remotes、endpoints、exposer、storage、async 队列/消费者、environment variables。
- 包结构：根目录与 `web/main/` 的 scripts、直接依赖、`@pc-nexus/*` 包匹配度，以及明显未使用或缺失的包。
- 源码连线：Custom UI 入口、Bridge 调用（`invoke`/`api.invoke`/`remote.invoke`）、Resolver 名称、handler 具名导出、PingCode REST API 调用（`as: "app"` vs `as: "user"`）、存储使用（KVS/CES/NOS）、外部 fetch、异步队列、日志。
- 运行 `nexus lint` 收集机械性问题。
- 就绪缺口：缺少验证命令、文档过期、行为风险足以支撑时缺失测试，以及专业 skill 跟进建议。

输出是一份简洁的就绪报告，包含按优先级排序的发现、无问题领域和建议下一步。

## 文件

- `SKILL.md`：触发条件、边界、工作流、检查项与报告模板，供 agent 宿主读取。

## 示例提示词

```text
审查我的 Nexus 应用，我准备部署了。
```

```text
这个 Nexus 应用能发布了吗？
```

```text
对这个 manifest 和源码做一次通用应用审查。
```

```text
检查这个 Nexus 应用是否发布就绪，有深度安全问题就路由到对应 skill。
```

完整工作流见 [SKILL.md](SKILL.md)。
