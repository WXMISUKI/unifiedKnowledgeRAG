## MODIFIED Requirements

### Requirement: Markdown section chunking can run as an evaluation candidate
The system SHALL generate section-aware markdown evidence chunks for local evaluation without changing the default Qdrant ingestion strategy.

#### Scenario: Section chunks are generated

- **WHEN** a markdown source is chunked with the section-aware candidate
- **THEN** the system groups content under markdown headings into section chunks with source id, document id, chunk id, title, text, citation, and chunking strategy metadata

#### Scenario: Section candidate preserves stable citations

- **WHEN** a known local source is chunked with the section-aware candidate
- **THEN** the generated chunks use deterministic section candidate citations rather than generic fallback citations

#### Scenario: Section candidate can be used in smoke evaluation

- **WHEN** local Qdrant smoke evaluation explicitly selects `markdown-section-v1`
- **THEN** the smoke path indexes section chunks for comparison evidence without changing default ingestion

#### Scenario: Token-window candidate can be used in smoke evaluation

- **WHEN** local Qdrant smoke evaluation explicitly selects `token-window-v1`
- **THEN** the smoke path indexes token-window chunks for comparison evidence without changing default ingestion

#### Scenario: Default ingestion remains paragraph based

- **WHEN** Qdrant source ingestion loads chunks for runtime indexing
- **THEN** it continues using `markdown-paragraph-v1` unless a future approved change switches the strategy

## ADDED Requirements

### Requirement: Token-window chunking can run as an evaluation candidate

The system SHALL generate token-window evidence chunks for local evaluation without adding production tokenizer dependencies or changing default Qdrant ingestion.

#### Scenario: Token-window chunks are generated

- **WHEN** a markdown source is chunked with the token-window candidate
- **THEN** the system emits deterministic chunks with source id, document id, chunk id, title, text, citation, and chunking strategy metadata

#### Scenario: Token-window chunks overlap

- **WHEN** source content exceeds the configured token window
- **THEN** consecutive token-window chunks share configured overlap units to reduce boundary loss

#### Scenario: Token-window candidate preserves stable citations

- **WHEN** a known local source is chunked with the token-window candidate
- **THEN** generated chunks use deterministic token-window candidate citations or explicit business anchors

#### Scenario: Token-window remains evaluation-only

- **WHEN** token-window chunking is available
- **THEN** runtime Qdrant ingestion defaults remain unchanged
