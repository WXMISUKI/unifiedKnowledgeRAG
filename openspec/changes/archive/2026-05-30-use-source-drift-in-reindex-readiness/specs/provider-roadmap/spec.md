## ADDED Requirements

### Requirement: Source drift evidence informs Phase 6 reindex planning
The project SHALL allow Phase 2 source freshness evidence to inform Phase 6 reindex readiness recommendations without changing runtime retrieval behavior.

#### Scenario: Drift-informed reindex planning is phase-aligned
- **WHEN** an OpenSpec change connects source fingerprint diagnostics to reindex readiness evidence
- **THEN** the change identifies Phase 2 and Phase 6 as the roadmap phases it connects

#### Scenario: Drift-informed planning does not automate indexing
- **WHEN** the provider reports that changed source documents should be reindexed
- **THEN** it does not automatically create ingestion jobs, rebuild indexes, or change retrieval defaults
