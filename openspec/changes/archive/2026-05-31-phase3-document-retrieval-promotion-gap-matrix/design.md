## Context

Phase 3 promotion work is evidence-gated. The repository already has dense-only, hybrid, gating, aggregation, relation-aware grading, and FP/FN review artifacts, but they are spread across multiple files and are easy to review in isolation while still missing the bigger decision picture.

The gap matrix is intended to be the single read-only view that answers:

- What candidate families exist?
- What evidence do we already have?
- Which promotion gates are still open?
- What should the next Phase 3 slice target?

## Goals / Non-Goals

**Goals:**

- Create one review artifact that consolidates the current Phase 3 promotion picture.
- Keep the artifact local, deterministic, and easy to refresh later.
- Make the missing evidence explicit so later export work can reuse the same structure.

**Non-Goals:**

- Changing runtime retrieval defaults.
- Adding new retrieval behavior, rerankers, GraphRAG execution, or deployment automation.
- Automatically approving Qdrant, BGE-M3, hybrid retrieval, aggregation, or relation-aware grading for production use.

## Decisions

- Use a simple gate matrix with one row per candidate family.
  This keeps the report readable and makes future export automation straightforward.

- Anchor each row to existing evidence artifacts.
  The matrix should point at the benchmark and review outputs already present in `docs/benchmark/chinese-seed/`.

- Keep the matrix read-only.
  It should be a review artifact, not a promotion mechanism.

## Risks / Trade-offs

- The matrix may drift if benchmark artifacts change and the summary is not refreshed.
  Mitigation: the second Phase 3 slice will introduce an export workflow for the same structure.

- A compact matrix can hide nuance if it is too terse.
  Mitigation: include direct evidence paths and explicit open-gate notes rather than only aggregate scores.
