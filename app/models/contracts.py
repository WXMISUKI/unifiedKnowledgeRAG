from typing import Any

from pydantic import BaseModel, Field


class ComponentStatus(BaseModel):
    status: str
    reason: str | None = None
    backend: str | None = None
    backend_status: str | None = None
    index_status: str | None = None


class HealthResponse(BaseModel):
    status: str
    service: str
    rag: ComponentStatus
    answer: ComponentStatus
    graph: ComponentStatus


class CapabilityInvocation(BaseModel):
    protocol: str = "http"
    method: str
    path: str
    request_schema_ref: str | None = None
    response_schema_ref: str | None = None
    example_request: dict[str, Any] | None = None


class Capability(BaseModel):
    id: str
    status: str
    description: str
    reason: str | None = None
    invocation: CapabilityInvocation | None = None


class CapabilitiesResponse(BaseModel):
    capabilities: list[Capability]


class ProviderIntegrationManifest(BaseModel):
    provider_id: str
    provider_name: str
    provider_version: str
    manifest_version: str
    contract_version: str
    component_role: str
    compatible_control_planes: list[str]
    description: str
    endpoints: dict[str, str]
    capability_ids: list[str]
    evidence: dict[str, str]
    boundaries: dict[str, str]


class ProviderPreflightCheck(BaseModel):
    name: str
    passed: bool
    status: str
    details: dict[str, Any] = Field(default_factory=dict)
    reason: str | None = None


class ProviderPreflightResponse(BaseModel):
    provider_id: str
    contract_version: str
    manifest_version: str
    requested_contract_version: str
    requested_capability_ids: list[str]
    bindable: bool
    control_plane_hint: str
    checks: list[ProviderPreflightCheck]


class ProviderHandoffEvidenceArtifact(BaseModel):
    id: str
    category: str
    path: str
    present: bool
    status: str
    summary: str
    recommended_action: str


class ProviderHandoffBundleResponse(BaseModel):
    id: str
    generated_at: str
    status: str
    provider: dict[str, Any]
    evidence_artifacts: list[ProviderHandoffEvidenceArtifact]
    operation_notes: list[str] = Field(default_factory=list)
    json_path: str | None = None
    markdown_path: str | None = None


class KnowledgeBaseSource(BaseModel):
    id: str
    type: str = "rag"
    status: str
    owner: str
    version: str
    embedding_model: str
    vector_store: str
    freshness: str
    retrieval_backend: str | None = None
    backend_status: str | None = None
    backend_reason: str | None = None
    index_status: str | None = None
    index_reason: str | None = None
    indexed_at: str | None = None
    latest_index_job_id: str | None = None


class GraphSource(BaseModel):
    id: str
    type: str = "graph"
    status: str
    owner: str
    ontology_version: str
    graph_store: str
    entity_types: list[str] = Field(default_factory=list)
    relation_types: list[str] = Field(default_factory=list)


class CatalogResponse(BaseModel):
    knowledge_bases: list[KnowledgeBaseSource]
    graphs: list[GraphSource]


