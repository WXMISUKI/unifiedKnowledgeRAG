# Design: Expand Hybrid Gating Benchmark

## Context

The previous `exact-identifier-containment-gate-v1` proved that full query identifiers can block unsupported token-overlap false positives while preserving the original exact-term cases. The remaining weakness is substring containment: a partial identifier like `AF-REFUND` could match a longer evidence identifier like `AF-REFUND-02`.

## Approach

The gate should:

1. Extract identifier-like tokens from the query.
2. Extract identifier-like tokens from each evidence snippet.
3. Retain a document only when every query identifier is present as an exact extracted evidence identifier.
4. Pass through documents unchanged when the query contains no identifiers.

The expanded fixtures should include:

- supported multi-identifier cases where all query identifiers are present in one evidence chunk;
- unsupported partial identifier cases;
- unsupported same-prefix but different-suffix cases.

## Evidence

The existing hybrid gating export helper can evaluate any positive fixture plus any expected-empty fixture. This change will add expanded fixtures and export a separate report under `docs/benchmark/chinese-seed/hybrid-gating-candidates-expanded/`.

## Boundary

This is still local seed evidence. Passing it does not approve runtime hybrid gating because real enterprise corpora may contain aliases, split identifiers across chunks, OCR mistakes, or operator shorthand that require separate policy.
