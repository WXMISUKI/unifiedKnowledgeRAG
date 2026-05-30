from app.config import Settings, get_settings
from app.models.contracts import ProviderPreflightCheck, ProviderPreflightResponse
from app.services.provider_capabilities import build_capabilities_response
from app.services.provider_health import build_health_response
from app.services.provider_manifest import build_provider_integration_manifest


REQUIRED_CAPABILITY_IDS = [
    "knowledge.rag.source_documents",
    "knowledge.rag.retrieve",
    "knowledge.rag.answer",
    "knowledge.graph.query",
]


def build_provider_preflight_response(
    settings: Settings | None = None,
    required_contract_version: str | None = None,
    required_capability_ids: list[str] | None = None,
) -> ProviderPreflightResponse:
    settings = settings or get_settings()
    manifest = build_provider_integration_manifest()
    health = build_health_response(settings)
    capabilities = build_capabilities_response(settings)
    capabilities_by_id = {capability.id: capability for capability in capabilities.capabilities}
    requested_contract_version = required_contract_version or manifest.contract_version
    requested_capability_ids = required_capability_ids or REQUIRED_CAPABILITY_IDS

    checks = [
        _manifest_check(manifest),
        _contract_version_check(manifest, requested_contract_version),
        _health_check(health),
        _required_capabilities_check(capabilities_by_id, requested_capability_ids),
        _schema_refs_check(capabilities_by_id, requested_capability_ids),
        _planned_graph_boundary_check(capabilities_by_id),
    ]
    bindable = all(check.passed for check in checks)
    return ProviderPreflightResponse(
        provider_id=manifest.provider_id,
        contract_version=manifest.contract_version,
        manifest_version=manifest.manifest_version,
        requested_contract_version=requested_contract_version,
        requested_capability_ids=requested_capability_ids,
        bindable=bindable,
        control_plane_hint="MyPrivateAgent",
        checks=checks,
    )


def _manifest_check(manifest) -> ProviderPreflightCheck:
    passed = (
        manifest.provider_id == "unifiedKnowledgeProvider"
        and manifest.component_role == "knowledge_data_plane"
        and "MyPrivateAgent" in manifest.compatible_control_planes
    )
    return ProviderPreflightCheck(
        name="manifest_identity",
        passed=passed,
        status="ready" if passed else "failed",
        details={
            "provider_id": manifest.provider_id,
            "component_role": manifest.component_role,
            "compatible_control_planes": manifest.compatible_control_planes,
            "contract_version": manifest.contract_version,
        },
        reason=None if passed else "Provider manifest identity is incompatible.",
    )


def _contract_version_check(
    manifest,
    required_contract_version: str,
) -> ProviderPreflightCheck:
    passed = manifest.contract_version == required_contract_version
    return ProviderPreflightCheck(
        name="contract_version",
        passed=passed,
        status="ready" if passed else "failed",
        details={
            "required_contract_version": required_contract_version,
            "provider_contract_version": manifest.contract_version,
        },
        reason=None if passed else "Provider contract version is incompatible.",
    )


def _health_check(health) -> ProviderPreflightCheck:
    passed = health.status == "ok"
    return ProviderPreflightCheck(
        name="health_readiness",
        passed=passed,
        status=health.status,
        details={
            "service": health.service,
            "rag_status": health.rag.status,
            "rag_backend": health.rag.backend,
            "rag_backend_status": health.rag.backend_status,
            "rag_index_status": health.rag.index_status,
            "answer_status": health.answer.status,
            "answer_backend": health.answer.backend,
            "graph_status": health.graph.status,
        },
        reason=None if passed else "Provider health is degraded.",
    )


def _required_capabilities_check(
    capabilities_by_id,
    required_capability_ids: list[str],
) -> ProviderPreflightCheck:
    missing = [
        capability_id
        for capability_id in required_capability_ids
        if capability_id not in capabilities_by_id
    ]
    passed = not missing
    return ProviderPreflightCheck(
        name="required_capabilities",
        passed=passed,
        status="ready" if passed else "failed",
        details={
            "required_capability_ids": required_capability_ids,
            "available_capability_ids": sorted(capabilities_by_id),
            "missing_capability_ids": missing,
        },
        reason=None if passed else "Required provider capabilities are missing.",
    )


def _schema_refs_check(
    capabilities_by_id,
    required_capability_ids: list[str],
) -> ProviderPreflightCheck:
    missing_schema_refs = []
    for capability_id in required_capability_ids:
        capability = capabilities_by_id.get(capability_id)
        if capability is None:
            continue
        invocation = capability.invocation if capability else None
        if invocation is None or not invocation.response_schema_ref:
            missing_schema_refs.append(capability_id)
            continue
        method = invocation.method.upper()
        has_request_contract = bool(invocation.request_schema_ref)
        has_get_example = method == "GET" and bool(invocation.example_request)
        if method != "GET" and not has_request_contract:
            missing_schema_refs.append(capability_id)
            continue
        if method == "GET" and not has_get_example:
            missing_schema_refs.append(capability_id)
    passed = not missing_schema_refs
    return ProviderPreflightCheck(
        name="schema_references",
        passed=passed,
        status="ready" if passed else "failed",
        details={
            "openapi_path": "/openapi.json",
            "checked_capability_ids": [
                capability_id
                for capability_id in required_capability_ids
                if capability_id in capabilities_by_id
            ],
            "missing_schema_ref_capability_ids": missing_schema_refs,
        },
        reason=None if passed else "Capability schema references are incomplete.",
    )


def _planned_graph_boundary_check(capabilities_by_id) -> ProviderPreflightCheck:
    graph_capability = capabilities_by_id.get("knowledge.graph.query")
    graph_status = graph_capability.status if graph_capability else "missing"
    passed = graph_status in {"planned", "ready"}
    return ProviderPreflightCheck(
        name="graph_boundary",
        passed=passed,
        status=graph_status,
        details={
            "capability_id": "knowledge.graph.query",
            "capability_status": graph_status,
            "execution_status": "planned",
            "reason": graph_capability.reason if graph_capability else None,
        },
        reason=None if passed else "Graph query contract boundary is missing.",
    )
