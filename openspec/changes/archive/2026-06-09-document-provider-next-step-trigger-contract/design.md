## Context

到当前阶段为止，provider 侧已经形成了比较完整的轻量闭环：

- local business golden cases
- failed-question / confirmation evidence
- source evaluation pack catalog
- source onboarding scaffold
- 多个真实 source onboarding validation
- source onboarding catalog
- onboarding summary bridge
- template example promotion to a real minimal baseline

这意味着 provider 的通用 onboarding / evidence / discovery 主链已经足够完整。如果继续在缺少新证据的情况下增加 provider 工作，最容易陷入局部无限优化，偏离“轻量 provider、evidence-first、caller/control-plane 边界清晰”的总设计目标。

## Goals / Non-Goals

**Goals:**

- 明确当前 provider 默认进入“暂停扩张、等待触发条件”的姿态。
- 定义哪些新证据可以重新打开 provider 开发。
- 明确哪些问题属于 caller/control-plane，不应回流到本项目。
- 用轻量决策记录方式降低未来反复讨论的成本。

**Non-Goals:**

- 不新增 runtime 行为。
- 不新增新的 source、catalog 或 evaluation pack。
- 不引入 query rewrite、rerank、hybrid retrieval、GraphRAG。
- 不处理 caller 侧 orchestration、policy、final answer、权限审计等职责。

## Decisions

### 1. 用“触发条件合同”而不是继续做功能切片

当前最需要的不是再补一个功能点，而是防止无证据扩张。

原因：

- provider 基线能力已足够完整
- 后续是否继续开发应由新证据驱动
- 这更符合 `RAG_Techniques` 的 failure-mode-driven 原则

### 2. 允许继续开发的触发条件只保留少数几类

建议仅接受以下触发类型：

- `real_caller_feedback_trigger`
- `repeated_cross_source_failure_class_trigger`
- `provider_owned_gap_trigger`
- `runtime_strategy_evaluation_trigger`

原因：

- 能避免“因为还能做就继续做”
- 能把后续 change 选择从兴趣驱动改成证据驱动

### 3. caller/control-plane 问题明确不回流 provider

例如：

- 最终回答策略
- 权限与审批
- source-to-agent binding policy
- 平台治理与审计

原因：

- 这些不属于本项目的轻量 provider 边界
- 回流后会把 provider 逐步推成重型平台

## Risks / Trade-offs

- [看起来像“只写文档不做事”] -> 这条切片的价值在于冻结边界，减少后续无证据开发，是项目纪律的一部分。
- [触发条件可能被写得过泛] -> 明确要求“真实 caller 反馈”或“跨 source 重复失败类”等更强信号。
- [未来仍有人想继续补 provider 小功能] -> 用该合同作为评审前置条件，要求每个新 change 显式声明触发器。
