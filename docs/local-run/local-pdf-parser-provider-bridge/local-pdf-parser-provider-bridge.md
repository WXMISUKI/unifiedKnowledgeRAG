# Local PDF Parser Provider Bridge

- Report: `local-pdf-parser-provider-bridge-v1`
- Decision: `go`
- Reason: `local_pdf_parser_provider_bridge_ready`
- Generated At: `2026-06-07T10:42:05.352440+00:00`
- PDF Path: `D:\xwechat_files\wxid_pc6sc451nt9022_dea0\msg\file\2026-06\公司简介2025年10月27日(1).pdf`
- Provider: `http://127.0.0.1:8080/ocr`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025 trial`
- Max Pages: `5`
- Artifact Path: `docs\local-run\local-pdf-parser-provider-bridge\parser-artifacts\local-pdf-parser-artifact.json`

## Steps

| Step | Status | Reason | Artifacts |
|---|---|---|---|
| `parser_provider_call` | `go` | `parser_provider_text_ready` | `n/a` |
| `normalized_parser_artifact` | `go` | `normalized_parser_artifact_written` | `artifact=docs\local-run\local-pdf-parser-provider-bridge\parser-artifacts\local-pdf-parser-artifact.json` |
| `parser_artifact_local_ingestion_loop` | `go` | `parser_artifact_local_ingestion_ready` | `json=docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\parser-artifact-local-ingestion-loop.json, markdown=docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\parser-artifact-local-ingestion-loop.md, materialized_markdown=docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source.md` |

## Downstream

| Field | Value |
|---|---|
| `decision` | `go` |
| `reason_code` | `parser_artifact_local_ingestion_ready` |
| `artifact_id` | `company_profile_2025_trial_paddleocr_pdf_pages_1_5` |
| `source_id` | `company_profile_2025_trial` |
| `materialized_markdown_path` | `docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source.md` |
| `source_overlay_path` | `docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source-overlay.json` |
| `json_path` | `docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\parser-artifact-local-ingestion-loop.json` |
| `markdown_path` | `docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\parser-artifact-local-ingestion-loop.md` |
| `summary` | `{"approved_source_ingestion_decision": "go", "artifact_materialized": true, "final_decision": "go", "graph_execution_status": "not_executed", "myprivateagent_call_status": "not_called", "ocr_service_status": "not_started", "raw_parser_execution_status": "not_executed", "runtime_promotion_status": "keep_runtime_defaults", "source_binding_status": "not_created", "step_count": 2, "vector_database_status": "not_promoted"}` |

## Summary

| Metric | Value |
|---|---|
| `final_decision` | `go` |
| `source_binding_status` | `not_created` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `retrieval_backend_promotion_status` | `not_changed` |
| `myprivateagent_call_status` | `not_called` |
| `ocr_service_start_status` | `not_started` |
| `graph_execution_status` | `not_executed` |
| `input_status` | `ready` |
| `provider_status` | `ready` |
| `normalized_artifact_status` | `written` |
| `text_block_count` | `112` |
| `downstream_decision` | `go` |
| `downstream_reason_code` | `parser_artifact_local_ingestion_ready` |

## Recommended Actions

- use_generated_source_id_for_local_rag_questions
- review_pdf_parser_quality_before_productizing_upload_flow
- keep_myprivateagent_as_optional_orchestrator_not_parser_middleman

## Non-Goals

- does_not_start_paddleocr_or_ocr_services
- does_not_call_myprivateagent
- does_not_create_source_to_agent_binding
- does_not_mutate_chat_runtime
- does_not_promote_retrieval_backend
- does_not_add_background_worker
- does_not_execute_graphrag
