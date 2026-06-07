# Approved Local Source Registration

- Report: `approved-local-corpus-source-registration-v1`
- Status: `registered`
- Reason: `approved_local_source_registered`
- Generated At: `2026-06-07T01:27:08.613113+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025 trial`
- Registration Status: `registered`
- Handoff Path: `D:\AI\AIcode\unifiedKnowledgeRAG\docs\local-run\corpus-caller-handoff\local-corpus-caller-handoff.json`
- Registry Path: `app\data\local_sources\approved_sources.json`
- Materialized Source Path: `app\data\sources\company_profile_2025_trial.md`

## Summary

| Metric | Value |
|---|---|
| `source_id` | `company_profile_2025_trial` |
| `registry_status` | `written` |
| `materialized_source_status` | `written` |
| `content_sha256` | `dadf096f29bb53c50d38df810c486a5fb61d3d88ce193d869009a301f89f5703` |
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
