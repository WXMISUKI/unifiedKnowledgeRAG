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

### Requirement: Graph schema contract smoke advances lightweight GraphRAG boundary evidence

The project SHALL treat graph schema discovery smoke evidence as Phase 5 boundary work when it validates graph namespace metadata without adding graph execution or graph-store dependencies.

#### Scenario: Graph schema smoke is phase-aligned

- **WHEN** an OpenSpec change adds local contract smoke coverage for `GET /api/graph/schemas`
- **THEN** the roadmap records it as lightweight Phase 5 graph boundary evidence rather than GraphRAG execution promotion

#### Scenario: Graph schema smoke preserves graph gate

- **WHEN** provider contract smoke validates graph schema discovery
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes

### Requirement: Evidence packaging changes advance Phase 4 without changing provider scope

The project SHALL treat retrieval evidence packs, citation policy metadata, insufficient-evidence diagnostics, caller consumption contracts, caller-consumption smoke, and readiness exports as Phase 4 roadmap work when they help callers answer safely without moving final answer policy into the provider.

#### Scenario: Evidence packaging is phase-aligned

- **WHEN** an OpenSpec change adds evidence pack metadata, a caller consumption contract, a caller-consumption smoke, or a readiness export for RAG retrieve or answer envelopes
- **THEN** the change identifies Phase 4 as the roadmap phase it advances

#### Scenario: Evidence packaging does not imply answer policy ownership

- **WHEN** the provider exposes evidence status, allowed citations, caller consumption rules, or readiness summaries
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

### Requirement: Source binding compact summaries stay lightweight

The project SHALL treat source binding aggregate counts as lightweight Phase 2 and Phase 6 evidence when they summarize existing source readiness rows without changing binding policy or executing provider capabilities.

#### Scenario: Source binding compact summary is phase-aligned

- **WHEN** an OpenSpec change adds compact counts to source binding evidence
- **THEN** the roadmap records it as source readiness and handoff evidence rather than source-to-agent binding execution

#### Scenario: Source binding compact summary preserves provider boundary

- **WHEN** source binding compact counts are generated
- **THEN** binding policy, approvals, audit, registration, final answer workflow, ingestion execution, retrieval execution, and GraphRAG execution remain outside this provider

### Requirement: Source binding aggregate reuse stays lightweight

The project SHALL treat reuse of source binding aggregate counts in handoff and deployed-smoke evidence as lightweight Phase 2 and Phase 6 consistency work when it avoids duplicated aggregation without changing provider scope.

#### Scenario: Aggregate reuse is phase-aligned

- **WHEN** an OpenSpec change makes evidence summaries prefer source binding aggregate counts
- **THEN** the roadmap records it as source readiness and handoff consistency evidence rather than source-to-agent binding execution

#### Scenario: Aggregate reuse preserves provider boundary

- **WHEN** handoff or deployed-smoke evidence reuses source binding aggregate counts
- **THEN** binding policy, approvals, audit, registration, final answer workflow, ingestion execution, retrieval execution, and GraphRAG execution remain outside this provider

### Requirement: Customer-like benchmark expansion advances Phase 3 evidence quality

The project SHALL treat customer-like benchmark fixture expansion as Phase 3 retrieval evidence work when it improves promotion review quality without changing runtime defaults.

#### Scenario: Customer-like expansion remains evidence-only

- **WHEN** an OpenSpec change expands customer-like benchmark fixtures
- **THEN** the roadmap records the work as evidence-only Phase 3 review coverage rather than runtime promotion

### Requirement: Phase 3 evidence refresh preserves lightweight promotion boundaries

The project SHALL treat post-fixture evidence regeneration as Phase 3 maintenance when it keeps benchmark artifacts current without changing runtime defaults.

#### Scenario: Evidence refresh is phase-aligned

- **WHEN** benchmark fixture updates require regenerated Chinese-seed evidence
- **THEN** the roadmap records the work as retrieval evidence maintenance rather than runtime retrieval promotion

#### Scenario: Evidence refresh keeps provider boundary unchanged

