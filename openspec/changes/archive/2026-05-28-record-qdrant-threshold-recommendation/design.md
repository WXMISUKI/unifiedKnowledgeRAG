## Context

Threshold sweep evidence compares multiple Qdrant+BGE-M3 `RAG_SCORE_THRESHOLD` values. The current expanded Chinese seed set shows `0.7` satisfying all tracked metrics while lower thresholds fail expected-empty cases.

Changing the global default now would be premature because this is still a local seed benchmark. A safer step is to turn the sweep output into an explicit recommendation artifact that carries gates, selected threshold, and caveats.

## Goals / Non-Goals

**Goals:**
- Select a recommended local threshold from an existing sweep report using explicit gates.
- Export JSON and Markdown recommendation evidence.
- Keep recommendation generation local and review-oriented.
- Preserve the existing runtime default and environment override behavior.

**Non-Goals:**
- Do not change `Settings.rag_score_threshold` default.
- Do not add dynamic thresholding, reranking, or empty-intent classification.
- Do not expose a new HTTP API.
- Do not claim production approval from seed evidence.

## Decisions

1. Recommendation consumes sweep JSON rather than rerunning Qdrant.

   The sweep report is already the durable evidence. Reading it avoids repeated embedding work and keeps recommendation generation deterministic.

2. Select the lowest passing threshold.

   If multiple thresholds satisfy the gates, the helper chooses the lowest threshold to avoid unnecessarily suppressing valid recall while still meeting precision/empty-handling gates.

3. Use explicit gates.

   Gates default to `1.0` for hit rate, citation match rate, and empty handling rate for the local seed recommendation, but CLI options can relax them for experiments.

## Risks / Trade-offs

- [Risk] A perfect local seed recommendation may be mistaken for production readiness.
  -> Mitigation: the exported recommendation includes a non-production approval status and caveats.

- [Risk] Lowest passing threshold may still be too high for future real documents.
  -> Mitigation: recommendation is regenerated from fresh sweep evidence as the benchmark grows.
