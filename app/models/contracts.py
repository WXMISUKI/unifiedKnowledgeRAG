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
    graph: ComponentStatus


class Capability(BaseModel):
    id: str
    status: str
    description: str


class CapabilitiesResponse(BaseModel):
    capabilities: list[Capability]


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


class ProviderError(BaseModel):
    code: str
    message: str


class IngestionJobRequest(BaseModel):
    source_id: str = Field(min_length=1)


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
    error: ProviderError | None = None


class IngestionJobDetailResponse(BaseModel):
    ok: bool
    job: IndexLifecycleJob | None = None
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
