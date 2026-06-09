## ADDED Requirements

### Requirement: Source onboarding artifacts can be discovered through a unified catalog view
The system SHALL allow existing source onboarding artifacts to be scanned and summarized through a unified discovery view without changing runtime retrieval defaults.

#### Scenario: Onboarding catalog summarizes per-source artifact presence
- **WHEN** the source onboarding catalog is exported from the onboarding artifact root
- **THEN** the report includes one entry per discovered `source_id`
- **AND** each entry records template presence, real baseline fixture presence, validation report presence, and current onboarding status

#### Scenario: Validation-ready sources expose current decision
- **WHEN** a source onboarding directory includes a real validation report
- **THEN** the catalog entry records the validation decision and reason code
- **AND** callers can use it as evidence-only onboarding readiness signal

### Requirement: Onboarding discovery stays lighter than source registration
The system SHALL treat onboarding discovery as evidence-only source visibility rather than provider registration or aggregate-baseline expansion.

#### Scenario: Onboarding catalog does not register or promote sources
- **WHEN** the source onboarding catalog is exported
- **THEN** it does not automatically register a source into the provider runtime catalog
- **AND** it does not automatically add the source into the aggregate real-business baseline

#### Scenario: Template-only sources remain visible without fake promotion
- **WHEN** a source onboarding directory only contains generated templates and no real baseline validation report
- **THEN** the catalog still exposes that source as a visible onboarding entry
- **AND** the entry remains in a template-only or review-like state rather than a ready runtime state
