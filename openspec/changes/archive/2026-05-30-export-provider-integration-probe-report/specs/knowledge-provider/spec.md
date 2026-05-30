## ADDED Requirements

### Requirement: Provider integration probe evidence can be exported
The system SHALL provide a local export command for provider integration probe evidence so external control planes can persist machine-readable and human-readable provider binding results.

#### Scenario: Integration probe evidence exports for default provider
- **WHEN** a caller runs the provider integration probe export command with the default local provider configuration
- **THEN** the system writes JSON and Markdown files that include provider identity, contract version, requested binding requirements, bindable status, preflight checks, capability binding statuses, invocation paths, and example request coverage

#### Scenario: Integration probe export fails closed
- **WHEN** the integration probe report is not bindable
- **THEN** the export command still writes evidence files and exits with a failure status

#### Scenario: Integration probe export remains read-only
- **WHEN** the integration probe export command runs
- **THEN** it does not execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, or graph queries

#### Scenario: Integration probe Markdown is reviewable
- **WHEN** the integration probe Markdown report is rendered
- **THEN** it summarizes provider identity, bindability, preflight checks, capability ids, statuses, invocation paths, and example request coverage without embedding full request payloads
