## ADDED Requirements

### Requirement: Open-source RAG engine candidates are evaluated through shared evidence

The retrieval benchmark harness SHALL define a common evidence shape for optional open-source RAG engine candidates before any candidate is promoted or integrated as a runtime backend.

#### Scenario: Candidate evaluation uses comparable inputs

- **WHEN** an open-source RAG engine candidate is evaluated
- **THEN** it uses the current canonical fixture cases plus customer-like Chinese cases when available
- **AND** it records the candidate id, candidate type, adapter mode, source corpus, query set, and runtime environment assumptions

#### Scenario: Candidate evaluation reports comparable quality and operations signals

- **WHEN** a candidate evaluation report is exported
- **THEN** it includes citation fidelity, citation granularity, hit/miss behavior, false-positive and false-negative review, latency/resource profile, deployment footprint, backup/recovery posture, private-network feasibility, and dependency/license notes

#### Scenario: Candidate evaluation maps to an explicit decision

- **WHEN** candidate evidence is reviewed
- **THEN** the result is recorded as one of `keep_current_default`, `continue_spike`, or `eligible_for_promotion_review`
- **AND** runtime defaults remain unchanged unless a separate promotion change is approved

### Requirement: Graph-aware and platform candidates preserve GraphRAG boundaries

The retrieval benchmark harness SHALL keep graph-aware or platform candidates behind use-case and evidence gates until relationship-heavy retrieval needs are proven.

#### Scenario: Graph-aware candidate requires relationship-heavy cases

- **WHEN** LightRAG, Microsoft GraphRAG, or another graph-aware candidate is evaluated
- **THEN** the evaluation includes concrete entity, relation, path, and source-evidence expectations before any GraphRAG runtime integration is considered

#### Scenario: Platform candidate may be reference-only

- **WHEN** Dify, Langflow, RAGFlow, or another platform candidate is evaluated for product capability comparison
- **THEN** the evaluation may be recorded as `reference_only` without adding provider dependencies or changing provider runtime behavior
