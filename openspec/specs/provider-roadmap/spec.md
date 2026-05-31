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

### Requirement: Graph boundary preflight summaries advance use-case-driven GraphRAG readiness

The project SHALL treat graph namespace summaries in provider preflight as Phase 5 boundary evidence when they help callers discover planned graph capability without adding graph execution or graph-store dependencies.

#### Scenario: Graph boundary preflight summary is phase-aligned

- **WHEN** an OpenSpec change adds graph schema counts or graph namespace ids to provider preflight evidence
- **THEN** the roadmap records it as lightweight Phase 5 GraphRAG boundary/readiness work rather than graph execution promotion

#### Scenario: Graph boundary preflight summary preserves graph gate

- **WHEN** provider preflight summarizes graph namespaces
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes

### Requirement: Evidence packaging changes advance Phase 4 without changing provider scope
The project SHALL treat retrieval evidence packs, citation policy metadata, and insufficient-evidence diagnostics as Phase 4 roadmap work when they help callers answer safely without moving final answer policy into the provider.

#### Scenario: Evidence packaging is phase-aligned
- **WHEN** an OpenSpec change adds evidence pack metadata for RAG retrieve or answer envelopes
- **THEN** the change identifies Phase 4 as the roadmap phase it advances

#### Scenario: Evidence packaging does not imply answer policy ownership
- **WHEN** the provider exposes evidence status or allowed citations
- **THEN** the roadmap boundary still states that the caller owns final user-facing answer style, refusal policy, and workflow decisions

### Requirement: Evidence provenance advances Phase 4 packaging
The project SHALL treat provider-owned evidence provenance as Phase 4 evidence packaging work when it helps callers answer from returned citations without moving final answer policy into the provider.

#### Scenario: Evidence provenance is phase-aligned
- **WHEN** an OpenSpec change adds provenance metadata to evidence packs
- **THEN** the roadmap records it as Phase 4 evidence packaging work

#### Scenario: Evidence provenance preserves caller ownership
- **WHEN** evidence packs include source path, chunk id, chunking strategy, and citation anchor metadata
- **THEN** the caller still owns final response style, refusal policy, approval workflow, and final orchestration

### Requirement: Deployment readiness evidence advances Phase 6 without expanding provider scope
The project SHALL treat local readiness reports, model artifact diagnostics, backup/reindex notes, and integration evidence summaries as Phase 6 operations work when they help deploy the provider component without moving control-plane governance into this module.

#### Scenario: Deployment readiness is phase-aligned
- **WHEN** an OpenSpec change adds local deployment readiness evidence
- **THEN** the change identifies Phase 6 as the roadmap phase it advances

#### Scenario: Deployment readiness does not imply platform ownership
- **WHEN** the provider exports readiness or operation notes
- **THEN** the roadmap boundary still states that external control planes own registration, heartbeat governance, audit policy, and agent binding decisions

### Requirement: Liveness and readiness probes advance Phase 6 high availability
The project SHALL treat liveness/readiness probe separation as Phase 6 deployment and operations work when it improves component availability without adding platform ownership.

#### Scenario: Probe split is phase-aligned
- **WHEN** an OpenSpec change adds separate liveness and readiness probes
- **THEN** the roadmap records it as lightweight Phase 6 high-availability work

#### Scenario: Probe split preserves provider boundary
- **WHEN** liveness and readiness probes are exposed
- **THEN** the provider still does not own orchestration, alert routing, autoscaling policy, registration, heartbeat governance, audit policy, or final answer workflow

### Requirement: Readiness HTTP status advances Phase 6 high availability
The project SHALL treat readiness HTTP status semantics as lightweight Phase 6 high-availability work when it helps deployment infrastructure stop routing traffic to degraded provider instances.

#### Scenario: Readiness status is phase-aligned
- **WHEN** an OpenSpec change makes `/ready` return HTTP 503 for degraded provider readiness
- **THEN** the roadmap records it as Phase 6 high-availability deployment work

#### Scenario: Readiness status preserves provider boundary
- **WHEN** readiness HTTP status is exposed
- **THEN** the provider still does not own orchestration, alert routing, autoscaling policy, registration, heartbeat governance, audit policy, or final answer workflow

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

### Requirement: Source binding summary bridges Phase 2 and Phase 6

The project SHALL treat source binding summary evidence as a lightweight bridge between Phase 2 document ingestion diagnostics and Phase 6 provider integration operations.

#### Scenario: Source binding summary is phase-aligned

- **WHEN** an OpenSpec change adds a read-only summary of source bindability for external control planes
- **THEN** the roadmap treats it as Phase 2 and Phase 6 work rather than source-to-agent control-plane ownership

#### Scenario: Source binding summary preserves provider boundary

- **WHEN** the provider reports source bindability facts and recommended actions
- **THEN** MyPrivateAgent or another external control plane still owns source-to-agent binding decisions, policy, approvals, audit, and final answer workflow

