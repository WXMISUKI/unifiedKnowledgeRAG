## Summary

Create a lightweight decision record that closes the current Phase 3 hybrid runtime promotion review loop.

## Phase Alignment

- Roadmap phase: Phase 3 retrieval promotion review.
- Nature: documentation-only governance artifact.
- Non-goal: runtime default change, retrieval backend change, embedding provider promotion, or GraphRAG execution enablement.

## Decision Record Content

- Decision metadata: date, scope, owner, status.
- Current runtime defaults snapshot:
  - retrieval backend `fixture`
  - embedding provider `mock`
  - runtime threshold `0.01`
- Evidence references:
  - hybrid runtime promotion decision readiness
  - hybrid runtime promotion decision smoke
  - phase3 retrieval readiness/runtime diagnostics/latency diagnostics/hybrid calibration
  - phase3 hybrid cross-case FP/FN smoke
  - phase3 aggregation/relation negative-control smoke
  - phase6 bridge readiness/smoke artifacts
- Open gates and required next evidence.
- Final verdict: keep runtime defaults; no production promotion in this slice.

## Verification

- `openspec validate document-phase3-hybrid-runtime-promotion-decision-record --strict`