- **WHEN** Chinese-seed evidence is refreshed
- **THEN** provider contracts, control-plane ownership, and GraphRAG execution boundaries remain unchanged

### Requirement: Phase 3 evidence summaries in handoff stay lightweight

The project SHALL treat compact Phase 3 retrieval evidence summaries in handoff as lightweight review ergonomics work when they improve discoverability without changing runtime promotion gates.

#### Scenario: Handoff Phase 3 summary is phase-aligned

- **WHEN** an OpenSpec change adds a compact Phase 3 baseline evidence summary row to handoff
- **THEN** the roadmap records it as Phase 3/Phase 6 evidence visibility rather than runtime retrieval promotion

#### Scenario: Handoff Phase 3 summary preserves provider boundary

- **WHEN** handoff includes compact Phase 3 benchmark summary metrics
- **THEN** retrieval defaults, control-plane ownership, and GraphRAG execution boundaries remain unchanged

### Requirement: Phase 3 FP/FN review export is phase-aligned

The project SHALL treat integration of local FP/FN review evidence into handoff and refresh as Phase 3/Phase 6 evidence visibility work.

#### Scenario: Handoff/refresh FP/FN integration remains evaluation-only

- **WHEN** an OpenSpec change integrates FP/FN review evidence into handoff bundle or refresh workflow
- **THEN** runtime retrieval defaults and promotion gates remain unchanged

### Requirement: Evidence refresh maintenance command remains explicit

The project SHALL keep the local evidence refresh maintenance command explicit in roadmap-adjacent tracking docs so current evidence state is reproducible and not confused with historical milestones.

#### Scenario: Tracker distinguishes historical and current benchmark baseline

- **WHEN** benchmark baseline size changes across archived Phase 3 slices
- **THEN** tracker wording marks older counts as historical and keeps the current canonical count explicit

#### Scenario: Tracker documents maintenance command

- **WHEN** reviewers need to refresh local handoff evidence
- **THEN** tracker documents `python scripts/export_provider_handoff_refresh.py` as the standard maintenance command

### Requirement: Deployment readiness guidance stays operator-facing

The project SHALL keep deployment readiness guidance in operator-facing documentation so review-state evidence can be turned into concrete deployment steps without changing runtime behavior.

#### Scenario: Operator guide maps review state to actions

- **WHEN** deployment readiness reports `review`
- **THEN** the guide explains the current blockers and the next operator actions required before deployment

#### Scenario: Operator guide preserves provider boundary

- **WHEN** deployment readiness guidance is published
- **THEN** it does not introduce runtime promotion logic, deployment automation, or governance ownership changes

### Requirement: Deployment readiness guidance includes a configuration reference

The project SHALL provide a deployment configuration reference that maps runtime environment variables, mount points, and evidence refresh commands to the current deployment readiness state.

#### Scenario: Operators can identify deployment inputs

- **WHEN** an operator reviews deployment readiness guidance
- **THEN** the configuration reference shows which environment variables and mounted paths are relevant for deployment preparation

#### Scenario: Configuration reference remains documentation-only

- **WHEN** the configuration reference is published
- **THEN** it does not change runtime defaults, deployment automation, or provider governance boundaries

### Requirement: Deployment readiness guidance includes a sequential runbook

The project SHALL provide a deployment readiness runbook that sequences the existing operator guide, config reference, evidence exports, and smoke checks into an ordered path for deployment preparation.

#### Scenario: Runbook gives an execution order

- **WHEN** an operator prepares a deployment candidate
- **THEN** the runbook presents the steps in order from current evidence review through refresh and optional deployed smoke

#### Scenario: Runbook remains documentation-only

- **WHEN** the runbook is published
- **THEN** it does not add deployment automation, runtime promotion logic, or governance ownership changes

### Requirement: Phase 3 retrieval promotion gap matrix is lightweight review ergonomics

The project SHALL treat a local Phase 3 retrieval promotion gap matrix as lightweight evidence review work when it consolidates current candidate evidence and open promotion gaps without changing runtime defaults.

#### Scenario: Gap matrix is published

- **WHEN** an OpenSpec change adds or refreshes the Phase 3 retrieval promotion gap matrix
- **THEN** the roadmap records it as Phase 3 evidence review work rather than runtime promotion

