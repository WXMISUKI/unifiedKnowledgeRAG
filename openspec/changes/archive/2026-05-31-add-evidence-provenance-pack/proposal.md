## Why

The provider already returns evidence packs, but each pack entry only carries the snippet, score, and citation. Callers need lightweight provenance such as source path, chunk id, chunking strategy, and citation anchor to judge evidence quality and debug retrieval without relying on another diagnostic endpoint.

## What Changes

- Add provider-owned provenance metadata to evidence pack entries.
- Populate provenance from fixture, LlamaIndex, and Qdrant retrieval paths where the backend already knows it.
- Keep the public `documents` response shape stable; provenance is added to `metadata.evidence_pack.evidence`.
- Document that this is evidence packaging work, not a reranker, parser overhaul, vector DB promotion, or GraphRAG feature.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Add provenance metadata to RAG evidence packs.
- `provider-roadmap`: Record evidence provenance as Phase 4 evidence packaging work.

## Impact

- Affected response metadata: `POST /api/rag/retrieve` and `POST /api/rag/answer` evidence packs
- Affected code: evidence pack builder and retrieval backend document metadata population
- Affected tests/docs/specs: evidence pack, provider contract, README, roadmap, OpenSpec specs
- No new dependencies, parser expansion, reranker, production vector DB default, GraphRAG execution, or caller final-answer policy changes
