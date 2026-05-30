## Why

`evidence_pack-v1` is now present on retrieve and answer envelopes, but the exported provider contract smoke only proves the answerable path. For external callers, the safer integration guarantee is that insufficient evidence is also machine-readable and fail-closed.

## What Changes

- Extend provider contract smoke with an insufficient-evidence RAG check.
- Verify empty retrieve and answer envelopes expose `evidence_pack.status=insufficient_evidence`, `reason=no_documents`, empty allowed citations, and zero evidence count.
- Export the updated smoke evidence to JSON and Markdown.
- Keep runtime retrieval, answer composition, hybrid retrieval, reranking, and GraphRAG defaults unchanged.

## Capabilities

### New Capabilities

### Modified Capabilities
- `knowledge-provider`: Provider contract smoke evidence covers fail-closed insufficient-evidence behavior for RAG evidence packs.
- `document-rag`: RAG evidence pack requirements are backed by executable smoke evidence for both answerable and insufficient-evidence paths.

## Impact

- Affected code: provider contract smoke service and tests.
- Affected docs/evidence: README and `docs/smoke/provider-contract/*`.
- API compatibility: no response schema or runtime behavior change beyond smoke coverage.
- Dependencies: none.
