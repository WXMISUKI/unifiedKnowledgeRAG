# Phase 6 BGE-M3 Comparison Smoke

- Report: `phase6-bge-m3-comparison-smoke-v1`
- Status: `ready`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-03T01:40:57.562470+00:00`

## Checks

| Check | Passed | Summary | Recommended Action |
|---|---|---|---|
| `comparison_contract_present` | `True` | present | `no_action_required` |
| `comparison_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `artifact_readiness_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_runtime_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `phase3_latency_diagnostics_present` | `True` | json_parse_ok | `no_action_required` |
| `deployment_readiness_present` | `True` | json_parse_ok | `no_action_required` |

## Summary

- Total checks: `6`
- Passed checks: `6`
- Failed checks: `0`

## Notes

- This smoke report is read-only and validates evidence-chain completeness only.
- No embedding execution, retrieval switching, or runtime promotion is performed.
- Use this artifact before starting private-network promotion review.
