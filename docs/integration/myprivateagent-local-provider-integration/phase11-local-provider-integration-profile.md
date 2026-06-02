# Phase 11 Local Provider Integration Profile

- Report: `phase11-local-provider-integration-profile-v1`
- Status: `blocked`
- Integration State: `blocked`
- Decision: `resolve_local_integration_blockers`
- Generated At: `2026-06-01T13:42:27.003659+00:00`

## Summary

| Metric | Value |
|---|---|
| total_signals | `4` |
| required_signals | `4` |
| ready_signals | `2` |
| review_signals | `1` |
| blocked_signals | `1` |
| local_provider_url | `http://127.0.0.1:8020` |
| api_key_mode | `not_configured_local_dev` |
| runtime_promotion_status | `keep_runtime_defaults` |
| source_binding_policy_owner | `caller` |
| open_gate_ids | `["phase10_local_consumer_readiness", "provider_handoff_bundle"]` |

## Signals

| Signal | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `phase10_local_consumer_readiness` | `True` | `review` | status=review; local_consumer_state=ready_for_local_consumer_probe_review | `review_evidence_notes` |
| `phase10_local_consumer_probe` | `True` | `ready` | status=ready; passed_checks=7/7 | `no_action_required` |
| `provider_integration_probe` | `True` | `ready` | bindable=True | `no_action_required` |
| `provider_handoff_bundle` | `True` | `blocked` | status=blocked | `review_evidence_notes` |

## Notes

- Phase 11 profile is read-only local integration evidence for MyPrivateAgent-style consumption.
- It does not mutate source bindings, switch runtime defaults, or enable GraphRAG execution.
