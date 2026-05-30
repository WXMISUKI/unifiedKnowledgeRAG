from abc import ABC, abstractmethod

from app.config import Settings
from app.models.contracts import EvidenceDocument
from app.services import document_retriever
from app.services.request_filter_context import RequestFilterContext
from app.services.source_catalog import knowledge_base_exists


class DocumentRetriever(ABC):
    backend_name: str

    @abstractmethod
    def retrieve(
        self,
        query: str,
        knowledge_base_ids: list[str],
        top_k: int,
        filter_context: RequestFilterContext | None = None,
    ) -> tuple[list[str], list[EvidenceDocument]]:
        raise NotImplementedError

    def build_answer_context(self, documents: list[EvidenceDocument]) -> str:
        return document_retriever.build_answer_context(documents)

    def readiness(self) -> tuple[str, str | None]:
        return "ready", None

    def unknown_sources(self, knowledge_base_ids: list[str]) -> list[str]:
        return [
            source_id
            for source_id in knowledge_base_ids
            if not knowledge_base_exists(source_id)
        ]

    def not_ready_sources(self, knowledge_base_ids: list[str]) -> list[str]:
        return []

    def filters_enforced(self) -> bool:
        return False


class FixtureDocumentRetriever(DocumentRetriever):
    backend_name = "fixture"

    def retrieve(
        self,
        query: str,
        knowledge_base_ids: list[str],
        top_k: int,
        filter_context: RequestFilterContext | None = None,
    ) -> tuple[list[str], list[EvidenceDocument]]:
        return document_retriever.retrieve(query, knowledge_base_ids, top_k)


class LlamaIndexDocumentRetriever(DocumentRetriever):
    backend_name = "llamaindex"

    def __init__(self, settings: Settings):
        self.settings = settings

    def retrieve(
        self,
        query: str,
        knowledge_base_ids: list[str],
        top_k: int,
        filter_context: RequestFilterContext | None = None,
    ) -> tuple[list[str], list[EvidenceDocument]]:
        from app.services.llamaindex_retriever import LlamaIndexLocalRetriever

        return LlamaIndexLocalRetriever(self.settings).retrieve(
            query=query,
            knowledge_base_ids=knowledge_base_ids,
            top_k=top_k,
        )

    def readiness(self) -> tuple[str, str | None]:
        from app.services.llamaindex_retriever import LlamaIndexLocalRetriever

        return LlamaIndexLocalRetriever(self.settings).readiness()

    def not_ready_sources(self, knowledge_base_ids: list[str]) -> list[str]:
        from app.services.index_lifecycle import not_ready_sources

        return not_ready_sources(knowledge_base_ids, self.settings)


class QdrantDocumentRetriever(DocumentRetriever):
    backend_name = "qdrant"

    def __init__(self, settings: Settings):
        self.settings = settings

    def retrieve(
        self,
        query: str,
        knowledge_base_ids: list[str],
        top_k: int,
        filter_context: RequestFilterContext | None = None,
    ) -> tuple[list[str], list[EvidenceDocument]]:
        from app.services.embedding_adapters import create_embedding_adapter
        from app.services.qdrant_vector_store import (
            create_qdrant_client,
            query_qdrant_documents_for_text,
            unknown_qdrant_sources,
        )

        unknown_sources = unknown_qdrant_sources(knowledge_base_ids)
        if unknown_sources:
            return unknown_sources, []
        documents = query_qdrant_documents_for_text(
            client=create_qdrant_client(self.settings),
            query=query,
            source_ids=knowledge_base_ids,
            settings=self.settings,
            embedding_adapter=create_embedding_adapter(self.settings),
            top_k=top_k,
            tenant_id=filter_context.tenant_id if filter_context else None,
            document_ids=filter_context.document_ids if filter_context else None,
            acl_tags=filter_context.acl_tags if filter_context else None,
        )
        return [], documents

    def readiness(self) -> tuple[str, str | None]:
        from app.services.embedding_adapters import create_embedding_adapter
        from app.services.qdrant_vector_store import (
            create_qdrant_client,
            ensure_qdrant_collection,
        )

        embedding_status, embedding_reason = create_embedding_adapter(
            self.settings
        ).readiness()
        qdrant_status, qdrant_reason = ensure_qdrant_collection(
            create_qdrant_client(self.settings),
            self.settings,
        )
        if embedding_status != "ready":
            return "degraded", f"Embedding adapter not ready: {embedding_reason}"
        if qdrant_status != "ready":
            return "degraded", f"Qdrant collection not ready: {qdrant_reason}"
        return "ready", None

    def not_ready_sources(self, knowledge_base_ids: list[str]) -> list[str]:
        from app.services.index_lifecycle import not_ready_sources

        return not_ready_sources(knowledge_base_ids, self.settings)

    def filters_enforced(self) -> bool:
        return True


def create_document_retriever(settings: Settings) -> DocumentRetriever:
    backend = settings.rag_retrieval_backend.lower()
    if backend == "fixture":
        return FixtureDocumentRetriever()
    if backend == "llamaindex":
        return LlamaIndexDocumentRetriever(settings)
    if backend == "qdrant":
        return QdrantDocumentRetriever(settings)
    raise ValueError(f"Unsupported RAG_RETRIEVAL_BACKEND: {settings.rag_retrieval_backend}")
