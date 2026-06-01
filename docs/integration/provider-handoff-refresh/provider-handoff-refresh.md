# Provider Handoff Evidence Refresh

- Report: `provider-handoff-refresh-v1`
- Status: `review`
- Generated At: `2026-06-01T01:10:40.141514+00:00`

## Refresh Steps

| Step | Category | Status | Output Paths | Recommended Action | Summary |
|---|---|---|---|---|---|
| `provider_integration_probe` | `integration` | `ready` | `docs\integration\provider-binding\provider-integration-probe.json`, `docs\integration\provider-binding\provider-integration-probe.md` | `no_action_required` | status=ready; bindable=True |
| `provider_contract_smoke` | `contract` | `ready` | `docs\smoke\provider-contract\provider-contract-smoke.json`, `docs\smoke\provider-contract\provider-contract-smoke.md` | `no_action_required` | status=ready; summary={"failed": 0, "passed": 9, "total": 9} |
| `deployment_readiness` | `operations` | `review` | `docs\operations\deployment-readiness\deployment-readiness.json`, `docs\operations\deployment-readiness\deployment-readiness.md` | `review_evidence_notes` | status=review; report_status=review |
| `reindex_readiness` | `operations` | `ready` | `docs\operations\reindex-readiness\reindex-readiness.json`, `docs\operations\reindex-readiness\reindex-readiness.md` | `no_action_required` | status=ready; report_status=ready |
| `source_binding_summary` | `source-binding` | `ready` | `docs\integration\source-bindings\provider-source-bindings.json`, `docs\integration\source-bindings\provider-source-bindings.md` | `no_action_required` | status=ready; report_status=ready |
| `phase3_fp_fn_review` | `retrieval-evidence` | `review` | `docs\benchmark\chinese-seed\fp-fn-review\phase3-fp-fn-review.json`, `docs\benchmark\chinese-seed\fp-fn-review\phase3-fp-fn-review.md` | `review_evidence_notes` | status=review |
| `phase3_retrieval_promotion_readiness` | `retrieval-evidence` | `review` | `docs\benchmark\chinese-seed\retrieval-promotion-readiness\phase3-retrieval-promotion-readiness.json`, `docs\benchmark\chinese-seed\retrieval-promotion-readiness\phase3-retrieval-promotion-readiness.md` | `review_evidence_notes` | status=review; summary={"blocked_gates": 0, "candidate_gates": 4, "open_gates": 7, "ready_gates": 0, "review_gates": 3, "supporting_evidence_ready": 2, "total_gates": 7} |
| `phase4_evidence_pack_readiness` | `evidence-packaging` | `ready` | `docs\benchmark\chinese-seed\evidence-pack-readiness\phase4-evidence-pack-readiness.json`, `docs\benchmark\chinese-seed\evidence-pack-readiness\phase4-evidence-pack-readiness.md` | `no_action_required` | status=ready; summary={"blocked_artifacts": 0, "evidence_pack_checks_passed": true, "ready_artifacts": 5, "required_artifacts": 2, "required_ready_artifacts": 2, "review_artifacts": 0, "smoke_passed": true, "total_artifacts": 5} |
| `phase4_caller_consumption_smoke` | `caller-consumption` | `ready` | `docs\smoke\evidence-pack-consumption\phase4-caller-consumption-smoke.json`, `docs\smoke\evidence-pack-consumption\phase4-caller-consumption-smoke.md` | `no_action_required` | status=ready; summary={"answerable_checks": 1, "contract_doc_present": 1, "failed": 0, "insufficient_checks": 1, "passed": 3, "total": 3} |
| `phase5_graph_use_case_readiness` | `graph-readiness` | `ready` | `docs\benchmark\chinese-seed\graph-use-case-readiness\phase5-graph-use-case-readiness.json`, `docs\benchmark\chinese-seed\graph-use-case-readiness\phase5-graph-use-case-readiness.md` | `no_action_required` | status=ready; summary={"blocked_artifacts": 0, "graph_ids": ["ecommerce_order_graph"], "graph_query_planned": true, "graph_query_status": "planned", "graph_schema_count": 1, "graph_stores": {"ecommerce_order_graph": "neo4j_planned"}, "preflight_graph_boundary_ready": true, "ready_artifacts": 3, "required_artifacts": 3, "required_ready_artifacts": 3, "review_artifacts": 0, "smoke_check_count": 9, "smoke_checks_passed": true, "smoke_graph_check_passed": true, "total_artifacts": 3} |
| `phase5_graph_boundary_smoke_summary` | `graph-boundary-smoke` | `ready` | `docs\smoke\graph-boundary-summary\phase5-graph-boundary-smoke-summary.json`, `docs\smoke\graph-boundary-summary\phase5-graph-boundary-smoke-summary.md` | `no_action_required` | status=ready; summary={"blocked_artifacts": 0, "entity_type_count": 4, "graph_checks_passed": 2, "graph_error_code": "GRAPH_NOT_IMPLEMENTED", "graph_ids": ["ecommerce_order_graph"], "graph_query_planned": true, "graph_query_status": "planned", "graph_schema_count": 1, "graph_status": "planned", "graph_store": "neo4j_planned", "ready_artifacts": 3, "relation_type_count": 3, "required_artifacts": 3, "required_ready_artifacts": 3, "review_artifacts": 0, "smoke_checks_passed": true, "smoke_checks_ready": 9, "smoke_checks_total": 9, "source_smoke_passed": true, "total_artifacts": 3} |
| `provider_handoff_bundle` | `handoff` | `review` | `docs\integration\provider-handoff\provider-handoff-bundle.json`, `docs\integration\provider-handoff\provider-handoff-bundle.md` | `review_evidence_notes` | status=review; report_status=review |

## Operation Notes

- This refresh workflow only regenerates local evidence files.
- External control planes still own provider registration, heartbeat governance, audit policy, source-to-agent binding decisions, and final answer policy.
- At least one refreshed report requires human review before promotion.
