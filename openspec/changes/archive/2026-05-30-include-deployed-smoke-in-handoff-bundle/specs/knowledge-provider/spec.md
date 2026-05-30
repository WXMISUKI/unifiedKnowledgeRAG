## ADDED Requirements

### Requirement: Provider handoff bundle includes optional deployed smoke evidence

The system SHALL include deployed provider smoke evidence in the provider handoff bundle as optional deployment evidence without requiring a running external provider URL during local handoff generation.

#### Scenario: Missing deployed smoke is reviewable

- **WHEN** the provider handoff bundle is generated and deployed provider smoke evidence is missing
- **THEN** the bundle includes a deployed smoke artifact row with `present=false`, `status=review`, and a recommended action to run deployed smoke after deployment

#### Scenario: Ready deployed smoke is summarized

- **WHEN** deployed provider smoke evidence exists with `status=ready`
- **THEN** the handoff bundle includes it with `status=ready` and summarizes the deployed base URL and handoff status

#### Scenario: Review deployed smoke is preserved

- **WHEN** deployed provider smoke evidence exists with `status=review`
- **THEN** the handoff bundle keeps the overall bundle reviewable rather than marking it ready

#### Scenario: Blocked deployed smoke blocks handoff

- **WHEN** deployed provider smoke evidence exists with `status=blocked`
- **THEN** the handoff bundle marks the deployed smoke row blocked and marks the overall bundle blocked

#### Scenario: Handoff bundle remains read-only

- **WHEN** the provider handoff bundle is generated
- **THEN** it does not run deployed smoke, call provider HTTP endpoints, execute retrieval or answer composition, create ingestion jobs, rebuild indexes, call embedding models, call vector databases, or execute GraphRAG
