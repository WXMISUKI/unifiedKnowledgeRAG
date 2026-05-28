## 1. Specification

- [x] 1.1 Add OpenSpec deltas for Qdrant source ingestion
- [x] 1.2 Validate `add-qdrant-source-ingestion-flow` with OpenSpec strict mode

## 2. Chunking and Source Loading

- [x] 2.1 Add local markdown source loading for Qdrant ingestion
- [x] 2.2 Add deterministic source-to-chunk conversion
- [x] 2.3 Preserve source/document/citation metadata

## 3. Qdrant Ingestion

- [x] 3.1 Embed chunks through the configured embedding adapter
- [x] 3.2 Ensure Qdrant collection before upsert
- [x] 3.3 Upsert chunks to Qdrant
- [x] 3.4 Write source index lifecycle ready status

## 4. Lifecycle Integration

- [x] 4.1 Add Qdrant branch to ingestion lifecycle build
- [x] 4.2 Keep fixture and LlamaIndex behavior unchanged
- [x] 4.3 Keep Qdrant opt-in

## 5. Verification

- [x] 5.1 Add tests for source chunking
- [x] 5.2 Add tests for Qdrant source ingestion helper
- [x] 5.3 Add tests for ingestion job completing Qdrant source
- [x] 5.4 Run `conda run -n GRAPHRAG python -m pytest -q`

## 6. Documentation

- [x] 6.1 Document Qdrant source ingestion flow in README
- [x] 6.2 Update production indexing architecture with chunking caveat
