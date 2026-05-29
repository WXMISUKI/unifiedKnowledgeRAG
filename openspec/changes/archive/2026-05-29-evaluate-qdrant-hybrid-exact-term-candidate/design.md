# Design: Qdrant Dense+Sparse Exact-Term Candidate

## Context

The previous dense-only smoke run showed that semantic vectors can miss exact identifiers even when the correct paragraph contains the queried string. Qdrant supports named dense and sparse vectors and Query API fusion, so the next smallest evidence slice is a local dense+sparse candidate.

## Approach

1. Keep the existing dense-only Qdrant path unchanged.
2. Add an evaluation-only hybrid collection preparation helper that creates:
   - `text-dense`: the existing dense BGE-M3 vector
   - `text-sparse`: a deterministic lexical sparse vector
3. Build lexical sparse vectors from exact-token features:
   - hyphenated identifiers such as `AF-REFUND-02`
   - alphanumeric segments such as `refund`, `02`, `ord`
   - normalized lowercase forms
4. Query Qdrant with two prefetches and Reciprocal Rank Fusion:
   - dense prefetch using BGE-M3
   - sparse prefetch using lexical sparse features
5. Export evidence as:
   - `qdrant-bge-m3-hybrid-exact-term-smoke.json`
   - `qdrant-bge-m3-hybrid-exact-term-smoke.md`

## Decision Boundary

If hybrid improves exact-term recall without creating expected-empty regressions in a follow-up stress run, it becomes a stronger candidate for production design. This change only proves the exact-term seed path. Runtime adoption still needs broader false-positive, threshold, chunking, and operational review.

## Risks

- The deterministic sparse vectorizer is intentionally simple and may overfit identifier-like local cases.
- Qdrant hybrid schema changes require reindexing, so production promotion must be a separate migration decision.
- Exact-term recall can improve while semantic precision or empty-query handling regresses; this change does not claim broad production readiness.
