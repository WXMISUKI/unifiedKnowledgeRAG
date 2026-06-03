## ADDED Requirements

### Requirement: Phase 12 open-source RAG engine evaluation remains provider-first

The project SHALL treat mature open-source RAG engines and platforms as evidence-backed candidates or references before any runtime replacement is considered.

#### Scenario: Short-term roadmap prioritizes MyPrivateAgent local RAG consumption

- **WHEN** the open-source RAG engine roadmap is reviewed
- **THEN** it identifies local MyPrivateAgent RAG consumption as the short-term priority
- **AND** it preserves the current provider HTTP contract, evidence pack, handoff, source-binding preview, and local verification artifacts as the integration surface

#### Scenario: Medium-term roadmap evaluates optional backend spikes

- **WHEN** Haystack, RAGFlow, LightRAG, pgvector, Qdrant, BGE-M3, or another RAG engine is considered
- **THEN** the roadmap treats it as an optional backend spike that must be compared through shared benchmark, citation, latency, deployment, and operations evidence

#### Scenario: Long-term roadmap preserves engine replaceability

- **WHEN** a future change proposes engine-agnostic backend selection
- **THEN** it keeps caller-facing provider contracts stable and hides framework-specific response shapes behind provider-owned adapters

### Requirement: Platform projects remain external references unless separately approved

The project SHALL keep platform-style open-source projects as product references or external integrations unless a separate evidence-backed change proves that a narrow backend capability belongs inside this provider.

#### Scenario: Platform capabilities do not move into the provider

- **WHEN** Dify, Langflow, RAGFlow, or another platform project is reviewed
- **THEN** workflow orchestration, agent identity, approval, audit, registration, heartbeat governance, source-to-agent binding, and final answer policy remain caller or external platform responsibilities

#### Scenario: Candidate review does not imply runtime promotion

- **WHEN** an open-source RAG candidate shows useful local evidence
- **THEN** Qdrant, BGE-M3, hybrid retrieval, pgvector, GraphRAG, rerankers, answer composition, and parser expansion remain non-default until a separate promotion change closes the required gates
