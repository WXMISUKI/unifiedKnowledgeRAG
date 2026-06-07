# Local Document Source Onboarding

- Report: `local-document-source-onboarding-loop-v1`
- Decision: `go`
- Reason: `local_document_source_onboarded`
- Generated At: `2026-06-07T08:23:24.619183+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025 trial`
- Markdown Path: `docs\local-run\pdf-derived-corpus\company_profile_2025_trial.md`
- Query: `公司主营业务是什么？`

## Steps

| Step | Status | Reason | Artifacts |
|---|---|---|---|
| `business_corpus_trial` | `go` | `local_business_corpus_usable` | `json=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\business-corpus-trial\local-business-corpus-trial.json, markdown=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\business-corpus-trial\local-business-corpus-trial.md, overlay=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\business-corpus-trial\local-business-corpus-source.json, chunks=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\business-corpus-trial\local-business-corpus-chunks.json` |
| `caller_handoff` | `ready_for_caller_review` | `trial_go_ready_for_caller_review` | `json=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\corpus-caller-handoff\local-corpus-caller-handoff.json, markdown=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\corpus-caller-handoff\local-corpus-caller-handoff.md` |
| `approved_source_registration` | `registered` | `approved_local_source_registered` | `json=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\approved-local-source-registration\approved-local-source-registration.json, markdown=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\approved-local-source-registration\approved-local-source-registration.md, materialized_source=app\data\sources\company_profile_2025_trial.md` |
| `acceptance_smoke` | `go` | `approved_local_corpus_accepted` | `json=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\approved-local-corpus-acceptance\approved-local-corpus-acceptance-smoke.json, markdown=docs\local-run\approved-source-ingestion-loop\document-source-onboarding\approved-local-corpus-acceptance\approved-local-corpus-acceptance-smoke.md` |

## Summary

| Metric | Value |
|---|---|
| `step_count` | `4` |
| `ready_step_count` | `4` |
| `review_step_count` | `0` |
| `blocked_step_count` | `0` |
| `final_decision` | `go` |
| `source_binding_status` | `not_created` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `graph_execution_status` | `not_executed` |

## Recommended Actions

- use_registered_source_for_myprivateagent_explicit_trial
- declare_source_id_in_domain_agent_manifest_when_needed
- keep_source_to_agent_binding_in_caller_control_plane

## Non-Goals

- does_not_parse_raw_pdf_as_supported_ingestion
- does_not_start_ocr_services
- does_not_create_source_to_agent_binding
- does_not_call_myprivateagent
- does_not_create_formal_ingestion_job
- does_not_promote_retrieval_backend
- does_not_call_vector_databases
- does_not_mutate_chat_runtime
- does_not_execute_graphrag
