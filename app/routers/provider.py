from fastapi import APIRouter

from app.models.contracts import ProviderIntegrationManifest, ProviderPreflightResponse
from app.services.provider_manifest import build_provider_integration_manifest
from app.services.provider_preflight import build_provider_preflight_response

router = APIRouter(prefix="/api/provider")


@router.get("/manifest", response_model=ProviderIntegrationManifest)
def manifest() -> ProviderIntegrationManifest:
    return build_provider_integration_manifest()


@router.get("/preflight", response_model=ProviderPreflightResponse)
def preflight() -> ProviderPreflightResponse:
    return build_provider_preflight_response()
