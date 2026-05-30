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

### Requirement: Evidence packaging changes advance Phase 4 without changing provider scope
The project SHALL treat retrieval evidence packs, citation policy metadata, and insufficient-evidence diagnostics as Phase 4 roadmap work when they help callers answer safely without moving final answer policy into the provider.

#### Scenario: Evidence packaging is phase-aligned
- **WHEN** an OpenSpec change adds evidence pack metadata for RAG retrieve or answer envelopes
- **THEN** the change identifies Phase 4 as the roadmap phase it advances

#### Scenario: Evidence packaging does not imply answer policy ownership
- **WHEN** the provider exposes evidence status or allowed citations
- **THEN** the roadmap boundary still states that the caller owns final user-facing answer style, refusal policy, and workflow decisions

### Requirement: Deployment readiness evidence advances Phase 6 without expanding provider scope
The project SHALL treat local readiness reports, model artifact diagnostics, backup/reindex notes, and integration evidence summaries as Phase 6 operations work when they help deploy the provider component without moving control-plane governance into this module.

#### Scenario: Deployment readiness is phase-aligned
- **WHEN** an OpenSpec change adds local deployment readiness evidence
- **THEN** the change identifies Phase 6 as the roadmap phase it advances

#### Scenario: Deployment readiness does not imply platform ownership
- **WHEN** the provider exports readiness or operation notes
- **THEN** the roadmap boundary still states that external control planes own registration, heartbeat governance, audit policy, and agent binding decisions

### Requirement: Reindex planning evidence advances Phase 6 operations
The project SHALL treat local reindex readiness plans and backup/reindex notes as Phase 6 operations evidence when they help operators review provider component state without changing runtime behavior.

#### Scenario: Reindex planning is phase-aligned
- **WHEN** an OpenSpec change adds read-only reindex planning evidence
- **THEN** the change identifies Phase 6 as the roadmap phase it advances

#### Scenario: Reindex planning does not imply worker infrastructure
- **WHEN** the provider exports reindex recommendations
- **THEN** it does not imply approval of production queue workers, schedulers, or automatic reindex execution

### Requirement: Provider handoff evidence advances Phase 6 operations
The project SHALL treat local provider handoff bundles as Phase 6 operations and integration evidence when they consolidate existing provider readiness artifacts without changing runtime behavior or moving control-plane responsibilities into this module.

#### Scenario: Handoff bundle is phase-aligned
- **WHEN** an OpenSpec change adds read-only handoff evidence for external provider integration
- **THEN** the change identifies Phase 6 as the roadmap phase it advances

#### Scenario: Handoff bundle preserves provider scope
- **WHEN** the provider exports handoff evidence
- **THEN** it does not imply ownership of provider registration, heartbeat governance, audit policy, source-to-agent binding decisions, or final answer policy

### Requirement: Handoff refresh evidence advances Phase 6 operations
The project SHALL treat local provider handoff refresh reports as Phase 6 operations evidence when they keep integration and readiness artifacts current without changing runtime behavior or expanding provider scope.

#### Scenario: Handoff refresh is phase-aligned
- **WHEN** an OpenSpec change adds a local evidence refresh workflow for provider handoff artifacts
- **THEN** the change identifies Phase 6 as the roadmap phase it advances

#### Scenario: Handoff refresh does not imply control-plane ownership
- **WHEN** the provider refreshes local handoff evidence
- **THEN** it does not imply ownership of provider registration, heartbeat governance, audit policy, source-to-agent binding decisions, or final answer policy

### Requirement: Source fingerprint diagnostics advance Phase 2 ingestion evidence
The project SHALL treat source document fingerprint and drift diagnostics as Phase 2 document ingestion baseline evidence when they help operators verify local source freshness without changing retrieval behavior.

#### Scenario: Fingerprint diagnostics are phase-aligned
- **WHEN** an OpenSpec change adds read-only source document fingerprint diagnostics
- **THEN** the change identifies Phase 2 as the roadmap phase it advances

#### Scenario: Fingerprint diagnostics do not imply ingestion promotion
- **WHEN** the provider reports source document drift
- **THEN** it does not automatically create ingestion jobs, rebuild indexes, promote chunking strategies, or change retrieval defaults

### Requirement: Source drift evidence informs Phase 6 reindex planning
The project SHALL allow Phase 2 source freshness evidence to inform Phase 6 reindex readiness recommendations without changing runtime retrieval behavior.

#### Scenario: Drift-informed reindex planning is phase-aligned
- **WHEN** an OpenSpec change connects source fingerprint diagnostics to reindex readiness evidence
- **THEN** the change identifies Phase 2 and Phase 6 as the roadmap phases it connects

#### Scenario: Drift-informed planning does not automate indexing
- **WHEN** the provider reports that changed source documents should be reindexed
- **THEN** it does not automatically create ingestion jobs, rebuild indexes, or change retrieval defaults

### Requirement: Phase 6 handoff evidence may be exposed through read-only HTTP discovery

The project SHALL allow Phase 6 integration and operations evidence to be exposed through lightweight read-only HTTP discovery when it helps external control planes bind the provider without taking over provider internals.

#### Scenario: Handoff API remains phase-aligned

- **WHEN** an OpenSpec change exposes existing handoff evidence through a read-only HTTP endpoint
- **THEN** the roadmap treats it as Phase 6 integration evidence rather than a runtime retrieval, GraphRAG, or platform-control feature

#### Scenario: Handoff API preserves provider boundary

- **WHEN** the provider exposes handoff evidence over HTTP
- **THEN** external control planes still own registration, heartbeat governance, audit policy, source-to-agent binding decisions, and final answer policy

### Requirement: Enterprise ingestion boundary advances Phase 2 without heavy parsers

The project SHALL treat pre-ingestion document diagnostics as Phase 2 enterprise document ingestion baseline work when it improves source readiness visibility without approving production parser dependencies.

#### Scenario: Ingestion boundary is phase-aligned

- **WHEN** an OpenSpec change adds source document ingestion preflight diagnostics
- **THEN** the roadmap treats it as Phase 2 document ingestion baseline work

#### Scenario: Parser dependencies remain gated

- **WHEN** ingestion preflight reports unsupported formats
- **THEN** it does not imply approval to add OCR, PDF, Word, Excel, HTML, table extraction, or layout parsing dependencies without a separate evidence-backed change
