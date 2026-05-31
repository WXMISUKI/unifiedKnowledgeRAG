## ADDED Requirements

### Requirement: Evidence refresh maintenance command remains explicit

The project SHALL keep the local evidence refresh maintenance command explicit in roadmap-adjacent tracking docs so current evidence state is reproducible and not confused with historical milestones.

#### Scenario: Tracker distinguishes historical and current benchmark baseline

- **WHEN** benchmark baseline size changes across archived Phase 3 slices
- **THEN** tracker wording marks older counts as historical and keeps the current canonical count explicit

#### Scenario: Tracker documents maintenance command

- **WHEN** reviewers need to refresh local handoff evidence
- **THEN** tracker documents `python scripts/export_provider_handoff_refresh.py` as the standard maintenance command
