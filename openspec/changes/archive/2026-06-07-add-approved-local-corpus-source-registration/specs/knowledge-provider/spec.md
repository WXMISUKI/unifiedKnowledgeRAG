## MODIFIED Requirements

### Requirement: Catalog exposes source readiness

The system SHALL expose a source catalog that lists knowledge bases and graph namespaces with stable ids, status, owners, version metadata, backend readiness metadata, durable source index lifecycle metadata, and explicitly approved local corpus sources.

#### Scenario: Catalog lists configured sources

- **WHEN** a caller requests `GET /api/catalog`
- **THEN** the response includes `knowledge_bases` and `graphs` arrays with stable source ids, readiness status, document retrieval backend metadata, and source index lifecycle status loaded from the local lifecycle store

#### Scenario: Catalog lists approved local corpus source

- **WHEN** an approved local source registry contains a registered source
- **THEN** the provider catalog includes that source id with owner, version, backend readiness, and index lifecycle metadata
- **AND** known-source checks accept that source id for RAG retrieve and answer requests
