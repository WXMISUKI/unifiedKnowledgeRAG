## ADDED Requirements

### Requirement: Markdown section chunking can run as an evaluation candidate

The system SHALL generate section-aware markdown evidence chunks for local evaluation without changing the default Qdrant ingestion strategy.

#### Scenario: Section chunks are generated
- **WHEN** a markdown source is chunked with the section-aware candidate
- **THEN** the system groups content under markdown headings into section chunks with source id, document id, chunk id, title, text, citation, and chunking strategy metadata

#### Scenario: Section candidate preserves stable citations
- **WHEN** a known local source is chunked with the section-aware candidate
- **THEN** the generated chunks use deterministic section candidate citations rather than generic fallback citations

#### Scenario: Default ingestion remains paragraph based
- **WHEN** Qdrant source ingestion loads chunks for runtime indexing
- **THEN** it continues using `markdown-paragraph-v1` unless a future approved change switches the strategy
