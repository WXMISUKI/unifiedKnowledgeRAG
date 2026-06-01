## ADDED Requirements

### Requirement: Phase 6 Qdrant vector-store readiness exports stay lightweight and review-only

The project SHALL treat Phase 6 Qdrant vector-store readiness exports as local evidence visibility work without changing runtime defaults.

#### Scenario: Qdrant readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Qdrant vector-store readiness export
- **THEN** the roadmap records it as Phase 6 operations evidence visibility work rather than retrieval runtime promotion

#### Scenario: Qdrant readiness export preserves boundaries

- **WHEN** the export summarizes deployment, backup/recovery contract, and reindex linkage
- **THEN** runtime defaults, provider HTTP contracts, and external control-plane ownership remain unchanged
