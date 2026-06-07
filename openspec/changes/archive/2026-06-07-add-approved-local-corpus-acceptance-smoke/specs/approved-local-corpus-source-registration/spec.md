## ADDED Requirements

### Requirement: Registered local corpus can feed acceptance smoke
The system SHALL allow a registered approved local corpus source to be used as input for a separate local acceptance smoke.

#### Scenario: Registered source feeds acceptance smoke
- **WHEN** an approved local source has `registration_status=registered`
- **THEN** an acceptance smoke can use that source id for catalog, manifest, retrieve, and answer checks

#### Scenario: Missing registration blocks acceptance smoke
- **WHEN** the approved local source registry does not contain the requested source id
- **THEN** the acceptance smoke reports `decision=blocked`
