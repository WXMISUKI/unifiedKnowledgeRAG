## Context

当前仓库已经不缺“能不能做更多 provider 功能”，而是缺“下一阶段怎么按顺序推进”。

结合项目定位：

- 本仓库是轻量 RAG provider
- 当前 provider baseline 已闭环
- 后续 reopen 必须由真实 trial 触发

因此最合理的下一步不是 provider 深挖，而是把 caller-side 实际推进顺序固化下来。

## Goals / Non-Goals

**Goals**

- 形成一份顺序化的 caller trial feedback runbook。
- 解释 Phase 15、Phase 16、trial outcome input contract、Phase 25 之间的关系。
- 给出“阶段拆分图”，明确当前、下一步、以及后续触发式阶段。

**Non-Goals**

- 不新增 provider runtime 能力。
- 不新增调用方自动化编排。
- 不做跨仓库执行。
- 不重开 query rewrite、rerank、hybrid、GraphRAG 等工作。

## Decisions

- 将后续阶段拆成三段：
  1. caller-side real trial access and output
  2. provider-side trial outcome feedback consumption
  3. trigger-based reopen or continued hold-state

- runbook 只写顺序与入口，不写调用方业务实现细节。

- 继续保持 boundary：
  - caller 执行 trial
  - provider 只消费结果并分类 follow-up posture

## Risks / Trade-offs

- 如果 runbook 写太泛，团队仍会各自理解 -> 用现有 Phase 15 / 16 / Phase 25 文档和 contract 作为固定锚点。
- 如果 runbook 写成平台流程，会越界 -> 保持文档只讨论 provider 视角下的接入与反馈闭环。
