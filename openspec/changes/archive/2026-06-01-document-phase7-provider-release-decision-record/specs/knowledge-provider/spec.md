## ADDED Requirements

### Requirement: Knowledge provider release verdict remains traceable by Phase 7 decision record

The system SHALL keep a documentation-only Phase 7 release decision record so callers and reviewers can trace current verdict, evidence basis, and open gates from one artifact.

#### Scenario: Decision record references Phase 7 acceptance, readiness, and smoke

- **WHEN** Phase 7 release decision record is authored
- **THEN** it references the Phase 7 acceptance contract, Phase 7 release-readiness export, and Phase 7 cross-phase consistency smoke

#### Scenario: Decision record does not imply runtime promotion

- **WHEN** the current verdict is not runtime-promotion-ready
- **THEN** runtime defaults remain unchanged and promotion remains separately gated
