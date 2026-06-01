# Provider Handoff Bundle

- Report: `provider-handoff-bundle-v1`
- Status: `review`
- Generated At: `2026-06-01T01:47:33.344631+00:00`
- Provider: `unifiedKnowledgeProvider`
- Contract: `knowledge-provider-contract-v1`
- Manifest: `provider-integration-manifest-v1`

## Evidence Artifacts

| Artifact | Category | Present | Status | Summary | Recommended Action |
|---|---|---|---|---|---|
| `provider_integration_probe` | `integration` | `True` | `ready` | bindable=True; checks=6; capabilities=5 | `no_action_required` |
| `provider_contract_smoke` | `contract` | `True` | `ready` | passed=True; checks=9/9 | `no_action_required` |
| `deployment_readiness` | `operations` | `True` | `review` | status=review | `review_evidence_notes` |
| `reindex_readiness` | `operations` | `True` | `ready` | status=ready | `no_action_required` |
| `source_binding_summary` | `source-binding` | `True` | `ready` | status=ready; bindable_sources=2/2; source_statuses=ready:2; recommended_actions=bind_source_from_control_plane:2 | `no_action_required` |
| `deployed_provider_smoke` | `deployed-integration` | `False` | `review` | Optional deployed evidence is missing. | `run_deployed_provider_smoke_after_deployment` |
| `phase3_seed_retrieval_baseline` | `retrieval-evidence` | `True` | `ready` | total_cases=29; hit_rate=0.9310; citation_match_rate=0.9310; empty_handling_rate=0.8182 | `no_action_required` |
| `phase3_fp_fn_review` | `retrieval-evidence` | `True` | `ready` | false_positive_count=2; false_negative_count=0; false_positive_rate=0.0690; false_negative_rate=0.0000 | `no_action_required` |
| `phase3_retrieval_promotion_readiness` | `retrieval-evidence` | `True` | `review` | status=review; decision=keep_runtime_defaults; open_gates=7; ready_gates=0; review_gates=3; candidate_gates=4 | `review_evidence_notes` |
| `phase3_candidate_runtime_diagnostics` | `retrieval-evidence` | `True` | `review` | status=review; decision=keep_runtime_defaults; ready_checks=0/6; review_checks=6; blocked_checks=0 | `review_evidence_notes` |
| `phase3_hybrid_cross_case_fp_fn_smoke` | `retrieval-evidence` | `True` | `ready` | status=ready; passed_checks=4/4; false_positive_count=2; false_negative_count=0 | `no_action_required` |
| `phase4_evidence_pack_readiness` | `evidence-packaging` | `True` | `ready` | status=ready; decision=keep_caller_ownership; smoke_passed=True; ready_artifacts=5/5; required_ready=2/2 | `no_action_required` |
| `phase4_caller_consumption_smoke` | `caller-consumption` | `True` | `ready` | status=ready; passed_checks=3/3; answerable_checks=1; insufficient_checks=1; contract_doc_present=True | `no_action_required` |
| `phase5_graph_use_case_readiness` | `graph-readiness` | `True` | `ready` | status=ready; decision=keep_graph_query_planned; graph_schema_count=1; graph_query_status=planned; graph_query_planned=True; preflight_graph_boundary_ready=True; smoke_graph_check_passed=True; smoke_checks_passed=True | `no_action_required` |
| `phase5_graph_boundary_smoke_summary` | `graph-boundary-smoke` | `True` | `ready` | status=ready; decision=keep_graph_query_planned; source_smoke_passed=True; graph_checks_passed=2; graph_schema_count=1; graph_query_status=planned; graph_query_planned=True; graph_error_code=GRAPH_NOT_IMPLEMENTED | `no_action_required` |

## Operation Notes

- This bundle is a read-only handoff index over existing local evidence files.
- Regenerate prerequisite evidence reports after configuration, dependency, source, or index lifecycle changes.
- External control planes still own provider registration, heartbeat governance, audit policy, and source-to-agent binding decisions.
- At least one evidence artifact requires human review before promotion.
- Deployed provider smoke evidence is optional before deployment; run it against the deployed base URL before external binding.
