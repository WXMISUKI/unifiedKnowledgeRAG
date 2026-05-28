## 1. Specification

- [x] 1.1 Add OpenSpec deltas for Qdrant text query orchestration
- [x] 1.2 Validate `add-qdrant-text-query-orchestration` with OpenSpec strict mode

## 2. Orchestration Helper

- [x] 2.1 Add Qdrant text query helper that embeds query text
- [x] 2.2 Reuse existing Qdrant source and tenant filters
- [x] 2.3 Preserve `EvidenceDocument` mapping behavior

## 3. Retriever Integration

- [x] 3.1 Wire `QdrantDocumentRetriever.retrieve` to the orchestration helper
- [x] 3.2 Compose Qdrant and embedding readiness
- [x] 3.3 Keep Qdrant opt-in and default backend unchanged

## 4. Verification

- [x] 4.1 Add tests for text query helper
- [x] 4.2 Add tests for Qdrant retriever integration
- [x] 4.3 Add tests for degraded embedding readiness
- [x] 4.4 Run `conda run -n GRAPHRAG python -m pytest -q`

## 5. Documentation

- [x] 5.1 Document Qdrant text query orchestration in README
- [x] 5.2 Update production indexing architecture with remaining production gaps
