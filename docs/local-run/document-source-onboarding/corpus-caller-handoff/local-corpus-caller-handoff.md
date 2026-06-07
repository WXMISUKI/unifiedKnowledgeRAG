# Local Corpus Caller Handoff

- Report: `local-corpus-caller-handoff-v1`
- Status: `ready_for_caller_review`
- Reason: `trial_go_ready_for_caller_review`
- Generated At: `2026-06-07T03:41:01.210410+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025 trial`
- Recommended Query: `公司主营业务是什么？`
- Registration Status: `not_registered`
- Caller Next Action: `review_trial_artifacts_before_formal_binding`

## Artifacts

| Artifact | Path |
|---|---|
| `trial_report` | `D:\AI\AIcode\unifiedKnowledgeRAG\docs\local-run\document-source-onboarding\business-corpus-trial\local-business-corpus-trial.json` |
| `markdown` | `D:\AI\AIcode\unifiedKnowledgeRAG\docs\local-run\pdf-derived-corpus\company_profile_2025_trial.md` |
| `overlay` | `docs\local-run\document-source-onboarding\business-corpus-trial\local-business-corpus-source.json` |
| `chunks` | `docs\local-run\document-source-onboarding\business-corpus-trial\local-business-corpus-chunks.json` |

## Summary

| Metric | Value |
|---|---|
| `status` | `ready_for_caller_review` |
| `trial_decision` | `go` |
| `source_id` | `company_profile_2025_trial` |
| `retrieved_evidence_count` | `3` |
| `answer_citation_count` | `3` |
| `invalid_citation_count` | `0` |
| `default_source_catalog_status` | `unchanged` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `graph_execution_status` | `not_executed` |

## Recommended Actions

- review_trial_artifacts_before_formal_binding
- decide_whether_to_formally_register_local_source
- keep_provider_default_catalog_unchanged_until_approved

## Non-Goals

- does_not_modify_default_source_catalog
- does_not_expose_provider_http_source
- does_not_create_source_binding
- does_not_run_formal_ingestion_job
- does_not_persist_index_lifecycle_state
- does_not_promote_retrieval_backend
- does_not_run_myprivateagent_orchestration
- does_not_execute_graphrag
- does_not_start_ocr_services
