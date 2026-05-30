# document-rag Specification

## Purpose
TBD - created by archiving change add-knowledge-provider-v1. Update Purpose after archive.
## Requirements
### Requirement: RAG sources are listed separately from graph sources

The system SHALL expose document RAG source metadata through a dedicated endpoint, including each source's configured retrieval backend and backend readiness status.

#### Scenario: RAG source list is available

- **WHEN** a caller requests `GET /api/rag/sources`
- **THEN** the response includes configured knowledge base ids, readiness status, version, freshness metadata, retrieval backend, and backend readiness status

### Requirement: RAG source document manifest is available

The system SHALL expose a read-only document manifest for each configured document RAG source so callers can inspect source documents, citation anchors, chunking metadata, and index readiness without running retrieval.

#### Scenario: Source document manifest is returned

- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for a configured RAG source
- **THEN** the response has `ok=true`, the requested source id, current index readiness metadata, and document manifests with document id, title, source path, format, version, chunking strategy, and citation anchors

#### Scenario: Unknown source returns structured error

- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for an unknown source
- **THEN** the response has `ok=false` and an `error.code` that identifies the unknown source

#### Scenario: Manifest does not execute retrieval work

- **WHEN** a caller requests a source document manifest
- **THEN** the provider does not run document retrieval, answer composition, embedding, vector search, ingestion, or graph execution

### Requirement: Source document manifest diagnostics are discoverable

The document RAG source document manifest endpoint SHALL be discoverable through provider-owned capability metadata.

#### Scenario: Source document manifest capability points to endpoint

- **WHEN** a caller inspects provider capabilities
- **THEN** the source document manifest capability identifies `GET /api/rag/sources/{source_id}/documents` and the `SourceDocumentManifestResponse` schema

#### Scenario: Diagnostic discovery does not change retrieval behavior

- **WHEN** source document manifest discovery metadata is added
- **THEN** existing retrieve and answer request and response contracts remain unchanged

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

#### Scenario: Long-section source paragraph has stable citation

- **WHEN** Qdrant ingestion chunks an added long-section benchmark paragraph
- **THEN** the chunk citation uses a stable business anchor for the long-section case

#### Scenario: Chunk metadata is preserved

- **WHEN** chunks are embedded and upserted to Qdrant
- **THEN** source id, document id, chunk id, citation, embedding metadata, and chunking strategy remain in the payload

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

### Requirement: RAG answer returns cited answer envelopes
The system SHALL expose a document RAG answer endpoint that composes a provider-owned answer envelope from configured retrieval evidence without changing the existing retrieval endpoint contract.

#### Scenario: Answer is composed from retrieved evidence
- **WHEN** a caller requests `POST /api/rag/answer` with a valid query and ready knowledge base id whose retrieval returns evidence
- **THEN** the response has `ok=true`, `result.answer_status=answered`, non-empty `result.answer`, non-empty `result.citations`, and the supporting `result.documents`

#### Scenario: Answer citations match supporting evidence
- **WHEN** the answer endpoint returns an answered result
- **THEN** every citation in `result.citations` corresponds to a citation in `result.documents`

#### Scenario: Retrieval endpoint remains unchanged
- **WHEN** the cited answer endpoint is added
- **THEN** `POST /api/rag/retrieve` continues to return the existing retrieval envelope with `answer_context` and `documents`

### Requirement: RAG answer fails closed when evidence is insufficient
The system SHALL return a successful answer envelope with an explicit insufficient-evidence status when retrieval produces no usable evidence.

#### Scenario: Retrieval has no evidence
- **WHEN** a caller requests `POST /api/rag/answer` with a valid query and ready knowledge base id whose retrieval returns no documents
- **THEN** the response has `ok=true`, `result.answer_status=insufficient_evidence`, an empty `result.answer`, an empty `result.citations`, and an empty `result.documents`

#### Scenario: Insufficient evidence is not a provider error
- **WHEN** the answer endpoint cannot answer because indexed evidence is insufficient
- **THEN** the response does not use `error` and instead reports the insufficiency in `result.answer_status`

### Requirement: RAG answer preserves retrieval guardrails
The system SHALL enforce existing source validation and index readiness checks before answer orchestration performs backend retrieval work.

#### Scenario: Unknown source is requested for answer
- **WHEN** a caller requests `POST /api/rag/answer` with an unknown knowledge base id
- **THEN** the response has `ok=false` and an `error.code` that identifies the unknown source

#### Scenario: Not-ready source is requested for answer
- **WHEN** a caller requests `POST /api/rag/answer` for a known source whose index status is not ready
- **THEN** the response has `ok=false` and an `error.code` that identifies the index readiness failure

### Requirement: RAG answer applies configurable evidence sufficiency policy
The system SHALL evaluate retrieved evidence against configurable answer sufficiency settings before returning an answered cited response.

