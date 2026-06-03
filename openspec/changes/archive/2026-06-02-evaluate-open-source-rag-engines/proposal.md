## Why

The project has matured through provider readiness, evidence packaging, GraphRAG boundary work, deployment readiness, MyPrivateAgent local verification, and hybrid runtime promotion review. The next decision is whether to keep improving the current lightweight provider or reuse a mature open-source RAG engine.

We need an explicit OpenSpec change that treats open-source RAG engines as evidence-backed candidates instead of immediate replacements. The short-term priority remains smooth local MyPrivateAgent RAG consumption; medium-term work can spike alternative backends; long-term work should keep the provider contract stable while making the underlying engine replaceable.

## What Changes

- Add a short/mid/long RAG engine evaluation roadmap.
- Define the candidate roles for LlamaIndex, Qdrant, pgvector, Haystack, RAGFlow, LightRAG, Microsoft GraphRAG, Dify, and Langflow.
- Define the evaluation gates that any reusable engine must pass before runtime promotion.
- Clarify that Dify/Langflow/RAGFlow-style platform capabilities are product references or external integrations, not provider-control-plane responsibilities.
- Preserve current runtime defaults, public HTTP contracts, GraphRAG planned boundary, and MyPrivateAgent ownership boundaries.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: add a Phase 12 open-source RAG engine evaluation roadmap that keeps the project provider-first and evidence-driven.
- `retrieval-benchmark-harness`: add shared evaluation requirements for external RAG engine candidates and optional backend spikes.

## Impact

- Adds `docs/roadmap/open_source_rag_engine_evaluation_roadmap.md`.
- Adds OpenSpec deltas for provider roadmap and retrieval benchmark harness.
- Does not migrate the runtime to another engine.
- Does not make Qdrant, BGE-M3, hybrid retrieval, GraphRAG, or any platform runtime default.
- Does not move caller control-plane responsibilities into this provider.
