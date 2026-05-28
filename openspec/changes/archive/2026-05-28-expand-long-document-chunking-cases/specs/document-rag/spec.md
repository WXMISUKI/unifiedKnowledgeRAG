## MODIFIED Requirements

### Requirement: Qdrant source ingestion builds evidence chunks
The system SHALL build Qdrant evidence chunks from local markdown source documents while preserving source metadata, stable business citation anchors for known local benchmark sources, and deterministic fallback citations for unmapped sources or paragraphs.

#### Scenario: Local source becomes Qdrant chunks

- **WHEN** a local markdown source is indexed for Qdrant
- **THEN** the system creates vector evidence chunks from its content with source id, document id, chunk id, title, text, citation, and chunking strategy metadata

#### Scenario: Known local source emits business citation

- **WHEN** Qdrant ingestion chunks a known local benchmark source paragraph with a source-specific business anchor
- **THEN** the chunk citation uses the business anchor instead of a generic chunk citation

#### Scenario: Unknown paragraph uses chunk fallback

- **WHEN** Qdrant ingestion chunks a source or paragraph without a source-specific business anchor
- **THEN** the chunk citation falls back to `document_id#chunk-N`

#### Scenario: Long-section source paragraph has stable citation

- **WHEN** Qdrant ingestion chunks an added long-section benchmark paragraph
- **THEN** the chunk citation uses a stable business anchor for the long-section case

#### Scenario: Qdrant source index marks source ready

- **WHEN** Qdrant source indexing succeeds for a known source
- **THEN** the system upserts embedded chunks and records the source index status as `ready`
