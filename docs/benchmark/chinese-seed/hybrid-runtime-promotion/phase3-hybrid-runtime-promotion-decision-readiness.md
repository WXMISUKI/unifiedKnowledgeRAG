# Phase 3 Hybrid Runtime Promotion Decision Readiness

- Report: `phase3-hybrid-runtime-promotion-decision-readiness-v1`
- Status: `review`
- Review State: `review`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-01T13:01:28.462590+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Signals | `15` |
| Required Signals | `14` |
| Ready Signals | `6` |
| Review Signals | `9` |
| Blocked Signals | `0` |
| Open Gate IDs | `["phase3_retrieval_promotion_readiness", "phase3_candidate_runtime_diagnostics", "phase3_candidate_latency_resource_diagnostics", "phase3_hybrid_fusion_threshold_calibration", "phase6_bge_m3_artifact_readiness", "phase6_bge_m3_vs_mock_fixture_diagnostics", "phase6_qdrant_vector_store_readiness", "phase6_qdrant_bge_private_network_promotion_readiness", "deployed_provider_smoke"]` |

## Signals

| Signal | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `phase3_hybrid_runtime_promotion_decision_contract` | `True` | `ready` | contract_present=true | `no_action_required` |
| `phase3_retrieval_promotion_readiness` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase3_candidate_runtime_diagnostics` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase3_candidate_latency_resource_diagnostics` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase3_hybrid_fusion_threshold_calibration` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase3_hybrid_cross_case_fp_fn_smoke` | `True` | `ready` | artifact_present=true; status=ready; decision=n/a | `no_action_required` |
| `phase3_aggregation_relation_negative_control_smoke` | `True` | `ready` | artifact_present=true; status=ready; decision=keep_runtime_defaults | `no_action_required` |
| `phase6_bge_m3_artifact_readiness` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase6_bge_m3_vs_mock_fixture_diagnostics` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase6_bge_m3_comparison_smoke` | `True` | `ready` | artifact_present=true; status=ready; decision=keep_runtime_defaults | `no_action_required` |
| `phase6_qdrant_vector_store_readiness` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase6_qdrant_backup_restore_smoke` | `True` | `ready` | artifact_present=true; status=ready; decision=keep_runtime_defaults | `no_action_required` |
| `phase6_qdrant_bge_private_network_promotion_readiness` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase6_qdrant_bge_private_network_promotion_smoke` | `True` | `ready` | artifact_present=true; status=ready; decision=keep_runtime_defaults | `no_action_required` |
| `deployed_provider_smoke` | `False` | `review` | artifact_present=true; status=review; decision=n/a | `review_evidence_notes` |

## Notes

- This report is local read-only promotion review evidence.
- It consolidates Phase 3 and Phase 6 bridge prerequisites for final hybrid runtime promotion review.
- Unless all required gates are ready, keep_runtime_defaults is the expected decision.
