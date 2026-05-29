import re
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
QDRANT_SECTION_CHUNKING_STRATEGY = "markdown-section-v1"
QDRANT_TOKEN_WINDOW_CHUNKING_STRATEGY = "token-window-v1"
TOKEN_WINDOW_DEFAULT_MAX_TOKENS = 120
TOKEN_WINDOW_DEFAULT_OVERLAP_TOKENS = 24
TOKEN_WINDOW_DEFAULT_MIN_TOKENS = 12
LOCAL_SOURCE_CITATION_ANCHORS = {
    "refund_policy_docs": {
        1: "refund_policy_2026#section-3",
        2: "refund_policy_2026#section-5",
        3: "refund_policy_2026#exception",
        4: "refund_policy_2026#high-value-review",
        5: "refund_policy_2026#address-change",
        6: "refund_policy_2026#appeal-review",
    },
    "logistics_faq": {
        1: "logistics_faq_2026#delay",
        2: "logistics_faq_2026#same-city-timeout",
        3: "logistics_faq_2026#lost-package",
        4: "logistics_faq_2026#address-intercept",
        5: "logistics_faq_2026#batch-exception",
    },
}
LOCAL_SOURCE_SECTION_CITATION_ANCHORS = {
    "refund_policy_docs": {
        1: "refund_policy_2026#section-candidate",
    },
    "logistics_faq": {
        1: "logistics_faq_2026#section-candidate",
    },
}
LOCAL_SOURCE_TOKEN_WINDOW_CITATION_ANCHORS = {
    "refund_policy_docs": {
        1: "refund_policy_2026#token-window-candidate-1",
    },
    "logistics_faq": {
        1: "logistics_faq_2026#token-window-candidate-1",
    },
}


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
            citation=_citation_for(source_id, document_id, index),
            vector=[],
            metadata={
                "tenant_id": "default",
                "source_path": str(source_path),
                "chunking_strategy": QDRANT_CHUNKING_STRATEGY,
            },
        )
        for index, paragraph in enumerate(paragraphs, start=1)
    ]


def markdown_source_to_section_chunks(
    source_id: str,
    source_path: Path,
    content: str,
) -> list[VectorEvidenceChunk]:
    document_id = _document_id_for(source_id)
    sections = _source_sections(content)
    return [
        VectorEvidenceChunk(
            point_id=f"{document_id}:section-{index}",
            source_id=source_id,
            document_id=document_id,
            chunk_id=f"section-{index}",
            title=section["title"],
            text=section["text"],
            citation=_section_citation_for(source_id, document_id, index),
            vector=[],
            metadata={
                "tenant_id": "default",
                "source_path": str(source_path),
                "chunking_strategy": QDRANT_SECTION_CHUNKING_STRATEGY,
                "section_title": section["title"],
            },
        )
        for index, section in enumerate(sections, start=1)
    ]


def markdown_source_to_token_window_chunks(
    source_id: str,
    source_path: Path,
    content: str,
    max_tokens: int = TOKEN_WINDOW_DEFAULT_MAX_TOKENS,
    overlap_tokens: int = TOKEN_WINDOW_DEFAULT_OVERLAP_TOKENS,
    min_tokens: int = TOKEN_WINDOW_DEFAULT_MIN_TOKENS,
) -> list[VectorEvidenceChunk]:
    _validate_token_window_settings(max_tokens, overlap_tokens, min_tokens)
    document_id = _document_id_for(source_id)
    title = _title_for(source_id, content)
    tokens = _tokenize_for_window(" ".join(_source_paragraphs(content)))
    windows = _token_windows(tokens, max_tokens, overlap_tokens, min_tokens)
    return [
        VectorEvidenceChunk(
            point_id=f"{document_id}:token-window-{index}",
            source_id=source_id,
            document_id=document_id,
            chunk_id=f"token-window-{index}",
            title=title,
            text=_join_window_tokens(window),
            citation=_token_window_citation_for(source_id, document_id, index),
            vector=[],
            metadata={
                "tenant_id": "default",
                "source_path": str(source_path),
                "chunking_strategy": QDRANT_TOKEN_WINDOW_CHUNKING_STRATEGY,
                "token_window_max_tokens": max_tokens,
                "token_window_overlap_tokens": overlap_tokens,
                "token_window_min_tokens": min_tokens,
            },
        )
        for index, window in enumerate(windows, start=1)
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


def _to_qdrant_filter(payload_filter: dict[str, Any]):
    must = payload_filter.get("must", [])
    if not must:
        return None

    from qdrant_client import models

    conditions = []
    for condition in must:
        key = condition["key"]
        match = condition["match"]
        if "value" in match:
            qdrant_match = models.MatchValue(value=match["value"])
        elif "any" in match:
            qdrant_match = models.MatchAny(any=match["any"])
        else:
            raise ValueError(f"Unsupported Qdrant match condition: {match}")
        conditions.append(models.FieldCondition(key=key, match=qdrant_match))
    return models.Filter(must=conditions)


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
        query_filter=_to_qdrant_filter(payload_filter),
        limit=top_k,
        with_payload=True,
    )
    hits = getattr(result, "points", result)
    documents = []
    for hit in hits:
        document = _hit_to_evidence_document(hit, min_score=settings.rag_score_threshold)
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


