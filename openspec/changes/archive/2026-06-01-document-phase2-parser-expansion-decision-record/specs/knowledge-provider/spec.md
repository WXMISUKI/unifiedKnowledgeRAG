## ADDED Requirements

### Requirement: Knowledge provider parser-expansion verdict remains traceable by decision record

The system SHALL keep a documentation-only Phase 2 parser-expansion decision record so reviewers can trace verdict, evidence basis, and open gates from one artifact.

#### Scenario: Decision record references readiness and smoke evidence

- **WHEN** Phase 2 parser-expansion decision record is generated
- **THEN** it references Phase 2 demand contract, source-format demand readiness export, and unsupported-format negative-control smoke

#### Scenario: Decision record does not imply runtime parser promotion

- **WHEN** the current verdict is `keep_markdown_baseline`
- **THEN** provider runtime parser defaults remain unchanged and parser expansion stays a separate future change
