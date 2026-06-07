# Local Enterprise Corpus Ingestion QA Loop

- Report: `local-enterprise-corpus-ingestion-qa-loop-v1`
- Decision: `go`
- Reason: `local_enterprise_corpus_qa_ready`
- Generated At: `2026-06-07T10:08:55.132786+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025 trial`
- Query: `公司主营业务是什么？`
- Input Path: `D:\AI\AIcode\unifiedKnowledgeRAG\docs\local-run\pdf-derived-corpus\company_profile_2025_trial.md`
- Input Format: `markdown`
- Materialized Markdown: `D:\AI\AIcode\unifiedKnowledgeRAG\docs\local-run\pdf-derived-corpus\company_profile_2025_trial.md`

## Downstream

| Field | Value |
|---|---|
| `decision` | `go` |
| `reason_code` | `local_approved_source_ingestion_ready` |
| `source_id` | `company_profile_2025_trial` |
| `title` | `公司简介 2025 trial` |
| `query` | `公司主营业务是什么？` |
| `top_k` | `3` |
| `json_path` | `docs\local-run\local-enterprise-corpus-ingestion-qa-loop\approved-source-ingestion-loop\local-approved-source-ingestion-loop.json` |
| `markdown_path` | `docs\local-run\local-enterprise-corpus-ingestion-qa-loop\approved-source-ingestion-loop\local-approved-source-ingestion-loop.md` |
| `summary` | `{"blocked_step_count": 0, "explicit_ingestion_job_created": true, "final_decision": "go", "graph_execution_status": "not_executed", "ready_step_count": 5, "review_step_count": 0, "runtime_promotion_status": "keep_runtime_defaults", "source_binding_status": "not_created", "step_count": 5}` |

## Summary

| Metric | Value |
|---|---|
| `input_status` | `ready` |
| `input_format` | `markdown` |
| `materialized_markdown_status` | `ready` |
| `downstream_decision` | `go` |
| `downstream_reason_code` | `local_approved_source_ingestion_ready` |
| `final_decision` | `go` |
| `source_binding_status` | `not_created` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `retrieval_backend_promotion_status` | `not_changed` |
| `graph_execution_status` | `not_executed` |

## Recommended Actions

- use_source_for_local_enterprise_rag_questions
- call_provider_rag_answer_with_registered_source_id
- keep_source_binding_decisions_in_myprivateagent_control_plane

## Non-Goals

- does_not_parse_raw_pdf_as_supported_direct_ingestion
- does_not_start_ocr_services
- does_not_start_parser_services
- does_not_call_myprivateagent
- does_not_create_source_to_agent_binding
- does_not_mutate_chat_runtime
- does_not_promote_retrieval_backend
- does_not_add_background_worker
- does_not_execute_graphrag
