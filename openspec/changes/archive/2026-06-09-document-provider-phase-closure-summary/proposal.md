## Why

当前 `unifiedKnowledgeRAG` 已经完成一轮相对完整的轻量 provider 通用化收口：

- real business golden-case baseline
- failed-question / confirmation evidence
- source evaluation pack catalog
- source onboarding scaffold
- 多个真实 source 的 onboarding validation
- source onboarding catalog
- onboarding summary bridge
- template onboarding 示例提升为真实 baseline
- provider next-step trigger contract

这意味着当前最需要的不是继续补一个 provider 小功能，而是把“这一阶段已经完成什么、当前为什么暂停、未来什么情况下才重新打开 provider 开发、哪些问题不属于 provider”的结论沉淀成正式的阶段收口文档。

否则后续最容易重新滑回局部无限优化：继续微调 onboarding、catalog、strategy 候选项，却没有新的真实触发器。

## What Changes

- 新增一条 provider 阶段收口总结切片，形成正式的 closure summary 文档。
- 在路线图和经验应用文档中，将“下一步”从继续找 provider 切片调整为“保持当前基线，等待触发器”。
- 更新 `provider-roadmap` 规格，明确当前阶段收口总结应作为未来 reopen provider 工作的参考入口。
- 更新进度台账，使“已完成 / 待处理 / 下一步”与当前暂停扩张姿态一致。

## Capabilities

### New Capabilities
- `provider-phase-closure-summary`: 以文档方式冻结当前 provider 阶段收口状态、冻结边界、重启触发器和推荐下一步方向

### Modified Capabilities
- `provider-roadmap`: 增加阶段收口总结的要求，要求未来 reopen provider 工作以前先参考收口总结而不是继续局部扩张

## Impact

- Affected docs:
  - `docs/progress/provider-phase-closure-summary.md`
  - `docs/roadmap/enterprise_rag_maturity_next_stages.md`
  - `docs/roadmap/rag_techniques_experience_application.md`
  - `docs/progress/provider-improvement-tracker.md`
- Affected specs:
  - `openspec/specs/provider-roadmap/spec.md`
- Affected change artifacts:
  - `openspec/changes/document-provider-phase-closure-summary/*`
