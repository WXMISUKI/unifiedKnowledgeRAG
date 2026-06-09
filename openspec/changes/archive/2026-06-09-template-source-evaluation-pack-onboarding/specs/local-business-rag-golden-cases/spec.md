## ADDED Requirements

### Requirement: New sources can receive standardized evaluation-pack templates
The system SHALL provide a standardized onboarding helper for future sources so baseline, failed-question, and confirmation pack templates can be generated without hand-copying existing fixtures.

#### Scenario: Onboarding helper writes three pack templates and a manifest
- **WHEN** source evaluation pack onboarding is exported for a new `source_id`
- **THEN** it writes baseline, failed-question, and confirmation fixture templates
- **AND** it writes a machine-readable onboarding manifest plus a Markdown guide

#### Scenario: Templates expose minimal required fields only
- **WHEN** the onboarding helper generates a pack template
- **THEN** each template includes the minimum required fields for that pack family
- **AND** the template remains clearly marked as scaffolding rather than a completed evaluation artifact

### Requirement: Onboarding templates remain evidence-only and strategy-neutral
The system SHALL treat source evaluation pack onboarding as template generation only, without changing runtime retrieval behavior or strategy gates.

#### Scenario: Onboarding helper does not run evaluation or change runtime defaults
- **WHEN** onboarding templates are generated
- **THEN** the helper does not execute retrieve/answer evaluation or promote any runtime strategy
- **AND** query rewrite, rerank, hybrid retrieval, source binding changes, and GraphRAG execution remain unchanged

#### Scenario: Onboarding manifest gives conservative next steps
- **WHEN** onboarding completes
- **THEN** the manifest lists conservative next steps for filling the templates and exporting real packs
- **AND** it does not automatically infer business questions or failure classes
