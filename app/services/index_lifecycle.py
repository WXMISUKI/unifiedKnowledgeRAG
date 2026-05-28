import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from app.config import Settings, get_settings
from app.models.contracts import IndexLifecycleJob, IndexStatusResponse, ProviderError
from app.services.source_catalog import knowledge_base_exists

_JOBS: dict[str, IndexLifecycleJob] = {}


def create_ingestion_job(source_id: str, settings: Settings | None = None) -> tuple[bool, IndexLifecycleJob | None, ProviderError | None]:
    settings = settings or get_settings()
    if not knowledge_base_exists(source_id):
        return False, None, ProviderError(
            code="UNKNOWN_KNOWLEDGE_BASE",
            message=f"Unknown knowledge base id: {source_id}",
        )

    requested_at = _now()
    job = IndexLifecycleJob(
        job_id=f"idx_{uuid.uuid4().hex}",
        source_id=source_id,
        status="running",
        requested_at=requested_at,
    )
    _JOBS[job.job_id] = job

    try:
        _build_source_index(source_id, settings, job.job_id)
    except Exception as exc:  # pragma: no cover - defensive failure path
        completed_at = _now()
        failed_job = job.model_copy(
            update={
                "status": "failed",
                "completed_at": completed_at,
                "error": ProviderError(code="INDEX_BUILD_FAILED", message=str(exc)),
            }
        )
        _JOBS[job.job_id] = failed_job
        _write_status_marker(
            settings=settings,
            source_id=source_id,
            status="failed",
            reason=str(exc),
            latest_job_id=job.job_id,
            indexed_at=None,
        )
        return True, failed_job, None

    completed_at = _now()
    completed_job = job.model_copy(update={"status": "completed", "completed_at": completed_at})
    _JOBS[job.job_id] = completed_job
    return True, completed_job, None


def get_index_status(source_id: str, settings: Settings | None = None) -> IndexStatusResponse:
    settings = settings or get_settings()
    backend = settings.rag_retrieval_backend.lower()

    if not knowledge_base_exists(source_id):
        return IndexStatusResponse(
            source_id=source_id,
            status="unknown",
            backend=backend,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id: {source_id}",
            ),
        )

    if backend == "fixture":
        return IndexStatusResponse(
            source_id=source_id,
            status="ready",
            backend=backend,
            reason="Fixture backend does not require an explicit persisted index.",
        )

    marker = _marker_path(settings, source_id)
    if not marker.exists():
        return IndexStatusResponse(
            source_id=source_id,
            status="not_indexed",
            backend=backend,
            reason="No explicit source index marker found.",
        )

    payload = json.loads(marker.read_text(encoding="utf-8"))
    return IndexStatusResponse(
        source_id=source_id,
        status=payload["status"],
        backend=backend,
        indexed_at=payload.get("indexed_at"),
        latest_job_id=payload.get("latest_job_id"),
        reason=payload.get("reason"),
    )


def not_ready_sources(source_ids: list[str], settings: Settings | None = None) -> list[str]:
    settings = settings or get_settings()
    return [
        source_id
        for source_id in source_ids
        if get_index_status(source_id, settings).status != "ready"
    ]


def clear_local_jobs_for_tests() -> None:
    _JOBS.clear()


def _build_source_index(source_id: str, settings: Settings, job_id: str) -> None:
    backend = settings.rag_retrieval_backend.lower()
    if backend == "fixture":
        return
    if backend != "llamaindex":
        raise ValueError(f"Unsupported RAG_RETRIEVAL_BACKEND: {settings.rag_retrieval_backend}")

    from app.services.llamaindex_retriever import LlamaIndexLocalRetriever

    LlamaIndexLocalRetriever(settings).build_index([source_id], latest_job_id=job_id)


def _write_status_marker(
    settings: Settings,
    source_id: str,
    status: str,
    reason: str | None,
    latest_job_id: str,
    indexed_at: str | None,
) -> None:
    marker = _marker_path(settings, source_id)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(
        json.dumps(
            {
                "source_id": source_id,
                "status": status,
                "reason": reason,
                "latest_job_id": latest_job_id,
                "indexed_at": indexed_at,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def _marker_path(settings: Settings, source_id: str) -> Path:
    return settings.rag_index_dir / f"{source_id}.index.json"


def _now() -> str:
    return datetime.now(UTC).isoformat()
