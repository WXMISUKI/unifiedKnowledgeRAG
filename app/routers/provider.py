from fastapi import APIRouter

from app.models.contracts import ProviderIntegrationManifest
from app.services.provider_manifest import build_provider_integration_manifest

router = APIRouter(prefix="/api/provider")


@router.get("/manifest", response_model=ProviderIntegrationManifest)
def manifest() -> ProviderIntegrationManifest:
    return build_provider_integration_manifest()
