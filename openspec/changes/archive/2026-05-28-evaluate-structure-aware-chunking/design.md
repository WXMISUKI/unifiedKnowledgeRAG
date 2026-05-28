## Context

The current Qdrant ingestion baseline chunks markdown by paragraph. That is simple and stable, but it does not represent the full production choice space for PDFs, Word documents, long sections, section summaries, or token-window overlap.

This change adds evaluation evidence only. It should help decide whether the next implementation should keep paragraph chunking, add section-aware chunking, or introduce token windows with overlap.

## Goals / Non-Goals

**Goals:**
- Represent chunking strategy candidates in a local evidence report.
- Compare basic source-derived metrics such as chunk count and citation stability.
- Explicitly flag which strategies are implemented vs pending.
- Keep the runtime Qdrant ingestion path unchanged.

**Non-Goals:**
- Do not switch `QDRANT_CHUNKING_STRATEGY`.
- Do not implement a final token-aware chunker.
- Do not add document parsing dependencies.
- Do not reindex production data.

## Decisions

1. Start with metadata-level evaluation.

   Only `markdown-paragraph-v1` is implemented. The evaluation report can still compare expected trade-offs for planned strategies, but it must mark them as `planned` rather than pretending they are runnable.

2. Export evidence under the existing Chinese seed benchmark directory.

   Chunking decisions are tied to retrieval quality, so the output belongs next to the existing retrieval candidate evidence.

3. Keep strategy ids stable.

   Candidate ids such as `markdown-section-v1` and `token-window-v1` should be reusable in future changes when they become real implementation options.

## Risks / Trade-offs

- [Risk] Metadata-level evaluation is not enough to prove retrieval quality.
  -> Mitigation: mark unimplemented candidates as `planned`; future changes must add runnable candidate evidence before promotion.

- [Risk] Users may confuse candidate evidence with runtime behavior.
  -> Mitigation: README and report status explicitly state that runtime ingestion remains `markdown-paragraph-v1`.
