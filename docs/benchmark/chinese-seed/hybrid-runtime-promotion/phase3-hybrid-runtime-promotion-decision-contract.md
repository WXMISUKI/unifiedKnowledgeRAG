# Phase 3 Hybrid Runtime Promotion Decision Contract

## Status

- Phase: `Phase 3 Retrieval Quality Promotion`
- Slice: `document-phase3-hybrid-runtime-promotion-decision-contract`
- Type: `documentation-only`
- Decision Boundary: `review-only; no runtime default change`

## Purpose

This contract defines the evidence inputs and decision semantics for the final Phase 3 hybrid runtime promotion review. It prevents premature promotion from isolated candidate wins and keeps the provider boundary lightweight.

## Decision Model

- `review_state`
  - `ready`: all required evidence is present and locally consistent for promotion review
  - `review`: evidence exists but open gates require human review or deployment follow-up
  - `blocked`: required evidence is missing or invalid
- `decision`
  - `promote_to_candidate_default`: candidate-level promotion review can proceed in a separate approved change
  - `keep_runtime_defaults`: runtime defaults remain unchanged in this cycle
  - `blocked`: promotion review cannot proceed until required evidence is restored

## Required Evidence Inputs

1. `docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-readiness.json`
2. `docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json`
3. `docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json`
4. `docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/phase3-hybrid-fusion-threshold-calibration.json`
5. `docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.json`
6. `docs/smoke/aggregation-relation-negative-control/phase3-aggregation-relation-negative-control-smoke.json`

## Supporting Phase 6 Bridge Evidence

1. `docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json`
2. `docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json`
3. `docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json`
4. `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json`
5. `docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json`
6. `docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.json`
7. `docs/smoke/private-network-promotion/phase6-qdrant-bge-private-network-promotion-smoke.json`

## Open Gates That Must Stay Visible

- deployed provider smoke on real deployment URL
- deployment sign-off for runtime and operations posture
- customer-like production-corpus validation for false-positive and false-negative stability

If any required gate is open, the expected outcome is `decision=keep_runtime_defaults`.

## Non-Goals

- no runtime backend switch
- no threshold default change
- no embedding provider default change
- no API contract change
- no GraphRAG execution implementation
- no caller control-plane ownership change

## Operator Note

This contract only defines review semantics. Any real default-promotion action must happen in a separate change with explicit approval and dedicated verification.
