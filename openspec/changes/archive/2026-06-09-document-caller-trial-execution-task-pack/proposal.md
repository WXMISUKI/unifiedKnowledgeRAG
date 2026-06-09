## Why

当前我们已经有：

- provider closure summary
- caller trial feedback runbook
- caller trial outcome input contract

但如果现在直接切到调用方仓库，仍然有一个实际协作问题：阶段2虽然方向明确，但还缺少一个更面向执行的任务包，告诉调用方应该准备什么、验证什么、产出什么、以及回传什么。

换句话说：

- runbook 解决了“顺序”
- input contract 解决了“格式”
- 现在还需要一份 task pack 解决“怎么真正执行”

这一步可以进一步减少后续协作中的解释成本，并避免重新回到 provider 内部继续找功能点。

## What Changes

- 新增一份 caller trial execution task pack 文档。
- 把阶段2拆成更具体的执行任务：前置检查、trial 执行、结果记录、outcome 输出、provider 回传。
- 更新路线图和进度台账，使阶段2从“建议方向”变成“可执行任务包”。

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: 记录 caller trial execution task pack 作为阶段2的执行辅助文档

## Impact

- Affected docs:
  - `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-execution-task-pack.md`
  - `docs/roadmap/enterprise_rag_maturity_next_stages.md`
  - `docs/progress/provider-improvement-tracker.md`
- No runtime code changes
- No API changes
