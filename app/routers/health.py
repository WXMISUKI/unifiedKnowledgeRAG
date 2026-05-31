from fastapi import APIRouter

from app.models.contracts import HealthResponse, LivenessResponse
from app.services.provider_health import build_health_response, build_liveness_response

router = APIRouter()


@router.get("/live", response_model=LivenessResponse)
def live() -> LivenessResponse:
    return build_liveness_response()


@router.get("/ready", response_model=HealthResponse)
def ready() -> HealthResponse:
    return build_health_response()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return build_health_response()
