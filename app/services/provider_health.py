from app.config import Settings, get_settings
from app.models.contracts import ComponentStatus, HealthResponse
from app.services.index_lifecycle import not_ready_sources
from app.services.rag_answer_orchestrator import answer_composer_readiness
from app.services.retrieval_backends import create_document_retriever
from app.services.source_catalog import KNOWLEDGE_BASES


def build_health_response(settings: Settings | None = None) -> HealthResponse:
    settings = settings or get_settings()
    retriever = create_document_retriever(settings)
    backend_status, backend_reason = retriever.readiness()
    answer_status, answer_reason, answer_backend, _answer_model = (
        answer_composer_readiness(settings)
    )
    index_not_ready = not_ready_sources([source.id for source in KNOWLEDGE_BASES], settings)
    index_status = "ready" if not index_not_ready else "degraded"
    service_status = (
        "ok"
        if backend_status == "ready"
        and index_status == "ready"
        and answer_status == "ready"
        else "degraded"
    )
    rag_status = (
        "ready" if backend_status == "ready" and index_status == "ready" else "degraded"
    )
    return HealthResponse(
        status=service_status,
        service="unifiedKnowledgeProvider",
        rag=ComponentStatus(
            status=rag_status,
            reason=backend_reason
            or (
                f"Source index not ready: {', '.join(index_not_ready)}"
                if index_not_ready
                else None
            ),
            backend=retriever.backend_name,
            backend_status=backend_status,
            index_status=index_status,
        ),
        answer=ComponentStatus(
            status=answer_status,
            reason=answer_reason,
            backend=answer_backend,
            backend_status=answer_status,
        ),
        graph=ComponentStatus(
            status="planned",
            reason="Graph query execution is not in slice v1.",
        ),
    )
