## MODIFIED Requirements

### Requirement: Qdrant source ingestion builds evidence chunks

The system SHALL convert configured local source documents into Qdrant evidence chunks during explicit Qdrant ingestion, using stable business citation anchors for known local benchmark sources and deterministic chunk fallback citations for other content.

#### Scenario: Markdown source is chunked

- **WHEN** Qdrant ingestion builds an index for a configured markdown source
- **THEN** the source content is converted into deterministic evidence chunks with stable source, document, chunk, title, text, and citation metadata

#### Scenario: Known local source emits business citation

- **WHEN** Qdrant ingestion chunks a known local benchmark source paragraph with an approved citation anchor
- **THEN** the chunk citation uses that source-specific business anchor instead of a generic `chunk-N` citation

#### Scenario: Unknown paragraph uses chunk fallback

- **WHEN** Qdrant ingestion chunks a source or paragraph without a source-specific business anchor
- **THEN** the chunk citation falls back to `document_id#chunk-N`

#### Scenario: Chunk metadata is preserved

- **WHEN** chunks are embedded and upserted to Qdrant
- **THEN** source id, document id, chunk id, citation, embedding metadata, and chunking strategy remain in the payload
