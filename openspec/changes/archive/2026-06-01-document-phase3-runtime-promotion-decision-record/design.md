## Summary

Create a lightweight decision record that closes the Phase 3 review loop for this iteration.

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
  - promotion readiness
  - runtime diagnostics
  - latency/resource diagnostics
  - hybrid fusion/threshold calibration
  - hybrid cross-case FP/FN smoke
  - aggregation/relation negative-control smoke
  - deployment readiness
- Open gates and required next evidence.
- Final verdict: keep runtime defaults; no production promotion in this slice.

## Verification

- `openspec validate document-phase3-runtime-promotion-decision-record --strict`
