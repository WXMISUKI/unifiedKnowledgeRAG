## Context

The current Qdrant query path maps every valid hit payload to `EvidenceDocument`, regardless of score. The application already has `Settings.rag_score_threshold`, and LlamaIndex uses it to filter retrieved nodes. Qdrant should use the same setting so retrieval behavior is consistent across backends.

The latest smoke evidence shows `hit_rate=0.8` but `empty_handling_rate=0.0`; each empty case returned some semantically nearby chunk. A threshold gate is not a final answer quality strategy, but it gives operators an explicit control and makes empty-result behavior measurable.

## Goals / Non-Goals

**Goals:**

- Filter Qdrant hits below `settings.rag_score_threshold`.
- Preserve valid payload mapping and malformed-hit skipping.
- Record `rag_score_threshold` in Qdrant smoke evidence.
- Re-export smoke evidence after the change.

**Non-Goals:**

- Do not choose a production threshold value.
- Do not add reranking, sparse vectors, ColBERT, hybrid search, or answer generation.
- Do not rewrite benchmark expected citations or chunking strategy.

## Decisions

1. Filter after Qdrant returns hits.

   This keeps the existing query API simple and works consistently for in-memory and remote Qdrant clients. Future work may push score threshold into Qdrant request parameters if useful, but post-filtering is adequate for the current contract.

2. Use the existing `RAG_SCORE_THRESHOLD` setting.

   The setting already exists and LlamaIndex honors it. Reusing it avoids another backend-specific knob and makes smoke runs easier to compare.

3. Record, not tune, the threshold in evidence.

   This change provides the mechanism and evidence metadata. Selecting a better threshold should happen from benchmark results, not hidden defaults.

## Risks / Trade-offs

- [Risk] A threshold that is too high can hide useful evidence. -> Mitigation: keep the default low and make the threshold visible in smoke evidence.
- [Risk] A threshold alone may not fix all empty cases. -> Mitigation: record the result and use misses to justify reranker or empty-intent detection later.
- [Risk] Qdrant score scales can vary by distance/model. -> Mitigation: treat threshold values as backend/model-specific evaluation data, not universal truth.
