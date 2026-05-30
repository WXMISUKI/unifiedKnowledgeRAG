from fastapi import APIRouter

from app.models.contracts import CapabilitiesResponse
from app.services.provider_capabilities import build_capabilities_response

router = APIRouter(prefix="/api")


@router.get("/capabilities", response_model=CapabilitiesResponse)
def capabilities() -> CapabilitiesResponse:
    return build_capabilities_response()
