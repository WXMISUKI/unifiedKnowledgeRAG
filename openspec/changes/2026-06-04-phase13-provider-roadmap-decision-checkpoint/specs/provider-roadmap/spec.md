## ADDED Requirements

### Requirement: Phase 13 provider roadmap decision checkpoint stays global and provider-first

The project SHALL export a local Phase 13 provider-roadmap decision checkpoint that consolidates the current Phase 12b through Phase 12f evidence chain, provider handoff visibility, and roadmap posture into one review artifact before any further backend spike is chosen.

#### Scenario: Phase 13 checkpoint exports a global recommendation

- **WHEN** the Phase 13 checkpoint is exported
- **THEN** it records the current Phase 12b through Phase 12f evidence chain and the next recommended focus
- **AND** it prefers resuming provider integration hardening when pgvector live-probe evidence is still blocked or only rerun-ready

#### Scenario: Phase 13 keeps backend tuning bounded

- **WHEN** the checkpoint is reviewed
- **THEN** it treats pgvector as candidate-only
- **AND** it does not start a Phase 12g tuning loop by default
- **AND** it does not change runtime defaults

#### Scenario: Phase 13 preserves ownership boundaries

- **WHEN** the checkpoint is consumed
- **THEN** caller control-plane ownership, GraphRAG execution, and final promotion decisions remain outside this provider

### Requirement: Phase 13 checkpoint remains visible in handoff evidence

The project SHALL surface the Phase 13 provider-roadmap decision checkpoint through provider handoff bundle and refresh evidence as optional review input.

#### Scenario: Handoff visibility includes the checkpoint

- **WHEN** provider handoff bundle or refresh evidence is regenerated
- **THEN** the Phase 13 checkpoint appears as optional evidence with its decision and recommendation

#### Scenario: The checkpoint stays review-only

- **WHEN** the Phase 13 checkpoint is reviewed
- **THEN** it remains read-only
- **AND** it does not imply runtime promotion or backend migration by itself