#### Scenario: Evidence passes sufficiency policy
- **WHEN** a caller requests `POST /api/rag/answer` and retrieved documents satisfy the configured minimum evidence count and minimum top evidence score
- **THEN** the response has `ok=true`, `result.answer_status=answered`, non-empty `result.answer`, and metadata describing the sufficiency policy

#### Scenario: Evidence fails minimum top score
- **WHEN** a caller requests `POST /api/rag/answer` and retrieved documents do not satisfy the configured minimum top evidence score
- **THEN** the response has `ok=true`, `result.answer_status=insufficient_evidence`, an empty `result.answer`, empty `result.citations`, and metadata describing the failed gate

#### Scenario: Evidence fails minimum count
- **WHEN** a caller requests `POST /api/rag/answer` and retrieved documents do not satisfy the configured minimum evidence count
- **THEN** the response has `ok=true`, `result.answer_status=insufficient_evidence`, an empty `result.answer`, empty `result.citations`, and metadata describing the failed gate

#### Scenario: Retrieved evidence remains inspectable after gate failure
- **WHEN** the answer endpoint refuses to answer because retrieved evidence fails the sufficiency policy
- **THEN** the response keeps the retrieved `result.documents` for diagnostics without endorsing them as answer citations

### Requirement: RAG answer composer is provider configurable
The system SHALL select the cited answer composer from provider configuration while preserving the existing answer endpoint contract.

#### Scenario: Deterministic composer is selected
- **WHEN** `RAG_ANSWER_COMPOSER` is unset or configured as `deterministic`
- **THEN** `POST /api/rag/answer` uses the deterministic cited composer and returns composer provider metadata

#### Scenario: Unsupported composer is selected
- **WHEN** `RAG_ANSWER_COMPOSER` is configured to an unsupported value
- **THEN** `POST /api/rag/answer` returns `ok=false` with a structured composer configuration error

### Requirement: Hosted and local answer composers fail closed until approved
The system SHALL expose hosted and local answer composer configuration names without calling hosted APIs or local LLM runtimes until explicit implementation changes approve them.

#### Scenario: Hosted composer is not implemented
- **WHEN** `RAG_ANSWER_COMPOSER=hosted`
- **THEN** `POST /api/rag/answer` returns `ok=false` with a structured composer not implemented error before generating an answer

#### Scenario: Local composer is not implemented
- **WHEN** `RAG_ANSWER_COMPOSER=local`
- **THEN** `POST /api/rag/answer` returns `ok=false` with a structured composer not implemented error before generating an answer

### Requirement: RAG answer builds a cited prompt package
The system SHALL build a provider-owned cited-answer prompt package from the user query and gated retrieval evidence before composing an answered result.

#### Scenario: Answered result includes prompt package metadata
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata` includes a prompt package id, citation policy, and allowed citations derived from the supporting evidence

#### Scenario: Prompt package citations match answer citations
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** the prompt package allowed citations match `result.citations`

#### Scenario: Insufficient evidence has no endorsed prompt package
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=insufficient_evidence`
- **THEN** the result does not expose endorsed prompt package metadata

### Requirement: RAG answer renders cited prompt packages
The system SHALL render cited-answer prompt packages into provider-owned model-ready message structures before composing an answered result.

#### Scenario: Answered result includes prompt render metadata
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata` includes prompt render metadata with renderer id and message count

#### Scenario: Render metadata aligns with prompt package
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** the prompt render metadata references the same prompt package id as `result.metadata.prompt_package.id`

#### Scenario: Insufficient evidence has no endorsed prompt render
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=insufficient_evidence`
- **THEN** the result does not expose endorsed prompt render metadata

### Requirement: RAG answer validates cited output
The system SHALL validate cited answer output against the prompt package citation constraints before returning an answered result.

#### Scenario: Answered output passes validation
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata` includes output validation metadata showing validation passed

#### Scenario: Answer citations are constrained
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** every returned citation is included in `result.metadata.prompt_package.allowed_citations`

#### Scenario: Invalid cited output fails closed
- **WHEN** a composer output includes citations outside the prompt package allowed citations
- **THEN** the provider treats the output as not validated and does not endorse it as an answered result

### Requirement: RAG answer parses cited output before validation
The system SHALL parse generated cited answer text into structured answer text and citations before applying output validation.

#### Scenario: Answered result includes parser metadata
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata` includes output parser metadata showing parser id and extracted citation count

#### Scenario: Parsed citations drive validation
- **WHEN** generated answer text contains bracketed citations
- **THEN** output validation uses the parsed citations from that text

#### Scenario: Missing citations fail validation
- **WHEN** generated answer text contains no citations
- **THEN** output validation treats the output as missing citations and the provider does not endorse it as an answered result

### Requirement: RAG answer uses shared finalization pipeline
The system SHALL finalize cited answer candidates through a shared provider-owned pipeline before returning an answered result.

