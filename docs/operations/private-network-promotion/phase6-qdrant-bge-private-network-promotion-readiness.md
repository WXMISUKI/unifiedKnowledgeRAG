# Phase 6 Qdrant+BGE Private-Network Promotion Readiness

- Report: `phase6-qdrant-bge-private-network-promotion-readiness-v1`
- Status: `review`
- Promotion Review State: `review`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-01T08:16:02.479167+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Signals | `12` |
| Required Signals | `9` |
| Ready Signals | `3` |
| Review Signals | `9` |
| Blocked Signals | `0` |
| Open Gate IDs | `["qdrant_vector_store_readiness", "bge_m3_artifact_readiness", "bge_m3_comparison_diagnostics", "phase3_runtime_diagnostics", "phase3_latency_diagnostics", "deployment_readiness", "phase3_fp_fn_review", "phase3_hybrid_calibration", "deployed_provider_smoke"]` |

## Signals

| Signal | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `private_network_review_contract` | `True` | `ready` | contract_present=true | `no_action_required` |
| `qdrant_vector_store_readiness` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `qdrant_backup_restore_smoke` | `True` | `ready` | artifact_present=true; status=ready; decision=keep_runtime_defaults | `no_action_required` |
| `bge_m3_artifact_readiness` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `bge_m3_comparison_diagnostics` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `bge_m3_comparison_smoke` | `True` | `ready` | artifact_present=true; status=ready; decision=keep_runtime_defaults | `no_action_required` |
| `phase3_runtime_diagnostics` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `phase3_latency_diagnostics` | `True` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `deployment_readiness` | `True` | `review` | artifact_present=true; status=review; decision=n/a | `review_evidence_notes` |
| `phase3_fp_fn_review` | `False` | `review` | artifact_present=true; status=review; decision=n/a | `review_evidence_notes` |
| `phase3_hybrid_calibration` | `False` | `review` | artifact_present=true; status=review; decision=keep_runtime_defaults | `review_evidence_notes` |
| `deployed_provider_smoke` | `False` | `review` | artifact_present=false | `run_deployed_provider_smoke_after_deployment` |

## Notes

- This report is local read-only promotion review evidence.
- Use it to decide whether private-network candidate review can proceed.
- Even when ready_for_private_network_candidate, runtime defaults remain unchanged until separate promotion approval.
