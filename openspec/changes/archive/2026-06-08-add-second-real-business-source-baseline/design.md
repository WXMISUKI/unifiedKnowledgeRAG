## Context

The provider already has a reusable local business golden-case baseline and an aggregate wrapper, but the checked-in aggregate evidence still carries only `company_profile_2025_trial`. That means the project has format support for multi-source evidence, but not yet a second real source in the actual baseline. The repository already includes lightweight business documents such as `refund_policy_docs.md`, which makes it possible to expand the baseline without adding new ingestion infrastructure or turning this change into a strategy-upgrade loop.

## Goals / Non-Goals

**Goals:**

- Append one second real business source to the aggregate baseline.
- Reuse the existing aggregate exporter and per-source baseline logic.
- Keep the checked-in report deterministic and easy to rerun locally.
- Make the next-stage recommendation depend on observed aggregate outcome rather than on technique popularity.

**Non-Goals:**

- No query rewrite, HyDE, HyPE, rerank, hybrid retrieval, RAPTOR, Self/Corrective RAG, or GraphRAG execution work.
- No Qdrant, pgvector, BGE-M3, or embedding/runtime promotion.
- No source-to-agent binding, caller orchestration, or MyPrivateAgent integration changes.
- No parser engine ownership, OCR expansion, or public HTTP API changes.

## Decisions

1. **Use `refund_policy_docs` as the second real source.**
   - Rationale: The source already exists in the repository as a lightweight business document with clear positive and negative control question candidates, so it can expand real-input coverage without requiring new ingestion work.
   - Alternative considered: Introduce a new external document now. That would add source-preparation work and slow down this evidence slice.

2. **Refresh the checked-in aggregate fixture and report instead of building a new exporter path.**
   - Rationale: The service and exporter already support multi-source aggregation. This slice should prove real-input expansion, not create more framework.
   - Alternative considered: Add a second command or a second output family. That would duplicate maintenance for little value.

3. **Treat the second source as evidence-only even if it passes cleanly.**
   - Rationale: A clean two-source `go` result means we still need more real inputs before promoting advanced retrieval techniques. It is a signal to keep expanding real evidence, not to optimize locally.
   - Alternative considered: Trigger chunking or retrieval strategy work immediately after a second `go`. That would still be premature because no accepted failure mode would exist.

## Risks / Trade-offs

- **Risk: The second source is smaller and easier than the company-profile corpus.** -> Mitigation: Keep the recommendation conservative and treat this slice as breadth expansion, not as proof that strategy upgrades are unnecessary forever.
- **Risk: The second source may not be visible through the current provider source catalog.** -> Mitigation: Verify real export behavior and fail closed with focused tests if source readiness is missing.
- **Risk: The aggregate report could still remain `go`, leaving no immediate technical optimization task.** -> Mitigation: Preserve the roadmap rule that the next slice is more real inputs or real failed questions, not forced strategy work.
