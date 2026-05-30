## ADDED Requirements

### Requirement: Provider deployed HTTP smoke evidence can be exported

The system SHALL provide a read-only deployed provider smoke probe that validates an already-running provider component over HTTP using a configured base URL and optional provider API credentials.

#### Scenario: Deployed smoke validates public health

- **WHEN** the deployed smoke probe runs against a reachable provider base URL
- **THEN** it requests `GET /health` without provider API credentials and records the provider health status in the exported evidence

#### Scenario: Deployed smoke validates authenticated discovery

- **WHEN** the deployed smoke probe runs with a provider API key
- **THEN** it sends provider API credentials to `GET /api/provider/manifest`, `GET /api/provider/preflight`, and `GET /api/provider/handoff`

#### Scenario: Deployed smoke writes review artifacts

- **WHEN** the deployed smoke export command completes
- **THEN** it writes machine-readable JSON and human-readable Markdown files with base URL, check status, provider identity, handoff status, and operation notes without writing secret values

#### Scenario: Deployed smoke fails closed

- **WHEN** the provider base URL is unreachable, returns a non-200 discovery response, returns invalid JSON, exposes an incompatible manifest or preflight, or reports blocked handoff evidence
- **THEN** the deployed smoke report marks status `blocked` and the export command exits with a failure status after writing evidence when possible

#### Scenario: Deployed smoke remains read-only

- **WHEN** deployed smoke runs
- **THEN** it does not execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, model downloads, or GraphRAG
