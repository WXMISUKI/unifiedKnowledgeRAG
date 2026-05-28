# document-rag Specification

## Purpose
TBD - created by archiving change add-knowledge-provider-v1. Update Purpose after archive.
## Requirements
### Requirement: RAG sources are listed separately from graph sources

The system SHALL expose document RAG source metadata through a dedicated endpoint, including each source's configured retrieval backend and backend readiness status.

#### Scenario: RAG source list is available

- **WHEN** a caller requests `GET /api/rag/sources`
- **THEN** the response includes configured knowledge base ids, readiness status, version, freshness metadata, retrieval backend, and backend readiness status

### Requirement: RAG retrieve returns compact evidence context

The system SHALL return compact answer context and document evidence for matching document RAG queries while preserving the existing response contract across retrieval backends and enforcing explicit source index lifecycle readiness before backend retrieval work begins.

#### Scenario: Retrieval finds matching documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query and ready knowledge base id whose index status is ready
- **THEN** the response has `ok=true`, `result.answer_context`, and `result.documents` with stable `citation` values

#### Scenario: LlamaIndex retrieval preserves provider citations

- **WHEN** the LlamaIndex backend returns matching indexed nodes
- **THEN** each response document is assembled from provider-owned metadata and includes `source_id`, `document_id`, `title`, `snippet`, `score`, and stable `citation`

#### Scenario: Indexed source is not ready

- **WHEN** a caller requests `POST /api/rag/retrieve` for a known source whose index status is not ready
- **THEN** the response has `ok=false` and an `error.code` that identifies the index readiness failure

#### Scenario: Not-ready source does not execute backend retrieval

- **WHEN** a caller requests `POST /api/rag/retrieve` for a known source whose index status is not ready
- **THEN** the provider returns `INDEX_NOT_READY` before calling the selected backend retrieval implementation

### Requirement: RAG retrieval backend is configurable

The system SHALL select the document retrieval backend from configuration without changing the HTTP API contract.

#### Scenario: Fixture backend is selected

- **WHEN** `RAG_RETRIEVAL_BACKEND` is configured as `fixture`
- **THEN** document retrieval uses the deterministic local fixture backend

#### Scenario: LlamaIndex backend is selected

- **WHEN** `RAG_RETRIEVAL_BACKEND` is configured as `llamaindex`
- **THEN** document retrieval uses the LlamaIndex-backed local index service

### Requirement: LlamaIndex backend manages local index readiness

The system SHALL report local LlamaIndex readiness from explicit source index lifecycle state rather than performing hidden indexing during retrieval.

#### Scenario: LlamaIndex index is ready

- **WHEN** configured source documents and source index lifecycle status are ready
- **THEN** the backend readiness status is `ready`

#### Scenario: LlamaIndex index is unavailable

- **WHEN** configured source documents or source index lifecycle status cannot be loaded or built
- **THEN** the backend readiness status is `degraded` with a machine-readable reason

### Requirement: RAG retrieve handles empty retrieval explicitly

The system SHALL treat no matching evidence as a successful empty retrieval result.

#### Scenario: Retrieval finds no documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query that has no matching evidence
- **THEN** the response has `ok=true`, an empty `result.documents` array, and an empty `result.answer_context`

#### Scenario: LlamaIndex retrieval finds no documents

- **WHEN** a LlamaIndex retrieval query has no matching evidence above the configured threshold
- **THEN** the response has `ok=true`, an empty `result.documents` array, and an empty `result.answer_context`

### Requirement: RAG retrieve rejects unknown sources

The system SHALL reject retrieval requests for unknown or unavailable knowledge base ids with structured provider errors before backend retrieval work begins.

#### Scenario: Unknown source is requested

- **WHEN** a caller requests `POST /api/rag/retrieve` with an unknown knowledge base id
- **THEN** the response has `ok=false` and an `error.code` that identifies the unknown source

#### Scenario: Unknown source does not execute backend retrieval

- **WHEN** a caller requests `POST /api/rag/retrieve` with an unknown knowledge base id
- **THEN** the provider returns `UNKNOWN_KNOWLEDGE_BASE` before calling the selected backend retrieval implementation

### Requirement: Qdrant vector points preserve retrieval evidence metadata

The system SHALL map indexed evidence chunks to Qdrant point payloads while preserving citation and enterprise metadata fields.

#### Scenario: Evidence chunk becomes Qdrant point

- **WHEN** an evidence chunk is mapped for Qdrant
- **THEN** the point includes a stable id, named vector, source id, document id, chunk id, title, citation, and text payload

#### Scenario: Enterprise metadata is preserved

- **WHEN** an evidence chunk includes tenant, ACL, document version, embedding model, or chunking strategy metadata
- **THEN** the Qdrant payload preserves those fields for later filtering and audit

#### Scenario: Retrieval filter is built

- **WHEN** source ids and tenant id are supplied for Qdrant retrieval
- **THEN** the adapter builds a payload filter that includes tenant and source constraints

### Requirement: Qdrant collection can be prepared explicitly

The system SHALL prepare a configured Qdrant collection only through explicit Qdrant adapter calls.

#### Scenario: Qdrant collection is ready

- **WHEN** the configured Qdrant collection exists or can be created
- **THEN** the Qdrant adapter reports collection readiness as `ready`

#### Scenario: Qdrant collection is unavailable

