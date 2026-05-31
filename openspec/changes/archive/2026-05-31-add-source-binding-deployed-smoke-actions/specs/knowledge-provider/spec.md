## ADDED Requirements

### Requirement: Deployed smoke summarizes source binding actions

The system SHALL include compact source status and recommended action rollups when deployed provider smoke validates live source binding evidence.

#### Scenario: Deployed smoke summarizes source binding statuses

- **WHEN** the deployed provider smoke probe receives source binding summary evidence from `GET /api/provider/source-bindings`
- **THEN** the `provider_source_bindings` check details include counts for source binding row statuses

#### Scenario: Deployed smoke summarizes source binding recommended actions

- **WHEN** the deployed provider smoke probe receives source binding summary evidence from `GET /api/provider/source-bindings`
- **THEN** the `provider_source_bindings` check details include counts for source binding recommended actions

#### Scenario: Deployed smoke source binding action summary remains read-only

- **WHEN** source binding status and action counts are summarized in deployed provider smoke evidence
- **THEN** the probe does not create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG
