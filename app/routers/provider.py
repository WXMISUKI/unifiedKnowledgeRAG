from fastapi import APIRouter, Query

from app.models.contracts import (
    ProviderHandoffBundleResponse,
    ProviderIntegrationManifest,
    ProviderPreflightResponse,
)
from app.services.provider_handoff_bundle import (
    build_provider_handoff_bundle_report,
    provider_handoff_bundle_report_to_dict,
)
from app.services.provider_manifest import build_provider_integration_manifest
from app.services.provider_preflight import build_provider_preflight_response

router = APIRouter(prefix="/api/provider")


@router.get("/manifest", response_model=ProviderIntegrationManifest)
def manifest() -> ProviderIntegrationManifest:
    return build_provider_integration_manifest()


@router.get("/handoff", response_model=ProviderHandoffBundleResponse)
def handoff() -> dict:
    report = build_provider_handoff_bundle_report()
    return provider_handoff_bundle_report_to_dict(report)


@router.get("/preflight", response_model=ProviderPreflightResponse)
def preflight(
    required_contract_version: str | None = None,
    required_capability_ids: list[str] | None = Query(default=None),
) -> ProviderPreflightResponse:
    return build_provider_preflight_response(
        required_contract_version=required_contract_version,
        required_capability_ids=required_capability_ids,
    )
