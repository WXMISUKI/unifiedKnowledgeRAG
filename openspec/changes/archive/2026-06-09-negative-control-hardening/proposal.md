## Why

真实业务 aggregate baseline 经过第二 source 扩展、failure-mode 分类和 markdown provenance 对齐后，当前只剩下 `refund_policy_docs` 的 `negative_control_leakage`。现在需要用一个最小、可验证、可回退的切片收口这类误召回，避免在没有更多真实 failure 证据前跳到 query rewrite、rerank、hybrid retrieval 或 GraphRAG。

## What Changes

- 为真实业务 aggregate baseline 增加一个专门面向 negative control 的轻量 hardening 切片。
- 收紧 fixture document retriever 对弱 lexical overlap 的放行条件，降低仅凭通用业务词片产生的误召回。
- 保持 refund-policy 的 exact-term 正例和现有 company-profile 正例通过，不更换检索后端、不引入高级检索策略。
- 刷新 aggregate golden-case 报告与进度台账，确认剩余 review 是否被消除。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-business-rag-golden-cases`: 增加 negative-control hardening 要求，使真实业务 baseline 能抑制弱词片重叠导致的 expected-empty evidence leakage，同时保持已通过的正例稳定。

## Impact

- Affected code: `app/services/document_retriever.py`, `app/services/local_business_rag_golden_cases.py`
- Affected tests: `tests/test_real_business_corpus_golden_cases.py`, `tests/test_local_business_rag_golden_cases.py`, and a new focused retriever test
- Affected artifacts: `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.json`, `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.md`, `docs/progress/provider-improvement-tracker.md`
