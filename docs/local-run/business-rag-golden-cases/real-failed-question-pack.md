# Real Failed Question Pack Baseline

- Report: `real-failed-question-pack-baseline-v1`
- Decision: `review`
- Reason: `real_business_corpus_baseline_needs_review`
- Generated At: `2026-06-09T03:05:50.634264+00:00`
- Case File: `docs\local-run\business-rag-golden-cases\real-failed-question-pack.fixture.json`

## Summary

| Metric | Value |
|---|---|
| `source_count` | `3` |
| `case_count` | `6` |
| `answerable_case_count` | `3` |
| `expected_empty_case_count` | `3` |
| `hit_rate` | `1.0` |
| `citation_match_rate` | `1.0` |
| `empty_handling_rate` | `0.6667` |
| `invalid_citation_count` | `0` |
| `review_sources` | `["refund_policy_docs"]` |
| `blocked_sources` | `[]` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `source_binding_status` | `not_created` |
| `graph_execution_status` | `not_executed` |
| `final_decision` | `review` |

## Failure Modes

| Failure Mode | Count |
|---|---|
| `citation_or_evidence` | `2` |
| `query_mismatch` | `2` |
| `unclassified` | `2` |

## Question Origins

| Origin | Count |
|---|---|
| `accepted_real_failure_candidate` | `2` |
| `real_boundary_question` | `2` |
| `real_cross_domain_trap` | `2` |

## Review Observations

| Observation | Count |
|---|---|
| `negative_control_leakage` | `1` |

## Source Reports

| Source | Decision | Cases | Hit Rate | Citation Match | Empty Handling | Chunk Quality |
|---|---|---:|---:|---:|---:|---|
| `company_profile_2025_trial` | `go` | `2` | `1.0` | `1.0` | `1.0` | `ready` |
| `logistics_faq` | `go` | `2` | `1.0` | `1.0` | `1.0` | `ready` |
| `refund_policy_docs` | `review` | `2` | `1.0` | `1.0` | `0.0` | `ready` |

## Recommended Actions

- confirm_failed_question_pack_review_cases_before_strategy_changes
- classify_accepted_failure_candidates_and_cross_domain_traps
- review_negative_control_hardening_scope_before_strategy_changes
- confirm_query_mismatch_failure_before_query_rewrite_candidate

## Non-Goals

- does_not_change_public_http_apis
- does_not_create_source_to_agent_binding
- does_not_call_myprivateagent
- does_not_start_or_adopt_parser_engines
- does_not_promote_qdrant_pgvector_bge_m3_hybrid_or_rerankers
- does_not_enable_query_rewrite_hyde_hype_raptor_or_self_rag
- does_not_execute_graphrag
- does_not_change_runtime_retrieval_defaults
