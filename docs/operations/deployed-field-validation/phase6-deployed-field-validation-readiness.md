# Phase 6 Deployed Field Validation Readiness

- Report: `phase6-deployed-field-validation-readiness-v1`
- Status: `review`
- Field Validation State: `review`
- Decision: `keep_local_review_until_deployed_smoke`
- Generated At: `2026-06-04T07:37:45.431804+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Signals | `4` |
| Required Signals | `3` |
| Ready Signals | `1` |
| Review Signals | `3` |
| Blocked Signals | `0` |
| Live URL Present | `True` |
| Open Gate IDs | `["deployment_readiness", "provider_handoff_bundle", "deployed_provider_smoke"]` |

## Signals

| Signal | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `deployed_field_validation_contract` | `True` | `ready` | contract_present=true | `no_action_required` |
| `deployment_readiness` | `True` | `review` | artifact_present=true; status=review; retrieval_backend=fixture | `review_evidence_notes` |
| `provider_handoff_bundle` | `True` | `review` | artifact_present=true; status=review; artifact_count=50 | `review_evidence_notes` |
| `deployed_provider_smoke` | `False` | `review` | artifact_present=true; status=review; base_url=http://127.0.0.1:8020; handoff_status=review | `review_evidence_notes` |

## Notes

- This report is local read-only field validation evidence.
- It only summarizes existing deployment, handoff, and deployed smoke artifacts.
- A live URL is required before the field validation posture can be considered ready.
