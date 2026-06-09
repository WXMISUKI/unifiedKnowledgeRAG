## Why

当前我们已经完成了：

- provider closure summary
- caller trial feedback runbook
- caller trial execution task pack
- caller trial outcome input contract
- Phase 25 provider-side feedback consumption

这意味着 post-closure 的 3 个阶段里，阶段1和阶段2已经准备好，阶段3也有基础能力。但还有一个实际协作缺口：

- 当 Phase 25 返回 `no_provider_action_required`、`provider_review_required`、`provider_blocked` 时，后续动作虽然大方向明确，但还没有一份固定的 follow-up 决策矩阵。

如果不补这份矩阵，真实 trial 回来之后仍然容易重新进入临时讨论：

- 这算不算 reopen provider
- review 要不要立刻开 change
- blocked 算不算 provider-owned
- 哪些情况仍然应该继续 hold

## What Changes

- 新增一份 Phase 25 follow-up decision matrix 文档。
- 把 Phase 25 的三个结果状态映射到明确的后续动作。
- 更新路线图与进度台账，使阶段3不再只是“有能力”，而是“有明确决策入口”。

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: 记录 Phase 25 follow-up decision matrix 作为阶段3的默认决策入口

## Impact

- Affected docs:
  - `docs/integration/myprivateagent-live-trial-outcome-feedback/phase25-followup-decision-matrix.md`
  - `docs/roadmap/enterprise_rag_maturity_next_stages.md`
  - `docs/progress/provider-improvement-tracker.md`
- No runtime code changes
- No API changes
