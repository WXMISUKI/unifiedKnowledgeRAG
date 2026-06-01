## ADDED Requirements

### Requirement: Graph boundary smoke summaries advance Phase 5 without executing GraphRAG

The project SHALL treat a local graph boundary smoke summary as Phase 5 boundary work when it consolidates graph schema discovery and the planned graph query boundary without adding graph execution or graph-store dependencies.

#### Scenario: Graph boundary smoke summary is phase-aligned

- **WHEN** an OpenSpec change adds a graph boundary smoke summary
- **THEN** the roadmap records it as lightweight Phase 5 GraphRAG boundary/readiness work rather than graph execution promotion

#### Scenario: Graph boundary smoke summary preserves graph gate

- **WHEN** the summary consolidates graph schema discovery or planned query boundaries
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes
