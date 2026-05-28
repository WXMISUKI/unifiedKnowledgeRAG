from fastapi import APIRouter

from app.config import get_settings
from app.models.contracts import (
    IngestionJobDetailResponse,
    IngestionJobListResponse,
    IngestionJobRequest,
    IngestionJobResponse,
)
from app.services.index_lifecycle import (
    create_ingestion_job,
    get_ingestion_job,
    list_ingestion_jobs,
    retry_ingestion_job,
)

router = APIRouter(prefix="/api/ingestion")


@router.post("/jobs", response_model=IngestionJobResponse)
def create_job(request: IngestionJobRequest) -> IngestionJobResponse:
    ok, job, error = create_ingestion_job(request.source_id, get_settings())
    return IngestionJobResponse(ok=ok, job=job, error=error)


@router.get("/jobs", response_model=IngestionJobListResponse)
def list_jobs(source_id: str | None = None, status: str | None = None) -> IngestionJobListResponse:
    jobs = list_ingestion_jobs(source_id=source_id, status=status, settings=get_settings())
    return IngestionJobListResponse(ok=True, jobs=jobs)


@router.get("/jobs/{job_id}", response_model=IngestionJobDetailResponse)
def get_job(job_id: str) -> IngestionJobDetailResponse:
    ok, job, error = get_ingestion_job(job_id, get_settings())
    return IngestionJobDetailResponse(ok=ok, job=job, error=error)


@router.post("/jobs/{job_id}/retry", response_model=IngestionJobResponse)
def retry_job(job_id: str) -> IngestionJobResponse:
    ok, job, error = retry_ingestion_job(job_id, get_settings())
    return IngestionJobResponse(ok=ok, job=job, error=error)
