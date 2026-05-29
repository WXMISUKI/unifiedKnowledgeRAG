# Design: Evaluate Hybrid Gating Candidate

## Context

Current evidence:

- Dense-only Qdrant+BGE-M3 exact-term smoke missed identifier-heavy cases.
- Dense+sparse hybrid recall passed the exact-term fixture.
- Hybrid empty-stress returned evidence for unsupported identifier-like queries.

## Candidate

`exact-identifier-containment-gate-v1` extracts identifier-like tokens such as `AF-REFUND-02`, `RFD-2026-003`, `LST-BATCH-OPS`, and `ORD-ZS-2026-0007` from the query. If identifiers are present, a retrieved evidence chunk is retained only when its snippet contains every query identifier exactly. If no identifiers are present, the candidate passes evidence through unchanged.

This is intentionally narrow. It protects exact identifier questions without making a broad semantic relevance claim.

## Evidence Shape

The report records:

- raw hybrid returned citations;
- gated returned citations;
- extracted query identifiers;
- aggregate benchmark metrics after gating;
- Qdrant, embedding, sparse vector, and fixture metadata.

## Promotion Boundary

Passing this local seed only proves the minimum false-positive control for the current fixture. Runtime adoption still requires broader customer-like cases, answer/evidence grading review, and a production decision for sparse vector generation or reranking.
