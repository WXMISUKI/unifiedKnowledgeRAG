## Why

Phase 3 has many candidate-level retrieval artifacts, but promotion decisions are still spread across multiple benchmark and handoff files. Reviewers can see that Qdrant, BGE-M3, hybrid retrieval, hybrid gating, aggregation, and relation-aware grading remain non-default, yet there is no single protocol that defines how to evaluate these candidates consistently before any runtime promotion discussion.

## What Changes

- Add a local Phase 3 retrieval candidate evaluation protocol document under `docs/benchmark/chinese-seed/`.
- Define stable evaluation gates for Qdrant, BGE-M3, hybrid retrieval, hybrid gating, aggregation, relation-aware grading, and deployed smoke follow-up.
- Clarify required evidence classes: customer-like benchmark coverage, FP/FN review, latency and deployment diagnostics, and deployment-site smoke evidence.
- Keep the protocol read-only and review-oriented; do not change runtime defaults, API contracts, or candidate promotion decisions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records the protocol as lightweight Phase 3 evidence-governance work.
- `retrieval-benchmark-harness`: treats the protocol as a local review contract for candidate evaluation gates.

## Impact

- Affected docs: new protocol document plus roadmap/tracker references.
- Affected code/runtime: none.
- Affected APIs: none.
- Runtime defaults remain unchanged (`fixture` retrieval and non-promoted candidates stay as-is).
