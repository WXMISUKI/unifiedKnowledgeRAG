## ADDED Requirements

### Requirement: Phase 6 Qdrant backup/restore smoke stays lightweight and read-only

The project SHALL treat Phase 6 Qdrant backup/restore smoke summaries as local operations evidence maintenance without changing runtime defaults.

#### Scenario: Backup/restore smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes Qdrant backup/restore smoke evidence
- **THEN** the roadmap records it as Phase 6 evidence maintenance work rather than runtime promotion

#### Scenario: Backup/restore smoke preserves boundaries

- **WHEN** smoke summaries validate backup/restore prerequisites
- **THEN** they do not execute backup/restore actions and do not move control-plane ownership into the provider
