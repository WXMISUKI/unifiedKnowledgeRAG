## ADDED Requirements

### Requirement: Reindex planning evidence advances Phase 6 operations
The project SHALL treat local reindex readiness plans and backup/reindex notes as Phase 6 operations evidence when they help operators review provider component state without changing runtime behavior.

#### Scenario: Reindex planning is phase-aligned
- **WHEN** an OpenSpec change adds read-only reindex planning evidence
- **THEN** the change identifies Phase 6 as the roadmap phase it advances

#### Scenario: Reindex planning does not imply worker infrastructure
- **WHEN** the provider exports reindex recommendations
- **THEN** it does not imply approval of production queue workers, schedulers, or automatic reindex execution
