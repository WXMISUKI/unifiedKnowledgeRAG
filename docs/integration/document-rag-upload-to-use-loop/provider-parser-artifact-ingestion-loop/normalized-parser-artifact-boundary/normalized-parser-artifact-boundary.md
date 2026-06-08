# Normalized Parser Artifact Boundary

- Report: `normalized-parser-artifact-ingestion-boundary-v1`
- Decision: `go`
- Reason: `parser_artifact_ready_for_local_onboarding`
- Generated At: `2026-06-08T01:32:38.260829+00:00`
- Artifact Path: `D:\AI\AIcode\MyPrivateAgent\docs\integration\document-rag-upload-to-use-loop\parser-artifacts\document-rag-parser-artifact.json`
- Artifact ID: `company_profile_2025_trial_ocr_document_upload`
- Source ID: `company_profile_2025_trial`
- Parser ID: `myprivateagent-ocr-artifact-handoff-v1`
- Materialized Markdown: `docs\integration\document-rag-upload-to-use-loop\provider-parser-artifact-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source.md`
- Source Overlay: `docs\integration\document-rag-upload-to-use-loop\provider-parser-artifact-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source-overlay.json`

## Summary

| Metric | Value |
|---|---|
| `final_decision` | `go` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `source_binding_status` | `not_created` |
| `raw_parser_execution_status` | `not_executed` |
| `ocr_service_status` | `not_started` |
| `ingestion_job_status` | `not_created` |
| `vector_database_status` | `not_called` |
| `graph_execution_status` | `not_executed` |
| `text_block_count` | `502` |
| `citation_anchor_count` | `502` |
| `materialized_markdown_status` | `written` |
| `source_overlay_status` | `written` |

## Recommended Actions

- run_local_document_source_onboarding_with_materialized_markdown
- run_local_approved_source_ingestion_loop_after_onboarding

## Non-Goals

- does_not_parse_raw_pdf
- does_not_start_ocr_services
- does_not_call_paddleocr_or_parser_engines
- does_not_create_source_to_agent_binding
- does_not_call_myprivateagent
- does_not_create_ingestion_job
- does_not_promote_retrieval_backend
- does_not_call_vector_databases
- does_not_execute_graphrag
