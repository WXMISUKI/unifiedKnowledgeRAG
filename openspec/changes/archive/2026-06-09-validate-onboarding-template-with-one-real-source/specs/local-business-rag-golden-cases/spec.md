## ADDED Requirements

### Requirement: A new real source can validate the onboarding template path through a minimal baseline
The system SHALL allow at least one new real source to validate the onboarding template path by producing a minimal local baseline report without changing runtime strategy defaults.

#### Scenario: Split refund source can produce a minimal baseline report
- **WHEN** `split_refund_policy_docs` is validated through the standard onboarding and local baseline path
- **THEN** the provider can generate onboarding templates, a filled baseline fixture, and a local baseline report for that source
- **AND** the result remains evidence-only rather than a runtime strategy promotion

#### Scenario: Validation source keeps fail-closed behavior visible
- **WHEN** the minimal baseline for the new real source includes an expected-empty negative control
- **THEN** the report still records whether the source fails closed without endorsed citations
- **AND** advanced retrieval strategies remain unchanged

### Requirement: New-source onboarding validation remains smaller than source expansion
The system SHALL treat the first real-source onboarding validation as a template-path proof rather than an immediate aggregate baseline expansion.

#### Scenario: Validation does not force aggregate expansion
- **WHEN** the first new real source baseline report is exported
- **THEN** the source can remain outside the main multi-source aggregate baseline
- **AND** callers can use the result as template-path evidence before deciding whether to expand aggregate breadth
