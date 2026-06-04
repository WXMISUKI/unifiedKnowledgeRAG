# Phase 10 MyPrivateAgent Local Consumer Probe

- Report: `phase10-myprivateagent-local-consumer-probe-v1`
- Status: `ready`
- Decision: `keep_provider_side_consumer_probe_review`
- Generated At: `2026-06-04T07:37:45.602287+00:00`

## Summary

| Metric | Value |
|---|---|
| total_checks | `7` |
| passed_checks | `7` |
| failed_checks | `0` |
| readiness_status | `review` |
| local_consumer_state | `ready_for_local_consumer_probe_review` |
| local_provider_url | `http://127.0.0.1:8020` |
| api_key_mode | `not_configured_local_dev` |
| runtime_promotion_status | `keep_runtime_defaults` |

## Checks

| Check | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `phase10_local_consumer_readiness` | `True` | `ready` | readiness_present=true; status=review | `no_action_required` |
| `phase10_contract_content` | `True` | `ready` | contract_required_tokens_present=true | `no_action_required` |
| `local_access_mode` | `True` | `ready` | base_url=http://127.0.0.1:8020; api_key_mode=not_configured_local_dev | `no_action_required` |
| `handoff_phase10_presence` | `True` | `ready` | phase10_handoff_artifacts_present=true | `no_action_required` |
| `evidence_pack_caller_smoke` | `True` | `ready` | status=ready | `no_action_required` |
| `graph_planned_boundary` | `True` | `ready` | readiness_graph_boundary_ready=True; provider_smoke_graph_boundary_ready=True | `no_action_required` |
| `runtime_promotion_boundary` | `True` | `ready` | runtime_promotion_ready=False; runtime_promotion_status=keep_runtime_defaults | `no_action_required` |

## Notes

- This probe is caller-shaped but provider-side and read-only.
- It validates local consumer evidence alignment without running a live MyPrivateAgent integration.
- It does not create source bindings, execute GraphRAG, or promote runtime defaults.
