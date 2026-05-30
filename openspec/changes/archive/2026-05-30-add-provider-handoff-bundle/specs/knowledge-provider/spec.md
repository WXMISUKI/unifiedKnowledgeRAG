## ADDED Requirements

### Requirement: Provider handoff bundle evidence can be exported
The system SHALL provide a local provider handoff bundle export so external control planes and deployment reviewers can inspect provider identity, contract version, integration evidence, and operations evidence from one review artifact.

#### Scenario: Handoff bundle includes provider identity
- **WHEN** the provider handoff bundle export runs
- **THEN** the report includes provider id, provider name, provider version, contract version, manifest version, and generated timestamp

#### Scenario: Handoff bundle summarizes required evidence artifacts
- **WHEN** the provider handoff bundle export runs
- **THEN** the report includes provider integration probe, provider contract smoke, deployment readiness, and reindex readiness artifact rows with paths, presence, status, summaries, and recommended actions

#### Scenario: Handoff bundle fails closed on missing evidence
- **WHEN** a required evidence artifact is missing
- **THEN** the report marks the artifact as missing, marks the bundle status as `blocked`, and recommends regenerating the missing artifact

#### Scenario: Handoff bundle remains read-only
- **WHEN** the provider handoff bundle export runs
- **THEN** it does not regenerate prerequisite reports, call provider HTTP endpoints, execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, or graph queries

#### Scenario: Handoff bundle writes review artifacts
- **WHEN** a caller runs the provider handoff bundle export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown evidence files
