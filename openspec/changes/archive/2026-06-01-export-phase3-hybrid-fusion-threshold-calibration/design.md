## Summary

Add one lightweight exporter that consolidates Phase 3 hybrid fusion and threshold evidence into a single local diagnostics artifact.

## Phase Alignment

- Roadmap phase: Phase 3 retrieval-quality promotion evidence review.
- Nature: evaluation-only evidence export.
- Non-goal: runtime promotion, threshold default change, retrieval backend switch, or API behavior change.

## Data Sources

- `docs/benchmark/chinese-seed/exact-term-candidates/qdrant-bge-m3-hybrid-exact-term-smoke.json`
- `docs/benchmark/chinese-seed/hybrid-empty-stress/qdrant-bge-m3-hybrid-empty-stress.json`
- `docs/benchmark/chinese-seed/hybrid-gating-candidates/qdrant-bge-m3-hybrid-exact-identifier-gate.json`
- `docs/benchmark/chinese-seed/hybrid-gating-candidates-expanded/qdrant-bge-m3-hybrid-exact-identifier-gate.json`
- `docs/benchmark/chinese-seed/noisy-identifier-gating-candidates/qdrant-bge-m3-hybrid-alias-identifier-gate.json`
- `docs/benchmark/chinese-seed/split-chunk-gating-candidates/qdrant-bge-m3-hybrid-exact-identifier-gate.json`
- `docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-threshold-recommendation.json`
- `docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-threshold-sweep.json`
- `docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json`
- `docs/operations/deployment-readiness/deployment-readiness.json`

## Export Output

- JSON: `docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/phase3-hybrid-fusion-threshold-calibration.json`
- Markdown: `docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/phase3-hybrid-fusion-threshold-calibration.md`

Core output sections:

- `summary`: total/ready/review/blocked signals.
- `calibration`: selected threshold, runtime threshold, threshold delta, fusion mode, score-filter mode.
- `signals`: compact readiness signals with recommended actions.
- `notes`: explicit statement that RRF fusion score semantics differ from dense-only threshold semantics.

## Handoff Integration

- Add optional handoff artifact id: `phase3_hybrid_fusion_threshold_calibration`.
- Add non-blocking refresh step before later Phase 3 smoke summary aggregation.

## Verification

- Focused pytest:
  - `tests/test_phase3_hybrid_fusion_threshold_calibration.py`
  - `tests/test_provider_handoff_bundle.py`
  - `tests/test_provider_handoff_refresh.py`
- `openspec validate export-phase3-hybrid-fusion-threshold-calibration --strict`