### Requirement: Source binding evidence participates in Phase 6 handoff

The project SHALL include source binding evidence in Phase 6 handoff artifacts when it helps external control planes review source readiness without moving binding policy into the provider.

#### Scenario: Source binding evidence is phase-aligned

- **WHEN** an OpenSpec change exports source binding summary evidence and adds it to handoff refresh
- **THEN** the roadmap treats it as Phase 2/6 evidence work

#### Scenario: Source binding evidence preserves provider boundary

- **WHEN** source binding evidence is included in the handoff bundle
- **THEN** MyPrivateAgent or another external control plane still owns source-to-agent binding decisions, policy, approvals, audit, and final answer workflow

### Requirement: Source binding coverage advances lightweight evidence review

The project SHALL treat source binding coverage summaries as Phase 2 and Phase 6 bridge work when they expose existing citation, chunk, and parser readiness evidence without adding parser, indexing, retrieval, answer composition, or GraphRAG responsibilities.

#### Scenario: Coverage summary is phase-aligned

- **WHEN** an OpenSpec change adds citation, chunk, or parser coverage counts to source binding review
- **THEN** the roadmap records it as lightweight evidence review that supports enterprise ingestion and external binding readiness

#### Scenario: Coverage summary preserves provider boundary

- **WHEN** source binding coverage is exposed through API or handoff evidence
- **THEN** source-to-agent binding policy, approvals, audit, parser expansion, ingestion execution, and final answer workflow remain owned outside this provider

### Requirement: Source package context advances lightweight binding review

The project SHALL treat source package context in source binding summaries as Phase 2 and Phase 6 bridge work when it exposes existing business and parser expectation metadata without adding binding policy, parser expansion, indexing execution, retrieval execution, answer composition, or GraphRAG responsibilities.

#### Scenario: Package context summary is phase-aligned

- **WHEN** an OpenSpec change adds source package context to source binding review
- **THEN** the roadmap records it as lightweight evidence review that supports enterprise source onboarding and external binding readiness

#### Scenario: Package context summary preserves provider boundary

- **WHEN** source package context is exposed through API or handoff evidence
- **THEN** source-to-agent binding policy, sensitivity-based approval, audit, parser expansion, ingestion execution, and final answer workflow remain owned outside this provider

### Requirement: Source binding capability promotion advances Phase 6 integration

The project SHALL treat source binding review capability promotion as Phase 6 integration work when it helps external control planes discover provider-owned binding evidence without making the provider a policy engine.

#### Scenario: Source binding capability is phase-aligned

- **WHEN** an OpenSpec change promotes source binding summary to a formal provider capability
- **THEN** the roadmap records it as lightweight Phase 6 integration work

#### Scenario: Source binding capability preserves external ownership

- **WHEN** source binding review is discoverable through provider capabilities
- **THEN** source-to-agent binding policy, approvals, audit, and execution remain owned by MyPrivateAgent or another external control plane

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

### Requirement: Source package and chunk manifest advance Phase 2 ingestion evidence
The project SHALL treat source package metadata and chunk manifest diagnostics as Phase 2 document ingestion baseline work when they help operators review source readiness without adding heavy parser or indexing infrastructure.

#### Scenario: Source package work is phase-aligned
- **WHEN** an OpenSpec change adds source package metadata or chunk manifest diagnostics
- **THEN** the roadmap records it as Phase 2 ingestion evidence work

#### Scenario: Source package work preserves lightweight scope
- **WHEN** the provider exposes source package or chunk manifest diagnostics
- **THEN** the provider still does not own source-to-agent binding approval, audit policy, OCR workflows, production parser expansion, embedding selection, vector-store promotion, or GraphRAG execution

### Requirement: Phase 6 may include lightweight component access guards

The project SHALL allow lightweight component access controls as Phase 6 deployment work when they protect provider HTTP APIs without moving external control-plane policy ownership into the provider.

#### Scenario: Access guard is phase-aligned

- **WHEN** an OpenSpec change adds an optional provider API token gate
- **THEN** the roadmap treats it as Phase 6 deployment and operations work

#### Scenario: Access guard preserves provider boundary

- **WHEN** provider API token protection is enabled
- **THEN** MyPrivateAgent or another caller still owns user identity, roles, approvals, audit policy, source-to-agent binding, and final answer policy

### Requirement: Access metadata advances Phase 6 integration

The project SHALL treat machine-readable provider access metadata as Phase 6 integration work when it helps external control planes connect to the provider component without taking over identity or policy ownership.

#### Scenario: Access metadata is phase-aligned

- **WHEN** an OpenSpec change adds component access metadata to the provider manifest
- **THEN** the roadmap treats it as Phase 6 integration evidence

#### Scenario: Access metadata preserves provider boundary

