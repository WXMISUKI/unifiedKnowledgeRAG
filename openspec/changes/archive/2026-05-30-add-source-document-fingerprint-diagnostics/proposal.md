## Why

The source document manifest is useful for binding and citation diagnostics, but it currently lists static provider-owned metadata only. In enterprise document RAG, source files can change independently from manifest metadata and persisted index state. Callers and operators need a lightweight way to see whether a source document exists and whether its current bytes match the manifest's expected fingerprint before trusting citations or deciding to reindex.

This change advances roadmap Phase 2 by adding read-only source document fingerprint diagnostics. It avoids heavier document parsing, indexing, vector-store calls, and production dependency decisions.

## What Changes

- Add optional fingerprint diagnostics to each source document manifest entry.
- Include source file presence, byte size, sha256 digest, expected sha256 when known, and drift status.
- Mark default local fixture documents as in sync using expected hashes.
- Keep the manifest endpoint read-only and side-effect free.

## Impact

- Affected specs:
  - `document-rag`: source document manifests include content fingerprint diagnostics.
  - `provider-roadmap`: Phase 2 document ingestion evidence includes lightweight drift diagnostics.
- Affected code:
  - Source document manifest service and response model.
- Affected tests/docs:
  - Contract tests and README/roadmap guidance.

## Non-Goals

- No OCR, PDF/Word parsing, table extraction, or directory crawling.
- No ingestion job creation, reindex execution, embedding, vector database query, or GraphRAG execution.
- No runtime change to retrieval, answer composition, Qdrant ingestion defaults, or chunking strategy promotion.
