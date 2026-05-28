from pathlib import Path
from datetime import UTC, datetime

from app.config import Settings
from app.models.contracts import EvidenceDocument
from app.services.source_catalog import get_knowledge_base, knowledge_base_exists


class LlamaIndexLocalRetriever:
    backend_name = "llamaindex"

    def __init__(self, settings: Settings):
        self.settings = settings

    def retrieve(
        self,
        query: str,
        knowledge_base_ids: list[str],
        top_k: int,
    ) -> tuple[list[str], list[EvidenceDocument]]:
        unknown_sources = [
            source_id
            for source_id in knowledge_base_ids
            if not knowledge_base_exists(source_id)
        ]
        if unknown_sources:
            return unknown_sources, []

        from app.services.index_lifecycle import not_ready_sources

        if not_ready_sources(knowledge_base_ids, self.settings):
            return [], []

        index = self._load_or_build_index(knowledge_base_ids)
        retriever = index.as_retriever(similarity_top_k=top_k)
        nodes = retriever.retrieve(query)
        documents = [
            self._node_to_document(node)
            for node in nodes
            if self._node_score(node) >= self.settings.rag_score_threshold
        ]
        return [], documents[:top_k]

    def readiness(self) -> tuple[str, str | None]:
        if not self.settings.rag_source_dir.exists():
            return "degraded", f"Source directory not found: {self.settings.rag_source_dir}"

        available_sources = [
            source_id
            for source_id in ("refund_policy_docs", "logistics_faq")
            if self._source_path(source_id).exists()
        ]
        if not available_sources:
            return "degraded", "No configured LlamaIndex source documents found."

        from app.services.index_lifecycle import not_ready_sources

        not_ready = not_ready_sources(available_sources, self.settings)
        if not_ready:
            return "degraded", f"Source index not ready: {', '.join(not_ready)}"
        return "ready", None

    def build_index(self, knowledge_base_ids: list[str], latest_job_id: str) -> None:
        unknown_sources = [
            source_id
            for source_id in knowledge_base_ids
            if not knowledge_base_exists(source_id)
        ]
        if unknown_sources:
            raise ValueError(f"Unknown knowledge base id(s): {', '.join(unknown_sources)}")

        self._load_or_build_index(knowledge_base_ids)
        for source_id in knowledge_base_ids:
            self._write_status_marker(
                source_id=source_id,
                status="ready",
                reason=None,
                latest_job_id=latest_job_id,
                indexed_at=datetime.now(UTC).isoformat(),
            )

    def _load_or_build_index(self, knowledge_base_ids: list[str]):
        self._configure_llamaindex()

        from llama_index.core import Document, VectorStoreIndex

        documents = []
        for source_id in knowledge_base_ids:
            source_path = self._source_path(source_id)
            if not source_path.exists():
                continue
            source = get_knowledge_base(source_id)
            documents.append(
                Document(
                    text=source_path.read_text(encoding="utf-8"),
                    metadata={
                        "source_id": source_id,
                        "document_id": _document_id_for(source_id),
                        "title": _title_for(source_id),
                        "citation": _citation_for(source_id),
                        "source_status": source.status if source else "unknown",
                    },
                )
            )

        if not documents:
            return VectorStoreIndex.from_documents([])

        return VectorStoreIndex.from_documents(documents)

    def _configure_llamaindex(self) -> None:
        from llama_index.core import Settings as LlamaSettings
        from llama_index.core.embeddings import MockEmbedding

        LlamaSettings.embed_model = MockEmbedding(embed_dim=384)
        LlamaSettings.llm = None

    def _source_path(self, source_id: str) -> Path:
        return self.settings.rag_source_dir / f"{source_id}.md"

    def _write_status_marker(
        self,
        source_id: str,
        status: str,
        reason: str | None,
        latest_job_id: str,
        indexed_at: str | None,
    ) -> None:
        marker = self.settings.rag_index_dir / f"{source_id}.index.json"
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(
            (
                "{\n"
                f'  "source_id": "{source_id}",\n'
                f'  "status": "{status}",\n'
                f'  "reason": {self._json_string(reason)},\n'
                f'  "latest_job_id": "{latest_job_id}",\n'
                f'  "indexed_at": {self._json_string(indexed_at)}\n'
                "}\n"
            ),
            encoding="utf-8",
        )

    def _json_string(self, value: str | None) -> str:
        if value is None:
            return "null"
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'

    def _node_to_document(self, node) -> EvidenceDocument:
        metadata = node.node.metadata
        return EvidenceDocument(
            source_id=metadata["source_id"],
            document_id=metadata["document_id"],
            title=metadata["title"],
            snippet=node.node.get_content(metadata_mode="none"),
            score=float(self._node_score(node)),
            citation=metadata["citation"],
        )

    def _node_score(self, node) -> float:
        return float(node.score or 0.0)


def _document_id_for(source_id: str) -> str:
    return {
        "refund_policy_docs": "refund_policy_2026",
        "logistics_faq": "logistics_faq_2026",
    }.get(source_id, source_id)


def _title_for(source_id: str) -> str:
    return {
        "refund_policy_docs": "售后退款规则",
        "logistics_faq": "物流常见问题",
    }.get(source_id, source_id)


def _citation_for(source_id: str) -> str:
    return {
        "refund_policy_docs": "refund_policy_2026#section-3",
        "logistics_faq": "logistics_faq_2026#delay",
    }.get(source_id, source_id)
