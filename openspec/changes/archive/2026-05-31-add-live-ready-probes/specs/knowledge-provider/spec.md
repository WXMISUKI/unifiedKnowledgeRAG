## ADDED Requirements

### Requirement: Provider exposes separate liveness and readiness probes

The system SHALL expose lightweight liveness and readiness probes for high-availability deployments while keeping `/health` compatible.

#### Scenario: Liveness probe is side-effect free

- **WHEN** a caller requests `GET /live`
- **THEN** the response reports the provider process as live without constructing retrieval backends, checking indexes, running answer readiness, executing ingestion, calling vector stores, or executing GraphRAG

#### Scenario: Readiness probe reports traffic readiness

- **WHEN** a caller requests `GET /ready`
- **THEN** the response includes the same machine-readable readiness details as `/health` for service, RAG, answer, and graph status

#### Scenario: Health endpoint remains compatible

- **WHEN** a caller requests `GET /health`
- **THEN** the endpoint continues to return the existing readiness response shape

#### Scenario: Manifest advertises operational probes

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include `live` and `ready` paths for external discovery
