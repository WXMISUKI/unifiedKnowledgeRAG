## Context

The Qdrant + BGE-M3 smoke path now runs local source ingestion, vector retrieval, and benchmark evidence export against Chinese seed cases. After aligning local markdown citations, aggregate hit rate and citation match rate are high, while one expected-empty case still returns evidence at `RAG_SCORE_THRESHOLD=0.5`.

Threshold choice affects precision and recall. Raising it may improve empty handling, but can also suppress valid positive evidence. The provider needs a repeatable way to compare thresholds before changing defaults or adding heavier retrieval stages.

## Goals / Non-Goals

**Goals:**
- Run Qdrant+BGE smoke evidence across multiple score thresholds using one command.
- Export durable JSON and Markdown evidence that compares summary metrics per threshold.
- Preserve existing single-threshold smoke export behavior.
- Keep the feature local and review-oriented.

**Non-Goals:**
- Do not change the default `RAG_SCORE_THRESHOLD`.
- Do not add reranker, hybrid retrieval, sparse vectors, or empty-intent classification.
- Do not expose a new HTTP API.
- Do not introduce a new dependency.

## Decisions

1. Add threshold sweep as a benchmark evidence helper, not retrieval behavior.

   The sweep belongs next to `export_qdrant_bge_smoke_evidence` because it evaluates the same local smoke path. This keeps production retrieval untouched while producing decision evidence.

2. Reuse the existing smoke helper per threshold.

   Each threshold run gets a settings copy with a different `rag_score_threshold`. This is simpler than threading thresholds through lower-level Qdrant functions and avoids changing retrieval contracts.

3. Export stable filenames.

   The sweep writes `qdrant-bge-m3-threshold-sweep.json` and `.md` in the selected output directory. Per-threshold reports are embedded in those files rather than writing many separate candidate files.

4. Keep CLI behavior backward compatible.

   `--rag-score-threshold` keeps exporting the existing single report. A new repeatable `--threshold-sweep` option triggers sweep export instead.

## Risks / Trade-offs

- [Risk] Running several thresholds repeats source ingestion and embedding work, which is slower with local BGE-M3.
  -> Mitigation: keep threshold values explicit and small; this is an operator-triggered evidence command, not a runtime path.

- [Risk] Threshold tuning overfits the seed fixture corpus.
  -> Mitigation: report is framed as seed evidence only and documentation directs future decisions to add customer-specific cases.

- [Risk] A sweep can show trade-offs but not explain why a case failed.
  -> Mitigation: include case-level misses in each embedded report so follow-up changes can target empty-intent detection, chunking, reranker, or hybrid retrieval.
