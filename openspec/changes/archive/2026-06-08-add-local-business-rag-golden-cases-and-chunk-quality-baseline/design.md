## Context

The provider can already register a local company-profile corpus, ingest parser-derived markdown, and return cited answers with insufficient-evidence negative controls. The remaining gap is repeatability: the successful trial needs to become a stable local quality baseline that future RAG improvements can compare against.

This design follows `docs/roadmap/rag_techniques_experience_application.md`: use real golden cases and chunk-quality diagnostics before adopting query rewrite, rerank, hybrid retrieval, RAPTOR, Self/Corrective RAG, or GraphRAG.

## Goals / Non-Goals

**Goals:**

- Create a small reusable golden-case fixture for `company_profile_2025_trial`.
- Export a JSON and Markdown report under `docs/local-run/business-rag-golden-cases/`.
- Evaluate both answerable and expected-empty cases through the existing provider-local retrieval/answer contracts.
- Report chunk-quality diagnostics from existing source/chunk artifacts.
- Produce a `go`, `review`, or `blocked` decision that can guide the next RAG maturity slice.

**Non-Goals:**

- No public HTTP API changes.
- No runtime retrieval default changes.
- No Qdrant, pgvector, BGE-M3, hybrid retrieval, rerank, GraphRAG, RAPTOR, or query-rewrite promotion.
- No source-to-agent binding or MyPrivateAgent orchestration.
- No parser engine adoption inside this provider.

## Decisions

1. **Use a checked-in local golden-case fixture.**
   - Rationale: Golden questions should be reviewable and stable across future candidate comparisons.
   - Alternative considered: generate cases dynamically from previous reports. That is harder to review and can hide test drift.

2. **Run in-process provider logic instead of requiring a live HTTP server.**
   - Rationale: Existing local evidence exporters are lightweight and can run without deployment setup.
   - Alternative considered: live HTTP smoke. That is already covered elsewhere and would make this quality baseline depend on service startup.

3. **Classify report decisions conservatively.**
   - `blocked` means required local source/chunk artifacts are missing or invalid.
   - `review` means the report ran but answerable cases miss evidence, expected-empty cases return citations, or chunk-quality thresholds need attention.
   - `go` means golden cases and chunk-quality diagnostics pass the current lightweight thresholds.

4. **Keep chunk diagnostics descriptive, not prescriptive.**
   - Rationale: The baseline should expose tiny/noisy chunks and citation coverage, but it should not change chunking defaults by itself.
   - Alternative considered: automatically merge or rewrite chunks. That would skip the evidence gate and risk changing citation behavior without review.

## Risks / Trade-offs

- **Risk: The first fixture is too small.** -> Mitigation: Treat it as the first reusable baseline and keep future real documents as additive fixtures.
- **Risk: Heuristic chunk-quality thresholds are imperfect.** -> Mitigation: Report raw counts, ratios, and samples so reviewers can override the simple decision when needed.
- **Risk: The fixture encourages overfitting to one company-profile document.** -> Mitigation: Document that passing this baseline is not production approval and does not promote retrieval backends.
- **Risk: Generated Markdown evidence can become stale.** -> Mitigation: Keep a single exporter command and update progress notes when evidence is refreshed.
