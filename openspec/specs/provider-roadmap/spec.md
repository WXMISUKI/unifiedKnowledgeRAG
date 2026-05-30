# provider-roadmap Specification

## Purpose
Define the lightweight staged roadmap and phase gates for `unifiedKnowledgeRAG` so the provider stays focused on knowledge data-plane responsibilities while future OpenSpec changes remain phase-aligned and evidence-driven.
## Requirements
### Requirement: Provider roadmap preserves lightweight data-plane scope
The project SHALL maintain a staged roadmap that keeps this module focused on knowledge data-plane responsibilities: retrieving trusted evidence, preserving citations, exposing readiness and integration metadata, and returning provider-owned diagnostic evidence to external callers.

#### Scenario: Roadmap separates provider and caller responsibilities
- **WHEN** the project roadmap is reviewed
- **THEN** it states that MyPrivateAgent or another caller owns agent identity, policy, approval, final answer presentation, task execution, and runtime orchestration

#### Scenario: Provider remains evidence-first
- **WHEN** future work proposes answer generation, agentic retrieval, GraphRAG, reranking, or hybrid retrieval
- **THEN** the roadmap frames those features as evidence packaging or retrieval-quality improvements rather than broad agent-platform responsibilities

### Requirement: Provider roadmap defines phase gates
The project SHALL define phase gates with concrete outcomes and evidence so future OpenSpec changes can be selected by project value rather than local optimization alone.

#### Scenario: Future changes identify a phase
- **WHEN** a future OpenSpec change is proposed
- **THEN** it identifies the roadmap phase it advances or explains why it is outside the staged roadmap

#### Scenario: Runtime promotion requires evidence
- **WHEN** a future change promotes a candidate retrieval mode, embedding model, vector-store behavior, reranker, answer composer, or GraphRAG behavior into a runtime default
- **THEN** it references machine-readable evidence or explicitly records the missing evidence as an open gate

#### Scenario: Candidate work stays reversible
- **WHEN** a future change adds evaluation-only or candidate-only behavior
- **THEN** it avoids changing default runtime behavior unless the relevant phase gate says promotion criteria are met

### Requirement: Provider roadmap keeps GraphRAG optional and use-case driven
The project SHALL keep GraphRAG storage and graph query execution behind a separate phase gate until a concrete relationship-heavy business use case is defined.

#### Scenario: GraphRAG is not pulled in by document RAG work
- **WHEN** document RAG ingestion, chunking, vector retrieval, or evidence packaging changes are implemented
- **THEN** they do not implicitly add graph storage, entity extraction, ontology workflow, or graph query execution

#### Scenario: GraphRAG phase requires concrete evidence
- **WHEN** GraphRAG execution is proposed
- **THEN** the proposal identifies target graph use cases, expected entities/relations/paths, source evidence rules, and operational ownership before adding graph-store dependencies
