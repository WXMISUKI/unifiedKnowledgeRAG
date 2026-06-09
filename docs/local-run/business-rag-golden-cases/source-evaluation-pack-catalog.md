# Source Evaluation Pack Catalog

- Report: `source-evaluation-pack-catalog-v1`
- Decision: `review`
- Reason: `source_evaluation_pack_catalog_needs_review`
- Generated At: `2026-06-09T07:20:33.781066+00:00`

## Summary

| Metric | Value |
|---|---|
| `pack_count` | `4` |
| `available_pack_count` | `4` |
| `missing_pack_count` | `0` |
| `baseline_pack_count` | `2` |
| `failed_question_pack_count` | `1` |
| `confirmation_pack_count` | `1` |
| `review_pack_ids` | `["real-failed-question-pack-baseline-v1", "refund-organization-negative-control-confirmation-v1"]` |
| `missing_pack_ids` | `[]` |
| `onboarding_catalog_present` | `True` |
| `onboarding_source_count` | `3` |
| `onboarding_ready_source_count` | `3` |
| `onboarding_template_only_source_count` | `0` |
| `onboarding_review_source_count` | `0` |
| `onboarding_ready_source_ids` | `["invoice_policy_faq", "source_template_example", "split_refund_policy_docs"]` |

## Onboarding Summary

| Metric | Value |
|---|---|
| `onboarding_catalog_present` | `True` |
| `onboarding_source_count` | `3` |
| `onboarding_ready_source_count` | `3` |
| `onboarding_template_only_source_count` | `0` |
| `onboarding_review_source_count` | `0` |
| `onboarding_ready_source_ids` | `["invoice_policy_faq", "source_template_example", "split_refund_policy_docs"]` |

## Packs

| Pack ID | Type | Scope | Decision | Cases | Next Gate | Available |
|---|---|---|---|---:|---|---|
| `local-business-rag-golden-cases-v1` | `baseline_pack` | `single_source` | `go` | `6` | `expand_real_sources_or_failed_packs` | `True` |
| `real-business-corpus-golden-cases-v1` | `baseline_pack` | `multi_source` | `go` | `12` | `expand_real_sources_or_failed_packs` | `True` |
| `real-failed-question-pack-baseline-v1` | `failed_question_pack` | `multi_source` | `review` | `6` | `confirm_failure_class_before_strategy_changes` | `True` |
| `refund-organization-negative-control-confirmation-v1` | `confirmation_pack` | `single_source_confirmation` | `review` | `8` | `open_refund_negative_control_hardening_scope_review` | `True` |

## Recommended Actions

- confirm_failure_class_before_strategy_changes
- review_confirmed_failure_class_scope_before_strategy_changes

## Non-Goals

- does_not_rerun_underlying_retrieval_evaluations
- does_not_change_runtime_retrieval_defaults
- does_not_enable_query_rewrite_rerank_or_hybrid
- does_not_create_source_to_agent_binding
- does_not_execute_graphrag
