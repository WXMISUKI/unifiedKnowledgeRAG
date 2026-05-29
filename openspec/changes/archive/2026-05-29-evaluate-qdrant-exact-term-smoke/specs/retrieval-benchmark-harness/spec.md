## ADDED Requirements

### Requirement: Qdrant exact-term smoke evidence can be exported locally

The system SHALL provide a named local export path for running the exact-term identifier fixture through Qdrant+BGE smoke retrieval without changing runtime defaults.

#### Scenario: Exact-term Qdrant smoke evidence is exported

- **WHEN** the exact-term Qdrant smoke helper is run with source ids and an output directory
- **THEN** it indexes the sources, evaluates the exact-term identifier fixture, and writes JSON and Markdown evidence files with stable exact-term filenames

#### Scenario: Exact-term Qdrant smoke keeps expected citations

- **WHEN** dense-only retrieval returns citations that differ from the exact-term fixture expectations
- **THEN** the evidence records the miss instead of rewriting expected citations

#### Scenario: Exact-term Qdrant smoke remains evaluation-only

- **WHEN** exact-term Qdrant smoke evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and hybrid retrieval decisions remain unchanged

## MODIFIED Requirements

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

#### Scenario: Exact-term Qdrant dense evidence is exported

- **WHEN** exact-term identifier cases are evaluated against Qdrant+BGE dense retrieval
- **THEN** the system writes local JSON and Markdown evidence that includes Qdrant metadata, indexed sources, returned citations, and benchmark metrics

#### Scenario: Exact-term evidence remains local

- **WHEN** exact-term identifier evidence is exported
- **THEN** runtime retrieval defaults, answer generation behavior, and public HTTP APIs remain unchanged
