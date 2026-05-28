## ADDED Requirements

### Requirement: Qdrant retrieval respects score threshold

The system SHALL filter Qdrant retrieval hits using the configured retrieval score threshold before returning evidence documents.

#### Scenario: Qdrant hit meets threshold

- **WHEN** a Qdrant hit has valid evidence payload and score greater than or equal to `RAG_SCORE_THRESHOLD`
- **THEN** the hit is returned as an `EvidenceDocument`

#### Scenario: Qdrant hit is below threshold

- **WHEN** a Qdrant hit has valid evidence payload but score below `RAG_SCORE_THRESHOLD`
- **THEN** the hit is omitted from returned evidence

#### Scenario: Qdrant retrieval has no hits above threshold

- **WHEN** all Qdrant hits are below `RAG_SCORE_THRESHOLD`
- **THEN** retrieval returns an empty document list using the existing successful empty retrieval contract
