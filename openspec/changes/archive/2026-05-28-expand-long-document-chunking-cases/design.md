## Context

Current Qdrant source ingestion uses `markdown-paragraph-v1`: each markdown paragraph becomes one evidence chunk. This is a useful baseline, but enterprise documents often contain long procedural sections where the relevant answer is a smaller detail within a dense paragraph.

The next safe step is not to replace chunking yet. Instead, add long-section benchmark cases so threshold and chunking decisions are tested against a more realistic shape.

## Goals / Non-Goals

**Goals:**
- Add long-section positive retrieval cases to the Chinese seed benchmark.
- Keep fixture and Qdrant citations aligned for new paragraphs.
- Regenerate evidence and recommendation files.
- Document whether the current `0.7` local recommendation survives the expanded cases.

**Non-Goals:**
- Do not implement token-aware chunking, overlap, summaries, reranker, or hybrid retrieval.
- Do not change runtime default `RAG_SCORE_THRESHOLD`.
- Do not add PDF/Word parsing.
- Do not add customer private data.

## Decisions

1. Add new paragraphs to existing source fixtures.

   This keeps the corpus small and deterministic while representing longer enterprise sections. It also lets both fixture and Qdrant paths use the same source ids.

2. Use explicit business citation anchors for new paragraphs.

   Qdrant paragraph indexes must map to stable citations; otherwise citation failures would reflect mapping gaps instead of retrieval quality.

3. Add benchmark category `long-section`.

   A separate category makes it visible if longer chunks become the weak area in future reports.

## Risks / Trade-offs

- [Risk] Long paragraphs in markdown are still simpler than real PDFs or Word documents.
  -> Mitigation: treat this as a seed stress test before adding real document parsing.

- [Risk] Dense retrieval may pass the seed but still fail when sections are much larger.
  -> Mitigation: document remaining risk and use this evidence to justify the next chunking change if misses appear.
