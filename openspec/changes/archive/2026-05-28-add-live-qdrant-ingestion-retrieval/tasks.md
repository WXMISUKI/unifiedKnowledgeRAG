## 1. Specification

- [x] 1.1 Add OpenSpec deltas for live Qdrant ingestion and retrieval helpers
- [x] 1.2 Validate `add-live-qdrant-ingestion-retrieval` with OpenSpec strict mode

## 2. Dependency and Client

- [x] 2.1 Add `qdrant-client` dependency
- [x] 2.2 Add lazy Qdrant client construction
- [x] 2.3 Add collection readiness helper

## 3. Ingestion Helper

- [x] 3.1 Add Qdrant point upsert helper
- [x] 3.2 Preserve existing evidence payload contract during upsert
- [x] 3.3 Keep upsert callable with fake clients in tests

## 4. Retrieval Helper

- [x] 4.1 Add vector query helper with source and tenant filtering
- [x] 4.2 Map Qdrant hits to `EvidenceDocument`
- [x] 4.3 Skip malformed hits without breaking the whole result
- [x] 4.4 Keep text embedding out of scope

## 5. Verification

- [x] 5.1 Add tests for collection readiness
- [x] 5.2 Add tests for upsert calls
- [x] 5.3 Add tests for query filter and result mapping
- [x] 5.4 Run `conda run -n GRAPHRAG python -m pytest -q`

## 6. Documentation

- [x] 6.1 Document Qdrant live adapter usage in README
- [x] 6.2 Update production indexing architecture with embedding boundary
