## ADDED Requirements

### Requirement: Provider handoff includes compact Phase 3 retrieval baseline evidence

The system SHALL include an optional Phase 3 retrieval baseline evidence row in provider handoff so external reviewers can inspect key benchmark summary metrics without opening benchmark reports separately.

#### Scenario: Handoff summarizes Phase 3 baseline evidence

- **WHEN** provider handoff reads the fixture Chinese-seed baseline evidence artifact
- **THEN** it summarizes `total_cases`, `hit_rate`, `citation_match_rate`, and `empty_handling_rate` in the artifact summary

#### Scenario: Missing Phase 3 baseline evidence does not block handoff by itself

- **WHEN** the Phase 3 baseline evidence artifact is absent
- **THEN** handoff marks that artifact as reviewable optional evidence and keeps existing required-artifact blocking behavior unchanged

#### Scenario: Phase 3 baseline summary remains read-only

- **WHEN** provider handoff summarizes Phase 3 baseline evidence
- **THEN** it does not run benchmark exports, change retrieval defaults, execute retrieval, create ingestion jobs, rebuild indexes, or execute GraphRAG
