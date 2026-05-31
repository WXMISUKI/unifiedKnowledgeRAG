## ADDED Requirements

### Requirement: Provider handoff summarizes source binding actions

The system SHALL include compact source status and recommended action rollups when the provider handoff bundle summarizes existing source binding evidence.

#### Scenario: Handoff summarizes source binding statuses

- **WHEN** the provider handoff bundle reads present source binding summary evidence
- **THEN** the `source_binding_summary` artifact summary includes counts for source binding row statuses

#### Scenario: Handoff summarizes source binding recommended actions

- **WHEN** the provider handoff bundle reads present source binding summary evidence
- **THEN** the `source_binding_summary` artifact summary includes counts for source binding recommended actions

#### Scenario: Handoff source binding action summary remains read-only

- **WHEN** source binding status and action counts are summarized in provider handoff evidence
- **THEN** the provider does not regenerate evidence, call provider HTTP endpoints, create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG
