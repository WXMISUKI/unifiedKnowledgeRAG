from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from app.config import Settings
from app.models.contracts import EvidenceDocument, IndexStatusResponse
from app.services.embedding_adapters import EmbeddingAdapter, create_embedding_adapter
from app.services.index_lifecycle_store import IndexLifecycleStore
from app.services.source_catalog import get_knowledge_base, knowledge_base_exists


QDRANT_CHUNKING_STRATEGY = "markdown-paragraph-v1"


@dataclass(frozen=True)
class VectorEvidenceChunk:
    point_id: str
    source_id: str
    document_id: str
    chunk_id: str
    title: str
    text: str
    citation: str
    vector: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


def chunk_to_qdrant_point(
    chunk: VectorEvidenceChunk,
    settings: Settings,
) -> dict[str, Any]:
    payload = {
        "tenant_id": chunk.metadata.get("tenant_id", "default"),
        "source_id": chunk.source_id,
        "document_id": chunk.document_id,
        "chunk_id": chunk.chunk_id,
        "title": chunk.title,
        "text": chunk.text,
        "citation": chunk.citation,
    }
    payload.update(chunk.metadata)
    payload["point_id"] = chunk.point_id
    return {
        "id": _qdrant_point_id(chunk.point_id),
        "vector": {settings.qdrant_vector_name: chunk.vector},
        "payload": payload,
    }


def build_qdrant_payload_filter(
    source_ids: list[str],
    tenant_id: str | None = None,
    document_ids: list[str] | None = None,
    acl_tags: list[str] | None = None,
) -> dict[str, Any]:
    must: list[dict[str, Any]] = []
    if tenant_id:
        must.append({"key": "tenant_id", "match": {"value": tenant_id}})
    if source_ids:
        must.append({"key": "source_id", "match": {"any": source_ids}})
    if document_ids:
        must.append({"key": "document_id", "match": {"any": document_ids}})
    if acl_tags:
        must.append({"key": "acl_tags", "match": {"any": acl_tags}})
    return {"must": must}


def unknown_qdrant_sources(source_ids: list[str]) -> list[str]:
    return [source_id for source_id in source_ids if not knowledge_base_exists(source_id)]


def build_qdrant_source_index(
    source_id: str,
    settings: Settings,
    latest_job_id: str,
    client=None,
) -> int:
    chunks = embed_qdrant_chunks(
        load_qdrant_source_chunks(source_id, settings),
        create_embedding_adapter(settings),
    )
    client = client or create_qdrant_client(settings)
    status, reason = ensure_qdrant_collection(client, settings)
    if status != "ready":
        raise RuntimeError(reason or "Qdrant collection is not ready.")
    count = upsert_qdrant_chunks(client, chunks, settings)
    IndexLifecycleStore(settings).write_source_status(IndexStatusResponse(
        source_id=source_id,
        status="ready",
        backend="qdrant",
        indexed_at=datetime.now(UTC).isoformat(),
        latest_job_id=latest_job_id,
        reason=f"Upserted {count} Qdrant chunk(s).",
    ))
    return count


def load_qdrant_source_chunks(
    source_id: str,
    settings: Settings,
) -> list[VectorEvidenceChunk]:
    if not knowledge_base_exists(source_id):
        raise ValueError(f"Unknown knowledge base id: {source_id}")
    source_path = settings.rag_source_dir / f"{source_id}.md"
    if not source_path.exists():
        raise FileNotFoundError(f"Source document not found: {source_path}")
    return markdown_source_to_qdrant_chunks(
        source_id=source_id,
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
    )


def markdown_source_to_qdrant_chunks(
    source_id: str,
    source_path: Path,
    content: str,
) -> list[VectorEvidenceChunk]:
    document_id = _document_id_for(source_id)
    title = _title_for(source_id, content)
    paragraphs = _source_paragraphs(content)
    return [
        VectorEvidenceChunk(
            point_id=f"{document_id}:chunk-{index}",
            source_id=source_id,
            document_id=document_id,
            chunk_id=f"chunk-{index}",
            title=title,
            text=paragraph,
            citation=f"{document_id}#chunk-{index}",
            vector=[],
            metadata={
                "tenant_id": "default",
                "source_path": str(source_path),
                "chunking_strategy": QDRANT_CHUNKING_STRATEGY,
            },
        )
        for index, paragraph in enumerate(paragraphs, start=1)
    ]


def create_qdrant_client(settings: Settings):
    from qdrant_client import QdrantClient

    if settings.qdrant_url == ":memory:":
        return QdrantClient(":memory:")
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)


