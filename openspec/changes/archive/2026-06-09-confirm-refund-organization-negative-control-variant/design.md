## Context

项目当前已经具备两个互补的 baseline：

- breadth baseline: `real-business-corpus-golden-cases.json`，当前 `go`
- failure baseline: `real-failed-question-pack.json`，当前保留一个 refund 组织类 question trap

但 failed-question-pack 的作用主要是“暴露候选问题”，并不负责把某一类 failure 细化确认为稳定 pattern。结合 `RAG_Techniques` 的经验，这一步更适合建立一个小而专注的 confirmation baseline，而不是直接切入 query rewrite 或更重的 retrieval strategy。

现有 `local_business_rag_golden_cases.py` 已经提供：

- source-by-source conservative evaluation
- go/review/blocked 一致语义
- failure mode / question origin / review observation 汇总

因此本次实现不需要新建评估引擎，只需要在现有 aggregate report 之上增加一个 refund 专项确认报告。

## Goals / Non-Goals

**Goals:**

- 用最小样本确认 refund 组织/部门/员工名单类问法是否已经形成稳定 failure class。
- 让报告能区分“负控泄漏”与“正向问法 wording mismatch”。
- 给下一条切片提供一个明确 gate，而不是直接推动高级策略实现。
- 保持 provider 轻量、evidence-first、可回退。

**Non-Goals:**

- 不引入 query rewrite、HyDE、HyPE。
- 不引入 rerank、fusion/hybrid retrieval。
- 不修改 chunking default 或 runtime retrieval defaults。
- 不引入 GraphRAG、RAPTOR、Self-RAG、CRAG。
- 不修改公共 HTTP API。
- 不新增 source binding、caller policy 或 control-plane 责任。

## Decisions

### 1. 复用现有 aggregate evaluation，引入独立 confirmation report

confirmation baseline 仍然调用 `run_real_business_corpus_golden_cases(...)`，只是在结果上再做一层 refund 专项归纳。

原因：

- 保持与现有 baseline 相同的 `go/review/blocked` 语义
- 避免新建另一套判定逻辑
- 后续如果还有别的 source-specific confirmation baseline，也可以复用这条路径

### 2. 在同一 source 里同时放入 fail-closed 变体和 answerable 变体

这个 confirmation baseline 不只看“组织类负控是否泄漏”，还要看“相邻语义域里的角色/职责类问法是否仍可 answer”。

原因：

- 如果只有组织类问法，就无法区分它是 leakage 还是 wording mismatch
- 把负控与正控都放入一组小样本里，才能得到保守但可行动的 verdict

### 3. verdict 只输出下一条 evidence gate，不直接触发策略实现

confirmation report 会输出：

- `likely_failure_class`
- `recommended_next_gate`

但不会自动触发 query rewrite、retriever hardening 或 runtime promotion。

原因：

- 当前项目边界是 lightweight provider
- 这一步的目标是提高“下一条切片怎么选”的决策质量，而不是顺手推进策略实现

## Verdict Rules

### `confirmed_negative_control_variant`

满足：

- 组织类 expected-empty 变体中存在 `review`
- answerable 角色/职责变体保持通过

含义：

- 当前更像负控泄漏问题
- 下一步应考虑 negative-control hardening 范围确认，而不是 query rewrite

### `confirmed_query_mismatch_variant`

满足：

- 组织类 expected-empty 变体保持 fail-closed
- answerable 角色/职责变体出现 evidence miss / answerable review

含义：

- 当前更像 wording mismatch / query mismatch
- 下一步应先继续沉淀 wording-gap 证据，再决定是否值得进入 query rewrite candidate

### `mixed_signal_needs_more_cases`

满足：

- expected-empty review 与 answerable review 同时存在

含义：

- 负控与正控都不稳定
- 下一步应先补更小样本，不做策略升级

### `not_enough_evidence`

满足：

- 当前样本既没有稳定 review，也没有足够一致的 pattern

含义：

- 暂不打开新的 retrieval strategy slice

## Risks / Trade-offs

- [组织类负控已经被前一轮 hardening 修复，导致这次与 failed-question-pack 结论不同] -> 这是本次 change 想确认的核心事实，允许出现；如果结论变化，说明 failed-question-pack 需要被重新解释而不是继续沿用旧假设。
- [角色类问法本身更像 paraphrase，不一定全部通过] -> 这正是 confirmation baseline 的价值所在；如果它们稳定 miss，就说明下一条切片更接近 query mismatch。
- [报告结论过度依赖极少数样本] -> 通过把 verdict 限定为 next-gate recommendation，而不是直接触发实现，保持保守。