#### Scenario: Gap matrix is read-only

- **WHEN** the gap matrix is reviewed
- **THEN** it does not change retrieval defaults, provider HTTP contracts, or promotion gates

### Requirement: Phase 3 readiness export is lightweight review visibility

The project SHALL treat a local Phase 3 retrieval promotion readiness export as lightweight Phase 3 evidence visibility work when it consolidates current promotion gaps without changing runtime defaults.

#### Scenario: Readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes the Phase 3 readiness export
- **THEN** the roadmap records it as Phase 3 evidence visibility rather than runtime promotion

#### Scenario: Readiness export preserves provider boundary

- **WHEN** the readiness export is reviewed
- **THEN** it does not change retrieval defaults, provider HTTP contracts, or promotion gates

### Requirement: Graph use-case readiness contracts advance Phase 5 without executing GraphRAG

The project SHALL treat a local graph use-case readiness contract as Phase 5 boundary work when it explains which questions are graph-worthy and which should remain in document RAG without adding graph execution or graph-store dependencies.

#### Scenario: Graph use-case readiness contract is phase-aligned

- **WHEN** an OpenSpec change adds a graph use-case readiness contract document
- **THEN** the roadmap records it as lightweight Phase 5 GraphRAG boundary/readiness work rather than graph execution promotion

#### Scenario: Graph use-case readiness contract preserves graph gate

- **WHEN** the contract documents relationship-heavy cases, document-RAG-only cases, or source evidence rules
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes

### Requirement: Graph use-case readiness exports advance Phase 5 without executing GraphRAG

The project SHALL treat a local graph use-case readiness export as Phase 5 boundary work when it consolidates graph use-case contract evidence and planned graph query boundaries without adding graph execution or graph-store dependencies.

#### Scenario: Graph use-case readiness export is phase-aligned

- **WHEN** an OpenSpec change adds a graph use-case readiness export
- **THEN** the roadmap records it as lightweight Phase 5 GraphRAG boundary/readiness work rather than graph execution promotion

#### Scenario: Graph use-case readiness export preserves graph gate

- **WHEN** the export summarizes graph schema discovery, graph statuses, or planned query boundaries
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes

### Requirement: Graph boundary smoke summaries advance Phase 5 without executing GraphRAG

The project SHALL treat a local graph boundary smoke summary as Phase 5 boundary work when it consolidates graph schema discovery and the planned graph query boundary without adding graph execution or graph-store dependencies.

#### Scenario: Graph boundary smoke summary is phase-aligned

- **WHEN** an OpenSpec change adds a graph boundary smoke summary
- **THEN** the roadmap records it as lightweight Phase 5 GraphRAG boundary/readiness work rather than graph execution promotion

#### Scenario: Graph boundary smoke summary preserves graph gate

- **WHEN** the summary consolidates graph schema discovery or planned query boundaries
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes

### Requirement: Phase 3 candidate evaluation protocols stay lightweight and review-only

The project SHALL treat Phase 3 retrieval candidate evaluation protocols as lightweight evidence-governance work when they standardize gate review expectations without changing runtime defaults.

#### Scenario: Protocol document is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 retrieval candidate evaluation protocol
- **THEN** the roadmap records it as Phase 3 evidence-governance work rather than retrieval runtime promotion

#### Scenario: Protocol document preserves provider boundaries

- **WHEN** the protocol defines gate expectations for Qdrant, BGE-M3, hybrid retrieval, hybrid gating, aggregation, or relation-aware grading
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG execution boundaries, and caller ownership remain unchanged until separate evidence-backed promotion changes are approved

### Requirement: Phase 3 runtime diagnostics exports stay lightweight and evaluation-only

The project SHALL treat Phase 3 candidate runtime diagnostics exports as lightweight evidence visibility work when they summarize promotion prerequisites without changing runtime defaults.

#### Scenario: Runtime diagnostics export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 candidate runtime diagnostics export
- **THEN** the roadmap records it as Phase 3 evidence visibility work rather than runtime promotion

#### Scenario: Runtime diagnostics export preserves boundaries

