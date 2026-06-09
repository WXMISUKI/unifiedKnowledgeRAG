## Context

当前仓库已经有：

- 统一的 source evaluation pack catalog
- source onboarding 模板生成能力
- 多个真实 source 的最小 onboarding 验证样本

但这些结果分散在 `docs/local-run/business-rag-golden-cases/onboarding/<source_id>/` 下，调用者或维护者如果想快速判断“某个 source 当前处于模板态、已填 baseline、还是已完成最小验证”，仍需要逐目录查看。对于一个强调轻量、通用、evidence-first 的 provider 来说，这会提高后续 source onboarding 的摩擦。

因此本次设计补的是一层非常轻的 discovery bridge：只扫描既有 onboarding 产物，生成统一视图，不回写运行时状态，不替代主 evaluation pack catalog，不引入自动注册/自动决策。

## Goals / Non-Goals

**Goals:**

- 为 onboarding 目录生成统一 discovery/catalog 视图。
- 让每个 source 的模板、baseline fixture、validation report 和当前状态可被统一查看。
- 给出轻量 recommended next step，帮助后续继续按“模板 -> baseline -> validation”节奏推进。
- 保持 provider 通用能力增强，而不是具体业务专项扩展。

**Non-Goals:**

- 不自动注册 source 到主 provider catalog。
- 不自动把 source 并入 aggregate baseline。
- 不重新运行 retrieval evaluation。
- 不修改现有 source evaluation pack catalog 语义。
- 不引入 query rewrite、rerank、hybrid retrieval、GraphRAG。

## Decisions

### 1. 扫描现有 onboarding 目录，而不是新增状态登记表

直接以 `docs/local-run/business-rag-golden-cases/onboarding/*` 为事实来源。

原因：

- 当前产物已经稳定存在
- 避免再引入一份手工同步台账
- 继续保持 evidence-first，而不是额外平台状态层

### 2. 状态机保持很轻，只做 evidence discovery

每个 source 只判断为类似：

- `template_only`
- `baseline_ready`
- `review`
- `missing`

并附带 `validation_decision` 与 `recommended_next_step`。

原因：

- 当前目标是帮助发现和复用
- 不是构建复杂 onboarding workflow engine

### 3. 与主 source evaluation pack catalog 并行，而不是直接并入

新桥接产物只描述 onboarding source 级别证据，不修改现有 baseline/failed-pack/confirmation pack catalog。

原因：

- 两者关注点不同
- 避免把 onboarding source 的中间态误当成统一评估 pack 的稳定输入

## Risks / Trade-offs

- [onboarding 目录结构将来变化] -> 通过集中 service 封装扫描规则，后续只需改一处。
- [状态过于轻量，不能表达所有细节] -> 这是刻意边界；详细证据仍回到各 source 自身产物查看。
- [与 pack catalog 概念接近，可能让人混淆] -> 在字段和文档里明确这是 source onboarding discovery，不是主 pack catalog。