#### Scenario: Valid candidate is finalized as answered
- **WHEN** a composer candidate answer text contains allowed citations
- **THEN** the finalization pipeline returns an answered result with prompt package, prompt render, output parser, and output validation metadata

#### Scenario: Invalid candidate fails closed
- **WHEN** a composer candidate answer text contains no citations or citations outside the allowed prompt package citations
- **THEN** the finalization pipeline returns an insufficient-evidence result rather than an answered result

#### Scenario: Public answer contract is preserved
- **WHEN** deterministic answer composition uses the shared finalization pipeline
- **THEN** the public `POST /api/rag/answer` response remains compatible with the existing cited answer envelope

### Requirement: RAG answer exposes machine-readable answer trace metadata
The system SHALL include a compact machine-readable answer trace in document RAG answer metadata for successful answer envelopes.

#### Scenario: Answered result includes answer trace
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata.answer_trace` includes a trace id, trace version, final status, and ordered stages for retrieval, evidence gate, composer, output parser, output validator, and final decision

#### Scenario: Evidence gate failure includes answer trace
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=insufficient_evidence` because the evidence gate failed
- **THEN** `result.metadata.answer_trace` includes retrieval, evidence gate, composer, and final decision stages without prompt text or raw generated output

#### Scenario: Finalizer validation failure includes answer trace
- **WHEN** the shared finalization pipeline rejects a composer candidate because citations are missing or invalid
- **THEN** `result.metadata.answer_trace` includes output parser, output validator, and final decision stages that explain the fail-closed decision

#### Scenario: Answer trace preserves existing answer contract
- **WHEN** answer trace metadata is added
- **THEN** the existing answer, citations, documents, prompt package, prompt render, output parser, and output validation metadata remain compatible

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

### Requirement: RAG retrieval exposes machine-readable retrieval trace metadata
The system SHALL include compact retrieval trace metadata in successful document RAG retrieval and answer envelopes.

#### Scenario: Retrieval result includes retrieval trace
- **WHEN** `POST /api/rag/retrieve` returns `ok=true`
- **THEN** `result.metadata.retrieval_trace` includes trace id, trace version, retrieval backend, requested source ids, top-k, document count, citations, score summary, and filter context metadata

#### Scenario: Empty retrieval includes retrieval trace
- **WHEN** `POST /api/rag/retrieve` returns an empty successful result
- **THEN** `result.metadata.retrieval_trace.document_count` is zero and citations are empty

#### Scenario: Answer result includes retrieval trace
- **WHEN** `POST /api/rag/answer` returns a successful answer envelope
- **THEN** `result.metadata.retrieval_trace` is present alongside answer metadata so retrieval and answer decisions can be correlated

#### Scenario: Retrieval trace preserves existing contracts
- **WHEN** retrieval trace metadata is added
- **THEN** existing retrieval documents, answer context, answer trace, and request filter context fields remain compatible

### Requirement: RAG retrieval exposes provider evidence pack metadata
The system SHALL include a compact provider-owned evidence pack in successful document RAG retrieval metadata so callers can compose answers from allowed citations without inferring the citation policy from raw documents.

#### Scenario: Retrieval with evidence includes evidence pack
- **WHEN** `POST /api/rag/retrieve` returns `ok=true` with retrieved documents
- **THEN** `result.metadata.evidence_pack` includes pack id, version `evidence-pack-v1`, status `answerable`, citation policy, allowed citations, evidence count, score summary, retrieval backend, requested source ids, and compact evidence entries

#### Scenario: Evidence pack citations match returned documents
- **WHEN** `POST /api/rag/retrieve` returns an evidence pack
- **THEN** every allowed citation in the pack corresponds to a citation in `result.documents`

#### Scenario: Empty retrieval includes insufficient evidence pack
- **WHEN** `POST /api/rag/retrieve` returns `ok=true` with no retrieved documents
- **THEN** `result.metadata.evidence_pack` has status `insufficient_evidence`, reason `no_documents`, zero evidence count, and no allowed citations

### Requirement: RAG answer reuses retrieval evidence pack metadata
The system SHALL include the same retrieval-owned evidence pack metadata in successful document RAG answer envelopes before answer-specific prompt or validation metadata is considered.

#### Scenario: Answered result includes evidence pack
- **WHEN** `POST /api/rag/answer` returns `ok=true` with `result.answer_status=answered`
- **THEN** `result.metadata.evidence_pack` is present and its allowed citations include every returned answer citation

#### Scenario: Insufficient answer includes diagnostic evidence pack
- **WHEN** `POST /api/rag/answer` returns `ok=true` with `result.answer_status=insufficient_evidence`
- **THEN** `result.metadata.evidence_pack` remains present for diagnostics and does not expose unsupported citations as endorsed answer citations

#### Scenario: Evidence pack preserves existing contracts
- **WHEN** evidence pack metadata is added to retrieval and answer responses
- **THEN** existing answer context, documents, retrieval trace, answer trace, prompt package, prompt render, output parser, and output validation metadata remain compatible
