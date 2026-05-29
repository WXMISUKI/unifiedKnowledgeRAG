# Design: Hybrid Empty Stress Evidence

## Context

Hybrid exact-term evidence shows strong recall on identifier-heavy cases. The remaining risk is over-retrieval: unsupported questions can share lexical identifiers with known source chunks, causing sparse retrieval to return evidence where the correct behavior is no evidence.

## Approach

1. Keep the main retrieval seed and exact-term fixture unchanged.
2. Add `tests/fixtures/hybrid_empty_stress_cases.json` for unsupported cases that overlap with known lexical identifiers.
3. Reuse the Qdrant hybrid smoke path, but export with stable empty-stress filenames:
   - `qdrant-bge-m3-hybrid-empty-stress.json`
   - `qdrant-bge-m3-hybrid-empty-stress.md`
4. Preserve misses honestly: expected-empty cases should report `empty_query_handling=false` if hybrid returns evidence.

## Candidate Cases

The fixture should include unsupported questions such as:

- A fake refund form `AF-REFUND-99`.
- A fake policy code `RFD-2026-999`.
- A fake logistics workflow `LST-BATCH-BILLING`.
- A fake order-like id `ORD-ZS-2026-9999`.

These intentionally share lexical structure with known source evidence without being supported by the local documents.

## Decision Boundary

If hybrid empty-stress fails, the next step is not runtime promotion. We should evaluate a hybrid threshold/gating strategy, sparse weighting, lexical allowlists, or evidence grading before any runtime switch.

If it passes, hybrid still needs broader expected-empty and customer-specific evidence before production promotion.
