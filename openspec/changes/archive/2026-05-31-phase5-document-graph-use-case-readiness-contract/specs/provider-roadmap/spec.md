## ADDED Requirements

### Requirement: Graph use-case readiness contracts advance Phase 5 without executing GraphRAG

The project SHALL treat a local graph use-case readiness contract as Phase 5 boundary work when it explains which questions are graph-worthy and which should remain in document RAG without adding graph execution or graph-store dependencies.

#### Scenario: Graph use-case readiness contract is phase-aligned

- **WHEN** an OpenSpec change adds a graph use-case readiness contract document
- **THEN** the roadmap records it as lightweight Phase 5 GraphRAG boundary/readiness work rather than graph execution promotion

#### Scenario: Graph use-case readiness contract preserves graph gate

- **WHEN** the contract documents relationship-heavy cases, document-RAG-only cases, or source evidence rules
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes
