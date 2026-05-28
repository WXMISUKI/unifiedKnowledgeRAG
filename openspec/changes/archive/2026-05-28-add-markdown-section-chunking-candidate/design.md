## Context

The current Qdrant ingestion baseline uses `markdown-paragraph-v1`: each paragraph becomes one evidence chunk. The candidate report now lists `markdown-section-v1` as planned, but it is not runnable. A section-aware candidate should group content under markdown headings so we can inspect chunk counts and citation stability before deciding whether it deserves retrieval benchmark promotion.

## Goals / Non-Goals

**Goals:**
- Add section-aware markdown chunk generation as an evaluation-only helper.
- Mark `markdown-section-v1` as runnable in chunking candidate evidence.
- Preserve citation and metadata contracts for generated chunks.
- Keep Qdrant source ingestion unchanged.

**Non-Goals:**
- Do not replace `load_qdrant_source_chunks` or `QDRANT_CHUNKING_STRATEGY`.
- Do not add PDF/Word parsing or tokenizer dependencies.
- Do not claim retrieval metrics for section-aware chunking yet.
- Do not change score threshold recommendation.

## Decisions

1. Implement section chunking as a separate helper.

   `markdown_source_to_section_chunks(...)` will produce `VectorEvidenceChunk` objects with strategy metadata `markdown-section-v1`. Existing ingestion continues calling `markdown_source_to_qdrant_chunks(...)`.

2. Use heading-derived section boundaries.

   A new chunk starts at a markdown heading. Paragraphs after that heading are grouped into the same section until the next heading. If a document only has one heading, the candidate produces one section-level chunk.

3. Reuse stable local source citations where possible.

   For local fixture sources, section chunks use deterministic section candidate citations. This is evidence metadata for evaluation, not the final enterprise citation model.

## Risks / Trade-offs

- [Risk] Current local sources have shallow heading structure, so section chunks may be too broad.
  -> Mitigation: report chunk counts and caveats; do not promote section chunking without retrieval benchmark evidence.

- [Risk] Section-level citation can be less precise than paragraph citation.
  -> Mitigation: keep paragraph baseline as runtime default and mark section candidate evidence separately.
