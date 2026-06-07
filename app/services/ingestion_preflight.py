from pathlib import Path

from app.config import Settings, get_settings
from app.models.contracts import (
    IngestionDocumentChunkPreview,
    IngestionDocumentPreflight,
    IngestionSourcePreflightResponse,
    IngestionSourcePreflightResult,
    ProviderError,
    SourceChunkManifest,
    SourceDocumentManifest,
)
from app.services.index_lifecycle import get_index_status
from app.services.source_catalog import get_knowledge_base
from app.services.source_document_manifest import (
    SOURCE_DOCUMENT_MANIFESTS,
    build_chunk_manifest,
    get_source_document_manifests_for,
)
from app.services.source_package import get_source_package


SUPPORTED_FORMATS = {"markdown"}
MAX_CHUNK_PREVIEW_COUNT = 3
MAX_CHUNK_PREVIEW_CHARS = 160


def get_ingestion_source_preflight(
    source_id: str,
    settings: Settings | None = None,
) -> IngestionSourcePreflightResponse:
    settings = settings or get_settings()
    source = get_knowledge_base(source_id)
    if source is None:
        return IngestionSourcePreflightResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id: {source_id}",
                details={
                    "requested_source_id": source_id,
                    "unknown_source_ids": [source_id],
                },
            ),
        )

    index_status = get_index_status(source_id, settings)
    documents = [
        _preflight_document(document)
        for document in get_source_document_manifests_for(source_id)
    ]
    status = _source_status(documents)
    return IngestionSourcePreflightResponse(
        ok=True,
        result=IngestionSourcePreflightResult(
            source_id=source_id,
            status=status,
            retrieval_backend=settings.rag_retrieval_backend.lower(),
            index_status=index_status.status,
            index_reason=index_status.reason,
            latest_index_job_id=index_status.latest_job_id,
            source_package=get_source_package(source_id),
            documents=documents,
            operation_notes=_operation_notes(status, documents),
            recommended_action=_source_recommended_action(status, documents),
        ),
    )


def _preflight_document(document: SourceDocumentManifest) -> IngestionDocumentPreflight:
    source_path = Path(document.source_path)
    format_supported = document.format.lower() in SUPPORTED_FORMATS
    if not source_path.exists():
        return _document_result(
            document=document,
            format_supported=format_supported,
            file_status="missing",
            parser_status="missing_source_file",
            recommended_action="restore_source_file_before_ingestion",
            reason="Source file is missing.",
        )
    if not format_supported:
        return _document_result(
            document=document,
            format_supported=False,
            file_status="present",
            parser_status="unsupported_format",
            recommended_action="add_parser_support_before_ingestion",
            reason=f"Unsupported document format for this slice: {document.format}",
        )

    text = source_path.read_text(encoding="utf-8")
    chunks = _markdown_chunks(text)
    chunk_manifest = build_chunk_manifest(document, source_path)
    if not chunks:
        return _document_result(
            document=document,
            format_supported=True,
            file_status="present",
            parser_status="empty_content",
            recommended_action="repair_source_content_before_ingestion",
            reason="Markdown source file has no chunkable content.",
        )
    if not document.citation_anchors:
        return _document_result(
            document=document,
            format_supported=True,
            file_status="present",
            parser_status="missing_citation_anchors",
            chunk_count=len(chunks),
            chunk_preview=_chunk_preview(chunks),
            chunk_manifest=chunk_manifest,
            recommended_action="add_citation_anchors_before_ingestion",
            reason="Document manifest has no citation anchors.",
        )
    return _document_result(
        document=document,
        format_supported=True,
        file_status="present",
        parser_status="ready",
        chunk_count=len(chunks),
        chunk_preview=_chunk_preview(chunks),
        chunk_manifest=chunk_manifest,
        recommended_action="run_ingestion_job",
    )


def _document_result(
    *,
    document: SourceDocumentManifest,
    format_supported: bool,
    file_status: str,
    parser_status: str,
    recommended_action: str,
    reason: str | None = None,
    chunk_count: int = 0,
    chunk_preview: list[IngestionDocumentChunkPreview] | None = None,
    chunk_manifest: list[SourceChunkManifest] | None = None,
) -> IngestionDocumentPreflight:
    return IngestionDocumentPreflight(
        document_id=document.document_id,
        title=document.title,
        source_path=document.source_path,
        format=document.format,
        format_supported=format_supported,
        file_status=file_status,
        parser_status=parser_status,
        chunking_strategy=document.chunking_strategy,
        chunk_count=chunk_count,
        chunk_preview=chunk_preview or [],
        chunk_manifest=chunk_manifest or [],
        citation_anchor_count=len(document.citation_anchors),
        recommended_action=recommended_action,
        reason=reason,
    )


def _markdown_chunks(text: str) -> list[str]:
    chunks: list[str] = []
    current_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current_lines:
                chunks.append(" ".join(current_lines))
                current_lines = []
            continue
        if line.startswith("#"):
            continue
        current_lines.append(line)
    if current_lines:
        chunks.append(" ".join(current_lines))
    return chunks


def _chunk_preview(chunks: list[str]) -> list[IngestionDocumentChunkPreview]:
    return [
        IngestionDocumentChunkPreview(
            chunk_id=f"chunk-{index}",
            text_preview=chunk[:MAX_CHUNK_PREVIEW_CHARS],
            char_count=len(chunk),
        )
        for index, chunk in enumerate(chunks[:MAX_CHUNK_PREVIEW_COUNT], start=1)
    ]


def _source_status(documents: list[IngestionDocumentPreflight]) -> str:
    if not documents:
        return "blocked"
    if all(document.parser_status == "ready" for document in documents):
        return "ready"
    return "blocked"


def _source_recommended_action(
    status: str,
    documents: list[IngestionDocumentPreflight],
) -> str:
    if status == "ready":
        return "run_ingestion_job"
    actions = {document.recommended_action for document in documents}
    for action in [
        "restore_source_file_before_ingestion",
        "add_parser_support_before_ingestion",
        "repair_source_content_before_ingestion",
        "add_citation_anchors_before_ingestion",
    ]:
        if action in actions:
            return action
    return "review_ingestion_preflight"


def _operation_notes(
    status: str,
    documents: list[IngestionDocumentPreflight],
) -> list[str]:
    notes = [
        "Ingestion preflight is read-only and does not create jobs or rebuild indexes.",
        "Only markdown parsing is supported in this slice; other formats require separate parser decisions.",
    ]
    if status != "ready":
        notes.append("At least one document must be fixed before ingestion should run.")
    if any(document.chunk_preview for document in documents):
        notes.append("Chunk preview is capped and intended for diagnostics, not full content export.")
    return notes
