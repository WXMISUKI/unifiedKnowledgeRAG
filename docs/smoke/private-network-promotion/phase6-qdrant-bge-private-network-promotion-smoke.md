# Phase 6 Private-Network Promotion Smoke

- Report: `phase6-qdrant-bge-private-network-promotion-smoke-v1`
- Status: `ready`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-01T13:01:28.413252+00:00`

## Checks

| Check | Passed | Summary | Recommended Action |
|---|---|---|---|
| `private_network_review_contract_present` | `True` | present | `no_action_required` |
| `private_network_promotion_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `qdrant_vector_store_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `qdrant_backup_restore_smoke_present` | `True` | json_parse_ok | `no_action_required` |
| `bge_artifact_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `bge_comparison_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `bge_comparison_smoke_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_runtime_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_latency_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `deployment_readiness_present` | `True` | json_parse_ok | `no_action_required` |

## Summary

- Total checks: `10`
- Passed checks: `10`
- Failed checks: `0`

## Notes

- This smoke report validates private-network promotion evidence-chain completeness only.
- It does not run retrieval execution, model download, deployment automation, or runtime promotion.
- Use it before manual private-network candidate promotion review.