- **WHEN** runtime diagnostics summarize retrieval backend, embedding provider, artifact status, and deployment-evidence presence
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged

### Requirement: Phase 3 cross-case FP/FN smoke remains lightweight evidence maintenance

The project SHALL treat Phase 3 hybrid cross-case FP/FN smoke as lightweight evidence maintenance when it validates risk-signal visibility without changing runtime defaults.

#### Scenario: Cross-case smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes cross-case hybrid FP/FN smoke evidence
- **THEN** the roadmap records it as Phase 3 evidence maintenance and review ergonomics work

#### Scenario: Cross-case smoke preserves boundaries

- **WHEN** cross-case smoke reports false-positive/false-negative risk signals
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged

### Requirement: Phase 3 candidate latency/resource diagnostics exports stay lightweight and evaluation-only

The project SHALL treat Phase 3 candidate latency/resource diagnostics exports as lightweight evidence visibility work when they summarize latency shape and resource posture without changing runtime defaults.

#### Scenario: Latency/resource export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 candidate latency/resource diagnostics export
- **THEN** the roadmap records it as Phase 3 evidence visibility work rather than runtime promotion

#### Scenario: Latency/resource export preserves boundaries

- **WHEN** latency/resource diagnostics summarize local benchmark latency and resource/deployment posture
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged

### Requirement: Phase 3 aggregation and relation-aware negative-control smoke stays lightweight and evaluation-only

The project SHALL treat the Phase 3 aggregation/relation negative-control smoke as lightweight evidence visibility work when it summarizes over-broad aggregation risk and relation-aware grading alignment without changing runtime defaults.

#### Scenario: Negative-control smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 aggregation/relation negative-control smoke
- **THEN** the roadmap records it as Phase 3 evidence maintenance work rather than runtime promotion

#### Scenario: Negative-control smoke preserves runtime defaults

- **WHEN** the smoke validates positive and negative aggregation controls plus relation-aware grading alignment
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged

### Requirement: Phase 3 hybrid fusion calibration exports stay lightweight and evaluation-only

The project SHALL treat Phase 3 hybrid fusion/threshold calibration exports as lightweight evidence visibility work when they summarize candidate calibration context without changing runtime defaults.

#### Scenario: Calibration export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 hybrid fusion/threshold calibration export
- **THEN** the roadmap records it as Phase 3 evidence visibility work rather than runtime promotion

#### Scenario: Calibration export preserves boundaries

- **WHEN** calibration evidence summarizes candidate hybrid fusion and threshold context
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged

### Requirement: Phase 3 runtime promotion decision SHALL be explicitly recorded

The project SHALL preserve a documentation-only decision record for each Phase 3 promotion review cycle before any runtime default promotion.

#### Scenario: Decision record captures no-promotion verdict

- **WHEN** Phase 3 evidence remains candidate-level or review-level
- **THEN** the decision record states `keep_runtime_defaults` and lists open gates for production promotion

#### Scenario: Decision record remains boundary-safe

- **WHEN** the decision record is published
- **THEN** it does not change provider runtime defaults, public API contracts, GraphRAG planned boundary, or caller ownership responsibilities

### Requirement: BGE-M3 artifact readiness is treated as Phase 6 bridge evidence

The project SHALL treat BGE-M3 artifact readiness as lightweight deployment evidence that supports Phase 3 promotion review without changing runtime defaults.

#### Scenario: Artifact readiness is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes BGE-M3 artifact readiness evidence
- **THEN** the roadmap records it as Phase 6 deployment evidence with Phase 3 bridge value

#### Scenario: Artifact readiness preserves boundaries

- **WHEN** the readiness report summarizes checksum-aware model artifact state
- **THEN** runtime embedding defaults, provider HTTP contracts, and promotion decisions remain unchanged

### Requirement: Qdrant deployment/backup/recovery readiness is treated as Phase 6 operations evidence

The project SHALL treat Qdrant vector-store deployment, backup, and recovery readiness as lightweight Phase 6 operations evidence without changing runtime defaults.

