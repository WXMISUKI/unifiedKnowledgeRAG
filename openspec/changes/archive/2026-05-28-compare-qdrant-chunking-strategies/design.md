## Context

The project currently has a runnable paragraph chunking baseline and a runnable section chunking candidate. The benchmark evidence still only runs Qdrant+BGE against the runtime paragraph path. A chunking switch can change both recall and citation precision, so comparison must be explicit.

## Goals / Non-Goals

**Goals:**
- Run Qdrant+BGE smoke evidence for selected chunking strategies.
- Export side-by-side summary metrics and embedded reports.
- Keep default Qdrant ingestion as `markdown-paragraph-v1`.
- Make citation precision loss visible if section-level citations do not match paragraph-level expected citations.

**Non-Goals:**
- Do not promote `markdown-section-v1` as default.
- Do not change benchmark expected citations to make section chunks look better.
- Do not add reranker, hybrid retrieval, or token-window chunking.
- Do not add a public HTTP API.

## Decisions

1. Add a `chunking_strategy` parameter to smoke indexing.

   The smoke helper can choose paragraph or section chunks while the runtime ingestion path remains unchanged.

2. Use current benchmark expectations unchanged.

   If section chunks return section-level citations instead of paragraph citations, citation match should drop. That is valuable evidence, not a test failure.

3. Export comparison under chunking candidates.

   Files live under `docs/benchmark/chinese-seed/chunking-candidates/` because this is chunking strategy evidence rather than a new retrieval backend.

## Risks / Trade-offs

- [Risk] Section chunking may score well on hit rate but poorly on citation match.
  -> Mitigation: preserve both metrics and document that precision matters before promotion.

- [Risk] Running multiple Qdrant+BGE smoke paths repeats embedding work.
  -> Mitigation: comparison remains a local evidence command, not a runtime path.
