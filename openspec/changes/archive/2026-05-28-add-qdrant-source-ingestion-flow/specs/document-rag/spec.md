## ADDED Requirements

### Requirement: Qdrant source ingestion builds evidence chunks

The system SHALL convert configured local source documents into Qdrant evidence chunks during explicit Qdrant ingestion.

#### Scenario: Markdown source is chunked

- **WHEN** Qdrant ingestion builds an index for a configured markdown source
- **THEN** the source content is converted into deterministic evidence chunks with stable source, document, chunk, title, text, and citation metadata

#### Scenario: Chunk metadata is preserved

- **WHEN** chunks are embedded and upserted to Qdrant
- **THEN** source id, document id, chunk id, citation, embedding metadata, and chunking strategy remain in the payload

### Requirement: Qdrant ingestion participates in index lifecycle

The system SHALL allow the existing ingestion job lifecycle to build Qdrant indexes when Qdrant is explicitly selected.

#### Scenario: Qdrant source ingestion succeeds

- **WHEN** an ingestion job runs with `RAG_RETRIEVAL_BACKEND=qdrant` for a valid source
- **THEN** the source chunks are embedded, upserted to Qdrant, and source index status is marked `ready`

#### Scenario: Qdrant source document is missing

- **WHEN** Qdrant ingestion runs for a source whose local document is missing
- **THEN** the ingestion job fails with a structured index build failure
