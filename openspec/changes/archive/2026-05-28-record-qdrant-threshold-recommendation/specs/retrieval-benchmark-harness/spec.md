## ADDED Requirements

### Requirement: Qdrant threshold recommendation evidence can be exported locally

The system SHALL derive a local Qdrant+BGE threshold recommendation from threshold sweep evidence without changing runtime defaults.

#### Scenario: Threshold recommendation is exported
- **WHEN** a threshold sweep report and quality gates are provided
- **THEN** the system writes JSON and Markdown recommendation files with the selected threshold, gates, source sweep path, metrics, and caveats

#### Scenario: Lowest passing threshold is selected
- **WHEN** multiple threshold sweep rows satisfy the configured quality gates
- **THEN** the recommendation selects the lowest passing threshold

#### Scenario: No threshold satisfies the gates
- **WHEN** no threshold sweep row satisfies the configured quality gates
- **THEN** recommendation generation fails with a clear error and does not write a misleading recommendation

#### Scenario: Recommendation does not change defaults
- **WHEN** threshold recommendation evidence is exported
- **THEN** the runtime `RAG_SCORE_THRESHOLD` default remains unchanged and the recommendation is marked as local seed evidence only
