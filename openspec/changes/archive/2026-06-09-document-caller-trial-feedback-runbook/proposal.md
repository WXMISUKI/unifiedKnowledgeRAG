## Why

当前我们已经完成了：

- provider phase closure
- caller trial outcome input contract
- Phase 15 dispatch package
- Phase 16 minimal access loop
- Phase 25 live trial outcome feedback closure

但“下一阶段具体怎么推进”对团队来说还不够顺手。现在最缺的不是新的 provider 能力，而是一份顺序化、可执行的 caller-side 接入与反馈回写 runbook：

- 第一步看什么
- 第二步用什么 evidence
- 第三步怎么开始 repo-side trial
- 第四步 trial 结果如何按合同输出
- 第五步 provider 如何消费并给出 follow-up posture

如果没有这份 runbook，团队仍可能回到两个低效方向：

- 继续在 provider 内部找功能点
- 每次接入 trial 都重新解释 Phase 15 / 16 / 25 的关系

## What Changes

- 新增一份 caller trial feedback runbook，串起 Phase 15、Phase 16、trial outcome input contract 和 Phase 25。
- 在文档中正式拆出后续阶段顺序，明确当前第一阶段优先目标是“真实 caller 接入与反馈闭环”。
- 更新路线图和进度台账，使“阶段拆分”对后续协作更清晰。

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: 记录 caller trial feedback runbook 作为 post-closure 阶段的首个执行入口

## Impact

- Affected docs:
  - `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-feedback-runbook.md`
  - `docs/roadmap/enterprise_rag_maturity_next_stages.md`
  - `docs/progress/provider-improvement-tracker.md`
- No runtime code changes
- No API changes
- No retrieval strategy changes
