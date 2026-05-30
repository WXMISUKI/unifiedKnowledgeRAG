## 1. Contract And Manifest Service

- [x] 1.1 Add source document manifest response models.
- [x] 1.2 Add provider-owned static manifests for current local RAG sources.
- [x] 1.3 Add read-only manifest lookup with structured unknown-source errors and index readiness metadata.

## 2. API And Documentation

- [x] 2.1 Expose `GET /api/rag/sources/{source_id}/documents`.
- [x] 2.2 Document the manifest endpoint and its diagnostic-only behavior in README.

## 3. Verification

- [x] 3.1 Add contract tests for successful manifest, unknown source, and no retriever construction.
- [x] 3.2 Run focused tests, full pytest, and strict OpenSpec validation.
