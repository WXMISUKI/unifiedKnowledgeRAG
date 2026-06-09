## ADDED Requirements

### Requirement: Template onboarding example can become a real minimal baseline example
The system SHALL allow the existing template onboarding example to be promoted into a real minimal baseline example without changing runtime retrieval defaults.

#### Scenario: Template example can export a real baseline validation report
- **WHEN** `source_template_example` is validated through the standard onboarding and local baseline path
- **THEN** the provider can generate a real baseline fixture and a local baseline validation report for that example source
- **AND** the result remains evidence-only rather than a runtime strategy promotion

#### Scenario: Template example keeps answerable and fail-closed structure
- **WHEN** the real minimal baseline for `source_template_example` is exported
- **THEN** it includes answerable and expected-empty cases
- **AND** advanced retrieval strategies remain unchanged

### Requirement: Real example promotion improves onboarding discovery without aggregate expansion
The system SHALL treat the promoted template example as onboarding proof and discovery improvement rather than immediate aggregate baseline expansion.

#### Scenario: Promoted example no longer appears as template-only
- **WHEN** the source onboarding catalog is refreshed after `source_template_example` receives a real baseline validation report
- **THEN** the example source no longer appears in `template_only_source_ids`
- **AND** it appears as an onboarding-ready source

#### Scenario: Promoted example still does not auto-expand main baseline
- **WHEN** `source_template_example` passes its real minimal baseline validation
- **THEN** the source remains outside the main aggregate real-business baseline unless a future change explicitly adds it
- **AND** pack-level summary treats it as onboarding evidence only
