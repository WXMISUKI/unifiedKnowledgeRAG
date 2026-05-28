import uuid
from datetime import UTC, datetime

from app.config import Settings, get_settings
from app.models.contracts import (
    IndexLifecycleJob,
    IndexStatusResponse,
    ProviderError,
    IngestionJobRetentionResult,
    IngestionJobRecoveryResult,
)
from app.services.index_lifecycle_store import IndexLifecycleStore
from app.services.source_catalog import knowledge_base_exists


def create_ingestion_job(source_id: str, settings: Settings | None = None) -> tuple[bool, IndexLifecycleJob | None, ProviderError | None]:
    settings = settings or get_settings()
    store = IndexLifecycleStore(settings)
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
    store.append_job(job)

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
        store.append_job(failed_job)
        store.write_source_status(IndexStatusResponse(
            source_id=source_id,
            status="failed",
            backend=settings.rag_retrieval_backend.lower(),
            indexed_at=None,
            latest_job_id=job.job_id,
            reason=str(exc),
        ))
        return True, failed_job, None

    completed_at = _now()
    completed_job = job.model_copy(update={"status": "completed", "completed_at": completed_at})
    store.append_job(completed_job)
    return True, completed_job, None


def list_ingestion_jobs(
    source_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
    settings: Settings | None = None,
) -> tuple[list[IndexLifecycleJob], int, bool]:
    settings = settings or get_settings()
    store = IndexLifecycleStore(settings)
    total = store.count_jobs(source_id=source_id, status=status)
    jobs = store.list_jobs(
        source_id=source_id,
        status=status,
        limit=limit,
        offset=offset,
    )
    return jobs, total, offset + len(jobs) < total


def compact_ingestion_jobs(
    keep_latest: int,
    settings: Settings | None = None,
) -> IngestionJobRetentionResult:
    settings = settings or get_settings()
    before_count, after_count, removed_count = IndexLifecycleStore(settings).compact_jobs(keep_latest)
    return IngestionJobRetentionResult(
        before_count=before_count,
        after_count=after_count,
        removed_count=removed_count,
        keep_latest=keep_latest,
    )


def get_ingestion_job(
    job_id: str,
    settings: Settings | None = None,
) -> tuple[bool, IndexLifecycleJob | None, ProviderError | None]:
    settings = settings or get_settings()
    job = IndexLifecycleStore(settings).get_job(job_id)
    if job is None:
        return False, None, ProviderError(
            code="JOB_NOT_FOUND",
            message=f"Unknown ingestion job id: {job_id}",
        )
    return True, job, None


def retry_ingestion_job(
    job_id: str,
    settings: Settings | None = None,
) -> tuple[bool, IndexLifecycleJob | None, ProviderError | None]:
    settings = settings or get_settings()
    ok, job, error = get_ingestion_job(job_id, settings)
    if not ok or job is None:
        return False, None, error
    if job.status != "failed":
        return False, None, ProviderError(
            code="JOB_RETRY_NOT_ALLOWED",
            message=f"Only failed ingestion jobs can be retried: {job_id}",
        )
    return create_ingestion_job(job.source_id, settings)


def cancel_ingestion_job(
    job_id: str,
    reason: str,
    settings: Settings | None = None,
) -> tuple[bool, IndexLifecycleJob | None, ProviderError | None]:
    settings = settings or get_settings()
    store = IndexLifecycleStore(settings)
    job = store.get_job(job_id)
    if job is None:
        return False, None, ProviderError(
            code="JOB_NOT_FOUND",
            message=f"Unknown ingestion job id: {job_id}",
        )
    if job.status != "running":
        return False, None, ProviderError(
            code="JOB_CANCEL_NOT_ALLOWED",
            message=f"Only running ingestion jobs can be canceled: {job_id}",
        )

    canceled_job = job.model_copy(
        update={
            "status": "canceled",
            "completed_at": _now(),
            "error": ProviderError(code="JOB_CANCELED", message=reason),
        }
    )
    store.append_job(canceled_job)
    _write_terminal_source_status_if_latest_source_job(
        store=store,
        settings=settings,
        job=canceled_job,
        status="canceled",
        reason=reason,
    )
    return True, canceled_job, None


def recover_stale_running_jobs(
    max_age_seconds: int,
    settings: Settings | None = None,
) -> IngestionJobRecoveryResult:
    settings = settings or get_settings()
    store = IndexLifecycleStore(settings)
    recovered_ids: list[str] = []
    for job in store.stale_running_jobs(max_age_seconds):
        reason = f"Running ingestion job exceeded max_age_seconds={max_age_seconds}."
        failed_job = job.model_copy(
            update={
                "status": "failed",
                "completed_at": _now(),
                "error": ProviderError(code="STALE_RUNNING_JOB", message=reason),
            }
        )
        store.append_job(failed_job)
        _write_terminal_source_status_if_latest_source_job(
            store=store,
            settings=settings,
            job=failed_job,
            status="failed",
            reason=reason,
        )
        recovered_ids.append(job.job_id)
    return IngestionJobRecoveryResult(
        recovered_count=len(recovered_ids),
        recovered_job_ids=recovered_ids,
        max_age_seconds=max_age_seconds,
    )


def get_index_status(source_id: str, settings: Settings | None = None) -> IndexStatusResponse:
    settings = settings or get_settings()
    backend = settings.rag_retrieval_backend.lower()
    store = IndexLifecycleStore(settings)

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

    status = store.read_source_status(source_id)
    if status is None:
        return IndexStatusResponse(
            source_id=source_id,
            status="not_indexed",
            backend=backend,
            reason="No explicit source index marker found.",
        )

    return status


def not_ready_sources(source_ids: list[str], settings: Settings | None = None) -> list[str]:
    settings = settings or get_settings()
    return [
        source_id
        for source_id in source_ids
        if get_index_status(source_id, settings).status != "ready"
    ]


def clear_local_jobs_for_tests(settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    IndexLifecycleStore(settings).clear_for_tests()


def _build_source_index(source_id: str, settings: Settings, job_id: str) -> None:
    backend = settings.rag_retrieval_backend.lower()
    if backend == "fixture":
        return
    if backend != "llamaindex":
        raise ValueError(f"Unsupported RAG_RETRIEVAL_BACKEND: {settings.rag_retrieval_backend}")

    from app.services.llamaindex_retriever import LlamaIndexLocalRetriever

    LlamaIndexLocalRetriever(settings).build_index([source_id], latest_job_id=job_id)


def _write_terminal_source_status_if_latest_source_job(
    store: IndexLifecycleStore,
    settings: Settings,
    job: IndexLifecycleJob,
    status: str,
    reason: str,
) -> None:
    latest_source_job = store.latest_job_for_source(job.source_id)
    if latest_source_job is None or latest_source_job.job_id != job.job_id:
        return
    store.write_source_status(IndexStatusResponse(
        source_id=job.source_id,
        status=status,
        backend=settings.rag_retrieval_backend.lower(),
        indexed_at=None,
        latest_job_id=job.job_id,
        reason=reason,
    ))


def _now() -> str:
    return datetime.now(UTC).isoformat()
