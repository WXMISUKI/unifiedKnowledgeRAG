from app.config import get_settings
from app.models.contracts import GraphSource, KnowledgeBaseSource


KNOWLEDGE_BASES = [
    KnowledgeBaseSource(
        id="refund_policy_docs",
        status="ready",
        owner="customer_service",
        version="2026-05-28",
        embedding_model="local-lexical-v1",
        vector_store="in_memory",
        freshness="static_fixture",
    ),
    KnowledgeBaseSource(
        id="logistics_faq",
        status="ready",
        owner="logistics",
        version="2026-05-28",
        embedding_model="local-lexical-v1",
        vector_store="in_memory",
        freshness="static_fixture",
    ),
]

EVALUATION_ONLY_KNOWLEDGE_BASE_IDS = {
    "split_refund_policy_docs",
}

GRAPHS = [
    GraphSource(
        id="ecommerce_order_graph",
        status="planned",
        owner="customer_service",
        ontology_version="2026-05",
        graph_store="neo4j_planned",
        entity_types=["Order", "Refund", "Shipment", "Customer"],
        relation_types=["has_refund", "shipped_by", "placed_by"],
    )
]


def list_knowledge_bases(settings=None) -> list[KnowledgeBaseSource]:
    settings = settings or get_settings()
    backend_status, backend_reason = _document_backend_readiness()
    from app.services.index_lifecycle import get_index_status

    return [
        source.model_copy(
            update={
                "retrieval_backend": settings.rag_retrieval_backend,
                "backend_status": backend_status,
                "backend_reason": backend_reason,
                "index_status": (index_status := get_index_status(source.id, settings)).status,
                "index_reason": index_status.reason,
                "indexed_at": index_status.indexed_at,
                "latest_index_job_id": index_status.latest_job_id,
            }
        )
        for source in KNOWLEDGE_BASES
    ]


def get_knowledge_base(source_id: str) -> KnowledgeBaseSource | None:
    return next((source for source in KNOWLEDGE_BASES if source.id == source_id), None)


def list_graphs() -> list[GraphSource]:
    return GRAPHS


def knowledge_base_exists(source_id: str) -> bool:
    return (
        get_knowledge_base(source_id) is not None
        or source_id in EVALUATION_ONLY_KNOWLEDGE_BASE_IDS
    )


def _document_backend_readiness() -> tuple[str, str | None]:
    from app.services.retrieval_backends import create_document_retriever

    retriever = create_document_retriever(get_settings())
    return retriever.readiness()
