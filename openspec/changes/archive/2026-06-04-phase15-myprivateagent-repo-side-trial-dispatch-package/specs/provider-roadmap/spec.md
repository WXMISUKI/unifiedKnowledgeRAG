## ADDED Requirements

### Requirement: Phase 15 MyPrivateAgent repo-side trial dispatch package stays provider-first
The project SHALL export a local Phase 15 MyPrivateAgent repo-side trial dispatch package that consolidates the current Phase 10, Phase 11, Phase 13, and Phase 14 evidence chain into one caller-facing dispatch artifact before any repo-side trial is initiated.

#### Scenario: Phase 15 dispatch package exports a caller-facing verdict
- **WHEN** the Phase 15 dispatch package is exported
- **THEN** it records the current local consumer, local provider integration, roadmap checkpoint, and acceptance posture
- **AND** it produces a dispatch verdict and caller checklist
- **AND** it keeps runtime defaults unchanged

#### Scenario: Phase 15 dispatch package preserves provider-only boundaries
- **WHEN** the dispatch package is reviewed
- **THEN** it uses provider-owned evidence and local environment posture
- **AND** it does not create source-to-agent binding
- **AND** it does not assume caller control-plane ownership
- **AND** it does not execute a repo-side trial

### Requirement: Phase 15 dispatch package classifies blockers explicitly
The project SHALL classify Phase 15 blockers so follow-up actions can distinguish provider evidence gaps, handoff visibility gaps, and external local environment readiness from a ready dispatch package.

#### Scenario: Blocker category is explicit when the dispatch package is not ready
- **WHEN** the Phase 15 dispatch package is not ready for repo-side trial dispatch
- **THEN** it records whether the blocker is provider evidence, handoff visibility, or external local environment readiness
- **AND** it keeps the next recommended action explicit
- **AND** it emits a caller checklist that reflects the blocker category

### Requirement: Phase 15 dispatch package remains visible in handoff evidence
The project SHALL surface the Phase 15 dispatch package through provider handoff bundle and refresh evidence as optional review input.

#### Scenario: Handoff visibility includes Phase 15
- **WHEN** provider handoff bundle or refresh evidence is regenerated
- **THEN** the Phase 15 dispatch package appears as optional evidence with its verdict and recommended next action

#### Scenario: Phase 15 dispatch package stays read-only
- **WHEN** the dispatch package is consumed
- **THEN** it remains read-only
- **AND** it does not imply runtime promotion, backend migration, or binding creation by itself