#### Scenario: Qdrant readiness contract is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes Qdrant deployment/backup/recovery readiness evidence
- **THEN** the roadmap records it as Phase 6 operations work instead of retrieval runtime promotion

#### Scenario: Qdrant readiness preserves boundaries

- **WHEN** Qdrant readiness evidence is reviewed
- **THEN** retrieval defaults, provider HTTP contracts, and external control-plane ownership remain unchanged

### Requirement: Phase 6 Qdrant vector-store readiness exports stay lightweight and review-only

The project SHALL treat Phase 6 Qdrant vector-store readiness exports as local evidence visibility work without changing runtime defaults.

#### Scenario: Qdrant readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Qdrant vector-store readiness export
- **THEN** the roadmap records it as Phase 6 operations evidence visibility work rather than retrieval runtime promotion

#### Scenario: Qdrant readiness export preserves boundaries

- **WHEN** the export summarizes deployment, backup/recovery contract, and reindex linkage
- **THEN** runtime defaults, provider HTTP contracts, and external control-plane ownership remain unchanged

### Requirement: Phase 6 Qdrant backup/restore smoke stays lightweight and read-only

The project SHALL treat Phase 6 Qdrant backup/restore smoke summaries as local operations evidence maintenance without changing runtime defaults.

#### Scenario: Backup/restore smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes Qdrant backup/restore smoke evidence
- **THEN** the roadmap records it as Phase 6 evidence maintenance work rather than runtime promotion

#### Scenario: Backup/restore smoke preserves boundaries

- **WHEN** smoke summaries validate backup/restore prerequisites
- **THEN** they do not execute backup/restore actions and do not move control-plane ownership into the provider

### Requirement: BGE-M3 quality/latency comparison contracts are Phase 6/Phase 3 bridge evidence

The project SHALL treat BGE-M3 vs mock/fixture quality and latency comparison contracts as lightweight Phase 6 deployment evidence with explicit Phase 3 promotion bridge value.

#### Scenario: Comparison contract is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a BGE-M3 quality/latency comparison contract
- **THEN** the roadmap records it as bridge evidence and not as runtime promotion

#### Scenario: Comparison contract preserves boundaries

- **WHEN** the comparison contract is reviewed
- **THEN** runtime defaults, provider HTTP contracts, and external control-plane ownership remain unchanged

### Requirement: Phase 6 BGE-M3 comparison diagnostics exports stay lightweight and evaluation-only

The project SHALL treat Phase 6 BGE-M3 vs mock/fixture diagnostics exports as local evidence visibility work without changing runtime defaults.

#### Scenario: Comparison diagnostics export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a BGE-M3 comparison diagnostics export
- **THEN** the roadmap records it as Phase 6/Phase 3 bridge evidence visibility rather than runtime promotion

#### Scenario: Comparison diagnostics preserve boundaries

- **WHEN** the export summarizes baseline/candidate quality-latency deltas and deployment linkage
- **THEN** runtime defaults, provider HTTP contracts, and external control-plane ownership remain unchanged

### Requirement: Phase 6 BGE-M3 comparison smoke stays lightweight and read-only

The project SHALL treat Phase 6 BGE-M3 comparison smoke summaries as local evidence maintenance without changing runtime defaults.

#### Scenario: Comparison smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes BGE-M3 comparison smoke evidence
- **THEN** the roadmap records it as Phase 6 evidence maintenance and not runtime promotion

#### Scenario: Comparison smoke preserves boundaries

- **WHEN** the smoke checks comparison evidence-chain prerequisites
- **THEN** it does not execute retrieval changes, model download, embedding execution, or control-plane policy

### Requirement: Qdrant+BGE-M3 private-network promotion review contracts are Phase 6/Phase 3 bridge evidence

The project SHALL treat Qdrant+BGE-M3 private-network promotion review contracts as lightweight Phase 6 evidence with explicit Phase 3 promotion bridge value.

#### Scenario: Private-network review contract is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a private-network promotion review contract
- **THEN** the roadmap records it as review-governance evidence and not runtime promotion

#### Scenario: Private-network review contract preserves boundaries

- **WHEN** the contract is reviewed
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged

