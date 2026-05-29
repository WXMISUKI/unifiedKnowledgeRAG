from fastapi import APIRouter

from app.models.contracts import (
    CatalogResponse,
    ProviderError,
    RagAnswerRequest,
    RagAnswerResponse,
    RagRetrieveRequest,
    RagRetrieveResponse,
    RagRetrieveResult,
)
from app.config import get_settings
from app.services.retrieval_backends import create_document_retriever
from app.services.rag_answer_orchestrator import compose_cited_answer
from app.services.source_catalog import list_knowledge_bases

router = APIRouter(prefix="/api/rag")


@router.get("/sources", response_model=CatalogResponse)
def sources() -> CatalogResponse:
    return CatalogResponse(knowledge_bases=list_knowledge_bases(), graphs=[])


@router.post("/retrieve", response_model=RagRetrieveResponse)
def retrieve_documents(request: RagRetrieveRequest) -> RagRetrieveResponse:
    retriever = create_document_retriever(get_settings())
    unknown_sources = retriever.unknown_sources(request.knowledge_base_ids)
    if unknown_sources:
        return RagRetrieveResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id(s): {', '.join(unknown_sources)}",
            ),
        )
    not_ready_sources = retriever.not_ready_sources(request.knowledge_base_ids)
    if not_ready_sources:
        return RagRetrieveResponse(
            ok=False,
            error=ProviderError(
                code="INDEX_NOT_READY",
                message=f"Source index is not ready: {', '.join(not_ready_sources)}",
            ),
        )
    unknown_sources, documents = retriever.retrieve(
        query=request.query,
        knowledge_base_ids=request.knowledge_base_ids,
        top_k=request.top_k,
    )
    if unknown_sources:
        return RagRetrieveResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id(s): {', '.join(unknown_sources)}",
            ),
        )

    return RagRetrieveResponse(
        ok=True,
        result=RagRetrieveResult(
            answer_context=retriever.build_answer_context(documents),
            documents=documents,
        ),
    )


@router.post("/answer", response_model=RagAnswerResponse)
def answer_documents(request: RagAnswerRequest) -> RagAnswerResponse:
    settings = get_settings()
    retriever = create_document_retriever(settings)
    unknown_sources = retriever.unknown_sources(request.knowledge_base_ids)
    if unknown_sources:
        return RagAnswerResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id(s): {', '.join(unknown_sources)}",
            ),
        )
    not_ready_sources = retriever.not_ready_sources(request.knowledge_base_ids)
    if not_ready_sources:
        return RagAnswerResponse(
            ok=False,
            error=ProviderError(
                code="INDEX_NOT_READY",
                message=f"Source index is not ready: {', '.join(not_ready_sources)}",
            ),
        )
    unknown_sources, documents = retriever.retrieve(
        query=request.query,
        knowledge_base_ids=request.knowledge_base_ids,
        top_k=request.top_k,
    )
    if unknown_sources:
        return RagAnswerResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id(s): {', '.join(unknown_sources)}",
            ),
        )

    return RagAnswerResponse(
        ok=True,
        result=compose_cited_answer(
            documents=documents,
            retrieval_backend=retriever.backend_name,
            min_evidence_count=settings.rag_answer_min_evidence_count,
            min_top_score=settings.rag_answer_min_evidence_score,
        ),
    )
