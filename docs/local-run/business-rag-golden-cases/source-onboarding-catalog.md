# Source Onboarding Catalog

- Report: `source-onboarding-catalog-v1`
- Decision: `go`
- Reason: `source_onboarding_catalog_ready`
- Generated At: `2026-06-09T06:50:18.457558+00:00`
- Onboarding Root: `docs\local-run\business-rag-golden-cases\onboarding`

## Summary

| Metric | Value |
|---|---|
| `source_count` | `3` |
| `ready_source_count` | `2` |
| `template_only_source_count` | `1` |
| `baseline_ready_source_count` | `0` |
| `review_source_count` | `0` |
| `missing_source_count` | `0` |
| `ready_source_ids` | `["invoice_policy_faq", "split_refund_policy_docs"]` |
| `template_only_source_ids` | `["source_template_example"]` |
| `onboarding_root` | `docs\local-run\business-rag-golden-cases\onboarding` |
| `output_dir` | `docs\local-run\business-rag-golden-cases` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `source_registration_status` | `not_created` |
| `aggregate_baseline_expansion_status` | `not_expanded` |

## Sources

| Source ID | Status | Templates | Baseline Fixture | Validation | Validation Decision | Next Step |
|---|---|---:|---|---|---|---|
| `invoice_policy_faq` | `ready` | `3` | `True` | `True` | `go` | `consider_catalog_bridge_or_add_next_distinct_source` |
| `source_template_example` | `template_only` | `3` | `False` | `False` | `n/a` | `fill_real_baseline_fixture` |
| `split_refund_policy_docs` | `ready` | `3` | `True` | `True` | `go` | `consider_catalog_bridge_or_add_next_distinct_source` |

## Recommended Actions

- fill_real_baseline_fixtures_for_template_only_sources
- consider_evidence_only_bridge_into_source_evaluation_pack_catalog

## Non-Goals

- does_not_register_sources_into_provider_runtime
- does_not_expand_main_aggregate_baseline_automatically
- does_not_rerun_retrieval_or_answer_evaluations
- does_not_change_runtime_retrieval_defaults
- does_not_enable_query_rewrite_rerank_hybrid_or_graphrag
