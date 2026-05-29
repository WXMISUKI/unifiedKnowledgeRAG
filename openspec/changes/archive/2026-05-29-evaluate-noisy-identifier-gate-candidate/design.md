# Design: Evaluate Noisy Identifier Gate Candidate

## Context

`exact-identifier-containment-gate-v1` compares extracted identifier sets. This is safer than substring containment, but it cannot recover aliases or OCR-like variants such as `2O26` vs `2026` unless the query identifier is normalized before gating.

## Candidate

`alias-aware-identifier-gate-v1` is evaluation-only. It:

1. Extracts identifier-like tokens from query and evidence snippets.
2. Canonicalizes identifier segments where a segment contains digits, replacing common OCR `o/O` with `0`.
3. Adds a small local alias map for current fixture shorthand, such as `AF退款02` to `af-refund-02` and `LST批量OPS` to `lst-batch-ops`.
4. Retains a document only when every canonical query identifier is present in the canonical evidence identifiers.
5. Passes documents through unchanged when no clean or alias identifier is found.

## Evidence

The evidence report should retain raw citations, gated citations, and extracted/canonical query identifiers so false positives and false negatives remain auditable.

## Boundary

This local alias map is not a production alias service. Production adoption still needs corpus-driven alias governance, auditability, and review for false positives caused by over-aggressive normalization.
