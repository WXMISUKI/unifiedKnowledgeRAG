from fastapi import APIRouter

from app.config import get_settings
from app.models.contracts import ComponentStatus, HealthResponse
from app.services.source_catalog import KNOWLEDGE_BASES
from app.services.index_lifecycle import not_ready_sources
from app.services.retrieval_backends import create_document_retriever

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    retriever = create_document_retriever(settings)
    backend_status, backend_reason = retriever.readiness()
    index_not_ready = not_ready_sources([source.id for source in KNOWLEDGE_BASES], settings)
    index_status = "ready" if not index_not_ready else "degraded"
    service_status = "ok" if backend_status == "ready" and index_status == "ready" else "degraded"
    return HealthResponse(
        status=service_status,
        service="unifiedKnowledgeProvider",
        rag=ComponentStatus(
            status="ready" if backend_status == "ready" and index_status == "ready" else "degraded",
            reason=backend_reason or (
                f"Source index not ready: {', '.join(index_not_ready)}"
                if index_not_ready
                else None
            ),
            backend=retriever.backend_name,
            backend_status=backend_status,
            index_status=index_status,
        ),
        graph=ComponentStatus(status="planned", reason="Graph query execution is not in slice v1."),
    )
