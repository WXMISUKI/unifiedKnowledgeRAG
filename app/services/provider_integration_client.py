import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol


DEFAULT_REQUIRED_CAPABILITY_IDS = [
    "knowledge.rag.retrieve",
    "knowledge.rag.answer",
    "knowledge.graph.query",
]


class JsonResponse(Protocol):
    status_code: int

    def json(self) -> dict[str, Any]:
        ...


class ReadOnlyHttpClient(Protocol):
    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | list[tuple[str, Any]] | None = None,
    ) -> JsonResponse:
        ...


@dataclass(frozen=True)
class ProviderCapabilityBinding:
    id: str
    status: str
    reason: str | None
    invocation: dict[str, Any]
    has_example_request: bool


@dataclass(frozen=True)
class ProviderIntegrationProbeReport:
    bindable: bool
    provider_id: str | None
    provider_name: str | None
    contract_version: str | None
    manifest_version: str | None
    requested_contract_version: str
    requested_capability_ids: list[str]
    capability_bindings: list[ProviderCapabilityBinding] = field(default_factory=list)
    checks: list[dict[str, Any]] = field(default_factory=list)
    errors: list[dict[str, Any]] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None

    def to_dict(self) -> dict[str, Any]:
        return provider_integration_probe_report_to_dict(self)


def probe_provider_binding(
    client: ReadOnlyHttpClient,
    *,
    required_contract_version: str = "knowledge-provider-contract-v1",
    required_capability_ids: list[str] | None = None,
) -> ProviderIntegrationProbeReport:
    requested_capability_ids = required_capability_ids or list(
        DEFAULT_REQUIRED_CAPABILITY_IDS
    )
    errors: list[dict[str, Any]] = []

    manifest = _get_json(client, "/api/provider/manifest", errors)
    preflight = _get_json(
        client,
        "/api/provider/preflight",
        errors,
        params=_preflight_params(
            required_contract_version,
            requested_capability_ids,
        ),
    )
    capabilities = _get_json(client, "/api/capabilities", errors)
    capability_bindings = _capability_bindings(
        capabilities.get("capabilities", []),
        requested_capability_ids,
    )
    missing_examples = [
        binding.id
        for binding in capability_bindings
        if not binding.has_example_request
    ]
    missing_capabilities = [
        capability_id
        for capability_id in requested_capability_ids
        if capability_id not in {binding.id for binding in capability_bindings}
    ]

    if missing_examples:
        errors.append(
            {
                "code": "MISSING_INVOCATION_EXAMPLE",
                "message": "Required capability invocation examples are missing.",
                "details": {"capability_ids": missing_examples},
            }
        )
    if missing_capabilities:
        errors.append(
            {
                "code": "MISSING_CAPABILITY",
                "message": "Required capabilities are missing from discovery.",
                "details": {"capability_ids": missing_capabilities},
            }
        )

    bindable = bool(preflight.get("bindable")) and not errors
    return ProviderIntegrationProbeReport(
        bindable=bindable,
        provider_id=manifest.get("provider_id"),
        provider_name=manifest.get("provider_name"),
        contract_version=manifest.get("contract_version"),
        manifest_version=manifest.get("manifest_version"),
        requested_contract_version=required_contract_version,
        requested_capability_ids=requested_capability_ids,
        capability_bindings=capability_bindings,
        checks=preflight.get("checks", []),
        errors=errors,
    )


