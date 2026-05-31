## ADDED Requirements

### Requirement: Graph boundary preflight summaries advance use-case-driven GraphRAG readiness

The project SHALL treat graph namespace summaries in provider preflight as Phase 5 boundary evidence when they help callers discover planned graph capability without adding graph execution or graph-store dependencies.

#### Scenario: Graph boundary preflight summary is phase-aligned

- **WHEN** an OpenSpec change adds graph schema counts or graph namespace ids to provider preflight evidence
- **THEN** the roadmap records it as lightweight Phase 5 GraphRAG boundary/readiness work rather than graph execution promotion

#### Scenario: Graph boundary preflight summary preserves graph gate

- **WHEN** provider preflight summarizes graph namespaces
- **THEN** graph query execution, graph storage, entity extraction, ontology workflows, source-to-graph indexing, and GraphRAG retrieval remain behind separate evidence-backed changes
