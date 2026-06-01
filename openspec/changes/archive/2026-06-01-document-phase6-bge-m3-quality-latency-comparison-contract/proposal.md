## Why

Phase 6 now has BGE-M3 artifact readiness and Qdrant operations readiness, but there is still no dedicated contract for comparing BGE-M3 candidate behavior against the current mock/fixture baseline. Without a stable comparison contract, Phase 3 promotion review remains hard to reproduce and easy to overfit.

## What Changes

- Add a local contract for BGE-M3 vs mock/fixture quality and latency comparison readiness.
- Define required evidence classes, comparison dimensions, and review-state interpretation.
- Keep this slice documentation-only and read-only.

## Capabilities

### New Capabilities

- `bge-m3-comparison-readiness`: contract for BGE-M3 candidate quality/latency comparison review before any runtime promotion.

### Modified Capabilities

- `provider-roadmap`: records BGE-M3 comparison contract as Phase 6/Phase 3 bridge evidence.
- `knowledge-provider`: records comparison-contract boundary as provider-owned read-only evidence guidance.

## Impact

- Affected docs: `docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-quality-latency-comparison-contract.md`.
- Affected specs: `provider-roadmap`, `knowledge-provider`.
- Runtime defaults, HTTP contracts, and control-plane ownership remain unchanged.
