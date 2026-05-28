## 1. Qdrant Threshold Filtering

- [x] 1.1 Apply `settings.rag_score_threshold` when mapping Qdrant hits to evidence documents.
- [x] 1.2 Preserve malformed-hit skipping and valid-hit mapping behavior.

## 2. Smoke Evidence And Docs

- [x] 2.1 Include `rag_score_threshold` in Qdrant smoke evidence metadata.
- [x] 2.2 Add focused tests for Qdrant threshold filtering and smoke metadata.
- [x] 2.3 Update README guidance for tuning score threshold.
- [x] 2.4 Run OpenSpec, pytest, and Qdrant+BGE smoke verification, then archive the change.
