## Summary

Create a lightweight contract document that defines how final Phase 3 hybrid runtime promotion decisions must consume evidence and stay boundary-safe.

## Phase Alignment

- Roadmap phase: Phase 3 retrieval quality promotion review.
- Nature: documentation-only governance contract.
- Non-goal: runtime default switching, threshold default updates, retrieval backend promotion, embedding provider promotion, or GraphRAG execution enablement.

## Contract Content

- Decision scope and status model:
  - `review_state`: `ready` | `review` | `blocked`
  - `decision`: `promote_to_candidate_default` | `keep_runtime_defaults` | `blocked`
- Required evidence classes:
  - Phase 3 promotion readiness export
  - Phase 3 runtime diagnostics export
  - Phase 3 latency/resource diagnostics export
  - Phase 3 hybrid fusion/threshold calibration export
  - Phase 3 hybrid cross-case FP/FN smoke
  - Phase 3 aggregation/relation negative-control smoke
- Supporting Phase 6 bridge evidence:
  - BGE-M3 artifact readiness
  - BGE-M3 comparison diagnostics/smoke
  - Qdrant vector-store readiness
  - Qdrant backup/restore smoke
  - Qdrant+BGE private-network promotion readiness/smoke
- Open-gate expectations:
  - deployed URL smoke and deployment sign-off remain explicit production gates
  - candidate evidence remains non-promotion unless all required gates are closed

## Verification

- `openspec validate document-phase3-hybrid-runtime-promotion-decision-contract --strict`