- **WHEN** the configured Qdrant collection cannot be reached or created
- **THEN** the Qdrant adapter reports readiness as `degraded` with a reason

### Requirement: Qdrant evidence chunks can be upserted

The system SHALL upsert provider-neutral evidence chunks into Qdrant using the established point and payload contract.

#### Scenario: Evidence chunks are upserted

- **WHEN** evidence chunks with vectors are sent to the Qdrant adapter
- **THEN** the adapter writes Qdrant points to the configured collection

#### Scenario: Evidence payload is preserved

- **WHEN** chunks are upserted
- **THEN** source, tenant, document, chunk, citation, text, and ACL metadata remain in the payload

### Requirement: Qdrant vector query maps hits to evidence documents

The system SHALL query Qdrant with an already-created query vector and map valid hits to provider evidence documents.

#### Scenario: Query vector returns hits

- **WHEN** a Qdrant query returns hits with required evidence payload fields
- **THEN** the adapter returns `EvidenceDocument` items with source, document, title, snippet, score, and citation

#### Scenario: Query text embedding remains out of scope

- **WHEN** the Qdrant adapter is called for vector query
- **THEN** the caller supplies the query vector and the adapter does not choose or call an embedding model

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

### Requirement: Embedding adapters expose a provider-neutral contract

The system SHALL convert text into dense vectors through a provider-neutral embedding adapter interface.

#### Scenario: Mock embedding is selected

- **WHEN** the embedding provider is configured as `mock`
- **THEN** the adapter returns deterministic vectors with the configured vector size

#### Scenario: Hosted embedding is not implemented

- **WHEN** the embedding provider is configured as `hosted` before a hosted model decision is approved
- **THEN** the adapter reports degraded readiness and fails closed when called

#### Scenario: Local embedding is not implemented

- **WHEN** the embedding provider is configured as `local` before a local model decision is approved
- **THEN** the adapter reports degraded readiness and fails closed when called

### Requirement: Qdrant chunks can receive vectors from embedding adapters

The system SHALL allow evidence chunks to be embedded before Qdrant upsert without changing their evidence payload metadata.

#### Scenario: Evidence chunk is embedded

- **WHEN** an evidence chunk text is embedded
- **THEN** the resulting Qdrant chunk keeps source, document, chunk, citation, text, and metadata fields while replacing the vector

#### Scenario: Text query orchestration remains separate

- **WHEN** embedding adapter helpers are added
- **THEN** the system does not automatically switch HTTP retrieval to Qdrant text-query mode

### Requirement: Qdrant text query uses embedding adapter orchestration

The system SHALL execute opt-in Qdrant text retrieval by embedding query text before vector search.

#### Scenario: Query text is embedded

- **WHEN** Qdrant text retrieval is requested
- **THEN** the query text is embedded through the configured embedding adapter before Qdrant vector query

#### Scenario: Qdrant hits become evidence documents

- **WHEN** Qdrant vector query returns valid evidence payload hits
- **THEN** the retrieval result contains `EvidenceDocument` items using the existing evidence mapping

#### Scenario: Qdrant remains opt-in

- **WHEN** Qdrant text query orchestration is available
- **THEN** the default retrieval backend remains unchanged

### Requirement: Qdrant readiness includes embedding readiness

The system SHALL report Qdrant backend readiness from both Qdrant collection readiness and embedding adapter readiness.

#### Scenario: Embedding adapter is degraded

- **WHEN** the configured embedding adapter is not ready
- **THEN** Qdrant backend readiness is degraded with an embedding reason

#### Scenario: Qdrant collection is degraded

- **WHEN** Qdrant collection readiness is degraded
- **THEN** Qdrant backend readiness is degraded with a Qdrant reason

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

### Requirement: Qdrant ingestion participates in index lifecycle

The system SHALL allow the existing ingestion job lifecycle to build Qdrant indexes when Qdrant is explicitly selected.

#### Scenario: Qdrant source ingestion succeeds

- **WHEN** an ingestion job runs with `RAG_RETRIEVAL_BACKEND=qdrant` for a valid source
- **THEN** the source chunks are embedded, upserted to Qdrant, and source index status is marked `ready`

#### Scenario: Qdrant source document is missing

- **WHEN** Qdrant ingestion runs for a source whose local document is missing
- **THEN** the ingestion job fails with a structured index build failure

### Requirement: Local BGE-M3 embeddings integrate with Qdrant evidence chunks

The system SHALL allow Qdrant evidence chunks to be embedded with the opt-in local BGE-M3 adapter.

#### Scenario: Qdrant chunks are embedded with BGE-M3

- **WHEN** `EMBEDDING_PROVIDER=bge_m3_local` is selected and Qdrant chunks are embedded
- **THEN** chunk metadata identifies the embedding provider and model used for dense vectors

#### Scenario: BGE-M3 is not the default path

- **WHEN** no embedding provider is configured
- **THEN** the system continues using the deterministic mock adapter for local contract tests

### Requirement: Local BGE-M3 model path supports offline retrieval evaluation

The system SHALL support using a pre-downloaded BGE-M3 model directory for local Qdrant retrieval evaluation.

#### Scenario: Offline model path is configured

- **WHEN** `EMBEDDING_MODEL_PATH` points to a downloaded BGE-M3 directory and `EMBEDDING_LOCAL_FILES_ONLY=true`
- **THEN** the local embedding adapter uses the local artifact path without requiring runtime model download
