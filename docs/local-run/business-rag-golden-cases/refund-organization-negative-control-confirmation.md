# Refund Organization Negative Control Confirmation

- Report: `refund-organization-negative-control-confirmation-v1`
- Decision: `review`
- Reason: `real_business_corpus_baseline_needs_review`
- Generated At: `2026-06-09T03:27:46.757482+00:00`
- Case File: `docs\local-run\business-rag-golden-cases\refund-organization-negative-control-confirmation.fixture.json`
- Source ID: `refund_policy_docs`

## Summary

| Metric | Value |
|---|---|
| `variant_count` | `8` |
| `expected_empty_variant_count` | `5` |
| `answerable_variant_count` | `3` |
| `expected_empty_review_count` | `2` |
| `answerable_pass_count` | `3` |
| `answerable_review_count` | `0` |
| `likely_failure_class` | `confirmed_negative_control_variant` |
| `recommended_next_gate` | `open_refund_negative_control_hardening_scope_review` |
| `source_decision` | `review` |
| `source_review_case_ids` | `["refund-organization-department-negative", "refund-organization-role-list-negative"]` |

## Review Patterns

| Pattern | Count |
|---|---|
| `answerable_case_passed` | `3` |
| `expected_answerable_evidence_missing` | `0` |
| `negative_control_passed` | `3` |
| `negative_control_returned_evidence` | `2` |
| `review_observation:negative_control_leakage` | `1` |

## Case Outcomes

| Case | Type | Expected | Status | Reason | Returned Citations |
|---|---|---|---|---|---|
| `refund-organization-department-negative` | `organization_negative_control` | `insufficient_evidence` | `review` | `negative_control_returned_evidence` | `refund_policy_2026#exact-refund-code` |
| `refund-organization-department-involved-negative` | `organization_negative_control` | `insufficient_evidence` | `ready` | `negative_control_passed` | `` |
| `refund-organization-owner-negative` | `organization_negative_control` | `insufficient_evidence` | `ready` | `negative_control_passed` | `` |
| `refund-organization-role-list-negative` | `organization_negative_control` | `insufficient_evidence` | `review` | `negative_control_returned_evidence` | `refund_policy_2026#exact-refund-code` |
| `refund-organization-staff-list-negative` | `organization_negative_control` | `insufficient_evidence` | `ready` | `negative_control_passed` | `` |
| `refund-role-high-value-review` | `role_lookup` | `answerable` | `ready` | `answerable_case_passed` | `refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#appeal-review` |
| `refund-role-appeal-review-owner` | `role_lookup` | `answerable` | `ready` | `answerable_case_passed` | `refund_policy_2026#appeal-review, refund_policy_2026#section-3, refund_policy_2026#section-5` |
| `refund-role-high-value-approval-review` | `role_lookup` | `answerable` | `ready` | `answerable_case_passed` | `refund_policy_2026#high-value-review` |

## Recommended Actions

- confirm_negative_control_scope_before_additional_retrieval_changes
- keep_query_rewrite_rerank_hybrid_and_graphrag_unpromoted

## Non-Goals

- does_not_change_public_http_apis
- does_not_create_source_to_agent_binding
- does_not_call_myprivateagent
- does_not_start_or_adopt_parser_engines
- does_not_promote_qdrant_pgvector_bge_m3_hybrid_or_rerankers
- does_not_enable_query_rewrite_hyde_hype_raptor_or_self_rag
- does_not_execute_graphrag
- does_not_change_runtime_retrieval_defaults
