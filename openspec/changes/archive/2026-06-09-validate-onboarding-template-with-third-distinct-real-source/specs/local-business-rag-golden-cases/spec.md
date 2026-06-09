## ADDED Requirements

### Requirement: A third distinct real source can validate the onboarding template path through a minimal baseline
The system SHALL allow a third distinct lightweight real source type to validate the onboarding template path by producing a minimal local baseline report without changing runtime strategy defaults.

#### Scenario: Lightweight invoice-policy source can produce a minimal baseline report
- **WHEN** `invoice_policy_faq` is validated through the standard onboarding and local baseline path
- **THEN** the provider can generate onboarding templates, a filled baseline fixture, and a local baseline report for that source
- **AND** the result remains evidence-only rather than a runtime strategy promotion

#### Scenario: Validation source preserves answerable and fail-closed structure
- **WHEN** the minimal baseline for the third distinct real source is exported
- **THEN** it includes answerable and expected-empty cases
- **AND** advanced retrieval strategies remain unchanged

### Requirement: Third-source validation remains smaller than aggregate expansion
The system SHALL treat the third distinct source onboarding validation as a template-path proof rather than an immediate aggregate baseline expansion.

#### Scenario: Validation does not automatically expand main breadth baseline
- **WHEN** the third distinct source baseline report is exported
- **THEN** the source can remain outside the main multi-source aggregate baseline
- **AND** callers can use the result as template-path evidence before any future breadth-expansion decision
