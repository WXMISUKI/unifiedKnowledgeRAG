## Why

Phase 3 and Phase 6 now provide multiple candidate-level retrieval artifacts, but hybrid runtime promotion still lacks a dedicated decision contract that defines required evidence inputs, review states, and boundary-safe non-goals. Without this contract, promotion discussion can drift from evidence review into premature runtime default changes.

## What Changes

- Add a Phase 3 hybrid runtime promotion decision contract under `docs/benchmark/chinese-seed/hybrid-runtime-promotion/`.
- Define required and optional evidence inputs, review-state semantics, and explicit non-goals for hybrid runtime promotion review.
- Keep this slice documentation-only; do not change runtime defaults, retrieval backend selection, or API behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records a dedicated contract for final Phase 3 hybrid runtime promotion review.
- `retrieval-benchmark-harness`: documents the required evidence contract for hybrid runtime promotion decisions.

## Impact

- Affected docs: one new contract markdown plus tracker refresh.
- No runtime, deployment, or API behavior impact.
