## ADDED Requirements

### Requirement: Provider health reports machine-readable readiness

The system SHALL expose provider health with machine-readable service, RAG, and graph readiness fields.

#### Scenario: Provider health is ready

- **WHEN** a caller requests `GET /health`
- **THEN** the response includes `status`, `service`, `rag.status`, and `graph.status`

### Requirement: Provider capabilities expose stable knowledge capability ids

The system SHALL expose stable capability identifiers for document RAG retrieval and graph query boundaries.

#### Scenario: Capabilities are discoverable

- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes `knowledge.rag.retrieve` and `knowledge.graph.query` capability ids with machine-readable status

### Requirement: Catalog exposes source readiness

The system SHALL expose a source catalog that lists knowledge bases and graph namespaces with stable ids, status, owners, and version metadata.

#### Scenario: Catalog lists configured sources

- **WHEN** a caller requests `GET /api/catalog`
- **THEN** the response includes `knowledge_bases` and `graphs` arrays with stable source ids and readiness status

### Requirement: Graph schema boundary is explicit

The system SHALL expose graph schema metadata separately from document RAG retrieval.

#### Scenario: Graph schemas are discoverable

- **WHEN** a caller requests `GET /api/graph/schemas`
- **THEN** the response includes graph ids and serializable schema metadata

### Requirement: Graph query boundary returns structured status

The system SHALL expose a graph query endpoint that returns serializable graph result envelopes or structured provider errors.

#### Scenario: Graph query is not implemented in first slice

- **WHEN** a caller requests `POST /api/graph/query` during the document-RAG-only slice
- **THEN** the response uses a structured error code that states graph query execution is not implemented
