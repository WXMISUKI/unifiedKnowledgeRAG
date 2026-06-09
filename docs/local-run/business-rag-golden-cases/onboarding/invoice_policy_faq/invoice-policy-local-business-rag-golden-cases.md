# Local Business RAG Golden Cases

- Report: `local-business-rag-golden-cases-v1`
- Decision: `go`
- Reason: `local_business_rag_baseline_go`
- Generated At: `2026-06-09T04:41:10.701147+00:00`
- Source ID: `invoice_policy_faq`
- Case File: `docs\local-run\business-rag-golden-cases\onboarding\invoice_policy_faq\baseline-pack.fixture.json`

## Summary

| Metric | Value |
|---|---|
| `case_count` | `3` |
| `answerable_case_count` | `2` |
| `expected_empty_case_count` | `1` |
| `hit_rate` | `1.0` |
| `citation_match_rate` | `1.0` |
| `empty_handling_rate` | `1.0` |
| `invalid_citation_count` | `0` |
| `review_case_ids` | `[]` |
| `blocked_case_ids` | `[]` |
| `chunk_quality_status` | `ready` |
| `chunk_quality_reason` | `chunk_quality_ready` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `source_binding_status` | `not_created` |
| `graph_execution_status` | `not_executed` |
| `final_decision` | `go` |

## Chunk Quality

| Metric | Value |
|---|---|
| `status` | `ready` |
| `reason_code` | `chunk_quality_ready` |
| `provenance_mode` | `non_page` |
| `total_chunk_count` | `3` |
| `tiny_chunk_count` | `0` |
| `tiny_chunk_ratio` | `0.0` |
| `citation_anchor_count` | `3` |
| `citation_coverage_ratio` | `1.0` |
| `page_coverage_count` | `0` |
| `page_ids` | `[]` |
| `noisy_chunk_samples` | `[]` |
| `thresholds` | `{"max_tiny_chunk_ratio": 0.45, "min_chunk_count": 1, "min_citation_coverage_ratio": 0.8, "min_page_coverage_count": 1, "noisy_chunk_char_threshold": 6, "tiny_chunk_char_threshold": 20}` |

## Cases

| Case | Type | Expected | Status | Reason | Returned Citations |
|---|---|---|---|---|---|
| `invoice-issuance-time` | `issuance_time_lookup` | `answerable` | `ready` | `answerable_case_passed` | `invoice_policy_faq_2026#issuance-time, invoice_policy_faq_2026#correction-flow` |
| `invoice-required-fields` | `required_fields_lookup` | `answerable` | `ready` | `answerable_case_passed` | `invoice_policy_faq_2026#required-fields, invoice_policy_faq_2026#correction-flow` |
| `invoice-negative-cross-border-tax` | `negative_control` | `insufficient_evidence` | `ready` | `negative_control_passed` | `` |

## Review Observations

- none

## Recommended Actions

- reuse_golden_cases_before_future_rag_strategy_changes
- continue_testing_more_real_business_documents
- keep_runtime_defaults_until_candidate_evidence_passes

## Non-Goals

- does_not_change_public_http_apis
- does_not_create_source_to_agent_binding
- does_not_call_myprivateagent
- does_not_start_or_adopt_parser_engines
- does_not_promote_qdrant_pgvector_bge_m3_hybrid_or_rerankers
- does_not_enable_query_rewrite_hyde_hype_raptor_or_self_rag
- does_not_execute_graphrag
- does_not_change_runtime_retrieval_defaults
