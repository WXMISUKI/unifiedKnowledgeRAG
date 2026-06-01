# Provider Improvement Tracker

## Scope

- Project: `unifiedKnowledgeRAG`
- Roadmap: `docs/roadmap/lightweight_provider_roadmap.md`
- Mode: lightweight, agile, evidence-driven
- Rhythm: specification -> implementation -> archive

## Completed

- Phase 0 baseline contracts: health, manifest, capabilities, preflight, integration probe, contract smoke.
- Phase 2 diagnostics baseline: source manifest, fingerprint drift, ingestion preflight, chunk manifest, source package metadata.
- Phase 4 evidence packaging baseline: `evidence_pack-v1` and insufficient-evidence fail-closed behavior.
- Phase 4 evidence pack consumption contract documented (`2026-05-31-phase4-document-evidence-pack-consumption-contract`), translating `evidence_pack-v1` into caller-facing allowlist and fail-closed consumption rules.
- Phase 4 evidence pack readiness export implemented and refreshed (`2026-05-31-phase4-export-evidence-pack-readiness`), consolidating the consumption contract, provider contract smoke, and supporting evidence into a machine-readable review artifact.
- Phase 4 caller-consumption smoke implemented and refreshed (`2026-05-31-phase4-add-caller-consumption-smoke`), directly exercising `build_evidence_pack` for answerable and fail-closed caller branches.
- Phase 5 graph use-case readiness contract documented (`2026-05-31-phase5-document-graph-use-case-readiness-contract`), separating graph-worthy relationship-heavy questions from document-RAG-only questions.
- Phase 5 graph use-case readiness export implemented and refreshed (`2026-05-31-phase5-export-graph-use-case-readiness`), consolidating the graph contract, provider preflight graph boundary, and provider contract smoke into a machine-readable review artifact.
- Phase 5 graph boundary smoke summary implemented and refreshed (`2026-06-01-add-phase5-graph-boundary-smoke-summary`), condensing the graph schema discovery and planned graph query checks into a compact smoke artifact.
- Phase 5 boundary-only graph evidence: graph schema discovery in preflight/contract smoke; graph query remains planned boundary.
- Phase 6 operations baseline: deployment readiness, reindex readiness, handoff bundle, handoff refresh, handoff API.
- Phase 6 optional live-url evidence: deployed provider smoke and source-binding checks.
- Phase 6 deployed field validation contract documented (`document-phase6-deployed-field-validation-contract`), defining how a real deployed URL is interpreted as live field validation evidence without changing runtime defaults.
- Phase 6 deployed field validation readiness export implemented and refreshed (`export-phase6-deployed-field-validation-readiness`), summarizing deployment readiness, handoff bundle posture, and live URL smoke evidence as optional review input.
- Phase 6 deployed handoff consistency smoke implemented and refreshed (`add-phase6-deployed-handoff-consistency-smoke`), validating local consistency between deployed field-validation readiness and provider handoff bundle without live network calls.
- Phase 6 deployed field validation decision record documented (`document-phase6-deployed-field-validation-decision-record`), freezing the current live-url verdict and next-step gates in a documentation-only record.
- Phase 2 parser expansion demand contract documented (`document-phase2-parser-expansion-demand-contract`), defining evidence-gated non-Markdown parser expansion criteria while preserving Markdown as the lightweight baseline.
- Phase 2 source-format demand readiness export implemented and refreshed (`2026-06-01-export-phase2-source-format-demand-readiness`), summarizing markdown baseline posture, unsupported/non-markdown demand signals, and open expansion gates as a machine-readable local review artifact.
- Phase 2 unsupported-format negative-control smoke implemented and refreshed (`2026-06-01-add-phase2-unsupported-format-negative-control-smoke`), validating markdown positive controls and unsupported/non-markdown negative controls in a compact read-only smoke artifact.
- Phase 2 parser expansion decision record documented (`document-phase2-parser-expansion-decision-record`), explicitly recording this cycle's `keep_markdown_baseline` verdict and future parser-expansion gates.
- Phase 7 provider handoff acceptance contract documented (`document-phase7-provider-handoff-acceptance-contract`), defining required handoff evidence, optional review evidence, and cross-phase acceptance semantics without runtime promotion.
- Phase 7 provider release readiness export implemented and refreshed (`2026-06-01-export-phase7-provider-release-readiness`), summarizing required handoff gates and cross-phase review posture in one machine-readable local artifact.
- Phase 7 cross-phase handoff consistency smoke implemented and refreshed (`2026-06-01-add-phase7-cross-phase-handoff-consistency-smoke`), validating alignment across key phase decision/readiness/smoke evidence in a compact read-only artifact.
- Phase 7 provider release decision record documented (`document-phase7-provider-release-decision-record`), explicitly recording this cycle's `ready_for_local_provider_handoff_but_not_runtime_promotion` verdict.
- Phase 8 live URL validation execution contract documented (`document-phase8-live-url-validation-execution-contract`), defining deployed live validation inputs, endpoint scope, and status semantics without runtime promotion.
- Phase 8 live URL validation readiness export implemented and refreshed (`export-phase8-live-url-validation-readiness`), summarizing contract/Phase6/Phase7/deployed-smoke posture in one machine-readable local review artifact.
- Phase 8 live URL smoke consistency check implemented and refreshed (`add-phase8-live-url-smoke-consistency-check`), validating readiness-vs-handoff summary alignment in a compact read-only artifact.
- Phase 8 live URL validation decision record documented (`document-phase8-live-url-validation-decision-record`), explicitly freezing this cycle's `keep_runtime_defaults_until_live_url_validation` verdict and open gates.
- Source binding compact summary and aggregate count reuse in handoff/deployed-smoke evidence.
- Phase 3 customer-like benchmark expansion completed (`2026-05-31-expand-phase3-customer-like-benchmark-cases`) as a historical milestone; that slice first expanded baseline fixture to 24 cases before later extensions moved the canonical baseline to 26 cases.
- Phase 3 promotion customer-like benchmark expansion completed (`2026-05-31-phase3-expand-promotion-customer-like-cases`), extending the canonical baseline fixture to 29 cases and exposing a second expected-empty false-positive trap for promotion review.
- Phase 3 promotion customer-like gate cases v2 completed (`2026-06-01-expand-phase3-promotion-customer-like-gate-cases-v2`), extending the canonical baseline fixture to 32 cases and adding a third expected-empty false-positive trap for promotion review.
- Phase 3 handoff evidence summary completed and archived (`2026-05-31-add-phase3-evidence-summary-to-handoff`), adding optional baseline metric rollup to provider handoff bundle.
- Phase 3 false-positive/false-negative customer-like extension completed and archived (`2026-05-31-expand-phase3-fp-fn-customer-like-cases`), with baseline fixture expanded to 26 cases and one expected-empty false-positive risk explicitly exposed.
- Phase 3 FP/FN review export completed and archived (`2026-05-31-add-phase3-fp-fn-review-export`), adding a read-only summary artifact over benchmark evidence (`false_positive_count=2`, `false_negative_count=0`).
- Phase 3 FP/FN review integrated into handoff/refresh and archived (`2026-05-31-add-phase3-fp-fn-review-into-handoff-refresh`), with optional handoff summary row and non-blocking refresh step.
- Phase 3 retrieval promotion gap matrix documented (`2026-05-31-document-phase3-retrieval-promotion-gap-matrix`), summarizing current Qdrant/BGE-M3/hybrid/aggregation/relation-aware/deployed-smoke promotion gaps in one read-only review artifact.
- Phase 3 retrieval promotion readiness export implemented and refreshed (`2026-05-31-phase3-retrieval-promotion-readiness-export`), surfacing the gap matrix as machine-readable evidence and adding optional handoff/refresh visibility.
- Phase 3 retrieval candidate evaluation protocol documented (`2026-06-01-document-phase3-retrieval-candidate-evaluation-protocol`), standardizing gate expectations and required evidence classes across Qdrant/BGE-M3/hybrid/aggregation/relation-aware/deployed-smoke review.
- Phase 3 candidate runtime diagnostics export implemented and refreshed (`2026-06-01-export-phase3-candidate-runtime-diagnostics`), summarizing runtime-adjacent promotion prerequisites and adding optional handoff/refresh visibility.
- Phase 3 candidate latency/resource diagnostics export implemented and refreshed (`2026-06-01-export-phase3-candidate-latency-resource-diagnostics`), combining benchmark latency shape with deployment/runtime posture into optional handoff/refresh evidence.
- Phase 3 hybrid fusion/threshold calibration export implemented and refreshed (`2026-06-01-export-phase3-hybrid-fusion-threshold-calibration`), consolidating hybrid RRF context, dense-threshold recommendation context, FP/FN signal, and runtime threshold posture into one optional review artifact.
- Phase 3 hybrid runtime promotion decision contract documented (`document-phase3-hybrid-runtime-promotion-decision-contract`), defining required Phase 3 + Phase 6 bridge evidence inputs, decision-state semantics, and non-goal boundaries before any runtime default switch.
- Phase 3 runtime promotion decision record documented (`2026-06-01-document-phase3-runtime-promotion-decision-record`), explicitly recording this cycle's `keep_runtime_defaults` verdict and the remaining promotion gates.
- Phase 3 hybrid cross-case FP/FN smoke implemented and refreshed (`2026-06-01-add-phase3-hybrid-cross-case-fp-fn-smoke`), validating risk-case coverage, false-positive trap alignment, and positive-control stability from local evidence.
- Phase 3 aggregation/relation negative-control smoke implemented and refreshed (`2026-06-01-add-phase3-aggregation-relation-negative-control-smoke`), keeping the over-broad aggregation risk and relation-aware unsupported-case signal visible in one compact local review artifact.
- Phase 3 hybrid runtime promotion decision readiness export implemented and refreshed (`export-phase3-hybrid-runtime-promotion-decision-readiness`), consolidating Phase 3 and Phase 6 bridge prerequisites into one machine-readable final promotion review artifact.
- Phase 3 hybrid runtime promotion decision smoke implemented and refreshed (`add-phase3-hybrid-runtime-promotion-decision-smoke`), validating final promotion-review evidence-chain completeness in a compact local smoke artifact.
- Phase 3 hybrid runtime promotion decision record documented (`document-phase3-hybrid-runtime-promotion-decision-record`), explicitly recording this cycle's `keep_runtime_defaults` verdict and remaining promotion gates.
- Deployment readiness operator guide added for Phase 6 operations documentation, translating `review` evidence into operator steps without changing runtime behavior.
- Deployment readiness configuration reference added for Phase 6 operations documentation, mapping env vars, mounts, and evidence commands to the current deploy-prep state.
- Deployment readiness runbook added for Phase 6 operations documentation, sequencing review, configuration, refresh, and optional live smoke into a single operator flow.
- Phase 6 BGE-M3 artifact readiness bridge implemented and refreshed (`phase6-bge-m3-artifact-readiness`), adding checksum-aware manifest coverage and a local artifact readiness export for deployment and promotion review.
- Phase 6 BGE-M3 quality/latency comparison contract documented (`document-phase6-bge-m3-quality-latency-comparison-contract`), defining read-only comparison gates between BGE-M3 candidate evidence and mock/fixture baseline before promotion review.
- Phase 6 BGE-M3 vs mock/fixture diagnostics export implemented and refreshed (`export-phase6-bge-m3-vs-mock-fixture-diagnostics`), consolidating baseline/candidate deltas and deployment-linkage posture into a machine-readable bridge artifact.
- Phase 6 BGE-M3 comparison smoke implemented and refreshed (`add-phase6-bge-m3-comparison-smoke`), validating bridge evidence-chain completeness in a compact read-only smoke artifact.
- Phase 6 Qdrant+BGE-M3 private-network promotion review contract documented (`document-phase6-qdrant-bge-private-network-promotion-review-contract`), defining required review inputs and boundary-safe review states before candidate promotion.
- Phase 6 Qdrant+BGE-M3 private-network promotion readiness export implemented and refreshed (`export-phase6-qdrant-bge-private-network-promotion-readiness`), consolidating Qdrant/BGE/Phase3/deployment inputs into one machine-readable review artifact.
- Phase 6 Qdrant+BGE private-network promotion smoke implemented and refreshed (`add-phase6-qdrant-bge-private-network-promotion-smoke`), validating contract/readiness/prerequisite evidence-chain completeness in a compact read-only smoke artifact.
- Phase 6 Qdrant+BGE private-network promotion decision record documented (`document-phase6-qdrant-bge-private-network-promotion-decision-record`), explicitly recording current `keep_runtime_defaults` verdict and open gates.
- Phase 6 Qdrant deployment/backup/recovery contract documented (`document-phase6-qdrant-deployment-backup-recovery-contract`), defining operator-facing evidence gates before any Qdrant runtime promotion review.
- Phase 6 Qdrant vector-store readiness export implemented and refreshed (`export-phase6-qdrant-vector-store-readiness`), consolidating deployment/reindex/contract/candidate evidence into a machine-readable review artifact with optional handoff visibility.
- Phase 6 Qdrant backup/restore smoke implemented and refreshed (`add-phase6-qdrant-backup-restore-smoke`), validating prerequisite evidence coverage in a compact read-only smoke artifact.

