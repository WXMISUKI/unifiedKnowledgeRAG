## Summary

Implement a read-only diagnostics export that compares BGE-M3 candidate evidence against the mock/fixture baseline and links that comparison to Phase 6 artifact/deployment posture.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations, bridging to Phase 3 promotion review.
- Nature: local evidence visibility export.
- Non-goal: promotion decision or runtime default switch.

## Data Inputs

- `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json`
- `docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json`
- `docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json`
- `docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json`
- `docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json`
- `docs/operations/deployment-readiness/deployment-readiness.json`

## Output

- `docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json`
- `docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.md`

## Status Semantics

- `blocked`: critical artifacts missing.
- `review`: artifacts present but promotion gates open (expected in current local stage).
- `ready`: all comparison and deployment-linkage signals closed.
