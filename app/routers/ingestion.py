from fastapi import APIRouter

from app.config import get_settings
from app.models.contracts import IngestionJobRequest, IngestionJobResponse
from app.services.index_lifecycle import create_ingestion_job

router = APIRouter(prefix="/api/ingestion")


@router.post("/jobs", response_model=IngestionJobResponse)
def create_job(request: IngestionJobRequest) -> IngestionJobResponse:
    ok, job, error = create_ingestion_job(request.source_id, get_settings())
    return IngestionJobResponse(ok=ok, job=job, error=error)
