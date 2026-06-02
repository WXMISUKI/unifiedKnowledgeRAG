## ADDED Requirements

### Requirement: Phase 11 local provider integration dry-run remains evidence-only

The project SHALL treat Phase 11 MyPrivateAgent local provider integration dry-run artifacts as read-only provider-side evidence that validates local integration assumptions without changing runtime defaults.

#### Scenario: Phase 11 profile and smoke exports summarize integration assumptions

- **WHEN** Phase 11 local integration profile and smoke artifacts are exported
- **THEN** they summarize local URL, access mode, discovery compatibility, retrieval-consumption compatibility, and source-binding preview compatibility for MyPrivateAgent-style local integration

#### Scenario: Phase 11 preserves promotion and ownership boundaries

- **WHEN** Phase 11 dry-run evidence is generated
- **THEN** it does not imply runtime default promotion, GraphRAG execution enablement, source-to-agent binding mutation, or caller control-plane ownership transfer
