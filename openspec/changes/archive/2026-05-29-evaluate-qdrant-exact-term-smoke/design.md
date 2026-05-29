# Design: Qdrant+BGE Exact-Term Smoke Evidence

## Context

The exact-term fixture intentionally asks about strings that dense retrieval can struggle with:

- `RFD-2026-003`
- `AF-REFUND-02`
- `LST-BATCH-OPS`
- `ORD-ZS-2026-0007`

These cases are the right first gate before discussing hybrid retrieval because they test whether current dense-only retrieval already handles the simplest identifier-heavy workload.

## Approach

1. Keep runtime behavior unchanged.
2. Update local Qdrant markdown citation anchors so inserted exact-term paragraphs preserve business citation IDs.
3. Reuse the existing Qdrant smoke ingestion/query flow with the exact-term fixture.
4. Add a semantic export helper and CLI switch that writes:
   - `qdrant-bge-m3-exact-term-smoke.json`
   - `qdrant-bge-m3-exact-term-smoke.md`
5. Record the actual dense-only result in docs and specs.

## Decision Boundary

If dense-only Qdrant+BGE hits all exact-term cases with citation matches, hybrid retrieval remains deferred until broader or harder evidence shows misses. If dense-only misses any exact-term case, the next change should compare dense-only against a sparse or hybrid candidate rather than manually tuning expected citations.

## Risks

- Small fixture evidence can overstate readiness. The exported report is seed evidence only.
- Paragraph-level anchors are adequate for local markdown fixtures but not a production parser decision.
- BGE-M3 dense vectors do not exercise the model's sparse or ColBERT capabilities in this change.
