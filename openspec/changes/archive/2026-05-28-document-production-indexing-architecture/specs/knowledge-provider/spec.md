## MODIFIED Requirements

### Requirement: Provider capabilities expose stable knowledge capability ids

The system SHALL expose stable capability identifiers for document RAG retrieval and graph query boundaries while keeping production infrastructure choices behind explicit architecture decision records.

#### Scenario: Capabilities are discoverable

- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes `knowledge.rag.retrieve` and `knowledge.graph.query` capability ids with machine-readable status

#### Scenario: Production infrastructure is not yet selected

- **WHEN** embedding model, vector database, queue worker, reranker, or graph storage choices are still open
- **THEN** provider capabilities remain provider-neutral and do not expose implementation-specific dependency details as API contracts
