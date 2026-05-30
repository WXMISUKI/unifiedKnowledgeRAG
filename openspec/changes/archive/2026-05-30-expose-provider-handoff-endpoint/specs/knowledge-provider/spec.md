## ADDED Requirements

### Requirement: Provider exposes read-only handoff bundle API

The system SHALL expose the current provider handoff bundle through a read-only HTTP endpoint so external control planes can inspect provider identity, contract version, integration evidence, and operations evidence without reading local files directly.

#### Scenario: Handoff endpoint returns bundle status

- **WHEN** a caller requests `GET /api/provider/handoff`
- **THEN** the response includes the handoff bundle id, status, provider identity, required evidence artifact rows, and operation notes

#### Scenario: Handoff endpoint is advertised by manifest

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include `provider_handoff` with the path `/api/provider/handoff`

#### Scenario: Handoff endpoint fails closed on missing evidence

- **WHEN** a required handoff evidence artifact is missing
- **THEN** the endpoint response marks the artifact as `missing`, marks the bundle status as `blocked`, and recommends regenerating the missing artifact

#### Scenario: Handoff endpoint is side-effect free

- **WHEN** a caller requests `GET /api/provider/handoff`
- **THEN** the provider does not regenerate prerequisite reports, execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, or graph queries
