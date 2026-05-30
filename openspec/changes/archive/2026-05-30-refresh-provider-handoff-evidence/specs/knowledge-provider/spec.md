## ADDED Requirements

### Requirement: Provider handoff evidence can be refreshed locally
The system SHALL provide a local refresh command that regenerates provider handoff prerequisite evidence and the provider handoff bundle in a deterministic order for external control-plane review.

#### Scenario: Handoff evidence refresh runs prerequisite exporters
- **WHEN** the provider handoff evidence refresh command runs
- **THEN** it regenerates provider integration probe, provider contract smoke, deployment readiness, reindex readiness, and provider handoff bundle artifacts in that order

#### Scenario: Handoff evidence refresh writes a summary report
- **WHEN** the provider handoff evidence refresh command completes
- **THEN** it writes machine-readable JSON and human-readable Markdown summary files that include each refresh step, output paths, status, and recommended action

#### Scenario: Handoff evidence refresh fails closed
- **WHEN** a refresh step fails or returns blocked evidence
- **THEN** the refresh summary marks the overall status as `blocked` and identifies the failing step

#### Scenario: Handoff evidence refresh preserves review state
- **WHEN** all refresh steps complete but one regenerated report requires review
- **THEN** the refresh summary marks the overall status as `review` rather than `ready`

#### Scenario: Handoff evidence refresh remains local
- **WHEN** the provider handoff evidence refresh command runs
- **THEN** it does not start a server, add HTTP endpoints, create ingestion jobs, explicitly rebuild indexes, download models, call vector databases, or execute GraphRAG
