from fastapi import APIRouter

from app.models.contracts import (
    CatalogResponse,
    ProviderError,
    RagAnswerRequest,
    RagAnswerResponse,
    RagRetrieveRequest,
    RagRetrieveResponse,
    RagRetrieveResult,
    SourceDocumentManifestResponse,
)
from app.config import get_settings
from app.services.retrieval_backends import create_document_retriever
from app.services.rag_answer_orchestrator import create_answer_composer
from app.services.request_filter_context import normalize_request_filter_context
from app.services.retrieval_trace import build_retrieval_trace
from app.services.source_catalog import list_knowledge_bases
from app.services.source_document_manifest import get_source_document_manifest

router = APIRouter(prefix="/api/rag")


@router.get("/sources", response_model=CatalogResponse)
def sources() -> CatalogResponse:
    return CatalogResponse(knowledge_bases=list_knowledge_bases(), graphs=[])


@router.get("/sources/{source_id}/documents", response_model=SourceDocumentManifestResponse)
def source_documents(source_id: str) -> SourceDocumentManifestResponse:
    return get_source_document_manifest(source_id)


@router.post("/retrieve", response_model=RagRetrieveResponse)
def retrieve_documents(request: RagRetrieveRequest) -> RagRetrieveResponse:
    retriever = create_document_retriever(get_settings())
    filter_context = normalize_request_filter_context(request.filters)
    unknown_sources = retriever.unknown_sources(request.knowledge_base_ids)
    if unknown_sources:
        return RagRetrieveResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id(s): {', '.join(unknown_sources)}",
                details={
                    "requested_source_ids": request.knowledge_base_ids,
                    "unknown_source_ids": unknown_sources,
                },
            ),
        )
    not_ready_sources = retriever.not_ready_sources(request.knowledge_base_ids)
    if not_ready_sources:
        return RagRetrieveResponse(
            ok=False,
            error=ProviderError(
                code="INDEX_NOT_READY",
                message=f"Source index is not ready: {', '.join(not_ready_sources)}",
                details={
                    "requested_source_ids": request.knowledge_base_ids,
                    "not_ready_source_ids": not_ready_sources,
                    "retrieval_backend": retriever.backend_name,
                },
            ),
        )
    unknown_sources, documents = retriever.retrieve(
        query=request.query,
        knowledge_base_ids=request.knowledge_base_ids,
        top_k=request.top_k,
        filter_context=filter_context,
    )
    if unknown_sources:
        return RagRetrieveResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id(s): {', '.join(unknown_sources)}",
                details={
                    "requested_source_ids": request.knowledge_base_ids,
                    "unknown_source_ids": unknown_sources,
                },
            ),
        )

    filter_metadata = filter_context.metadata(
        backend=retriever.backend_name,
        enforced=retriever.filters_enforced(),
    )
    retrieval_trace = build_retrieval_trace(
        backend=retriever.backend_name,
        requested_source_ids=request.knowledge_base_ids,
        top_k=request.top_k,
        documents=documents,
        filter_context=filter_metadata,
    )
    return RagRetrieveResponse(
        ok=True,
        result=RagRetrieveResult(
            answer_context=retriever.build_answer_context(documents),
            documents=documents,
            metadata={
                "request_filter_context": filter_metadata,
                "retrieval_trace": retrieval_trace,
            },
        ),
    )


@router.post("/answer", response_model=RagAnswerResponse)
def answer_documents(request: RagAnswerRequest) -> RagAnswerResponse:
    settings = get_settings()
    filter_context = normalize_request_filter_context(request.filters)
    composer, composer_error = create_answer_composer(settings)
    if composer_error is not None or composer is None:
        return RagAnswerResponse(ok=False, error=composer_error)

    retriever = create_document_retriever(settings)
    unknown_sources = retriever.unknown_sources(request.knowledge_base_ids)
    if unknown_sources:
        return RagAnswerResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id(s): {', '.join(unknown_sources)}",
                details={
                    "requested_source_ids": request.knowledge_base_ids,
                    "unknown_source_ids": unknown_sources,
                },
            ),
        )
    not_ready_sources = retriever.not_ready_sources(request.knowledge_base_ids)
    if not_ready_sources:
        return RagAnswerResponse(
            ok=False,
            error=ProviderError(
                code="INDEX_NOT_READY",
                message=f"Source index is not ready: {', '.join(not_ready_sources)}",
                details={
                    "requested_source_ids": request.knowledge_base_ids,
                    "not_ready_source_ids": not_ready_sources,
                    "retrieval_backend": retriever.backend_name,
                },
            ),
        )
    unknown_sources, documents = retriever.retrieve(
        query=request.query,
        knowledge_base_ids=request.knowledge_base_ids,
        top_k=request.top_k,
        filter_context=filter_context,
    )
    if unknown_sources:
        return RagAnswerResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id(s): {', '.join(unknown_sources)}",
                details={
                    "requested_source_ids": request.knowledge_base_ids,
                    "unknown_source_ids": unknown_sources,
                },
            ),
        )

    filter_metadata = filter_context.metadata(
        backend=retriever.backend_name,
        enforced=retriever.filters_enforced(),
    )
    retrieval_trace = build_retrieval_trace(
        backend=retriever.backend_name,
        requested_source_ids=request.knowledge_base_ids,
        top_k=request.top_k,
        documents=documents,
        filter_context=filter_metadata,
    )
    return RagAnswerResponse(
        ok=True,
        result=composer.compose(
            query=request.query,
            documents=documents,
            retrieval_backend=retriever.backend_name,
            min_evidence_count=settings.rag_answer_min_evidence_count,
            min_top_score=settings.rag_answer_min_evidence_score,
            request_filter_context=filter_metadata,
            retrieval_trace=retrieval_trace,
        ),
    )
