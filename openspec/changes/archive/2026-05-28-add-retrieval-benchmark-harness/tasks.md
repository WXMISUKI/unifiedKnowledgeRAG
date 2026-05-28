## 1. Specification

- [x] 1.1 Validate `add-retrieval-benchmark-harness` with OpenSpec strict mode
- [x] 1.2 Keep benchmark harness local and dependency-free

## 2. Benchmark Data

- [x] 2.1 Add structured benchmark fixture cases
- [x] 2.2 Include positive citation cases
- [x] 2.3 Include empty retrieval case

## 3. Benchmark Service

- [x] 3.1 Add benchmark case/result models or dataclasses
- [x] 3.2 Load benchmark cases from JSON
- [x] 3.3 Run cases through `create_document_retriever(settings)`
- [x] 3.4 Compute `hit_at_k`, `citation_match`, empty handling, and latency
- [x] 3.5 Compute aggregate summary metrics

## 4. Verification

- [x] 4.1 Add tests for benchmark case loading
- [x] 4.2 Add tests for fixture backend benchmark success metrics
- [x] 4.3 Add tests for empty retrieval metric
- [x] 4.4 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 4.5 Run `openspec validate add-retrieval-benchmark-harness --strict`

## 5. Documentation

- [x] 5.1 Document benchmark workflow in README
- [x] 5.2 Link benchmark evidence from production indexing architecture doc
