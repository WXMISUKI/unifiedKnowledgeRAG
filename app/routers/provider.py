from fastapi import APIRouter, Query

from app.models.contracts import ProviderIntegrationManifest, ProviderPreflightResponse
from app.services.provider_manifest import build_provider_integration_manifest
from app.services.provider_preflight import build_provider_preflight_response

router = APIRouter(prefix="/api/provider")


@router.get("/manifest", response_model=ProviderIntegrationManifest)
def manifest() -> ProviderIntegrationManifest:
    return build_provider_integration_manifest()


@router.get("/preflight", response_model=ProviderPreflightResponse)
def preflight(
    required_contract_version: str | None = None,
    required_capability_ids: list[str] | None = Query(default=None),
) -> ProviderPreflightResponse:
    return build_provider_preflight_response(
        required_contract_version=required_contract_version,
        required_capability_ids=required_capability_ids,
    )
