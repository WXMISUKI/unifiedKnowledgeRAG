## Context

`evidence_pack-v1` gives callers a stable bundle of returned citations, scores, snippets, and request context. The provider also has source document manifests and backend-specific chunk metadata, but callers currently need to join several diagnostics to understand where a returned snippet came from. Adding provenance directly to pack entries improves answer grounding and retrieval debugging while staying inside the provider's evidence-packaging responsibility.

## Goals / Non-Goals

**Goals:**

- Add deterministic provenance metadata to every evidence pack entry when available.
- Preserve the existing top-level returned document shape.
- Keep provenance provider-owned and backend-neutral enough for fixture, LlamaIndex, and Qdrant.

**Non-Goals:**

- Change retrieval ranking or scoring.
- Add new chunking strategies, rerankers, parser dependencies, vector DB defaults, or GraphRAG execution.
- Make the provider responsible for final answer style or citation policy beyond returned evidence.

## Decisions

- Store provenance in `metadata.evidence_pack.evidence[].provenance`.
  - Rationale: The evidence pack is already the caller-facing trust bundle; adding provenance there avoids broad response model churn.
  - Alternative considered: Add top-level fields to `EvidenceDocument`; rejected because many callers use the simpler document envelope and the pack is the right place for trust metadata.

- Add internal `EvidenceDocument.metadata` that is excluded from public document serialization.
  - Rationale: Retrieval backends can pass provenance to the pack builder without changing the external document list.
  - Alternative considered: Recompute all provenance from citation strings; rejected because Qdrant already carries richer backend metadata.

- Use stable keys: `source_path`, `chunk_id`, `chunking_strategy`, and `citation_anchor`.
  - Rationale: These are useful across local fixtures, LlamaIndex, and Qdrant and map to existing source diagnostics.

## Risks / Trade-offs

- Some backends may not know every provenance field. Mitigation: include only known non-empty fields while keeping required citation/source/document fields unchanged.
- Pack id changes because the pack content is richer. Mitigation: pack ids are deterministic fingerprints of the current pack, not long-lived external identifiers.
