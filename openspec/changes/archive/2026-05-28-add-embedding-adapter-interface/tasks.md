## 1. Specification

- [x] 1.1 Add OpenSpec deltas for embedding adapter boundary
- [x] 1.2 Validate `add-embedding-adapter-interface` with OpenSpec strict mode

## 2. Configuration

- [x] 2.1 Add embedding provider settings
- [x] 2.2 Keep default embedding provider deterministic and local

## 3. Adapter Interface

- [x] 3.1 Add embedding adapter abstract interface
- [x] 3.2 Add deterministic mock embedding adapter
- [x] 3.3 Add hosted and local placeholders that fail closed
- [x] 3.4 Add adapter factory

## 4. Qdrant Helper Integration

- [x] 4.1 Add helper to embed evidence chunks before Qdrant upsert
- [x] 4.2 Preserve existing Qdrant payload metadata
- [x] 4.3 Keep text query retrieval orchestration out of scope

## 5. Verification

- [x] 5.1 Add tests for mock embedding determinism and vector size
- [x] 5.2 Add tests for hosted/local fail-closed placeholders
- [x] 5.3 Add tests for Qdrant chunk embedding helper
- [x] 5.4 Run `conda run -n GRAPHRAG python -m pytest -q`

## 6. Documentation

- [x] 6.1 Document embedding adapter boundary in README
- [x] 6.2 Update production indexing architecture with hosted/local embedding decision path
