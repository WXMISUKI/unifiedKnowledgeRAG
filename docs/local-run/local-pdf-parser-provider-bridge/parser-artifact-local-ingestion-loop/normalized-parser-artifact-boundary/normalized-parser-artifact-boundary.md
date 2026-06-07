# Normalized Parser Artifact Boundary

- Report: `normalized-parser-artifact-ingestion-boundary-v1`
- Decision: `go`
- Reason: `parser_artifact_ready_for_local_onboarding`
- Generated At: `2026-06-07T10:42:04.924239+00:00`
- Artifact Path: `docs\local-run\local-pdf-parser-provider-bridge\parser-artifacts\local-pdf-parser-artifact.json`
- Artifact ID: `company_profile_2025_trial_paddleocr_pdf_pages_1_5`
- Source ID: `company_profile_2025_trial`
- Parser ID: `paddleocr-http-ocr-provider-v1`
- Materialized Markdown: `docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source.md`
- Source Overlay: `docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source-overlay.json`

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
| `text_block_count` | `112` |
| `citation_anchor_count` | `112` |
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
