## Why

当前 provider 侧已经完成了 trial dispatch、minimal access loop、live trial outcome feedback closure，说明下一阶段最有价值的工作不再是继续扩 provider 功能，而是让真实 caller 能稳定地把试运行结果回写给 provider。

虽然 Phase 25 已经支持读取一个显式 `trial_outcome_path`，但当前仓库仍缺少一个清晰、正式、可复用的“caller trial outcome 输入合同”：

- 调用方应该产出什么字段
- 哪些字段是 provider 判定所必需的
- 哪些字段只是可选增强信息
- provider 如何对缺失字段、未知状态和弱输入进行 fail-closed 处理

如果这个输入合同不明确，后续最容易出现两类问题：

- 调用方每次都临时约定 trial outcome 结构，导致 provider 反馈不稳定
- 我们继续在 provider 内部做局部优化，却没有形成稳定的真实反馈入口

## What Changes

- 新增一条 caller trial outcome 输入合同，明确 provider 期望消费的最小 JSON 结构。
- 为该合同补充示例输入文档与样例文件，便于外部调用方接入。
- 收紧并文档化 Phase 25 对 trial outcome 的最小字段要求与 fail-closed 行为。
- 更新路线图与进度台账，将该合同标记为“真实 caller 反馈闭环”的当前优先切片。

## Capabilities

### New Capabilities
- `caller-trial-outcome-input-contract`: 明确外部 caller 向 provider 回写 live trial 结果时的最小输入 schema、边界说明和 fail-closed 规则

### Modified Capabilities
- `myprivateagent-live-trial-outcome-feedback`: 从“能读取 trial outcome 文件”提升为“有明确输入合同、样例和最小校验入口的稳定反馈闭环”
- `provider-roadmap`: 将下一阶段优先级明确为真实 caller 反馈闭环，而不是继续 provider 内部功能扩张

## Impact

- Affected docs:
  - `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-outcome-input-contract.md`
  - `docs/integration/myprivateagent-live-trial-outcome-feedback/caller-trial-outcome-input-example.json`
  - `docs/roadmap/enterprise_rag_maturity_next_stages.md`
  - `docs/progress/provider-improvement-tracker.md`
- Affected code:
  - `app/services/phase25_myprivateagent_live_trial_outcome_feedback.py`
- Affected tests:
  - `tests/test_phase25_myprivateagent_live_trial_outcome_feedback.py`
- Affected specs:
  - `openspec/specs/provider-roadmap/spec.md`
  - `openspec/specs/myprivateagent-live-trial-outcome-feedback/spec.md`
