# Local Business RAG Golden Cases

- Report: `local-business-rag-golden-cases-v1`
- Decision: `go`
- Reason: `local_business_rag_baseline_go`
- Generated At: `2026-06-08T07:40:23.362975+00:00`
- Source ID: `company_profile_2025_trial`
- Case File: `docs\local-run\business-rag-golden-cases\company-profile-golden-cases.json`

## Summary

| Metric | Value |
|---|---|
| `case_count` | `6` |
| `answerable_case_count` | `4` |
| `expected_empty_case_count` | `2` |
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
| `total_chunk_count` | `1005` |
| `tiny_chunk_count` | `412` |
| `tiny_chunk_ratio` | `0.41` |
| `citation_anchor_count` | `1005` |
| `citation_coverage_ratio` | `1.0` |
| `page_coverage_count` | `10` |
| `page_ids` | `["page-1", "page-10", "page-2", "page-3", "page-4", "page-5", "page-6", "page-7", "page-8", "page-9"]` |
| `noisy_chunk_samples` | `[{"char_count": 52, "chunk_id": "chunk-2", "citation": "company_profile_2025_trial#chunk-2", "text_preview": "<!-- citation: company_profile_2025_trial#page-1 -->"}, {"char_count": 14, "chunk_id": "chunk-3", "citation": "company_profile_2025_trial#chunk-3", "text_preview": "江苏交通工程咨询监理有限公司"}, {"char_count": 52, "chunk_id": "chunk-4", "citation": "company_profile_2025_trial#chunk-4", "text_preview": "<!-- citation: company_profile_2025_trial#page-1 -->"}, {"char_count": 6, "chunk_id": "chunk-5", "citation": "company_profile_2025_trial#chunk-5", "text_preview": "JSTECS"}, {"char_count": 52, "chunk_id": "chunk-6", "citation": "company_profile_2025_trial#chunk-6", "text_preview": "<!-- citation: company_profile_2025_trial#page-1 -->"}, {"char_count": 52, "chunk_id": "chunk-8", "citation": "company_profile_2025_trial#chunk-8", "text_preview": "<!-- citation: company_profile_2025_trial#page-1 -->"}, {"char_count": 8, "chunk_id": "chunk-9", "citation": "company_profile_2025_trial#chunk-9", "text_preview": "公路业绩介绍材料"}, {"char_count": 52, "chunk_id": "chunk-10", "citation": "company_profile_2025_trial#chunk-10", "text_preview": "<!-- citation: company_profile_2025_trial#page-1 -->"}]` |
| `thresholds` | `{"max_tiny_chunk_ratio": 0.45, "min_chunk_count": 1, "min_citation_coverage_ratio": 0.8, "min_page_coverage_count": 1, "noisy_chunk_char_threshold": 6, "tiny_chunk_char_threshold": 20}` |

## Cases

| Case | Type | Expected | Status | Reason | Returned Citations |
|---|---|---|---|---|---|
| `business_scope` | `business_scope` | `answerable` | `ready` | `answerable_case_passed` | `company_profile_2025_trial#chunk-127, company_profile_2025_trial#chunk-203, company_profile_2025_trial#chunk-1` |
| `qualifications` | `qualification_lookup` | `answerable` | `ready` | `answerable_case_passed` | `company_profile_2025_trial#chunk-115, company_profile_2025_trial#chunk-1, company_profile_2025_trial#chunk-3` |
| `organization` | `organization_lookup` | `answerable` | `ready` | `answerable_case_passed` | `company_profile_2025_trial#chunk-51, company_profile_2025_trial#chunk-167, company_profile_2025_trial#chunk-663` |
| `project_scale` | `project_scale` | `answerable` | `ready` | `answerable_case_passed` | `company_profile_2025_trial#chunk-145, company_profile_2025_trial#chunk-3, company_profile_2025_trial#chunk-111` |
| `negative_refund_policy` | `negative_control` | `insufficient_evidence` | `ready` | `negative_control_passed` | `` |
| `negative_staff_roster` | `negative_control` | `insufficient_evidence` | `ready` | `negative_control_passed` | `` |

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
