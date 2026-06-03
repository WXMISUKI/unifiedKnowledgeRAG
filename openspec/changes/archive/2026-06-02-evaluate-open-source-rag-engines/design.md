## Design Overview

This change records a strategic provider-first selection path: keep `unifiedKnowledgeRAG` as a lightweight knowledge provider contract layer, and evaluate mature open-source RAG engines as replaceable backend candidates behind that contract.

The key architecture decision is that MyPrivateAgent and other callers integrate against the provider contract, not against a specific RAG framework. This keeps short-term delivery practical while avoiding long-term lock-in.

## Strategic Position

### Short Term: MyPrivateAgent Local RAG Consumption

Goal: make local MyPrivateAgent consumption smooth and predictable.

Preferred direction:

- keep the current LlamaIndex-backed baseline and existing provider APIs;
- keep mock/fixture retrieval available as a deterministic local baseline;
- use existing Phase 4 evidence pack, Phase 9/10/11 local-consumption evidence, and Phase 6 readiness artifacts as the integration backbone;
- treat Qdrant, BGE-M3, hybrid retrieval, and pgvector as gated candidate work;
- avoid heavy parser/platform expansion unless real customer corpus needs it.

Short-term exit criteria:

- MyPrivateAgent can discover provider health, manifest, preflight, capabilities, handoff, source-binding preview, and RAG retrieve evidence locally.
- Local access-key assumptions are documented and smokeable.
- Retrieval output remains citation-bearing and fail-closed through `evidence_pack-v1`.
- Runtime defaults remain unchanged unless a separate promotion change closes the gates.

### Mid Term: Optional Backend Spikes

Goal: compare mature projects without letting them reshape the provider scope prematurely.

Candidate backend spikes:

- Haystack pipeline spike for modular RAG pipeline comparison.
- RAGFlow external/backend spike for deep document parsing and platform reference comparison.
- LightRAG spike for lightweight graph-aware retrieval comparison.
- pgvector spike if PostgreSQL operational reuse is more valuable than a dedicated vector store.
- Qdrant+BGE-M3 continuation if vector-store and local embedding gates keep improving.

Mid-term exit criteria:

- Each candidate is evaluated with the same fixture/customer-like cases.
- Reports include citation fidelity, FP/FN behavior, latency/resource profile, deployment complexity, data residency posture, backup/recovery posture, and MyPrivateAgent contract compatibility.
- Candidate results end in one of: `keep_current_default`, `continue_spike`, or `eligible_for_promotion_review`.

### Long Term: Engine-Agnostic Provider Runtime

Goal: make retrieval infrastructure replaceable while the provider contract stays stable.

Long-term direction:

- define a small backend-adapter contract behind the current provider API;
- allow multiple retrieval/index backends without exposing framework-specific shapes to callers;
- keep GraphRAG execution use-case-driven and relationship-heavy;
- treat Dify and Langflow as external platforms or product references, not internal provider responsibilities;
- only promote defaults after customer-like evidence, deployment sign-off, and operations review are complete.

Long-term exit criteria:

- Runtime backend selection is explicit and reversible.
- Provider contracts remain stable across engine swaps.
- Promotion records clearly map evidence to runtime decisions.
- Caller ownership of final answer policy, orchestration, audit, registration, and source binding remains external.

## Candidate Roles

| Candidate | Role In This Project | Adoption Posture |
| --- | --- | --- |
| LlamaIndex | Current lightweight RAG baseline and adapter reference | Keep short-term baseline |
| Qdrant | Dedicated vector store candidate | Continue gated Phase 3/6 evidence |
| pgvector | PostgreSQL-native vector store candidate | Evaluate if operational reuse matters |
| BGE-M3 | Local Chinese-heavy embedding candidate | Continue artifact/quality/latency gates |
| Haystack | Modular RAG pipeline candidate | Spike as optional backend |
| RAGFlow | Deep document parsing and RAG platform reference | Spike externally; do not absorb control plane |
| LightRAG | Lightweight graph-aware RAG candidate | Spike only for relation-heavy evidence |
| Microsoft GraphRAG | Graph indexing/evidence architecture reference | Keep planned boundary until use case exists |
| Dify | LLM app/control-plane platform reference | External integration/reference only |
| Langflow | Visual workflow/control-plane platform reference | External integration/reference only |

## Evaluation Gates

Each candidate must be reviewed against:

- MyPrivateAgent local contract compatibility;
- citation fidelity and citation granularity;
- customer-like Chinese retrieval quality;
- false-positive and false-negative review;
- exact-term, alias, OCR-noise, split-chunk, and unsupported-domain behavior;
- latency and resource profile;
- deployment footprint for local, private-network, and future online modes;
- data residency and offline/private-network feasibility;
- backup, restore, reindex, and rollback posture;
- dependency, license, and maintenance risk;
- GraphRAG boundary impact.

## Non-Goals

- Replace the current provider with RAGFlow, Dify, Langflow, Haystack, or LightRAG immediately.
- Promote Qdrant, BGE-M3, hybrid retrieval, pgvector, GraphRAG, rerankers, or answer composition to runtime defaults.
- Add OCR/PDF/Word/Excel/table parsing before real corpus evidence requires it.
- Move final answer policy, provider registration, heartbeat governance, audit, source-to-agent binding, or workflow orchestration into this provider.
