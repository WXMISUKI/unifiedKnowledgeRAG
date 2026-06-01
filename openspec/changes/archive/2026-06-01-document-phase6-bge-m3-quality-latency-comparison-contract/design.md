## Summary

Define a Phase 6/Phase 3 bridge contract that standardizes BGE-M3 candidate quality and latency comparison against the current mock/fixture baseline.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations, with explicit Phase 3 promotion bridge value.
- Nature: documentation-only evidence contract.
- Non-goal: runtime promotion, backend default switch, or model download automation.

## Decisions

- Keep comparison read-only and evidence-first.
  The contract explains required evidence and interpretation rules, not runtime behavior changes.

- Compare by reproducible evidence sources.
  Baseline and candidate metrics must come from named local artifacts with explicit timestamps and backend context.

- Treat missing candidate artifacts as `review`, not synthetic pass/fail.
  This preserves conservative gate semantics for promotion review.

## Contract Focus

- Comparison dimensions: hit rate, citation match rate, empty handling rate, FP/FN signals, average/median/p95 latency, artifact readiness, and deployment linkage.
- Environment posture: local-files-only, private-network copyability, and mock/fixture fallback visibility.
- Decision boundary: always `keep_runtime_defaults` unless separate promotion change closes all open gates.
