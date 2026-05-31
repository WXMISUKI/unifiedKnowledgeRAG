## 1. Source Package And Chunk Models

- [x] 1.1 Add response models for source package metadata and chunk manifest entries.
- [x] 1.2 Add provider-owned source package metadata for existing RAG sources.
- [x] 1.3 Add deterministic markdown chunk manifest generation shared by diagnostics.

## 2. Diagnostic Surfaces

- [x] 2.1 Include source package metadata on source document manifest responses.
- [x] 2.2 Include source package metadata on ingestion preflight responses.
- [x] 2.3 Include chunk manifest entries on source document manifest and ingestion preflight documents.

## 3. Documentation And Specs

- [x] 3.1 Update README and lightweight roadmap for source package and chunk manifest diagnostics.
- [x] 3.2 Sync main OpenSpec specs for document-rag and provider-roadmap.

## 4. Verification And Archive

- [x] 4.1 Add focused tests for source package metadata, chunk manifests, unsupported formats, and read-only behavior.
- [x] 4.2 Run focused tests, full pytest, and strict OpenSpec validation.
- [x] 4.3 Archive the completed change and re-run strict spec validation.
