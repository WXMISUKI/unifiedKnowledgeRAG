# Provider Handoff Bundle

- Report: `provider-handoff-bundle-v1`
- Status: `review`
- Generated At: `2026-06-01T08:16:02.520710+00:00`
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
| `phase3_seed_retrieval_baseline` | `retrieval-evidence` | `True` | `ready` | total_cases=32; hit_rate=0.9062; citation_match_rate=0.9062; empty_handling_rate=0.7500 | `no_action_required` |
| `phase3_fp_fn_review` | `retrieval-evidence` | `True` | `ready` | false_positive_count=3; false_negative_count=0; false_positive_rate=0.0938; false_negative_rate=0.0000 | `no_action_required` |
| `phase3_retrieval_promotion_readiness` | `retrieval-evidence` | `True` | `review` | status=review; decision=keep_runtime_defaults; open_gates=7; ready_gates=0; review_gates=3; candidate_gates=4 | `review_evidence_notes` |
| `phase3_candidate_runtime_diagnostics` | `retrieval-evidence` | `True` | `review` | status=review; decision=keep_runtime_defaults; ready_checks=0/6; review_checks=6; blocked_checks=0 | `review_evidence_notes` |
| `phase3_candidate_latency_resource_diagnostics` | `retrieval-evidence` | `True` | `review` | status=review; decision=keep_runtime_defaults; total_signals=6; ready_signals=1; review_signals=5; backend=fixture; avg_latency_ms=0.2368; deployment_status=review; runtime_status=review | `review_evidence_notes` |
| `phase3_hybrid_fusion_threshold_calibration` | `retrieval-evidence` | `True` | `review` | status=review; decision=keep_runtime_defaults; ready_signals=3/6; review_signals=3; fusion=rrf; score_filter=disabled-for-rrf-fusion-score; selected_dense_threshold=0.7000; runtime_threshold=0.0100 | `review_evidence_notes` |
| `phase6_bge_m3_artifact_readiness` | `operations` | `True` | `review` | status=review; decision=keep_runtime_defaults; ready_signals=1/6; review_signals=5; path_exists=False; manifest_exists=False; checksum_coverage=0/0 | `review_evidence_notes` |
| `phase6_bge_m3_vs_mock_fixture_diagnostics` | `operations` | `True` | `review` | status=review; decision=keep_runtime_defaults; ready_signals=5/7; review_signals=2; hit_rate_delta=-0.1443; citation_match_rate_delta=-0.1443; empty_handling_rate_delta=-0.4643 | `review_evidence_notes` |
| `phase6_bge_m3_comparison_smoke` | `operations-smoke` | `True` | `ready` | status=ready; decision=keep_runtime_defaults; passed_checks=6/6; failed_checks=0 | `no_action_required` |
| `phase6_qdrant_vector_store_readiness` | `operations` | `True` | `review` | status=review; decision=keep_runtime_defaults; ready_signals=3/6; review_signals=3; backend=fixture; candidate_present=True; empty_handling_rate=0.2857 | `review_evidence_notes` |
| `phase6_qdrant_backup_restore_smoke` | `operations-smoke` | `True` | `ready` | status=ready; decision=keep_runtime_defaults; passed_checks=4/4; failed_checks=0 | `no_action_required` |
| `phase6_qdrant_bge_private_network_promotion_readiness` | `operations` | `True` | `review` | status=review; state=review; decision=keep_runtime_defaults; ready_signals=3/12; review_signals=9; blocked_signals=0 | `review_evidence_notes` |
| `phase6_qdrant_bge_private_network_promotion_smoke` | `operations-smoke` | `True` | `ready` | status=ready; decision=keep_runtime_defaults; passed_checks=10/10; failed_checks=0 | `no_action_required` |
| `phase3_hybrid_cross_case_fp_fn_smoke` | `retrieval-evidence` | `True` | `ready` | status=ready; passed_checks=4/4; false_positive_count=3; false_negative_count=0 | `no_action_required` |
| `phase3_aggregation_relation_negative_control_smoke` | `retrieval-evidence` | `True` | `ready` | status=ready; decision=keep_runtime_defaults; total_checks=4; passed_checks=4; failed_checks=0; relation_unsupported_count=1; expected_empty_pass_rate=1.0000 | `no_action_required` |
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
