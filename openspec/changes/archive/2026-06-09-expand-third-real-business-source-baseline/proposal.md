## Why

当前 aggregate real-business golden baseline 已经通过 `company_profile_2025_trial` 与 `refund_policy_docs` 两个 source 回到 `go`，这说明下一阶段最有价值的工作不再是局部 hardening，而是继续扩大真实业务样本覆盖面。现在引入第三个真实业务 source，可以让新的 failure mode 在更广的业务问题类型上自然暴露出来，避免在没有证据时提前引入高级 RAG 策略。

## What Changes

- 将 aggregate real-business golden baseline 从两个 source 扩展到三个 source。
- 把 `logistics_faq` 纳入 aggregate fixture，并补充物流流程、精确标识和 expected-empty negative control 的真实业务问题。
- 保持现有 aggregate 报告结构与 conservative source-by-source evaluation，不改变默认检索策略或运行时架构。
- 刷新 aggregate baseline 报告与进度台账，用新的 breadth evidence 作为后续 failure-driven 选择高级技术的前置依据。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-business-rag-golden-cases`: 扩展 aggregate local business baseline，使其可以稳定承载第三个真实业务 source，并在更多业务问题类型下继续输出 conservative evidence-only 结果。

## Impact

- Affected code: `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.fixture.json`
- Affected tests: `tests/test_real_business_corpus_golden_cases.py`
- Affected artifacts: `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.json`, `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.md`, `docs/progress/provider-improvement-tracker.md`
