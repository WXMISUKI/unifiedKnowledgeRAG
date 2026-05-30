## ADDED Requirements

### Requirement: Provider discovery exposes source document diagnostics
The provider discovery surface SHALL expose the document source manifest diagnostic capability so external control planes can discover and preflight it before binding.

#### Scenario: Manifest includes source document route template
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include a route template for `GET /api/rag/sources/{source_id}/documents`

#### Scenario: Capabilities include source document diagnostics
- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes `knowledge.rag.source_documents` with a GET invocation, path template, response schema reference, and example source id

#### Scenario: Preflight validates diagnostic capability
- **WHEN** provider preflight runs with default required capability ids
- **THEN** it includes `knowledge.rag.source_documents` in requested capability ids and validates it without requiring a request body schema

#### Scenario: Provider smoke covers diagnostic discovery
- **WHEN** provider contract smoke runs
- **THEN** it verifies manifest and capability metadata for the source document diagnostics surface without executing retrieval, ingestion, or graph work
