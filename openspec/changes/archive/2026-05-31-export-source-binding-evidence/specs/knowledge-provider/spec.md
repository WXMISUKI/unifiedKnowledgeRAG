## ADDED Requirements

### Requirement: Source binding summary evidence can be exported

The system SHALL provide a local export command for source binding summary evidence so deployment reviewers and external control planes can inspect source bindability from persisted handoff artifacts.

#### Scenario: Source binding evidence export writes artifacts

- **WHEN** a caller runs the source binding evidence export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown files containing source bindability status, recommended actions, and operation notes

#### Scenario: Source binding evidence participates in handoff bundle

- **WHEN** the provider handoff bundle is generated
- **THEN** it includes source binding evidence as a required local artifact and summarizes ready, review, blocked, or missing evidence states

#### Scenario: Handoff refresh regenerates source binding evidence

- **WHEN** the provider handoff evidence refresh command runs
- **THEN** it regenerates source binding evidence before regenerating the provider handoff bundle

#### Scenario: Source binding evidence export remains read-only

- **WHEN** source binding evidence is exported or refreshed
- **THEN** it does not create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG
