## ADDED Requirements

### Requirement: Provider integration probe supports external control-plane binding
The system SHALL provide a local read-only integration probe that external control planes can use as a reference binding flow for provider manifest, preflight, and capability discovery.

#### Scenario: Integration probe passes for default provider
- **WHEN** the integration probe runs against the default local provider with the current contract version and stable knowledge capability ids
- **THEN** it returns a machine-readable report with `bindable=true`, provider identity, manifest version, contract version, capability ids, capability statuses, invocation paths, and example request coverage

#### Scenario: Integration probe fails closed on incompatible requirements
- **WHEN** the integration probe is run with an unsupported required contract version or required capability id
- **THEN** it returns `bindable=false` and includes preflight check details that identify the incompatible requirement

#### Scenario: Integration probe is read-only
- **WHEN** the integration probe runs
- **THEN** it does not execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, or graph queries

#### Scenario: Integration probe preserves invocation examples
- **WHEN** the integration probe collects capability metadata
- **THEN** it includes each requested capability invocation and provider-owned example request without executing the example request
