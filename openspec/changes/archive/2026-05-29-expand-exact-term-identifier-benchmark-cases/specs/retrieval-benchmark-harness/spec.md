## ADDED Requirements

### Requirement: Exact-term identifier cases are maintained separately

The system SHALL maintain dedicated exact-term and identifier-heavy benchmark cases without replacing the baseline Chinese retrieval seed.

#### Scenario: Exact-term fixture is loaded separately

- **WHEN** exact-term identifier cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the baseline retrieval benchmark fixture

#### Scenario: Exact-term categories are represented

- **WHEN** exact-term identifier cases are loaded
- **THEN** the set includes policy code, form name, workflow acronym, and order-like id categories

#### Scenario: Exact-term evidence is exported

- **WHEN** exact-term identifier evidence is exported
- **THEN** the system writes local JSON and Markdown reports with benchmark metrics and per-case citations

#### Scenario: Exact-term evidence remains local

- **WHEN** exact-term identifier evidence is exported
- **THEN** runtime retrieval defaults, answer generation behavior, and public HTTP APIs remain unchanged
