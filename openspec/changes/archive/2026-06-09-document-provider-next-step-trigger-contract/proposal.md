## Why

当前 provider 已经完成了通用 onboarding、evidence、catalog 和最小真实 baseline 示例闭环。如果继续在没有新证据的情况下扩功能，最容易滑向局部无限优化。因此现在最合适的下一步不是继续扩 provider，而是把“何时继续、何时暂停、什么问题不应回流本项目”的触发条件正式固化。

## What Changes

- 新增一条 provider 下一阶段触发条件合同，明确当前应默认暂停 provider 扩张。
- 定义允许重新打开 provider 开发的触发器，例如真实 caller 反馈、跨 source 重复失败类、明确 provider-owned gap、或候选 runtime strategy 评估前置证据。
- 明确哪些问题仍属于 caller/control-plane 职责，不应作为 provider 下一阶段切片来源。
- 用轻量决策记录和路线/台账更新来冻结当前“等待触发条件”的姿态。

## Capabilities

### New Capabilities
- `provider-next-step-trigger-contract`: 固化 provider 继续开发、暂停扩张、以及职责边界的触发条件合同

### Modified Capabilities
- `provider-roadmap`: 增加当前 provider 进入收口期后的触发条件和暂停扩张规则

## Impact

- Affected docs:
  - `docs/roadmap/enterprise_rag_maturity_next_stages.md`
  - `docs/roadmap/rag_techniques_experience_application.md`
  - `docs/progress/provider-improvement-tracker.md`
- Affected specs:
  - `openspec/specs/provider-roadmap/spec.md`
- Affected change artifacts:
  - `openspec/changes/document-provider-next-step-trigger-contract/*`
