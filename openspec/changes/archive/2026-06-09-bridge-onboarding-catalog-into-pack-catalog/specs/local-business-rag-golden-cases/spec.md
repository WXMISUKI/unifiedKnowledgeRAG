## ADDED Requirements

### Requirement: Source evaluation pack catalog can expose onboarding maturity summary
The system SHALL allow the source evaluation pack catalog to expose a lightweight summary of source onboarding maturity without changing pack-level evaluation semantics.

#### Scenario: Pack catalog includes onboarding summary when onboarding catalog is present
- **WHEN** the source evaluation pack catalog is exported and `source-onboarding-catalog.json` is present
- **THEN** the pack catalog summary includes onboarding source counts and ready/template-only source summaries
- **AND** callers can inspect onboarding maturity from the pack-level discovery view

#### Scenario: Missing onboarding catalog does not block pack catalog export
- **WHEN** the source evaluation pack catalog is exported and `source-onboarding-catalog.json` is absent
- **THEN** the pack catalog still exports successfully
- **AND** the summary records that the onboarding catalog is not present

### Requirement: Onboarding bridge remains evidence-only and non-authoritative for pack decisions
The system SHALL treat onboarding summary data as optional discovery context rather than authoritative pack decision input.

#### Scenario: Onboarding summary does not override pack decision logic
- **WHEN** the source evaluation pack catalog includes onboarding summary data
- **THEN** the catalog `decision` continues to be derived from evaluation pack availability and pack decisions
- **AND** onboarding-ready sources do not automatically change a `review` or `blocked` pack catalog into `go`

#### Scenario: Onboarding summary does not imply runtime registration or aggregate expansion
- **WHEN** onboarding-ready sources appear in the pack catalog summary
- **THEN** the provider still treats them as evidence-only onboarding signals
- **AND** it does not automatically register them into runtime or expand the main aggregate baseline