## In Progress

- Keep local evidence artifacts aligned with current code/spec state after each accepted slice.
- Evidence refresh stage is now operationalized and should be maintained through:
  `python scripts/export_provider_handoff_refresh.py`

## Benchmark Fixture Scope

- Baseline retrieval fixture `tests/fixtures/retrieval_benchmark_cases.json` is expanded to 32 cases.
- Customer-like additions in this round:
  - one nuanced high-value refund review case (`policy-nuance`)
  - one logistics identifier case (`identifier-noise`)
  - one cross-domain expected-empty trap case (`empty`)
- Current empty-case count in baseline fixture: 12.

## Phase 3 Evidence Refresh

- Refresh changes:
  - `refresh-phase3-seed-evidence-after-fixture-expansion`
  - `2026-05-31-expand-phase3-fp-fn-customer-like-cases` follow-up refresh
  - `2026-05-31-phase3-expand-promotion-customer-like-cases` follow-up refresh
  - `2026-06-01-add-phase5-graph-boundary-smoke-summary` follow-up refresh
  - `2026-06-01-expand-phase3-promotion-customer-like-gate-cases-v2` follow-up refresh
- Refreshed artifact:
  - `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json`
  - `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.md`
  - `docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json`
  - `docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase3_fp_fn_review` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase3_fp_fn_review` step)
- Phase 5 graph boundary refresh additions:
  - `docs/smoke/graph-boundary-summary/phase5-graph-boundary-smoke-summary.json`
  - `docs/smoke/graph-boundary-summary/phase5-graph-boundary-smoke-summary.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase5_graph_boundary_smoke_summary` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase5_graph_boundary_smoke_summary` step)
- Phase 3 runtime diagnostics refresh additions:
  - `docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json`
  - `docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase3_candidate_runtime_diagnostics` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase3_candidate_runtime_diagnostics` step)
- Phase 3 latency/resource diagnostics refresh additions:
  - `docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json`
  - `docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase3_candidate_latency_resource_diagnostics` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase3_candidate_latency_resource_diagnostics` step)
- Phase 3 hybrid fusion calibration refresh additions:
  - `docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/phase3-hybrid-fusion-threshold-calibration.json`
  - `docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/phase3-hybrid-fusion-threshold-calibration.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase3_hybrid_fusion_threshold_calibration` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase3_hybrid_fusion_threshold_calibration` step)
- Phase 3 hybrid cross-case smoke refresh additions:
  - `docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.json`
  - `docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase3_hybrid_cross_case_fp_fn_smoke` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase3_hybrid_cross_case_fp_fn_smoke` step)
- Phase 3 aggregation/relation negative-control smoke refresh additions:
  - `docs/smoke/aggregation-relation-negative-control/phase3-aggregation-relation-negative-control-smoke.json`
  - `docs/smoke/aggregation-relation-negative-control/phase3-aggregation-relation-negative-control-smoke.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase3_aggregation_relation_negative_control_smoke` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase3_aggregation_relation_negative_control_smoke` step)
- Phase 3 hybrid runtime promotion decision readiness refresh additions:
  - `docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-readiness.json`
  - `docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-readiness.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase3_hybrid_runtime_promotion_decision_readiness` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase3_hybrid_runtime_promotion_decision_readiness` step)
- Phase 3 hybrid runtime promotion decision smoke refresh additions:
  - `docs/smoke/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-smoke.json`
  - `docs/smoke/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-smoke.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase3_hybrid_runtime_promotion_decision_smoke` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase3_hybrid_runtime_promotion_decision_smoke` step)
- Phase 6 BGE-M3 artifact readiness refresh additions:
  - `docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json`
  - `docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase6_bge_m3_artifact_readiness` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase6_bge_m3_artifact_readiness` step)
- Phase 6 BGE-M3 comparison diagnostics refresh additions:
  - `docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json`
  - `docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase6_bge_m3_vs_mock_fixture_diagnostics` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase6_bge_m3_vs_mock_fixture_diagnostics` step)
- Phase 6 BGE-M3 comparison smoke refresh additions:
  - `docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json`
  - `docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase6_bge_m3_comparison_smoke` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase6_bge_m3_comparison_smoke` step)
- Phase 6 Qdrant vector-store readiness refresh additions:
  - `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json`
  - `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase6_qdrant_vector_store_readiness` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase6_qdrant_vector_store_readiness` step)
- Phase 6 Qdrant backup/restore smoke refresh additions:
  - `docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json`
  - `docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase6_qdrant_backup_restore_smoke` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase6_qdrant_backup_restore_smoke` step)
- Phase 6 private-network promotion readiness refresh additions:
  - `docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.json`
  - `docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase6_qdrant_bge_private_network_promotion_readiness` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase6_qdrant_bge_private_network_promotion_readiness` step)
- Phase 6 private-network promotion smoke refresh additions:
  - `docs/smoke/private-network-promotion/phase6-qdrant-bge-private-network-promotion-smoke.json`
  - `docs/smoke/private-network-promotion/phase6-qdrant-bge-private-network-promotion-smoke.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase6_qdrant_bge_private_network_promotion_smoke` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase6_qdrant_bge_private_network_promotion_smoke` step)
- Phase 2 source-format demand readiness refresh additions:
  - `docs/operations/source-format-demand/phase2-source-format-demand-readiness.json`
  - `docs/operations/source-format-demand/phase2-source-format-demand-readiness.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase2_source_format_demand_readiness` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase2_source_format_demand_readiness` step)
- Phase 2 unsupported-format negative-control smoke refresh additions:
  - `docs/smoke/source-format-demand/phase2-unsupported-format-negative-control-smoke.json`
  - `docs/smoke/source-format-demand/phase2-unsupported-format-negative-control-smoke.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase2_unsupported_format_negative_control_smoke` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase2_unsupported_format_negative_control_smoke` step)
- Phase 7 provider release-readiness refresh additions:
  - `docs/operations/provider-release-readiness/phase7-provider-release-readiness.json`
  - `docs/operations/provider-release-readiness/phase7-provider-release-readiness.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase7_provider_release_readiness` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase7_provider_release_readiness` step)
- Phase 7 cross-phase handoff consistency smoke refresh additions:
  - `docs/smoke/cross-phase-handoff/phase7-cross-phase-handoff-consistency-smoke.json`
  - `docs/smoke/cross-phase-handoff/phase7-cross-phase-handoff-consistency-smoke.md`
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (includes optional `phase7_cross_phase_handoff_consistency_smoke` summary row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.json` (includes non-blocking `phase7_cross_phase_handoff_consistency_smoke` step)
- Refreshed baseline summary:
  - `total_cases=32`
  - `hit_rate=0.9062`
  - `citation_match_rate=0.9062`
  - `empty_handling_rate=0.7500`
  - `empty.total_cases=12`
  - `policy-nuance.total_cases=4`
  - `identifier-noise.total_cases=2`
- Maintenance rule:
  - Treat the above artifacts as current only after rerunning:
    `python scripts/export_provider_handoff_refresh.py`

## Pending

- Keep deployment readiness review notes actionable until non-mock embedding/retrieval candidates are promoted by evidence.
- Continue Phase 3 retrieval-quality promotion only with customer-like benchmark evidence; do not promote defaults by single-metric wins.
- Keep GraphRAG execution deferred until relationship-heavy use cases and operations ownership are explicitly approved.
- Keep parser expansion (PDF/Word/Excel/OCR) deferred until real corpus demand and separate evidence-backed changes.
- Continue next smallest Phase 3 slice on evaluation-only gating candidates with cross-case coverage, and avoid single-case overfitting.

## Next Step Plan

1. Keep Phase 3 protocol, runtime diagnostics, and cross-case smoke aligned with refreshed benchmark evidence.
2. Keep all Phase 3 candidate work evaluation-only and preserve runtime defaults.
3. Export refreshed evidence before comparing any new gate signal.
4. Promote nothing by default unless gate evidence clearly passes.

## Latest Refresh

- Run time: `2026-06-01T03:16:25.552258+00:00`
- Command: `python scripts/export_provider_handoff_refresh.py`
- Refresh status: `review`
- Step summary:
  - `provider_integration_probe`: `ready`
  - `provider_contract_smoke`: `ready` (`9/9` checks)
  - `deployment_readiness`: `review`
  - `reindex_readiness`: `ready`
  - `source_binding_summary`: `ready`
  - `phase3_fp_fn_review`: `review`
  - `phase3_retrieval_promotion_readiness`: `review`
  - `phase3_candidate_runtime_diagnostics`: `review`
  - `phase3_candidate_latency_resource_diagnostics`: `review`
  - `phase3_hybrid_cross_case_fp_fn_smoke`: `ready`
  - `phase3_aggregation_relation_negative_control_smoke`: `ready`
  - `phase4_evidence_pack_readiness`: `ready`
  - `phase4_caller_consumption_smoke`: `ready`
  - `phase5_graph_use_case_readiness`: `ready`
  - `phase5_graph_boundary_smoke_summary`: `ready`
  - `provider_handoff_bundle`: `review`

## Current Gaps To Close

- Deployment readiness remains `review` because embedding is still `mock`, retrieval backend is still `fixture`, model artifacts are not configured, and provider API key is not configured.
- The new deployment readiness operator guide documents the current `review` state and the required pre-deployment actions; it does not change the underlying readiness state.
- The deployment readiness config reference documents the current runtime surface and deployment modes; it does not change the underlying readiness state.
- The deployment readiness runbook sequences the operator guide, config reference, refresh commands, and optional deployed smoke into a single deployment-prep flow.
- Handoff bundle remains `review` because deployment readiness is `review` and optional deployed smoke evidence is not present for a live URL.
- Phase 3 candidate latency/resource diagnostics is `review` by design because it is a local evidence-only export that still depends on deployment/runtime posture and deployed smoke context.
- Phase 3 aggregation/relation negative-control smoke is `ready` because the positive split-chunk control, the same-document negative control, and the relation-aware unsupported-case label all match current local evidence.
- Runtime promotion gates remain open for Phase 3 and GraphRAG execution; current evidence is candidate-level, not production approval.
