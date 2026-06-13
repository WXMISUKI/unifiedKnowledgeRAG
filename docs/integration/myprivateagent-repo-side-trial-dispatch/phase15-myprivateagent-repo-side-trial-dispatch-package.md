# Phase 15 MyPrivateAgent Repo-Side Trial Dispatch Package

- Report: `phase15-myprivateagent-repo-side-trial-dispatch-package-v1`
- Status: `ready`
- Dispatch State: `ready_for_repo_side_trial_dispatch`
- Decision: `dispatch_myprivateagent_repo_side_trial`
- Generated At: `2026-06-13T13:10:48.544674+00:00`

## Summary

| Metric | Value |
|---|---|
| `roadmap_focus` | `myprivateagent_repo_side_trial_dispatch` |
| `dispatch_state` | `ready_for_repo_side_trial_dispatch` |
| `blocker_category` | `none` |
| `access_gate_status` | `ready` |
| `primitive_signal_ids` | `["phase10_myprivateagent_local_consumer_probe", "phase11_provider_discovery_smoke", "phase11_rag_retrieve_consumption_smoke", "phase11_source_binding_preview_smoke", "provider_contract_smoke"]` |
| `ready_primitive_signal_ids` | `["phase10_myprivateagent_local_consumer_probe", "phase11_provider_discovery_smoke", "phase11_rag_retrieve_consumption_smoke", "phase11_source_binding_preview_smoke", "provider_contract_smoke"]` |
| `review_primitive_signal_ids` | `[]` |
| `blocked_primitive_signal_ids` | `[]` |
| `missing_primitive_signal_ids` | `[]` |
| `open_review_context_signal_ids` | `["phase10_myprivateagent_local_consumer_readiness", "phase11_local_provider_integration_profile", "phase13_provider_roadmap_decision_checkpoint"]` |
| `phase10_status` | `review` |
| `phase11_status` | `review` |
| `phase13_status` | `review` |
| `phase14_status` | `ready` |
| `handoff_status` | `ready` |
| `total_signals` | `11` |
| `required_signals` | `5` |
| `ready_signals` | `8` |
| `review_signals` | `3` |
| `blocked_signals` | `0` |
| `ready_signal_ids` | `["provider_contract_smoke", "phase10_myprivateagent_local_consumer_probe", "phase11_provider_discovery_smoke", "phase11_rag_retrieve_consumption_smoke", "phase11_source_binding_preview_smoke", "phase14_myprivateagent_provider_integration_acceptance_checkpoint", "provider_handoff_bundle", "provider_handoff_refresh"]` |
| `review_signal_ids` | `["phase10_myprivateagent_local_consumer_readiness", "phase11_local_provider_integration_profile", "phase13_provider_roadmap_decision_checkpoint"]` |
| `blocked_signal_ids` | `[]` |
| `open_gate_ids` | `["phase10_myprivateagent_local_consumer_readiness", "phase11_local_provider_integration_profile", "phase13_provider_roadmap_decision_checkpoint"]` |
| `local_provider_url` | `http://127.0.0.1:8020` |
| `source_binding_policy_owner` | `caller` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `caller_checklist` | `["dispatch_myprivateagent_repo_side_trial", "capture_trial_outcome_and_refresh_evidence"]` |

## Caller Checklist

- dispatch_myprivateagent_repo_side_trial
- capture_trial_outcome_and_refresh_evidence

## Signals

| Signal | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `provider_contract_smoke` | `True` | `ready` | status=ready; passed=True; total_checks=unknown; failed_checks=unknown | `no_action_required` |
| `phase10_myprivateagent_local_consumer_readiness` | `False` | `review` | status=review; local_consumer_state=ready_for_local_consumer_probe_review; runtime_promotion_status=keep_runtime_defaults; source_binding_policy_owner=caller | `review_evidence_notes` |
| `phase10_myprivateagent_local_consumer_probe` | `True` | `ready` | status=ready; passed_checks=7/7; decision=keep_provider_side_consumer_probe_review | `no_action_required` |
| `phase11_local_provider_integration_profile` | `False` | `review` | status=review; integration_state=ready_for_local_provider_integration_review; local_provider_url=http://127.0.0.1:8020; api_key_mode=not_configured_local_dev | `review_evidence_notes` |
| `phase11_provider_discovery_smoke` | `True` | `ready` | status=ready; provider_discovery_state=ready; passed_checks=4/4 | `no_action_required` |
| `phase11_rag_retrieve_consumption_smoke` | `True` | `ready` | status=ready; rag_retrieve_state=ready; passed_checks=3/3 | `no_action_required` |
| `phase11_source_binding_preview_smoke` | `True` | `ready` | status=ready; source_binding_preview_state=ready; passed_checks=3/3 | `no_action_required` |
| `phase13_provider_roadmap_decision_checkpoint` | `False` | `review` | status=review; checkpoint_state=ready_for_provider_integration_hardening; decision=resume_provider_integration_hardening; roadmap_focus=resume_provider_integration_hardening; candidate_backend_posture=pause_pgvector_until_live_probe_executed; phase12d_status=blocked; phase12f_status=review | `review_evidence_notes` |
| `phase14_myprivateagent_provider_integration_acceptance_checkpoint` | `False` | `ready` | status=ready; acceptance_state=ready_for_myprivateagent_repo_side_trial; decision=approve_myprivateagent_repo_side_trial; roadmap_focus=myprivateagent_repo_side_trial; blocker_category=none; phase10_status=review; phase11_status=review; phase13_status=review | `no_action_required` |
| `provider_handoff_bundle` | `False` | `ready` | status=ready; overall_status=review; access_focused_status=ready; decision=review_evidence_notes; evidence_artifacts=53 | `no_action_required` |
| `provider_handoff_refresh` | `False` | `ready` | status=ready; overall_status=review; access_focused_status=ready; decision=review_evidence_notes; steps=52 | `no_action_required` |

## Notes

- This dispatch package is local, read-only evidence for a MyPrivateAgent repo-side trial dispatch decision.
- It keeps runtime defaults unchanged and does not create source-to-agent binding or control-plane ownership.
- The verdict is conservative and separates provider evidence gaps from external environment blockers.
