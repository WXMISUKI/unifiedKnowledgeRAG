# Approved Local Source Registration

- Report: `approved-local-corpus-source-registration-v1`
- Status: `registered`
- Reason: `approved_local_source_registered`
- Generated At: `2026-06-08T01:32:38.291277+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025-10-27`
- Registration Status: `registered`
- Handoff Path: `D:\AI\AIcode\unifiedKnowledgeRAG\docs\integration\document-rag-upload-to-use-loop\provider-parser-artifact-ingestion-loop\approved-source-ingestion-loop\document-source-onboarding\corpus-caller-handoff\local-corpus-caller-handoff.json`
- Registry Path: `app\data\local_sources\approved_sources.json`
- Materialized Source Path: `app\data\sources\company_profile_2025_trial.md`

## Summary

| Metric | Value |
|---|---|
| `source_id` | `company_profile_2025_trial` |
| `registry_status` | `written` |
| `materialized_source_status` | `written` |
| `content_sha256` | `2c08d5f9164bf0b0ccc15873567f6fb34592b06ba811123f4a4f32695e01a347` |
| `default_source_catalog_status` | `extended_with_approved_local_source` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `source_binding_status` | `not_created` |
| `graph_execution_status` | `not_executed` |

## Recommended Actions

- verify_registered_source_with_rag_sources
- run_retrieve_and_answer_smoke_for_registered_source
- keep_source_to_agent_binding_in_caller_control_plane

## Non-Goals

- does_not_create_source_to_agent_binding
- does_not_create_formal_ingestion_job
- does_not_promote_retrieval_backend
- does_not_start_ocr_services
- does_not_run_myprivateagent_orchestration
- does_not_call_vector_databases
- does_not_execute_graphrag
