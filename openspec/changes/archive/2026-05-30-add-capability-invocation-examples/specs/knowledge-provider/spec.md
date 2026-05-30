## ADDED Requirements

### Requirement: Provider capability invocations include example requests
The system SHALL include provider-owned example request payloads in capability invocation metadata for stable knowledge capability ids so external control planes can construct first-call probes without relying on implementation-specific defaults.

#### Scenario: Retrieval capability includes an example request
- **WHEN** a caller inspects the `knowledge.rag.retrieve` capability from `GET /api/capabilities`
- **THEN** its invocation metadata includes an `example_request` with a query, at least one knowledge base id, a bounded `top_k`, and integration filter context

#### Scenario: Answer capability includes an example request
- **WHEN** a caller inspects the `knowledge.rag.answer` capability from `GET /api/capabilities`
- **THEN** its invocation metadata includes an `example_request` compatible with the cited answer request schema

#### Scenario: Graph capability example preserves planned boundary
- **WHEN** a caller inspects the `knowledge.graph.query` capability from `GET /api/capabilities`
- **THEN** its invocation metadata includes an `example_request` compatible with the graph query request schema while the capability status remains `planned`

#### Scenario: Invocation examples remain provider neutral
- **WHEN** invocation examples are exposed
- **THEN** they do not expose embedding model, vector database, reranker, graph store, or answer composer implementation details as API contracts
