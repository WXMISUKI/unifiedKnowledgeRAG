## Summary

Add one lightweight exporter that consolidates the final hybrid runtime promotion decision prerequisites into a single local readiness artifact.

## Phase Alignment

- Roadmap phase: Phase 3 retrieval quality promotion review.
- Nature: evaluation-only evidence export.
- Non-goal: runtime promotion, retrieval backend switch, threshold default change, embedding default switch, or API behavior change.

## Inputs

- Contract:
  - `docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-contract.md`
- Phase 3 evidence:
  - `docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-readiness.json`
  - `docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json`
  - `docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json`
  - `docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/phase3-hybrid-fusion-threshold-calibration.json`
  - `docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.json`
  - `docs/smoke/aggregation-relation-negative-control/phase3-aggregation-relation-negative-control-smoke.json`
- Phase 6 bridge evidence:
  - `docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json`
  - `docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json`
  - `docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json`
  - `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json`
  - `docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json`
  - `docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.json`
  - `docs/smoke/private-network-promotion/phase6-qdrant-bge-private-network-promotion-smoke.json`
- Optional deployment evidence:
  - `docs/integration/deployed-provider-smoke/deployed-provider-smoke.json`

## Output

- JSON:
  - `docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-readiness.json`
- Markdown:
  - `docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-readiness.md`

Core sections:

- `summary`: total/required/ready/review/blocked/open gates.
- `signals`: per-artifact readiness signals with recommended actions.
- `review_state` and `decision`: bounded to `ready/review/blocked` and `keep_runtime_defaults` unless all required gates are ready.

## Handoff Integration

- Add optional handoff artifact id:
  - `phase3_hybrid_runtime_promotion_decision_readiness`
- Add non-blocking handoff refresh step before Phase 4 evidence-pack steps.

## Verification

- Focused pytest:
  - `tests/test_phase3_hybrid_runtime_promotion_decision_readiness.py`
  - `tests/test_provider_handoff_bundle.py`
  - `tests/test_provider_handoff_refresh.py`
- `openspec validate export-phase3-hybrid-runtime-promotion-decision-readiness --strict`