def ensure_qdrant_collection(client, settings: Settings) -> tuple[str, str | None]:
    try:
        if client.collection_exists(settings.qdrant_collection):
            return "ready", None
        from qdrant_client import models

        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config={
                settings.qdrant_vector_name: models.VectorParams(
                    size=settings.qdrant_vector_size,
                    distance=models.Distance.COSINE,
                )
            },
        )
        return "ready", None
    except Exception as exc:
        return "degraded", str(exc)


def upsert_qdrant_chunks(
    client,
    chunks: list[VectorEvidenceChunk],
    settings: Settings,
) -> int:
    points = [_to_qdrant_point_struct(chunk_to_qdrant_point(chunk, settings)) for chunk in chunks]
    if not points:
        return 0
    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
        wait=True,
    )
    return len(points)


def _to_qdrant_point_struct(point: dict[str, Any]):
    from qdrant_client import models

    return models.PointStruct(
        id=point["id"],
        vector=point["vector"],
        payload=point["payload"],
    )


def embed_qdrant_chunks(
    chunks: list[VectorEvidenceChunk],
    embedding_adapter: EmbeddingAdapter,
) -> list[VectorEvidenceChunk]:
    vectors = embedding_adapter.embed_batch([chunk.text for chunk in chunks])
    return [
        VectorEvidenceChunk(
            point_id=chunk.point_id,
            source_id=chunk.source_id,
            document_id=chunk.document_id,
            chunk_id=chunk.chunk_id,
            title=chunk.title,
            text=chunk.text,
            citation=chunk.citation,
            vector=vector,
            metadata={
                **chunk.metadata,
                "embedding_provider": embedding_adapter.provider_name,
                "embedding_model": embedding_adapter.model_name,
            },
        )
        for chunk, vector in zip(chunks, vectors)
    ]


def query_qdrant_documents(
    client,
    query_vector: list[float],
    source_ids: list[str],
    settings: Settings,
    top_k: int,
    tenant_id: str | None = None,
    document_ids: list[str] | None = None,
    acl_tags: list[str] | None = None,
) -> list[EvidenceDocument]:
    payload_filter = build_qdrant_payload_filter(
        source_ids=source_ids,
        tenant_id=tenant_id,
        document_ids=document_ids,
        acl_tags=acl_tags,
    )
    result = client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        using=settings.qdrant_vector_name,
        query_filter=payload_filter,
        limit=top_k,
        with_payload=True,
    )
    hits = getattr(result, "points", result)
    documents = []
    for hit in hits:
        document = _hit_to_evidence_document(hit)
        if document is not None:
            documents.append(document)
    return documents


def query_qdrant_documents_for_text(
    client,
    query: str,
    source_ids: list[str],
    settings: Settings,
    embedding_adapter: EmbeddingAdapter,
    top_k: int,
    tenant_id: str | None = None,
    document_ids: list[str] | None = None,
    acl_tags: list[str] | None = None,
) -> list[EvidenceDocument]:
    query_vector = embedding_adapter.embed_text(query)
    return query_qdrant_documents(
        client=client,
        query_vector=query_vector,
        source_ids=source_ids,
        settings=settings,
        top_k=top_k,
        tenant_id=tenant_id,
        document_ids=document_ids,
        acl_tags=acl_tags,
    )


def _hit_to_evidence_document(hit) -> EvidenceDocument | None:
    payload = _hit_value(hit, "payload") or {}
    score = _hit_value(hit, "score") or 0.0
    required_fields = ("source_id", "document_id", "title", "text", "citation")
    if any(field not in payload for field in required_fields):
        return None
    return EvidenceDocument(
        source_id=payload["source_id"],
        document_id=payload["document_id"],
        title=payload["title"],
        snippet=payload["text"],
        score=float(score),
        citation=payload["citation"],
    )


def _hit_value(hit, key: str):
    if isinstance(hit, dict):
        return hit.get(key)
    return getattr(hit, key, None)


def _qdrant_point_id(stable_id: str) -> str:
    return str(uuid5(NAMESPACE_URL, f"unifiedKnowledgeRAG:qdrant:{stable_id}"))


def _document_id_for(source_id: str) -> str:
    return {
        "refund_policy_docs": "refund_policy_2026",
        "logistics_faq": "logistics_faq_2026",
    }.get(source_id, source_id)


def _title_for(source_id: str, content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    source = get_knowledge_base(source_id)
    return source.id if source is not None else source_id


def _source_paragraphs(content: str) -> list[str]:
    paragraphs = []
    current_lines = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            if current_lines:
                paragraphs.append(" ".join(current_lines))
                current_lines = []
            continue
        if line.startswith("#"):
            continue
        current_lines.append(line)
    if current_lines:
        paragraphs.append(" ".join(current_lines))
    return paragraphs
