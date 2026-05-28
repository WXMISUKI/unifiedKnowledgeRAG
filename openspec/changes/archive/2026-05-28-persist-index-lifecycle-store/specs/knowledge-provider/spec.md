## MODIFIED Requirements

### Requirement: Catalog exposes source readiness

The system SHALL expose a source catalog that lists knowledge bases and graph namespaces with stable ids, status, owners, version metadata, backend readiness metadata, and durable source index lifecycle metadata.

#### Scenario: Catalog lists configured sources

- **WHEN** a caller requests `GET /api/catalog`
- **THEN** the response includes `knowledge_bases` and `graphs` arrays with stable source ids, readiness status, document retrieval backend metadata, and source index lifecycle status loaded from the local lifecycle store
