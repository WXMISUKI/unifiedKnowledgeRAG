## MODIFIED Requirements

### Requirement: Provider exposes source binding summary

The system SHALL expose a read-only source binding summary for external control planes to review configured knowledge source bindability, source package context, and binding evidence coverage before making source-to-agent binding decisions.

#### Scenario: Source binding summary lists configured sources

- **WHEN** a caller requests `GET /api/provider/source-bindings`
- **THEN** the response includes each configured knowledge base with source id, owner, source status, source domain, language, sensitivity, supported formats, citation granularity, retrieval backend, backend status, index status, document count, citation anchor count, chunk manifest count, parser-ready document count, unsupported document count, drift statuses, bindability, and recommended action

#### Scenario: Ready source is bindable

- **WHEN** a source has ready catalog status, ready retrieval backend, ready index status, in-sync document fingerprints, and ready ingestion preflight
- **THEN** the source binding row marks `bindable=true`, `status=ready`, and recommends `bind_source_from_control_plane`

#### Scenario: Package context fields are informational

- **WHEN** a source binding row includes domain, language, sensitivity, supported formats, and citation granularity
- **THEN** those fields summarize existing source package diagnostics without changing binding decisions by themselves

#### Scenario: Coverage fields are informational

- **WHEN** a source binding row includes citation, chunk, and parser coverage counts
- **THEN** those fields summarize existing manifest and preflight diagnostics without changing binding decisions by themselves

#### Scenario: Drifted source is blocked

- **WHEN** a source document fingerprint is `changed` or `missing`
- **THEN** the source binding row marks `bindable=false`, `status=blocked`, and recommends repairing or reingesting the source before binding

#### Scenario: Summary is advertised by manifest

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include `source_bindings` with the path `/api/provider/source-bindings`

#### Scenario: Source binding summary is read-only

- **WHEN** a caller requests `GET /api/provider/source-bindings`
- **THEN** the provider does not create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG

### Requirement: Source binding summary evidence can be exported

The system SHALL provide a local export command for source binding summary evidence so deployment reviewers and external control planes can inspect source bindability, source package context, and binding evidence coverage from persisted handoff artifacts.

#### Scenario: Source binding evidence export writes artifacts

- **WHEN** a caller runs the source binding evidence export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown files containing source bindability status, source package context, coverage counts, recommended actions, and operation notes

#### Scenario: Source binding evidence participates in handoff bundle

- **WHEN** the provider handoff bundle is generated
- **THEN** it includes source binding evidence as a required local artifact and summarizes ready, review, blocked, or missing evidence states

#### Scenario: Handoff refresh regenerates source binding evidence

- **WHEN** the provider handoff evidence refresh command runs
- **THEN** it regenerates source binding evidence before regenerating the provider handoff bundle

#### Scenario: Source binding evidence export remains read-only

- **WHEN** source binding evidence is exported or refreshed
- **THEN** it does not create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG
