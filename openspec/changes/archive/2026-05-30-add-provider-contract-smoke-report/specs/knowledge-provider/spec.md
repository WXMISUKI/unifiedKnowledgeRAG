## ADDED Requirements

### Requirement: Provider exposes executable contract smoke evidence
The system SHALL provide a local executable smoke report that validates the provider health, capability invocation metadata, document RAG retrieval, cited answer orchestration, and planned graph query boundary without requiring an external server.

#### Scenario: Smoke report passes for default provider configuration
- **WHEN** the smoke report is generated with the default local provider configuration
- **THEN** the report marks itself as passed and includes successful checks for health, capabilities, document retrieval, cited answer, and graph planned boundary behavior

#### Scenario: Smoke report includes integration-critical metadata
- **WHEN** the smoke report validates document retrieval and cited answer endpoints
- **THEN** the report includes evidence that retrieval trace metadata, request filter context metadata, answer trace metadata, and citations are present

#### Scenario: Smoke evidence can be exported
- **WHEN** a caller runs the provider contract smoke export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown evidence files without changing provider HTTP API contracts