def _hit_to_evidence_document(hit, min_score: float) -> EvidenceDocument | None:
    payload = _hit_value(hit, "payload") or {}
    score = _hit_value(hit, "score") or 0.0
    if float(score) < min_score:
        return None
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


def _citation_for(source_id: str, document_id: str, paragraph_index: int) -> str:
    return LOCAL_SOURCE_CITATION_ANCHORS.get(source_id, {}).get(
        paragraph_index,
        f"{document_id}#chunk-{paragraph_index}",
    )


def _section_citation_for(source_id: str, document_id: str, section_index: int) -> str:
    return LOCAL_SOURCE_SECTION_CITATION_ANCHORS.get(source_id, {}).get(
        section_index,
        f"{document_id}#section-{section_index}",
    )


def _token_window_citation_for(
    source_id: str,
    document_id: str,
    window_index: int,
) -> str:
    return LOCAL_SOURCE_TOKEN_WINDOW_CITATION_ANCHORS.get(source_id, {}).get(
        window_index,
        f"{document_id}#token-window-{window_index}",
    )


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


def _source_sections(content: str) -> list[dict[str, str]]:
    sections = []
    current_title = ""
    current_lines = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            if current_lines:
                sections.append({
                    "title": current_title,
                    "text": " ".join(current_lines),
                })
                current_lines = []
            current_title = line.lstrip("#").strip()
            continue
        current_lines.append(line)
    if current_lines:
        sections.append({
            "title": current_title or "Untitled Section",
            "text": " ".join(current_lines),
        })
    return sections


def _validate_token_window_settings(
    max_tokens: int,
    overlap_tokens: int,
    min_tokens: int,
) -> None:
    if max_tokens <= 0:
        raise ValueError("max_tokens must be greater than zero.")
    if min_tokens <= 0:
        raise ValueError("min_tokens must be greater than zero.")
    if overlap_tokens < 0:
        raise ValueError("overlap_tokens must be greater than or equal to zero.")
    if overlap_tokens >= max_tokens:
        raise ValueError("overlap_tokens must be smaller than max_tokens.")
    if min_tokens > max_tokens:
        raise ValueError("min_tokens must be smaller than or equal to max_tokens.")


def _tokenize_for_window(text: str) -> list[str]:
    return re.findall(r"[\u4e00-\u9fff]|[A-Za-z0-9_]+|[^\s]", text)


def _token_windows(
    tokens: list[str],
    max_tokens: int,
    overlap_tokens: int,
    min_tokens: int,
) -> list[list[str]]:
    if not tokens:
        return []
    step = max_tokens - overlap_tokens
    windows = []
    start = 0
    while start < len(tokens):
        window = tokens[start:start + max_tokens]
        if len(window) < min_tokens and windows:
            break
        windows.append(window)
        if start + max_tokens >= len(tokens):
            break
        start += step
    return windows


def _join_window_tokens(tokens: list[str]) -> str:
    text = ""
    previous = ""
    for token in tokens:
        if _needs_space_between(previous, token):
            text += " "
        text += token
        previous = token
    return text


def _needs_space_between(previous: str, current: str) -> bool:
    if not previous:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", previous) and re.fullmatch(
        r"[A-Za-z0-9_]+",
        current,
    ))