### Requirement: Phase 6 Qdrant+BGE-M3 private-network promotion readiness exports stay lightweight and review-only

The project SHALL treat Qdrant+BGE-M3 private-network promotion readiness exports as local evidence visibility work without changing runtime defaults.

#### Scenario: Private-network readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes private-network promotion readiness export evidence
- **THEN** the roadmap records it as Phase 6 bridge visibility and not runtime promotion

#### Scenario: Private-network readiness export preserves boundaries

- **WHEN** the export summarizes review gates and open evidence inputs
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged

### Requirement: Phase 6 private-network promotion smoke stays lightweight and read-only

The project SHALL treat private-network promotion smoke summaries as local Phase 6 evidence maintenance without changing runtime defaults.

#### Scenario: Private-network promotion smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes private-network promotion smoke evidence
- **THEN** the roadmap records it as Phase 6 evidence maintenance and not runtime promotion

#### Scenario: Private-network promotion smoke preserves boundaries

- **WHEN** smoke checks run
- **THEN** they do not execute runtime retrieval changes, model downloads, deployment automation, or control-plane policies

### Requirement: Private-network promotion decision records SHALL be explicit before runtime promotion

The project SHALL preserve a documentation-only decision record for each Qdrant+BGE private-network promotion review cycle before any runtime default promotion.

#### Scenario: Decision record captures keep-default verdict

- **WHEN** review evidence remains `review` or has open gates
- **THEN** the decision record states `keep_runtime_defaults` and lists open gates

#### Scenario: Decision record preserves boundaries

- **WHEN** the decision record is published
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged

### Requirement: Phase 3 hybrid runtime promotion decision review SHALL have a dedicated contract

The project SHALL maintain a documentation-only contract for the final Phase 3 hybrid runtime promotion review before any runtime default switch is considered.

#### Scenario: Hybrid decision contract is phase-aligned and evidence-driven

- **WHEN** a reviewer evaluates whether hybrid runtime defaults can be promoted
- **THEN** the contract lists required Phase 3 and Phase 6 bridge evidence inputs and explicit review-state semantics

#### Scenario: Hybrid decision contract preserves provider boundaries

- **WHEN** the contract is published or refreshed
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG planned boundaries, and caller control-plane ownership remain unchanged

### Requirement: Phase 3 hybrid runtime promotion decision readiness exports stay lightweight and review-only

The project SHALL treat hybrid runtime promotion decision readiness exports as local Phase 3 evidence visibility work without changing runtime defaults.

#### Scenario: Hybrid decision readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes hybrid runtime promotion decision readiness evidence
- **THEN** the roadmap records it as Phase 3 review visibility and not runtime promotion

#### Scenario: Hybrid decision readiness export preserves boundaries

- **WHEN** the export summarizes review signals and open gates
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG planned boundaries, and caller ownership remain unchanged

### Requirement: Phase 3 hybrid runtime promotion decision smoke remains lightweight evidence maintenance

The project SHALL treat Phase 3 hybrid runtime promotion decision smoke as lightweight evidence maintenance when it validates final decision evidence-chain completeness without changing runtime defaults.

#### Scenario: Hybrid decision smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes hybrid runtime promotion decision smoke evidence
- **THEN** the roadmap records it as Phase 3 evidence maintenance and review ergonomics work

#### Scenario: Hybrid decision smoke preserves boundaries

- **WHEN** smoke checks run
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged

### Requirement: Phase 3 hybrid runtime promotion decision SHALL be explicitly recorded

The project SHALL preserve a documentation-only final decision record for each Phase 3 hybrid runtime promotion review cycle before any runtime default promotion.

#### Scenario: Hybrid decision record captures keep-default verdict

- **WHEN** hybrid promotion evidence remains candidate-level or review-level
- **THEN** the decision record states `keep_runtime_defaults` and lists open gates for production promotion

#### Scenario: Hybrid decision record remains boundary-safe

- **WHEN** the hybrid decision record is published
- **THEN** it does not change provider runtime defaults, public API contracts, GraphRAG planned boundary, or caller ownership responsibilities

### Requirement: Phase 6 deployed field validation SHALL be explicitly contract-reviewed

