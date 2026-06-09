## Context

阶段1和阶段2已经告诉团队：

- 如何启动 caller-side trial
- 如何输出结果
- 如何把结果回传 provider

现在阶段3也需要一个同等清晰的入口，告诉团队：

- 看到 Phase 25 结果后到底怎么处理

这一步仍然保持轻量，不增加 provider 能力，只增加决策清晰度。

## Goals / Non-Goals

**Goals**

- 把 Phase 25 的输出状态映射为明确 follow-up 动作。
- 区分“继续 hold”、“人工 review”、“开 focused fix”。
- 保持 provider/caller 边界，不因为 review/blocked 就自动引入策略升级。

**Non-Goals**

- 不修改 Phase 25 运行逻辑。
- 不自动创建新的 change。
- 不自动判断 caller 仓库的内部问题。
- 不重新打开高级 RAG 技术路线。

## Decisions

- 矩阵按 Phase 25 `provider_action` 组织：
  - `no_provider_action_required`
  - `provider_review_required`
  - `provider_blocked`

- 每个状态说明：
  - default action
  - whether to reopen provider
  - what evidence to inspect next
  - what still remains out of scope

- 明确 `review` 不等于立即 reopen provider，必须先判断 provider-owned / caller-owned / corpus-owned。

## Risks / Trade-offs

- 如果矩阵太绝对，会误伤边界情况 -> 用“default action”而不是硬自动化动作。
- 如果矩阵太松，仍会回到口头讨论 -> 每个状态给出明确建议路径。
