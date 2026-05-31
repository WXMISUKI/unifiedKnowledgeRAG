## ADDED Requirements

### Requirement: Provider exposes source binding summary

The system SHALL expose a read-only source binding summary for external control planes to review configured knowledge source bindability before making source-to-agent binding decisions.

#### Scenario: Source binding summary lists configured sources

- **WHEN** a caller requests `GET /api/provider/source-bindings`
- **THEN** the response includes each configured knowledge base with source id, owner, source status, retrieval backend, backend status, index status, document count, drift statuses, bindability, and recommended action

#### Scenario: Ready source is bindable

- **WHEN** a source has ready catalog status, ready retrieval backend, ready index status, in-sync document fingerprints, and ready ingestion preflight
- **THEN** the source binding row marks `bindable=true`, `status=ready`, and recommends `bind_source_from_control_plane`

#### Scenario: Drifted source is blocked

- **WHEN** a source document fingerprint is `changed` or `missing`
- **THEN** the source binding row marks `bindable=false`, `status=blocked`, and recommends repairing or reingesting the source before binding

#### Scenario: Summary is advertised by manifest

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include `source_bindings` with the path `/api/provider/source-bindings`

#### Scenario: Source binding summary is read-only

- **WHEN** a caller requests `GET /api/provider/source-bindings`
- **THEN** the provider does not create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG
