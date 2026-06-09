## Context

项目目前已经有较成熟的 source-level evaluation 资产，但它们的入口是分散的：

- `local-business-rag-golden-cases`
- `real-business-corpus-golden-cases`
- `real-failed-question-pack`
- `refund-organization-negative-control-confirmation`

这些报告对开发者有用，但对“通用 provider 当前可用性如何、下一步应该扩 source 还是确认 failure class、什么时候才允许引入高级策略”还缺少一个统一目录视图。

`RAG_Techniques` 的企业级复用经验强调：

- 先把 baseline / golden questions / evaluation gates 体系化
- 再考虑 query rewrite、rerank、fusion/hybrid 等优化候选
- 不要让每次讨论都退回到某一个单独 notebook 或单独业务 case

因此，这一切片的重点不是再造新评估逻辑，而是把现有 pack 统一编目，形成 provider 级通用 gate 入口。

## Goals / Non-Goals

**Goals:**

- 给现有 evaluation artifacts 一个统一 catalog。
- 让 catalog 能表达 pack 类型、覆盖范围、当前 decision 和下一条推荐 gate。
- 为后续新 source 接入和策略候选评审提供稳定入口。
- 保持 provider 轻量、只做 evidence catalog，不触碰 runtime defaults。

**Non-Goals:**

- 不改变 retrieve/answer 行为。
- 不引入 query rewrite、rerank、hybrid retrieval。
- 不引入 GraphRAG。
- 不修改 source binding 策略。
- 不把 caller/control-plane 责任放进 provider。

## Decisions

### 1. 先做 catalog 投影，不强制重写所有现有 pack schema

这一切片优先新增统一 catalog，而不是先把所有已有 JSON schema 大改一遍。

原因：

- 风险更低
- 更容易快速形成通用入口
- 后续如果 catalog 证明稳定，再考虑把公共字段逐步前移到各独立报告 schema

### 2. catalog 只消费已生成 artifact，不重跑底层评估

catalog 直接读取现有 JSON artifact，形成统一摘要。

原因：

- 避免重复执行评估流程
- 保持职责清晰：catalog 是目录层，不是执行层
- 更符合 provider 的轻量边界

### 3. `recommended_next_gate` 保持建议性质

catalog 会输出“下一条建议 gate”，但不会自动触发实现。

原因：

- 我们当前要解决的是治理与可见性
- 不是把 provider 变成自动策略编排器

## Catalog Shape

每个 pack 条目至少应有：

- `pack_id`
- `pack_type`
- `source_scope`
- `artifact_json_path`
- `artifact_markdown_path`
- `decision`
- `reason_code`
- `case_count`
- `recommended_next_gate`

pack 类型当前至少覆盖：

- `baseline_pack`
- `failed_question_pack`
- `confirmation_pack`

## Risks / Trade-offs

- [catalog 与底层 artifact 口径漂移] -> 当前通过显式映射表和已有 JSON 字段抽取控制风险。
- [未生成 artifact 时 catalog 不完整] -> catalog 应显式输出缺失状态，而不是静默忽略。
- [catalog 被误解为自动决策器] -> 文档和 spec 中明确其为 evidence-only 目录层。
