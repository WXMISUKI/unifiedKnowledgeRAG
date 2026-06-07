# Approved Local Corpus Acceptance Smoke

- Report: `approved-local-corpus-acceptance-smoke-v1`
- Decision: `go`
- Reason: `approved_local_corpus_accepted`
- Generated At: `2026-06-07T08:23:24.617505+00:00`
- Source ID: `company_profile_2025_trial`

## Summary

| Metric | Value |
|---|---|
| `case_count` | `5` |
| `ready_case_count` | `5` |
| `review_case_count` | `0` |
| `blocked_case_count` | `0` |
| `invalid_citation_count` | `0` |
| `source_binding_status` | `not_created` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `graph_execution_status` | `not_executed` |

## Cases

| Case | Expected | Status | Retrieve | Answer | Citations | Invalid |
|---|---|---|---|---|---|---|
| `business_scope` | `answerable` | `ready` | `3` | `answered` | `3` | `0` |
| `qualifications` | `answerable` | `ready` | `3` | `answered` | `3` | `0` |
| `organization` | `answerable` | `ready` | `3` | `answered` | `3` | `0` |
| `project_scale` | `answerable` | `ready` | `3` | `answered` | `3` | `0` |
| `negative_refund_policy` | `insufficient_evidence` | `ready` | `0` | `insufficient_evidence` | `0` | `0` |

## Recommended Actions

- use_registered_local_corpus_for_myprivateagent_trial
- keep_source_to_agent_binding_in_caller_control_plane

## Non-Goals

- does_not_register_sources
- does_not_create_source_to_agent_binding
- does_not_create_formal_ingestion_job
- does_not_start_ocr_services
- does_not_promote_retrieval_backend
- does_not_run_myprivateagent_orchestration
- does_not_call_vector_databases
- does_not_execute_graphrag
