## Why

`real-failed-question-pack` 当前把 `refund_policy_docs` 的组织类问法标成了一个值得继续追踪的 review 信号，但我们还没有确认它到底属于哪一类稳定 failure：

- `confirmed_negative_control_variant`
- `confirmed_query_mismatch_variant`
- `mixed_signal_needs_more_cases`
- `not_enough_evidence`

在三个真实业务 source 的 aggregate baseline 已经保持 `go` 的前提下，下一步最合理的动作不是直接引入 query rewrite、rerank、hybrid retrieval 或 GraphRAG，而是用一个更小的 refund 专项确认基线，把这个 failure class 先确认清楚，避免围绕单条 case 做局部无限优化。

## What Changes

- 新增一个独立的 refund 组织类负控确认 fixture、导出脚本和 JSON/Markdown 报告。
- 在现有 real-business aggregate 评估引擎之上增加一个 confirmation report，输出：
  - `variant_count`
  - `expected_empty_variant_count`
  - `answerable_variant_count`
  - `expected_empty_review_count`
  - `answerable_pass_count`
  - `likely_failure_class`
  - `review_pattern_summary`
  - `recommended_next_gate`
- 用同一份 refund source 同时覆盖：
  - 应 fail-closed 的组织/部门/员工名单类问法
  - 应 answerable 的角色/复核职责类问法
- 保持 runtime retrieval defaults、公共 HTTP API、source binding、backend promotion 和 GraphRAG execution 不变。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-business-rag-golden-cases`: 扩展 real-business baseline 体系，使其能够导出一个 refund 专项 confirmation baseline，用于确认组织类边界问法的 failure class，而不是直接触发高级 RAG 策略升级。

## Impact

- Affected code: `app/services/local_business_rag_golden_cases.py`
- Affected scripts: `scripts/export_refund_organization_negative_control_confirmation.py`
- Affected tests: `tests/test_refund_organization_negative_control_confirmation.py`
- Affected artifacts:
  - `docs/local-run/business-rag-golden-cases/refund-organization-negative-control-confirmation.fixture.json`
  - `docs/local-run/business-rag-golden-cases/refund-organization-negative-control-confirmation.json`
  - `docs/local-run/business-rag-golden-cases/refund-organization-negative-control-confirmation.md`
