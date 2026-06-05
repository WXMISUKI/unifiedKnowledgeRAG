# Phase 6 Deployed Handoff Consistency Smoke

- Report: `phase6-deployed-handoff-consistency-smoke-v1`
- Status: `ready`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-05T01:54:02.059825+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Checks | `8` |
| Passed Checks | `8` |
| Failed Checks | `0` |
| Readiness Status | `review` |
| Bundle Status | `review` |
| Bundle Row Status | `review` |
| Field Validation State | `review` |
| Live URL Present | `True` |
| Open Gate Count | `3` |

## Checks

| Check | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `deployed_field_validation_readiness` | `True` | `ready` | artifact_present=true; status=review; field_validation_state=review; decision=keep_local_review_until_deployed_smoke; live_url_present=True; open_gate_count=3 | `no_action_required` |
| `provider_handoff_bundle` | `True` | `ready` | artifact_present=true; status=review; artifact_count=53 | `no_action_required` |
| `provider_handoff_bundle_row` | `True` | `ready` | bundle_row_present=true; bundle_row_status=review; bundle_row_summary=status=review; field_validation_state=review; decision=keep_local_review_until_deployed_smoke; live_url_present=True; open_gate_count=3 | `no_action_required` |
| `status_alignment` | `True` | `ready` | readiness_status=review; bundle_row_status=review | `no_action_required` |
| `field_validation_state_alignment` | `True` | `ready` | expected=review; bundle_summary=status=review; field_validation_state=review; decision=keep_local_review_until_deployed_smoke; live_url_present=True; open_gate_count=3 | `no_action_required` |
| `decision_alignment` | `True` | `ready` | expected=keep_local_review_until_deployed_smoke; bundle_summary=status=review; field_validation_state=review; decision=keep_local_review_until_deployed_smoke; live_url_present=True; open_gate_count=3 | `no_action_required` |
| `live_url_alignment` | `True` | `ready` | expected=True; bundle_summary=status=review; field_validation_state=review; decision=keep_local_review_until_deployed_smoke; live_url_present=True; open_gate_count=3 | `no_action_required` |
| `open_gate_alignment` | `True` | `ready` | expected=3; bundle_summary=status=review; field_validation_state=review; decision=keep_local_review_until_deployed_smoke; live_url_present=True; open_gate_count=3 | `no_action_required` |

## Notes

- This smoke report is local, read-only, and does not call the deployed provider.
- It only compares already-generated readiness and handoff bundle evidence.
- A deployed smoke report may still be needed separately for live URL validation.
