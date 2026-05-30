from fastapi import APIRouter

from app.models.contracts import HealthResponse
from app.services.provider_health import build_health_response

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return build_health_response()
