## Context

当前真实业务 aggregate baseline 只剩一个 review 信号：`refund_policy_docs` 的 expected-empty case `退款政策里的员工名单有哪些？` 会因为与退款政策文本共享 `退款`、`政策` 这类通用词片而被误召回。现有 fixture retriever 使用非常轻量的 token overlap 评分，既没有 rerank，也没有 query rewrite；这符合项目的轻量 provider 定位，但也意味着我们需要在现有 lexical 规则上补一个最小 hardening，而不是引入新的检索架构。

## Goals / Non-Goals

**Goals:**

- 让 `refund_policy_docs` 的 staff-roster negative control 回到 fail-closed。
- 保持 `refund_policy_docs` 的 exact-term 正例稳定通过。
- 保持 `company_profile_2025_trial` 已有 baseline 结果不退化。
- 继续维持 runtime backend、公共 API、source binding 和 GraphRAG 边界不变。

**Non-Goals:**

- 不切换默认 retrieval backend。
- 不引入 query rewrite、rerank、hybrid retrieval、GraphRAG、chunking default 调整。
- 不把 negative-control hardening 扩展成通用语义分类器或大规模规则库。

## Decisions

### 1. 在 fixture retriever 中增加“弱匹配抑制”门槛

对当前 document retriever 的 lexical overlap 结果增加一个很小的过滤层：

- 正常保留高于最小匹配分数的结果。
- 对低于最小分数的结果，仅在存在精确字母数字 token overlap 时保留。
- 这样可以让 `退款政策里的员工名单有哪些？` 这类只靠通用中文业务词片命中的 query 被过滤掉，同时保留 `RFD-2026-003`、`AF-REFUND-02` 这类 exact-term lookup。

选择它而不是更复杂规则的原因：

- 它直接针对当前唯一真实 failure。
- 它不改变系统边界，也不引入新的策略层。
- 它比“按 query 类型写特判”更通用，也比“全局提高阈值”更能保留 exact-term 场景。

### 2. 成功标准继续以 aggregate baseline 为准

实现完成后，不以单个函数分数变化为成功，而以真实 aggregate baseline 是否从 `review` 回到 `go` 作为主验收。这样可以避免围绕局部分数继续无限调优。

## Risks / Trade-offs

- [真实正例在低分区间被过滤] → 用 focused tests 覆盖 company-profile 正例和 refund exact-term 正例，确保 hardening 不伤主路径。
- [规则过宽，未来又放回弱误召回] → 把规则收敛成“最小分数 + exact-term override”，避免不断堆叠业务特判。
- [规则过窄，只对当前 case 生效] → 验证 real-business aggregate 报告而不是只看单元测试，保证这次 hardening 对真实 baseline 生效。
