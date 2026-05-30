## Context

The current retrieval-quality path has evidence for dense-only Qdrant+BGE-M3, dense+sparse hybrid recall, empty-stress false positives, exact identifier gating, noisy/alias-aware gating, alias governance, and split-chunk failure. The split-chunk evidence is important because it shows a different failure mode: relevant chunks are retrieved, but the strict gate rejects them because identifiers are distributed across chunks.

This change remains within the lightweight provider roadmap. It adds a local evaluation candidate so we can review evidence before any runtime promotion, rather than changing public retrieval behavior.

## Goals / Non-Goals

**Goals:**

- Evaluate whether grouping retrieved chunks by source/document can satisfy identifier coverage across multiple evidence chunks.
- Preserve raw hybrid citations and aggregated citations in the exported evidence so reviewers can see what was recovered and why.
- Keep the evaluation path runnable from the existing Qdrant+BGE smoke export script.
- Update specs and docs with the new evidence gate.

**Non-Goals:**

- Do not change `POST /api/rag/retrieve`, `POST /api/rag/answer`, provider capabilities, or default retrieval backend behavior.
- Do not promote hybrid retrieval, identifier gating, or multi-chunk aggregation to runtime defaults.
- Do not introduce reranker, parent document store, graph store, or production alias service dependencies.
- Do not claim production readiness from a single split-chunk fixture.

## Decisions

1. Use source/document-level grouping for the first aggregation candidate.

   The candidate groups raw hybrid hits by `(source_id, document_id)` and checks whether the union of identifiers across that group covers all query identifiers. This directly targets the current split-chunk miss while avoiding heavier parent/section indexing changes. A parent/section indexing candidate remains a later option if grouping evidence is too noisy.

2. Keep case scoring compatible with the existing benchmark report.

   Aggregated evidence is converted back into `RetrievalBenchmarkCaseResult` so hit rate, citation match rate, and empty handling rate remain comparable with earlier reports. Extra details live in the hybrid gating evidence case metadata: query identifiers, raw citations, aggregated citations, and whether aggregation was applied.

3. Add a dedicated CLI flag rather than overloading existing gating flags.

   A new flag makes the evidence mode explicit and keeps exact identifier gate and alias-aware gate reports stable for historical comparison.

4. Keep the implementation evaluation-only.

   This candidate is deliberately not connected to runtime retrieval backends. Promotion would require broader customer-like positives, expected-empty cases, noisy top-k cases, and a separate OpenSpec change.

## Risks / Trade-offs

- [Risk] Grouping chunks can recover split evidence but may over-broaden context when unrelated identifiers appear in the same document. → Mitigation: export raw and aggregated citations, keep the candidate offline, and require future expected-empty/noisy group fixtures before promotion.
- [Risk] A single split-chunk fixture can create false confidence. → Mitigation: document the evidence as local seed evidence only and retain runtime defaults.
- [Risk] Aggregation might hide citation granularity problems. → Mitigation: keep all returned citations visible and continue scoring against expected citation match.
