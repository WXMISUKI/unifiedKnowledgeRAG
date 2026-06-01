## ADDED Requirements

### Requirement: Qdrant deployment/backup/recovery readiness is treated as Phase 6 operations evidence

The project SHALL treat Qdrant vector-store deployment, backup, and recovery readiness as lightweight Phase 6 operations evidence without changing runtime defaults.

#### Scenario: Qdrant readiness contract is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes Qdrant deployment/backup/recovery readiness evidence
- **THEN** the roadmap records it as Phase 6 operations work instead of retrieval runtime promotion

#### Scenario: Qdrant readiness preserves boundaries

- **WHEN** Qdrant readiness evidence is reviewed
- **THEN** retrieval defaults, provider HTTP contracts, and external control-plane ownership remain unchanged
