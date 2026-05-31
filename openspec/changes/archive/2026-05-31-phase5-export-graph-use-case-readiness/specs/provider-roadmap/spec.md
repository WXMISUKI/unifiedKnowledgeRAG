## ADDED Requirements

### Requirement: Graph use-case readiness exports advance Phase 5 without executing GraphRAG

The project SHALL treat a local graph use-case readiness export as Phase 5 boundary work when it consolidates graph use-case contract evidence and planned graph query boundaries without adding graph execution or graph-store dependencies.

#### Scenario: Graph use-case readiness export is phase-aligned

- **WHEN** an OpenSpec change adds a graph use-case readiness export
- **THEN** the roadmap records it as lightweight Phase 5 GraphRAG boundary/readiness work rather than graph execution promotion

#### Scenario: Graph use-case readiness export preserves graph gate

- **WHEN** the export summarizes graph schema discovery, graph statuses, or planned query boundaries
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes
