# Parser-Derived Corpus Retrieval Quality Baseline

- Report: `parser-derived-corpus-retrieval-quality-baseline-v1`
- Decision: `go`
- Reason: `parser_derived_corpus_quality_baseline_go`
- Generated At: `2026-06-07T13:45:23.003039+00:00`
- Source ID: `company_profile_2025_trial`
- Case File: `docs\local-run\parser-derived-corpus-retrieval-quality-baseline\company-profile-quality-cases.json`

## Summary

| Metric | Value |
|---|---|
| `case_count` | `5` |
| `answerable_case_count` | `3` |
| `expected_empty_case_count` | `2` |
| `hit_rate` | `1.0` |
| `citation_match_rate` | `1.0` |
| `empty_handling_rate` | `1.0` |
| `invalid_citation_count` | `0` |
| `review_case_ids` | `[]` |
| `blocked_case_ids` | `[]` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `source_binding_status` | `not_created` |
| `graph_execution_status` | `not_executed` |
| `final_decision` | `go` |

## Cases

| Case | Expected | Status | Reason | Returned Citations |
|---|---|---|---|---|
| `business_scope` | `answerable` | `ready` | `answerable_case_passed` | `company_profile_2025_trial#chunk-123, company_profile_2025_trial#chunk-201, company_profile_2025_trial#chunk-1` |
| `service_scope` | `answerable` | `ready` | `answerable_case_passed` | `company_profile_2025_trial#chunk-147, company_profile_2025_trial#chunk-151, company_profile_2025_trial#chunk-1` |
| `profile_summary` | `answerable` | `ready` | `answerable_case_passed` | `company_profile_2025_trial#chunk-1, company_profile_2025_trial#chunk-45, company_profile_2025_trial#chunk-105` |
| `negative_contract_amount` | `insufficient_evidence` | `ready` | `negative_control_passed` | `` |
| `negative_staff_roster` | `insufficient_evidence` | `ready` | `negative_control_passed` | `` |

## Recommended Actions

- use_quality_baseline_as_stage4_candidate_backend_input
- keep_runtime_defaults_until_candidate_backend_review_passes

## Non-Goals

- does_not_parse_raw_pdf
- does_not_start_ocr_services
- does_not_create_ingestion_jobs
- does_not_call_myprivateagent
- does_not_create_source_to_agent_binding
- does_not_mutate_chat_runtime
- does_not_promote_qdrant_pgvector_bge_m3_hybrid_or_rerankers
- does_not_execute_graphrag