- **WHEN** the provider advertises accepted component access headers
- **THEN** MyPrivateAgent or another external control plane still owns user identity, roles, approvals, audit policy, source-to-agent binding, and final answer workflow

### Requirement: Phase 6 includes lightweight deployment profiles

The project SHALL treat container and compose deployment profiles as Phase 6 deployment work when they help run the provider as a component without introducing platform ownership.

#### Scenario: Deployment profile is phase-aligned

- **WHEN** an OpenSpec change adds Docker or compose deployment files for the provider component
- **THEN** the roadmap treats it as Phase 6 deployment and operations work

#### Scenario: Deployment profile preserves provider boundary

- **WHEN** a deployment profile is added
- **THEN** it does not imply ownership of TLS termination, reverse proxy policy, managed secrets, registration, heartbeat governance, audit policy, source-to-agent binding, or final answer policy

### Requirement: Deployed provider smoke advances Phase 6 operations

The project SHALL treat deployed provider HTTP smoke evidence as Phase 6 deployment and operations work when it helps verify an already-running provider component and live binding-review surfaces before external binding.

#### Scenario: Deployed smoke is phase-aligned

- **WHEN** an OpenSpec change adds a deployed HTTP smoke probe for provider discovery, source binding review, and handoff endpoints
- **THEN** the roadmap treats it as Phase 6 deployment and operations evidence rather than retrieval, GraphRAG, or platform-control work

#### Scenario: Deployed smoke preserves provider boundary

- **WHEN** deployed provider smoke evidence is exported
- **THEN** it does not imply ownership of TLS termination, reverse proxy policy, managed secrets, registration, heartbeat governance, audit policy, source-to-agent binding, or final answer policy

### Requirement: Source binding deployed smoke advances Phase 6 integration evidence

The project SHALL treat deployed source binding endpoint smoke as Phase 6 integration and operations evidence when it verifies that live provider binding-review surfaces are reachable without executing retrieval, ingestion, answer composition, or GraphRAG.

#### Scenario: Source binding deployed smoke is phase-aligned

- **WHEN** an OpenSpec change adds `GET /api/provider/source-bindings` to deployed smoke
- **THEN** the roadmap records it as lightweight Phase 6 deployed integration evidence

#### Scenario: Source binding deployed smoke preserves provider boundary

- **WHEN** deployed smoke validates source binding review over HTTP
- **THEN** source-to-agent binding creation, approvals, audit, heartbeat governance, registration, and final answer policy remain outside this provider

### Requirement: Deployed source binding action summaries advance Phase 6 integration evidence

The project SHALL treat source binding status and recommended action rollups in deployed provider smoke evidence as lightweight Phase 6 deployed integration work when they help external control planes review live source readiness without adding binding policy or runtime execution responsibilities.

#### Scenario: Deployed smoke action summary is phase-aligned

- **WHEN** an OpenSpec change enriches deployed provider smoke source binding evidence with source status counts or recommended action counts
- **THEN** the roadmap records it as Phase 6 deployed integration evidence with Phase 2 source binding context

#### Scenario: Deployed smoke action summary preserves provider boundary

- **WHEN** deployed provider smoke summarizes source binding statuses or recommended actions
- **THEN** source-to-agent binding policy, approvals, audit, registration, ingestion execution, retrieval execution, answer composition, and final answer workflow remain owned outside this provider

### Requirement: Handoff evidence may include optional deployed smoke

The project SHALL allow Phase 6 provider handoff evidence to include optional deployed smoke status so external control planes can review live deployment reachability without making local development depend on a deployed URL.

#### Scenario: Optional deployed smoke is phase-aligned

- **WHEN** an OpenSpec change adds deployed smoke evidence to the provider handoff bundle
- **THEN** the roadmap treats it as Phase 6 integration and operations evidence

#### Scenario: Optional deployed smoke preserves provider boundary

- **WHEN** deployed smoke is summarized in handoff evidence
- **THEN** it does not imply ownership of provider registration, heartbeat governance, audit policy, TLS termination, reverse proxy policy, managed secrets, source-to-agent binding, or final answer policy

### Requirement: Source binding handoff action summaries advance lightweight evidence review

The project SHALL treat source binding status and recommended action rollups in provider handoff evidence as Phase 2 and Phase 6 bridge work when they help external control planes review source readiness without adding binding policy or runtime execution responsibilities.

#### Scenario: Handoff action summary is phase-aligned

- **WHEN** an OpenSpec change enriches provider handoff source binding evidence with source status counts or recommended action counts
- **THEN** the roadmap records it as lightweight Phase 2/6 source binding evidence work

#### Scenario: Handoff action summary preserves provider boundary

- **WHEN** provider handoff evidence summarizes source binding statuses or recommended actions
- **THEN** source-to-agent binding policy, approvals, audit, registration, ingestion execution, retrieval execution, answer composition, and final answer workflow remain owned outside this provider
