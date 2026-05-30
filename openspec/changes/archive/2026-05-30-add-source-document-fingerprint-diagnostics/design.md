## Context

`GET /api/rag/sources/{source_id}/documents` is the lightweight Phase 2 diagnostic surface for source documents, citation anchors, chunking metadata, and index readiness. It currently cannot tell a caller whether the checked-in source file has changed since the manifest metadata was authored.

## Approach

Add optional document fingerprint fields to `SourceDocumentManifest`:

- `source_file_status`: `present` or `missing`
- `content_sha256`: sha256 of the current local file bytes when present
- `expected_content_sha256`: provider-owned expected digest when available
- `content_byte_size`: current file byte size when present
- `drift_status`: `in_sync`, `changed`, `missing`, or `unchecked`

The provider-owned static manifest will record expected sha256 values for the current local fixture documents. At request time the service reads only the listed file path for each manifest entry, computes the current sha256, and derives drift status.

## Drift Rules

- Missing file -> `source_file_status=missing`, `drift_status=missing`.
- Expected hash present and current hash matches -> `drift_status=in_sync`.
- Expected hash present and current hash differs -> `drift_status=changed`.
- Expected hash absent and file present -> `drift_status=unchecked`.

## Read-Only Boundary

This does not run retrieval, answer composition, ingestion, embedding, Qdrant, or GraphRAG. It also does not scan unlisted directories. It reads only the provider-owned manifest paths and returns diagnostic metadata.

## Risks

- Static expected hashes must be updated when fixture files intentionally change. Mitigation: tests assert the current fixture digests so drift is visible immediately.
- The current path is local-file oriented. That is acceptable for the current markdown baseline; future object-store or database-backed sources can add their own fingerprint source.
