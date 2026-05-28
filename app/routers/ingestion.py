from typing import Annotated

from fastapi import APIRouter, Query

from app.config import get_settings
from app.models.contracts import (
    IngestionJobDetailResponse,
    IngestionJobListResponse,
    IngestionJobRequest,
    IngestionJobResponse,
    IngestionJobCancelRequest,
    IngestionJobRetentionRequest,
    IngestionJobRetentionResponse,
    IngestionJobRecoveryRequest,
    IngestionJobRecoveryResponse,
)
from app.services.index_lifecycle import (
    cancel_ingestion_job,
    compact_ingestion_jobs,
    create_ingestion_job,
    get_ingestion_job,
    list_ingestion_jobs,
    recover_stale_running_jobs,
    retry_ingestion_job,
)

router = APIRouter(prefix="/api/ingestion")


@router.post("/jobs", response_model=IngestionJobResponse)
def create_job(request: IngestionJobRequest) -> IngestionJobResponse:
    ok, job, error = create_ingestion_job(request.source_id, get_settings())
    return IngestionJobResponse(ok=ok, job=job, error=error)


@router.get("/jobs", response_model=IngestionJobListResponse)
def list_jobs(
    source_id: str | None = None,
    status: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> IngestionJobListResponse:
    jobs, total, has_more = list_ingestion_jobs(
        source_id=source_id,
        status=status,
        limit=limit,
        offset=offset,
        settings=get_settings(),
    )
    return IngestionJobListResponse(
        ok=True,
        jobs=jobs,
        total=total,
        limit=limit,
        offset=offset,
        has_more=has_more,
    )


@router.post("/jobs/retention/compact", response_model=IngestionJobRetentionResponse)
def compact_jobs(request: IngestionJobRetentionRequest) -> IngestionJobRetentionResponse:
    result = compact_ingestion_jobs(request.keep_latest, get_settings())
    return IngestionJobRetentionResponse(ok=True, result=result)


@router.post("/jobs/recovery/stale-running", response_model=IngestionJobRecoveryResponse)
def recover_stale_running(request: IngestionJobRecoveryRequest) -> IngestionJobRecoveryResponse:
    result = recover_stale_running_jobs(request.max_age_seconds, get_settings())
    return IngestionJobRecoveryResponse(ok=True, result=result)


@router.get("/jobs/{job_id}", response_model=IngestionJobDetailResponse)
def get_job(job_id: str) -> IngestionJobDetailResponse:
    ok, job, error = get_ingestion_job(job_id, get_settings())
    return IngestionJobDetailResponse(ok=ok, job=job, error=error)


@router.post("/jobs/{job_id}/retry", response_model=IngestionJobResponse)
def retry_job(job_id: str) -> IngestionJobResponse:
    ok, job, error = retry_ingestion_job(job_id, get_settings())
    return IngestionJobResponse(ok=ok, job=job, error=error)


@router.post("/jobs/{job_id}/cancel", response_model=IngestionJobResponse)
def cancel_job(job_id: str, request: IngestionJobCancelRequest) -> IngestionJobResponse:
    ok, job, error = cancel_ingestion_job(job_id, request.reason, get_settings())
    return IngestionJobResponse(ok=ok, job=job, error=error)
