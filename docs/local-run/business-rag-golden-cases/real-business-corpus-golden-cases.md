# Real Business Corpus Golden Cases

- Report: `real-business-corpus-golden-cases-v1`
- Decision: `go`
- Reason: `real_business_corpus_baseline_go`
- Generated At: `2026-06-09T02:26:47.643709+00:00`
- Case File: `docs\local-run\business-rag-golden-cases\real-business-corpus-golden-cases.fixture.json`

## Summary

| Metric | Value |
|---|---|
| `source_count` | `2` |
| `case_count` | `9` |
| `answerable_case_count` | `6` |
| `expected_empty_case_count` | `3` |
| `hit_rate` | `1.0` |
| `citation_match_rate` | `1.0` |
| `empty_handling_rate` | `1.0` |
| `invalid_citation_count` | `0` |
| `review_sources` | `[]` |
| `blocked_sources` | `[]` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `source_binding_status` | `not_created` |
| `graph_execution_status` | `not_executed` |
| `final_decision` | `go` |

## Failure Modes

| Failure Mode | Count |
|---|---|
| `citation_or_evidence` | `3` |
| `unclassified` | `6` |

## Review Observations

| Observation | Count |
|---|---|

## Source Reports

| Source | Decision | Cases | Hit Rate | Citation Match | Empty Handling | Chunk Quality |
|---|---|---:|---:|---:|---:|---|
| `company_profile_2025_trial` | `go` | `6` | `1.0` | `1.0` | `1.0` | `ready` |
| `refund_policy_docs` | `go` | `3` | `1.0` | `1.0` | `1.0` | `ready` |

## Recommended Actions

- add_more_real_business_documents_or_real_failed_questions
- keep_advanced_rag_strategies_unpromoted_until_failures_appear

## Non-Goals

- does_not_change_public_http_apis
- does_not_create_source_to_agent_binding
- does_not_call_myprivateagent
- does_not_start_or_adopt_parser_engines
- does_not_promote_qdrant_pgvector_bge_m3_hybrid_or_rerankers
- does_not_enable_query_rewrite_hyde_hype_raptor_or_self_rag
- does_not_execute_graphrag
- does_not_change_runtime_retrieval_defaults
