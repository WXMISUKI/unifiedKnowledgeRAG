# Local RAG Business Corpus Usability Check

- Report: `local-rag-business-corpus-usability-check-v1`
- Decision: `go`
- Reason: `local_rag_business_corpus_usable`
- Generated At: `2026-06-07T05:21:39.808882+00:00`
- Source ID: `company_profile_2025_trial`
- Base URL: `http://127.0.0.1:8020`
- Live HTTP Included: `True`

## Summary

| Metric | Value |
|---|---|
| `required_check_count` | `3` |
| `go_check_count` | `3` |
| `review_check_count` | `0` |
| `blocked_check_count` | `0` |
| `skipped_check_count` | `0` |
| `live_http_required` | `True` |
| `default_rag_api_behavior` | `unchanged` |
| `myprivateagent_behavior` | `unchanged` |
| `source_binding_status` | `not_created` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `graph_execution_status` | `not_executed` |

## Checks

| Check | Required | Decision | Reason |
|---|---:|---|---|
| `local_business_corpus_trial` | `True` | `go` | `local_business_corpus_usable` |
| `approved_local_corpus_acceptance` | `True` | `go` | `approved_local_corpus_accepted` |
| `approved_local_corpus_live_http` | `True` | `go` | `approved_local_corpus_live_http_accepted` |

## Recommended Actions

- use_local_business_corpus_for_myprivateagent_trial
- keep_default_rag_behavior_unchanged

## Non-Goals

- does_not_start_server
- does_not_register_sources
- does_not_create_source_to_agent_binding
- does_not_create_formal_ingestion_job
- does_not_start_ocr_services
- does_not_promote_retrieval_backend
- does_not_run_myprivateagent_orchestration
- does_not_call_vector_databases
- does_not_execute_graphrag
- does_not_change_default_rag_api_behavior