def provider_integration_probe_report_to_dict(
    report: ProviderIntegrationProbeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_provider_integration_probe_markdown(
    report: ProviderIntegrationProbeReport,
) -> str:
    status = "bindable" if report.bindable else "not-bindable"
    lines = [
        "# Provider Integration Probe Report",
        "",
        f"- Status: `{status}`",
        f"- Provider: `{report.provider_id or 'unknown'}`",
        f"- Provider Name: `{report.provider_name or 'unknown'}`",
        f"- Contract Version: `{report.contract_version or 'unknown'}`",
        f"- Manifest Version: `{report.manifest_version or 'unknown'}`",
        f"- Requested Contract Version: `{report.requested_contract_version}`",
        f"- Requested Capabilities: `{', '.join(report.requested_capability_ids)}`",
        "",
        "## Capability Bindings",
        "",
        "| Capability | Status | Path | Example Request |",
        "|---|---|---|---|",
    ]
    for binding in report.capability_bindings:
        invocation_path = binding.invocation.get("path", "")
        example_status = "present" if binding.has_example_request else "missing"
        lines.append(
            f"| `{binding.id}` | `{binding.status}` | `{invocation_path}` | `{example_status}` |"
        )

    lines.extend(
        [
            "",
            "## Preflight Checks",
            "",
            "| Check | Status | Passed | Reason |",
            "|---|---|---|---|",
        ]
    )
    for check in report.checks:
        lines.append(
            "| "
            f"`{check.get('name', '')}` | "
            f"`{check.get('status', '')}` | "
            f"`{check.get('passed')}` | "
            f"`{check.get('reason') or ''}` |"
        )

    if report.errors:
        lines.extend(["", "## Errors", "", "| Code | Message |", "|---|---|"])
        for error in report.errors:
            lines.append(
                f"| `{error.get('code', '')}` | `{error.get('message', '')}` |"
            )
    lines.append("")
    return "\n".join(lines)


def export_provider_integration_probe_report(
    output_dir: Path = Path("docs/integration/provider-binding"),
    *,
    client: ReadOnlyHttpClient | None = None,
    required_contract_version: str = "knowledge-provider-contract-v1",
    required_capability_ids: list[str] | None = None,
) -> ProviderIntegrationProbeReport:
    if client is None:
        from fastapi.testclient import TestClient

        from app.main import create_app

        client = TestClient(create_app())

    report = probe_provider_binding(
        client,
        required_contract_version=required_contract_version,
        required_capability_ids=required_capability_ids,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "provider-integration-probe.json"
    markdown_path = output_dir / "provider-integration-probe.md"
    exported_report = ProviderIntegrationProbeReport(
        bindable=report.bindable,
        provider_id=report.provider_id,
        provider_name=report.provider_name,
        contract_version=report.contract_version,
        manifest_version=report.manifest_version,
        requested_contract_version=report.requested_contract_version,
        requested_capability_ids=report.requested_capability_ids,
        capability_bindings=report.capability_bindings,
        checks=report.checks,
        errors=report.errors,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            provider_integration_probe_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_provider_integration_probe_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _get_json(
    client: ReadOnlyHttpClient,
    path: str,
    errors: list[dict[str, Any]],
    *,
    params: dict[str, Any] | list[tuple[str, Any]] | None = None,
) -> dict[str, Any]:
    try:
        response = client.get(path, params=params)
    except Exception as error:
        errors.append(
            {
                "code": "HTTP_CLIENT_ERROR",
                "message": f"Failed to request {path}.",
                "details": {"error": f"{error.__class__.__name__}: {error}"},
            }
        )
        return {}

    if response.status_code != 200:
        errors.append(
            {
                "code": "HTTP_STATUS_ERROR",
                "message": f"Unexpected status from {path}.",
                "details": {"status_code": response.status_code},
            }
        )
        return {}

    try:
        payload = response.json()
    except Exception as error:
        errors.append(
            {
                "code": "INVALID_JSON",
                "message": f"Response from {path} is not valid JSON.",
                "details": {"error": f"{error.__class__.__name__}: {error}"},
            }
        )
        return {}

    if not isinstance(payload, dict):
        errors.append(
            {
                "code": "INVALID_JSON_SHAPE",
                "message": f"Response from {path} is not a JSON object.",
                "details": {"payload_type": type(payload).__name__},
            }
        )
        return {}
    return payload


def _preflight_params(
    required_contract_version: str,
    required_capability_ids: list[str],
) -> list[tuple[str, str]]:
    params = [("required_contract_version", required_contract_version)]
    params.extend(
        ("required_capability_ids", capability_id)
        for capability_id in required_capability_ids
    )
    return params


def _capability_bindings(
    discovered_capabilities: list[Any],
    required_capability_ids: list[str],
) -> list[ProviderCapabilityBinding]:
    capabilities_by_id = {
        capability["id"]: capability
        for capability in discovered_capabilities
        if isinstance(capability, dict) and isinstance(capability.get("id"), str)
    }
    bindings: list[ProviderCapabilityBinding] = []
    for capability_id in required_capability_ids:
        capability = capabilities_by_id.get(capability_id)
        if capability is None:
            continue
        invocation = capability.get("invocation") or {}
        bindings.append(
            ProviderCapabilityBinding(
                id=capability_id,
                status=capability.get("status", "unknown"),
                reason=capability.get("reason"),
                invocation=invocation,
                has_example_request=bool(invocation.get("example_request")),
            )
        )
    return bindings