The project SHALL maintain a documentation-only contract for deployed field validation before any runtime default promotion is considered.

#### Scenario: Deployed field validation contract is phase-aligned

- **WHEN** a reviewer evaluates a real deployed URL and its smoke evidence
- **THEN** the contract identifies Phase 6 as the roadmap phase and keeps the scope read-only

#### Scenario: Deployed field validation contract preserves provider boundaries

- **WHEN** the contract is published or refreshed
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged

### Requirement: Phase 6 deployed field validation readiness exports stay lightweight and review-only

The project SHALL treat deployed field validation readiness exports as local Phase 6 evidence visibility work without changing runtime defaults.

#### Scenario: Deployed field validation readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes deployed field validation readiness evidence
- **THEN** the roadmap records it as Phase 6 operations evidence visibility work rather than runtime promotion

#### Scenario: Deployed field validation readiness export preserves boundaries

- **WHEN** the export summarizes deployment readiness, handoff bundle posture, and deployed smoke evidence
- **THEN** runtime defaults, provider HTTP contracts, and external control-plane ownership remain unchanged

### Requirement: Deployed field-validation consistency smoke SHALL be explicit before promotion review

The project SHALL preserve a documentation-only deployed handoff consistency smoke for each Phase 6 field-validation review cycle before any runtime default promotion.

#### Scenario: Consistency smoke captures keep-default posture

- **WHEN** deployed field-validation evidence remains review-level or has open gates
- **THEN** the consistency smoke states that the local artifacts remain aligned without changing runtime defaults

#### Scenario: Consistency smoke preserves boundaries

- **WHEN** the consistency smoke is published
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged

### Requirement: Deployed field-validation decision records SHALL be explicit before promotion review

The project SHALL preserve a documentation-only decision record for each Phase 6 deployed field-validation review cycle before any runtime default promotion.

#### Scenario: Decision record captures keep-default verdict

- **WHEN** deployed field-validation evidence remains review-level or has open gates
- **THEN** the decision record states `keep_local_review_until_deployed_smoke` and lists open gates

#### Scenario: Decision record preserves boundaries

- **WHEN** the decision record is published
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged

### Requirement: Phase 9 MyPrivateAgent local-consumption evidence remains review-only

The project SHALL treat Phase 9 MyPrivateAgent local-consumption readiness and smoke exports as local review evidence without changing runtime defaults.

#### Scenario: Phase 9 readiness summarizes local-consumption posture

- **WHEN** the Phase 9 readiness export is generated
- **THEN** it summarizes local provider URL posture, Phase 7/8 readiness linkage, and caller-boundary ownership notes

#### Scenario: Phase 9 smoke checks local-consumption consistency

- **WHEN** the Phase 9 smoke export is generated
- **THEN** it validates key local-consumption evidence alignment without calling mutating endpoints

#### Scenario: Phase 9 preserves runtime-promotion boundary

- **WHEN** Phase 9 evidence is generated
- **THEN** it does not imply runtime default promotion approval

### Requirement: Phase 10 MyPrivateAgent local consumer verification remains read-only

The project SHALL treat Phase 10 MyPrivateAgent local consumer verification readiness and probe exports as provider-side, read-only verification evidence without changing runtime defaults or caller ownership boundaries.

#### Scenario: Phase 10 readiness summarizes caller-shaped local verification posture

- **WHEN** the Phase 10 local consumer readiness export is generated
- **THEN** it summarizes local provider URL assumptions, Phase 9 linkage, access-key posture, evidence-pack readiness, graph boundary posture, and runtime-promotion boundary status

#### Scenario: Phase 10 probe validates local consumer contract alignment

- **WHEN** the Phase 10 local consumer probe export is generated
- **THEN** it validates key MyPrivateAgent consumer expectations using existing provider evidence without calling mutating endpoints

#### Scenario: Phase 10 preserves provider and caller boundaries

- **WHEN** Phase 10 evidence is generated
- **THEN** it does not imply MyPrivateAgent repository changes, source-to-agent binding mutation, GraphRAG execution approval, or runtime default promotion

