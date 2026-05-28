## ADDED Requirements

### Requirement: Production retrieval decisions reference seed evidence bundle paths

The system SHALL keep local benchmark evidence paths available for later production indexing decisions.

#### Scenario: Production embedding or retrieval promotion is proposed

- **WHEN** a future change proposes production embedding, reranker, hybrid retrieval, or vector-store promotion
- **THEN** it references the exported Chinese seed evidence bundle or explains why fresher customer-specific evidence is required

#### Scenario: Seed evidence is interpreted

- **WHEN** exported Chinese seed evidence is reviewed
- **THEN** it is treated as an early comparison baseline and not as final production acceptance
