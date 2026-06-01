# Phase 8 Live URL Smoke Consistency Check

- Report: `phase8-live-url-smoke-consistency-check-v1`
- Status: `ready`
- Decision: `keep_runtime_defaults_until_live_url_validation`
- Generated At: `2026-06-01T11:51:13.981873+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Checks | `10` |
| Passed Checks | `10` |
| Failed Checks | `0` |
| Readiness Status | `review` |
| Bundle Status | `review` |
| Bundle Row Status | `review` |
| Live Validation State | `await_live_url_validation` |
| Deployed Smoke Present | `False` |
| Deployed Smoke Status | `review` |
| Live URL Present | `False` |
| Open Gate Count | `3` |

## Checks

| Check | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `phase8_live_url_validation_readiness` | `True` | `ready` | artifact_present=true; status=review; live_validation_state=await_live_url_validation; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=False; deployed_smoke_status=review; live_url_present=False; open_gate_count=3 | `no_action_required` |
| `provider_handoff_bundle` | `True` | `ready` | artifact_present=true; status=review; artifact_count=34 | `no_action_required` |
| `provider_handoff_bundle_row` | `True` | `ready` | bundle_row_present=true; bundle_row_status=review; bundle_row_summary=status=review; live_validation_state=await_live_url_validation; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=False; deployed_smoke_status=review; live_url_present=False; open_gate_count=3 | `no_action_required` |
| `status_alignment` | `True` | `ready` | readiness_status=review; bundle_row_status=review | `no_action_required` |
| `live_validation_state_alignment` | `True` | `ready` | expected=await_live_url_validation; bundle_summary=status=review; live_validation_state=await_live_url_validation; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=False; deployed_smoke_status=review; live_url_present=False; open_gate_count=3 | `no_action_required` |
| `decision_alignment` | `True` | `ready` | expected=keep_runtime_defaults_until_live_url_validation; bundle_summary=status=review; live_validation_state=await_live_url_validation; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=False; deployed_smoke_status=review; live_url_present=False; open_gate_count=3 | `no_action_required` |
| `deployed_smoke_present_alignment` | `True` | `ready` | expected=False; bundle_summary=status=review; live_validation_state=await_live_url_validation; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=False; deployed_smoke_status=review; live_url_present=False; open_gate_count=3 | `no_action_required` |
| `deployed_smoke_status_alignment` | `True` | `ready` | expected=review; bundle_summary=status=review; live_validation_state=await_live_url_validation; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=False; deployed_smoke_status=review; live_url_present=False; open_gate_count=3 | `no_action_required` |
| `live_url_present_alignment` | `True` | `ready` | expected=False; bundle_summary=status=review; live_validation_state=await_live_url_validation; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=False; deployed_smoke_status=review; live_url_present=False; open_gate_count=3 | `no_action_required` |
| `open_gate_count_alignment` | `True` | `ready` | expected=3; bundle_summary=status=review; live_validation_state=await_live_url_validation; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=False; deployed_smoke_status=review; live_url_present=False; open_gate_count=3 | `no_action_required` |

## Notes

- This smoke is local read-only consistency evidence.
- It compares the current Phase 8 readiness export with the handoff bundle row.
- It does not call deployed endpoints or promote runtime defaults.
