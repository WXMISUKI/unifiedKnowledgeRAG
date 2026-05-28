from abc import ABC, abstractmethod

from app.config import Settings
from app.models.contracts import EvidenceDocument
from app.services import document_retriever


class DocumentRetriever(ABC):
    backend_name: str

    @abstractmethod
    def retrieve(
        self,
        query: str,
        knowledge_base_ids: list[str],
        top_k: int,
    ) -> tuple[list[str], list[EvidenceDocument]]:
        raise NotImplementedError

    def build_answer_context(self, documents: list[EvidenceDocument]) -> str:
        return document_retriever.build_answer_context(documents)

    def readiness(self) -> tuple[str, str | None]:
        return "ready", None

    def not_ready_sources(self, knowledge_base_ids: list[str]) -> list[str]:
        return []


class FixtureDocumentRetriever(DocumentRetriever):
    backend_name = "fixture"

    def retrieve(
        self,
        query: str,
        knowledge_base_ids: list[str],
        top_k: int,
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


def create_document_retriever(settings: Settings) -> DocumentRetriever:
    backend = settings.rag_retrieval_backend.lower()
    if backend == "fixture":
        return FixtureDocumentRetriever()
    if backend == "llamaindex":
        return LlamaIndexDocumentRetriever(settings)
    raise ValueError(f"Unsupported RAG_RETRIEVAL_BACKEND: {settings.rag_retrieval_backend}")
