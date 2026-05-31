# Provider Handoff Evidence Refresh

- Report: `provider-handoff-refresh-v1`
- Status: `review`
- Generated At: `2026-05-31T06:51:27.724031+00:00`

## Refresh Steps

| Step | Category | Status | Output Paths | Recommended Action | Summary |
|---|---|---|---|---|---|
| `provider_integration_probe` | `integration` | `ready` | `docs\integration\provider-binding\provider-integration-probe.json`, `docs\integration\provider-binding\provider-integration-probe.md` | `no_action_required` | status=ready; bindable=True |
| `provider_contract_smoke` | `contract` | `ready` | `docs\smoke\provider-contract\provider-contract-smoke.json`, `docs\smoke\provider-contract\provider-contract-smoke.md` | `no_action_required` | status=ready; summary={"failed": 0, "passed": 9, "total": 9} |
| `deployment_readiness` | `operations` | `review` | `docs\operations\deployment-readiness\deployment-readiness.json`, `docs\operations\deployment-readiness\deployment-readiness.md` | `review_evidence_notes` | status=review; report_status=review |
| `reindex_readiness` | `operations` | `ready` | `docs\operations\reindex-readiness\reindex-readiness.json`, `docs\operations\reindex-readiness\reindex-readiness.md` | `no_action_required` | status=ready; report_status=ready |
| `source_binding_summary` | `source-binding` | `ready` | `docs\integration\source-bindings\provider-source-bindings.json`, `docs\integration\source-bindings\provider-source-bindings.md` | `no_action_required` | status=ready; report_status=ready |
| `provider_handoff_bundle` | `handoff` | `review` | `docs\integration\provider-handoff\provider-handoff-bundle.json`, `docs\integration\provider-handoff\provider-handoff-bundle.md` | `review_evidence_notes` | status=review; report_status=review |

## Operation Notes

- This refresh workflow only regenerates local evidence files.
- External control planes still own provider registration, heartbeat governance, audit policy, source-to-agent binding decisions, and final answer policy.
- At least one refreshed report requires human review before promotion.
