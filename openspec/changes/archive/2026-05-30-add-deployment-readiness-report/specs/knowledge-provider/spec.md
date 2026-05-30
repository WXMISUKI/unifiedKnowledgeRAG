## ADDED Requirements

### Requirement: Provider deployment readiness evidence can be exported
The system SHALL provide a local deployment readiness export that summarizes whether the provider is ready for local binding review and future deployment planning without requiring an external server.

#### Scenario: Readiness export includes core checks
- **WHEN** the deployment readiness export runs
- **THEN** the report includes provider health status, provider preflight bindability, provider contract smoke status, and a combined readiness status

#### Scenario: Readiness export includes configuration review
- **WHEN** the deployment readiness export runs
- **THEN** the report includes retrieval backend, embedding provider, embedding model, answer composer, Qdrant collection settings, and source/index paths without exposing secret values

#### Scenario: Readiness export remains local and read-only
- **WHEN** deployment readiness is exported
- **THEN** it does not start ingestion jobs, rebuild indexes, download models, call embedding services, call vector databases, or execute graph queries

#### Scenario: Readiness evidence writes review artifacts
- **WHEN** a caller runs the deployment readiness export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown evidence files
