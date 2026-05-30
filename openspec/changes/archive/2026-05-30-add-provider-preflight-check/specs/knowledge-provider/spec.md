## ADDED Requirements

### Requirement: Provider exposes binding preflight
The system SHALL expose a read-only provider preflight endpoint that summarizes whether the provider is currently bindable by an external control plane using the provider manifest, health readiness, capability coverage, and schema-reference coverage.

#### Scenario: Preflight passes for default local provider
- **WHEN** a caller requests `GET /api/provider/preflight` with the default local provider configuration
- **THEN** the response marks `bindable=true`, includes provider id and contract version, and includes passed checks for manifest, health, required capabilities, and schema references

#### Scenario: Preflight reports degraded readiness
- **WHEN** provider health is degraded
- **THEN** the preflight response marks `bindable=false` and includes a failed health readiness check with machine-readable details

#### Scenario: Preflight includes planned graph boundary
- **WHEN** graph query execution remains planned
- **THEN** the preflight response still includes `knowledge.graph.query` in required capability coverage while preserving its planned capability status in details

#### Scenario: Preflight is side-effect free
- **WHEN** a caller requests `GET /api/provider/preflight`
- **THEN** the provider does not start ingestion jobs, rebuild indexes, call document retrieval, call answer composition, call embedding models, call vector databases, or execute graph queries
