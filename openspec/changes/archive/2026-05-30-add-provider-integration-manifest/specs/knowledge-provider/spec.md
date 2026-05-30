## ADDED Requirements

### Requirement: Provider exposes integration manifest
The system SHALL expose a read-only provider integration manifest for external control planes that need to discover provider identity, component role, contract version, key endpoint paths, and supported knowledge capability ids before invoking provider capabilities.

#### Scenario: Manifest exposes provider identity and role
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the response includes provider id, provider name, provider version, manifest version, contract version, component role, and compatible control-plane metadata

#### Scenario: Manifest references integration endpoints
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the response includes stable paths for health, capabilities, OpenAPI schema, provider contract smoke evidence, and core RAG and graph capability endpoints

#### Scenario: Manifest lists supported capability ids
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the response includes `knowledge.rag.retrieve`, `knowledge.rag.answer`, and `knowledge.graph.query` as supported capability ids without exposing provider implementation internals as binding contracts

#### Scenario: Manifest is side-effect free
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the provider does not start ingestion jobs, rebuild indexes, call embedding models, call vector databases, or execute graph queries
