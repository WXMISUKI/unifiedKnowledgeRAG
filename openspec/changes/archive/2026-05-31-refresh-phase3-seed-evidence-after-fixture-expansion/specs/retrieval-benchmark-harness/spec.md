## ADDED Requirements

### Requirement: Seed evidence exports stay synchronized with canonical fixture revisions

The system SHALL regenerate Chinese-seed benchmark evidence after canonical fixture updates so review artifacts reflect the current case set and category summaries.

#### Scenario: Chinese-seed evidence reflects current baseline case count

- **WHEN** the Chinese-seed evidence export runs after fixture expansion
- **THEN** the exported retrieval baseline summary reflects the updated total baseline case count and category summaries

#### Scenario: Seed evidence refresh remains evaluation-only

- **WHEN** Chinese-seed evidence is regenerated
- **THEN** runtime retrieval defaults and production promotion gates remain unchanged unless separate gate evidence explicitly approves promotion
