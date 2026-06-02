# Provider Handoff Evidence Refresh

- Report: `provider-handoff-refresh-v1`
- Status: `blocked`
- Generated At: `2026-06-01T13:39:35.664348+00:00`

## Refresh Steps

| Step | Category | Status | Output Paths | Recommended Action | Summary |
|---|---|---|---|---|---|
| `provider_integration_probe` | `integration` | `ready` | `docs\integration\provider-binding\provider-integration-probe.json`, `docs\integration\provider-binding\provider-integration-probe.md` | `no_action_required` | status=ready; bindable=True |
| `provider_contract_smoke` | `contract` | `ready` | `docs\smoke\provider-contract\provider-contract-smoke.json`, `docs\smoke\provider-contract\provider-contract-smoke.md` | `no_action_required` | status=ready; summary={"failed": 0, "passed": 9, "total": 9} |
| `deployment_readiness` | `operations` | `review` | `docs\operations\deployment-readiness\deployment-readiness.json`, `docs\operations\deployment-readiness\deployment-readiness.md` | `review_evidence_notes` | status=review; report_status=review |
| `reindex_readiness` | `operations` | `ready` | `docs\operations\reindex-readiness\reindex-readiness.json`, `docs\operations\reindex-readiness\reindex-readiness.md` | `no_action_required` | status=ready; report_status=ready |
| `phase6_bge_m3_artifact_readiness` | `operations` | `review` | `docs\operations\bge-m3-artifact-readiness\phase6-bge-m3-artifact-readiness.json`, `docs\operations\bge-m3-artifact-readiness\phase6-bge-m3-artifact-readiness.md` | `review_evidence_notes` | status=review; summary={"blocked_signals": 0, "open_signal_ids": ["embedding_provider_candidate", "model_path_and_manifest_presence", "required_file_inventory", "checksum_coverage", "private_network_copy_posture"], "ready_signals": 1, "review_signals": 5, "total_signals": 6} |
| `phase6_bge_m3_vs_mock_fixture_diagnostics` | `operations` | `review` | `docs\operations\bge-m3-comparison-readiness\phase6-bge-m3-vs-mock-fixture-diagnostics.json`, `docs\operations\bge-m3-comparison-readiness\phase6-bge-m3-vs-mock-fixture-diagnostics.md` | `review_evidence_notes` | status=review; summary={"blocked_signals": 0, "open_signal_ids": ["artifact_readiness_linkage", "quality_non_regression_visibility"], "ready_signals": 5, "review_signals": 2, "total_signals": 7} |
| `phase6_bge_m3_comparison_smoke` | `operations-smoke` | `ready` | `docs\smoke\bge-m3-comparison\phase6-bge-m3-comparison-smoke.json`, `docs\smoke\bge-m3-comparison\phase6-bge-m3-comparison-smoke.md` | `no_action_required` | status=ready; summary={"failed_checks": 0, "passed_checks": 6, "total_checks": 6} |
| `phase6_qdrant_vector_store_readiness` | `operations` | `review` | `docs\operations\qdrant-vector-store-readiness\phase6-qdrant-vector-store-readiness.json`, `docs\operations\qdrant-vector-store-readiness\phase6-qdrant-vector-store-readiness.md` | `review_evidence_notes` | status=review; summary={"ready_signals": 3, "review_signals": 3, "total_signals": 6} |
| `phase6_qdrant_backup_restore_smoke` | `operations-smoke` | `ready` | `docs\smoke\qdrant-backup-restore\phase6-qdrant-backup-restore-smoke.json`, `docs\smoke\qdrant-backup-restore\phase6-qdrant-backup-restore-smoke.md` | `no_action_required` | status=ready; summary={"failed_checks": 0, "passed_checks": 4, "total_checks": 4} |
| `phase6_qdrant_bge_private_network_promotion_readiness` | `operations` | `review` | `docs\operations\private-network-promotion\phase6-qdrant-bge-private-network-promotion-readiness.json`, `docs\operations\private-network-promotion\phase6-qdrant-bge-private-network-promotion-readiness.md` | `review_evidence_notes` | status=review; summary={"blocked_signals": 0, "open_gate_ids": ["qdrant_vector_store_readiness", "bge_m3_artifact_readiness", "bge_m3_comparison_diagnostics", "phase3_runtime_diagnostics", "phase3_latency_diagnostics", "deployment_readiness", "phase3_fp_fn_review", "phase3_hybrid_calibration", "deployed_provider_smoke"], "ready_signals": 3, "required_signals": 9, "review_signals": 9, "total_signals": 12} |
| `phase6_qdrant_bge_private_network_promotion_smoke` | `operations-smoke` | `ready` | `docs\smoke\private-network-promotion\phase6-qdrant-bge-private-network-promotion-smoke.json`, `docs\smoke\private-network-promotion\phase6-qdrant-bge-private-network-promotion-smoke.md` | `no_action_required` | status=ready; summary={"failed_checks": 0, "passed_checks": 10, "total_checks": 10} |
| `source_binding_summary` | `source-binding` | `ready` | `docs\integration\source-bindings\provider-source-bindings.json`, `docs\integration\source-bindings\provider-source-bindings.md` | `no_action_required` | status=ready; report_status=ready |
| `phase2_source_format_demand_readiness` | `ingestion-evidence` | `ready` | `docs\operations\source-format-demand\phase2-source-format-demand-readiness.json`, `docs\operations\source-format-demand\phase2-source-format-demand-readiness.md` | `no_action_required` | status=ready; summary={"bindable_sources": 2, "format_expansion_demand_signal": false, "markdown_only_sources": 2, "non_markdown_sources": 0, "open_gate_count": 0, "parser_ready_documents": 2, "parser_status_counts": {"ready": 2}, "recommended_action_counts": {"bind_source_from_control_plane": 2}, "source_binding_ready": true, "source_binding_status": "ready", "source_status_counts": {"ready": 2}, "supported_format_counts": {"markdown": 2}, "total_sources": 2, "unsupported_documents": 0} |
| `phase2_unsupported_format_negative_control_smoke` | `ingestion-smoke` | `ready` | `docs\smoke\source-format-demand\phase2-unsupported-format-negative-control-smoke.json`, `docs\smoke\source-format-demand\phase2-unsupported-format-negative-control-smoke.md` | `no_action_required` | status=ready; summary={"failed_checks": 0, "format_expansion_demand_signal": false, "non_markdown_sources": 0, "parser_ready_documents": 2, "passed_checks": 5, "status": "ready", "total_checks": 5, "unsupported_documents": 0} |
| `phase6_deployed_field_validation_readiness` | `operations` | `blocked` | `docs\operations\deployed-field-validation\phase6-deployed-field-validation-readiness.json`, `docs\operations\deployed-field-validation\phase6-deployed-field-validation-readiness.md` | `resolve_step_failure` | status=blocked; summary={"blocked_signals": 1, "live_url_present": true, "open_gate_ids": ["deployment_readiness", "provider_handoff_bundle", "deployed_provider_smoke"], "ready_signals": 1, "required_signals": 3, "review_signals": 2, "total_signals": 4} |
| `phase3_fp_fn_review` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase3_retrieval_promotion_readiness` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase3_candidate_runtime_diagnostics` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase3_candidate_latency_resource_diagnostics` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase3_hybrid_fusion_threshold_calibration` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase3_hybrid_cross_case_fp_fn_smoke` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase3_aggregation_relation_negative_control_smoke` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase3_hybrid_runtime_promotion_decision_readiness` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase3_hybrid_runtime_promotion_decision_smoke` | `retrieval-evidence` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase4_evidence_pack_readiness` | `evidence-packaging` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase4_caller_consumption_smoke` | `caller-consumption` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase5_graph_use_case_readiness` | `graph-readiness` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase5_graph_boundary_smoke_summary` | `graph-boundary-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase7_provider_release_readiness` | `release-readiness` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase7_cross_phase_handoff_consistency_smoke` | `release-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase8_live_url_validation_readiness` | `live-url-validation` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase9_myprivateagent_local_consumption_readiness` | `local-consumption` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase9_myprivateagent_local_consumption_smoke` | `local-consumption-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase10_myprivateagent_local_consumer_readiness` | `local-consumer-verification` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase11_local_provider_integration_profile` | `local-provider-integration` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `provider_handoff_bundle` | `handoff` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase11_provider_discovery_smoke` | `local-provider-integration-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase10_myprivateagent_local_consumer_probe` | `local-consumer-verification-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase11_rag_retrieve_consumption_smoke` | `local-provider-integration-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase11_source_binding_preview_smoke` | `local-provider-integration-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase6_deployed_handoff_consistency_smoke` | `operations-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |
| `phase8_live_url_smoke_consistency_check` | `live-url-validation-smoke` | `skipped` | `none` | `not_run_due_to_previous_failure` | Skipped because an earlier refresh step was blocked. |

## Operation Notes

- This refresh workflow only regenerates local evidence files.
- External control planes still own provider registration, heartbeat governance, audit policy, source-to-agent binding decisions, and final answer policy.
- At least one refreshed report requires human review before promotion.
- Refresh stopped or skipped later steps because a blocking issue was detected.
