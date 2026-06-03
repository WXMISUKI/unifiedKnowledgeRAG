# Provider Handoff Bundle

- Report: `provider-handoff-bundle-v1`
- Status: `review`
- Generated At: `2026-06-03T02:41:59.371404+00:00`
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
| `phase2_source_format_demand_readiness` | `ingestion-evidence` | `True` | `ready` | status=ready; decision=keep_markdown_baseline; demand_signal=False; unsupported_documents=0; non_markdown_sources=0; open_gate_count=0 | `no_action_required` |
| `phase2_unsupported_format_negative_control_smoke` | `ingestion-smoke` | `True` | `ready` | status=ready; decision=keep_markdown_baseline; passed_checks=5/5; failed_checks=0; unsupported_documents=0; non_markdown_sources=0 | `no_action_required` |
| `deployed_provider_smoke` | `deployed-integration` | `True` | `review` | status=review; base_url=http://127.0.0.1:8020; handoff_status=review | `review_evidence_notes` |
| `phase6_deployed_field_validation_readiness` | `operations` | `True` | `review` | status=review; field_validation_state=review; decision=keep_local_review_until_deployed_smoke; live_url_present=True; open_gate_count=3 | `review_evidence_notes` |
| `phase6_deployed_handoff_consistency_smoke` | `operations-smoke` | `True` | `ready` | status=ready; decision=keep_runtime_defaults; passed_checks=8/8; failed_checks=0; readiness_status=review; bundle_status=review; bundle_row_status=review | `no_action_required` |
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
| `phase7_provider_release_readiness` | `release-readiness` | `True` | `review` | status=review; release_state=ready_for_local_handoff; decision=keep_runtime_defaults; local_handoff_ready=True; runtime_promotion_ready=False; open_gate_count=4 | `review_evidence_notes` |
| `phase7_cross_phase_handoff_consistency_smoke` | `release-smoke` | `True` | `ready` | status=ready; decision=keep_runtime_defaults_until_live_validation; passed_checks=6/6; failed_checks=0 | `no_action_required` |
| `phase8_live_url_validation_readiness` | `live-url-validation` | `True` | `review` | status=review; live_validation_state=review; decision=keep_runtime_defaults_until_live_url_validation; deployed_smoke_present=True; deployed_smoke_status=review; live_url_present=True; open_gate_count=3 | `review_evidence_notes` |
| `phase8_live_url_smoke_consistency_check` | `live-url-validation-smoke` | `True` | `ready` | status=ready; decision=keep_runtime_defaults_until_live_url_validation; passed_checks=10/10; failed_checks=0; readiness_status=review; bundle_status=review; bundle_row_status=review | `no_action_required` |
| `phase9_myprivateagent_local_consumption_readiness` | `local-consumption` | `True` | `review` | status=review; local_consumption_state=review; decision=keep_local_consumption_review; local_provider_url=http://127.0.0.1:8020; local_handoff_ready=True; runtime_promotion_ready=False; open_gate_count=3 | `review_evidence_notes` |
| `phase9_myprivateagent_local_consumption_smoke` | `local-consumption-smoke` | `True` | `ready` | status=ready; decision=keep_runtime_defaults; passed_checks=7/7; failed_checks=0; readiness_status=review; local_consumption_state=review | `no_action_required` |
| `phase10_myprivateagent_local_consumer_readiness` | `local-consumer-verification` | `True` | `review` | status=review; local_consumer_state=ready_for_local_consumer_probe_review; decision=run_local_consumer_probe_before_myprivateagent_integration; local_provider_url=http://127.0.0.1:8020; api_key_mode=not_configured_local_dev; graph_boundary_ready=True; runtime_promotion_status=keep_runtime_defaults; open_gate_count=3 | `review_evidence_notes` |
| `phase10_myprivateagent_local_consumer_probe` | `local-consumer-verification-smoke` | `True` | `ready` | status=ready; decision=keep_provider_side_consumer_probe_review; passed_checks=7/7; failed_checks=0; local_consumer_state=ready_for_local_consumer_probe_review; api_key_mode=not_configured_local_dev; runtime_promotion_status=keep_runtime_defaults | `no_action_required` |
| `phase11_local_provider_integration_profile` | `local-provider-integration` | `True` | `review` | status=review; integration_state=ready_for_local_provider_integration_review; decision=run_phase11_local_integration_smokes; local_provider_url=http://127.0.0.1:8020; api_key_mode=not_configured_local_dev; runtime_promotion_status=keep_runtime_defaults; open_gate_count=2 | `review_evidence_notes` |
| `phase11_provider_discovery_smoke` | `local-provider-integration-smoke` | `True` | `ready` | status=ready; decision=keep_discovery_read_only; passed_checks=4/4; failed_checks=0 | `no_action_required` |
| `phase11_rag_retrieve_consumption_smoke` | `local-provider-integration-smoke` | `True` | `ready` | status=ready; decision=keep_caller_consumption_fail_closed; passed_checks=3/3; failed_checks=0 | `no_action_required` |
| `phase11_source_binding_preview_smoke` | `local-provider-integration-smoke` | `True` | `ready` | status=ready; decision=keep_source_binding_preview_only; passed_checks=3/3; failed_checks=0 | `no_action_required` |
| `phase12_local_rag_integration_hardening_profile` | `local-rag-hardening` | `True` | `review` | status=review; hardening_state=ready_for_local_rag_hardening_review; decision=run_phase12_local_rag_integration_hardening_smoke; local_provider_url=http://127.0.0.1:8020; api_key_mode=not_configured_local_dev; open_gate_count=3 | `review_evidence_notes` |
| `phase12b_candidate_backend_evaluation_readiness` | `candidate-backend-evaluation` | `True` | `review` | status=review; evaluation_state=ready_for_candidate_backend_evaluation_review; decision=continue_spike; strategy_verdict=continue_provider_first_with_candidate_backends; review_ready_families=["local_provider_integration_gate", "retrieval_quality_candidates", "storage_and_private_network_candidates", "deployment_and_ops_candidates"]; reference_only_families=["reference_only_candidates"]; open_gate_count=15 | `review_evidence_notes` |
| `phase12c_pgvector_candidate_backend_readiness` | `candidate-backend-evaluation` | `True` | `blocked` | status=blocked; evaluation_state=pgvector_candidate_configuration_blocked; decision=keep_current_default; strategy_verdict=continue_provider_first_with_candidate_backends; pgvector_database_url_present=False; review_ready_families=["provider_integration_gate", "candidate_evidence_gate"]; ready_families=[]; blocked_families=["pgvector_configuration_gate"]; open_gate_count=15 | `resolve_failed_evidence` |
| `phase12d_pgvector_live_probe_readiness` | `candidate-backend-evaluation` | `True` | `blocked` | status=blocked; evaluation_state=pgvector_probe_configuration_blocked; decision=keep_current_default; strategy_verdict=continue_provider_first_with_candidate_backends; pgvector_database_url_present=False; pgvector_driver_available=False; review_ready_families=[]; ready_families=["candidate_evidence_bridge_gate"]; blocked_families=["pgvector_probe_gate", "pgvector_runtime_gate"]; open_gate_count=9 | `resolve_failed_evidence` |
| `phase3_hybrid_cross_case_fp_fn_smoke` | `retrieval-evidence` | `True` | `ready` | status=ready; passed_checks=4/4; false_positive_count=3; false_negative_count=0 | `no_action_required` |
| `phase3_aggregation_relation_negative_control_smoke` | `retrieval-evidence` | `True` | `ready` | status=ready; decision=keep_runtime_defaults; total_checks=4; passed_checks=4; failed_checks=0; relation_unsupported_count=1; expected_empty_pass_rate=1.0000 | `no_action_required` |
| `phase3_hybrid_runtime_promotion_decision_readiness` | `retrieval-evidence` | `True` | `review` | status=review; decision=keep_runtime_defaults; review_state=review; required_signals=14; ready_signals=6; open_gates=9; open_gate_count=9 | `review_evidence_notes` |
| `phase3_hybrid_runtime_promotion_decision_smoke` | `retrieval-evidence` | `True` | `ready` | status=ready; decision=keep_runtime_defaults; passed_checks=16/16; failed_checks=0 | `no_action_required` |
| `phase4_evidence_pack_readiness` | `evidence-packaging` | `True` | `ready` | status=ready; decision=keep_caller_ownership; smoke_passed=True; ready_artifacts=5/5; required_ready=2/2 | `no_action_required` |
| `phase4_caller_consumption_smoke` | `caller-consumption` | `True` | `ready` | status=ready; passed_checks=3/3; answerable_checks=1; insufficient_checks=1; contract_doc_present=True | `no_action_required` |
| `phase5_graph_use_case_readiness` | `graph-readiness` | `True` | `ready` | status=ready; decision=keep_graph_query_planned; graph_schema_count=1; graph_query_status=planned; graph_query_planned=True; preflight_graph_boundary_ready=True; smoke_graph_check_passed=True; smoke_checks_passed=True | `no_action_required` |
| `phase5_graph_boundary_smoke_summary` | `graph-boundary-smoke` | `True` | `ready` | status=ready; decision=keep_graph_query_planned; source_smoke_passed=True; graph_checks_passed=2; graph_schema_count=1; graph_query_status=planned; graph_query_planned=True; graph_error_code=GRAPH_NOT_IMPLEMENTED | `no_action_required` |

## Operation Notes

- This bundle is a read-only handoff index over existing local evidence files.
- Regenerate prerequisite evidence reports after configuration, dependency, source, or index lifecycle changes.
- External control planes still own provider registration, heartbeat governance, audit policy, and source-to-agent binding decisions.
- At least one evidence artifact requires human review before promotion.
