# Phase 3 Hybrid Runtime Promotion Decision Smoke

- Report: `phase3-hybrid-runtime-promotion-decision-smoke-v1`
- Status: `ready`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-03T02:41:59.310218+00:00`

## Checks

| Check | Passed | Summary | Recommended Action |
|---|---|---|---|
| `hybrid_runtime_promotion_contract_present` | `True` | present | `no_action_required` |
| `hybrid_runtime_promotion_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_retrieval_promotion_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_candidate_runtime_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_candidate_latency_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_hybrid_calibration_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_hybrid_cross_case_fp_fn_smoke_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_aggregation_relation_negative_control_smoke_present` | `True` | json_parse_ok | `no_action_required` |
| `phase6_bge_artifact_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `phase6_bge_comparison_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `phase6_bge_comparison_smoke_present` | `True` | json_parse_ok | `no_action_required` |
| `phase6_qdrant_vector_store_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `phase6_qdrant_backup_restore_smoke_present` | `True` | json_parse_ok | `no_action_required` |
| `phase6_private_network_promotion_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `phase6_private_network_promotion_smoke_present` | `True` | json_parse_ok | `no_action_required` |
| `hybrid_runtime_promotion_readiness_gate_visibility` | `True` | decision=keep_runtime_defaults; review_state=review; open_gate_count=9 | `no_action_required` |

## Summary

- Total checks: `16`
- Passed checks: `16`
- Failed checks: `0`

## Notes

- This smoke validates hybrid runtime promotion decision evidence-chain completeness only.
- It does not run retrieval execution, model download, deployment automation, or runtime promotion.
- Use it before final Phase 3 hybrid runtime promotion decision review.
