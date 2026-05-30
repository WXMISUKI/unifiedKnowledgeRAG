## ADDED Requirements

### Requirement: RAG requests expose normalized filter context
The system SHALL normalize request filters into provider-owned filter context metadata for document RAG retrieval and answer requests.

#### Scenario: Retrieval response includes request filter context
- **WHEN** a caller requests `POST /api/rag/retrieve` with supported filters
- **THEN** the response includes `result.metadata.request_filter_context` with supported filter fields and backend enforcement status

#### Scenario: Answer response includes request filter context
- **WHEN** a caller requests `POST /api/rag/answer` with supported filters
- **THEN** the response includes `result.metadata.request_filter_context` alongside answer trace metadata

#### Scenario: Qdrant retrieval applies supported filters
- **WHEN** Qdrant text retrieval is requested with `tenant_id`, `document_ids`, or `acl_tags`
- **THEN** the Qdrant backend uses those values when building the vector-store payload filter

#### Scenario: Non-enforcing backends report filter handling
- **WHEN** fixture or LlamaIndex retrieval receives request filters
- **THEN** retrieval behavior remains compatible and metadata reports that backend filter enforcement is not active for that backend

#### Scenario: Unknown filter keys are diagnosable
- **WHEN** request filters contain unsupported keys
- **THEN** the filter context preserves those keys under diagnostic metadata without treating them as enforced filters
