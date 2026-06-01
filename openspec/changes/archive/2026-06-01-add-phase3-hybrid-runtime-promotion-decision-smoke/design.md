## Summary

Add a compact read-only smoke artifact that checks final hybrid runtime promotion decision evidence-chain completeness.

## Phase Alignment

- Roadmap phase: Phase 3 retrieval quality promotion review.
- Nature: local smoke evidence maintenance.
- Non-goal: promotion execution or runtime default switching.

## Smoke Inputs

- hybrid runtime promotion decision contract
- hybrid runtime promotion decision readiness export
- phase3 retrieval readiness/runtime diagnostics/latency diagnostics
- phase3 hybrid calibration and two phase3 smoke artifacts
- phase6 bridge readiness/smoke artifacts for BGE, Qdrant, and private-network review

## Smoke Checks

1. Contract document exists.
2. Required readiness artifacts exist and parse as valid JSON.
3. Readiness export still exposes explicit review gates and decision semantics.

## Output

- `docs/smoke/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-smoke.json`
- `docs/smoke/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-smoke.md`

## Handoff Integration

- Add optional handoff artifact id:
  - `phase3_hybrid_runtime_promotion_decision_smoke`
- Add non-blocking refresh step after hybrid runtime promotion decision readiness.

## Verification

- Focused pytest:
  - `tests/test_phase3_hybrid_runtime_promotion_decision_smoke.py`
  - `tests/test_provider_handoff_bundle.py`
  - `tests/test_provider_handoff_refresh.py`
- `openspec validate add-phase3-hybrid-runtime-promotion-decision-smoke --strict`