class ProviderError(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class SourceDocumentManifest(BaseModel):
    document_id: str
    title: str
    source_path: str
    format: str
    version: str
    chunking_strategy: str
    citation_anchors: list[str] = Field(default_factory=list)
    source_file_status: str | None = None
    content_sha256: str | None = None
    expected_content_sha256: str | None = None
    content_byte_size: int | None = None
    drift_status: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceDocumentManifestResult(BaseModel):
    source_id: str
    status: str
    owner: str
    version: str
    retrieval_backend: str
    index_status: str
    index_reason: str | None = None
    indexed_at: str | None = None
    latest_index_job_id: str | None = None
    documents: list[SourceDocumentManifest]


class SourceDocumentManifestResponse(BaseModel):
    ok: bool
    result: SourceDocumentManifestResult | None = None
    error: ProviderError | None = None


class RagRetrieveRequest(BaseModel):
    query: str = Field(min_length=1)
    knowledge_base_ids: list[str] = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    filters: dict[str, Any] = Field(default_factory=dict)


class EvidenceDocument(BaseModel):
    source_id: str
    document_id: str
    title: str
    snippet: str
    score: float
    citation: str


class RagRetrieveResult(BaseModel):
    answer_context: str
    documents: list[EvidenceDocument]
    metadata: dict[str, Any] = Field(default_factory=dict)


class RagAnswerRequest(RagRetrieveRequest):
    pass


class RagAnswerResult(BaseModel):
    answer_status: str
    answer: str
    citations: list[str]
    documents: list[EvidenceDocument]
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestionJobRequest(BaseModel):
    source_id: str = Field(min_length=1)
    run_mode: str = Field(default="sync", pattern="^(sync|queued)$")


class IndexLifecycleJob(BaseModel):
    job_id: str
    source_id: str
    status: str
    requested_at: str
    completed_at: str | None = None
    error: ProviderError | None = None


class IngestionJobResponse(BaseModel):
    ok: bool
    job: IndexLifecycleJob | None = None
    error: ProviderError | None = None


class IngestionJobListResponse(BaseModel):
    ok: bool
    jobs: list[IndexLifecycleJob] = Field(default_factory=list)
    total: int = 0
    limit: int = 50
    offset: int = 0
    has_more: bool = False
    error: ProviderError | None = None


class IngestionJobDetailResponse(BaseModel):
    ok: bool
    job: IndexLifecycleJob | None = None
    error: ProviderError | None = None


class IngestionJobRetentionRequest(BaseModel):
    keep_latest: int = Field(default=100, ge=1, le=10000)


class IngestionJobRetentionResult(BaseModel):
    before_count: int
    after_count: int
    removed_count: int
    keep_latest: int


class IngestionJobRetentionResponse(BaseModel):
    ok: bool
    result: IngestionJobRetentionResult | None = None
    error: ProviderError | None = None


class IngestionJobCancelRequest(BaseModel):
    reason: str = Field(default="Canceled by operator.", min_length=1)


class IngestionJobRecoveryRequest(BaseModel):
    max_age_seconds: int = Field(default=3600, ge=0, le=604800)


class IngestionJobRecoveryResult(BaseModel):
    recovered_count: int
    recovered_job_ids: list[str] = Field(default_factory=list)
    max_age_seconds: int


class IngestionJobRecoveryResponse(BaseModel):
    ok: bool
    result: IngestionJobRecoveryResult | None = None
    error: ProviderError | None = None


class IngestionQueueRunResponse(BaseModel):
    ok: bool
    job: IndexLifecycleJob | None = None
    error: ProviderError | None = None


class IngestionDocumentChunkPreview(BaseModel):
    chunk_id: str
    text_preview: str
    char_count: int


class IngestionDocumentPreflight(BaseModel):
    document_id: str
    title: str
    source_path: str
    format: str
    format_supported: bool
    file_status: str
    parser_status: str
    chunking_strategy: str
    chunk_count: int = 0
    chunk_preview: list[IngestionDocumentChunkPreview] = Field(default_factory=list)
    citation_anchor_count: int = 0
    recommended_action: str
    reason: str | None = None


class IngestionSourcePreflightResult(BaseModel):
    source_id: str
    status: str
    retrieval_backend: str
    index_status: str
    index_reason: str | None = None
    latest_index_job_id: str | None = None
    documents: list[IngestionDocumentPreflight] = Field(default_factory=list)
    operation_notes: list[str] = Field(default_factory=list)
    recommended_action: str


class IngestionSourcePreflightResponse(BaseModel):
    ok: bool
    result: IngestionSourcePreflightResult | None = None
    error: ProviderError | None = None


class IndexStatusResponse(BaseModel):
    source_id: str
    status: str
    backend: str
    indexed_at: str | None = None
    latest_job_id: str | None = None
    reason: str | None = None
    error: ProviderError | None = None


class RagRetrieveResponse(BaseModel):
    ok: bool
    result: RagRetrieveResult | None = None
    error: ProviderError | None = None


class RagAnswerResponse(BaseModel):
    ok: bool
    result: RagAnswerResult | None = None
    error: ProviderError | None = None


class GraphSchemasResponse(BaseModel):
    graphs: list[GraphSource]


class GraphQueryRequest(BaseModel):
    graph_id: str
    query: str
    entity_ids: list[str] = Field(default_factory=list)
    relation_types: list[str] = Field(default_factory=list)
    filters: dict[str, Any] = Field(default_factory=dict)


class GraphQueryResult(BaseModel):
    graph_id: str
    entities: list[dict[str, Any]]
    relations: list[dict[str, Any]]
    paths: list[dict[str, Any]]
    evidence: list[dict[str, Any]]


class GraphQueryResponse(BaseModel):
    ok: bool
    result: GraphQueryResult | None = None
    error: ProviderError | None = None
