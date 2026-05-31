import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx


DEPLOYED_PROVIDER_SMOKE_REPORT_ID = "deployed-provider-smoke-v1"
EXPECTED_PROVIDER_ID = "unifiedKnowledgeProvider"
EXPECTED_CONTRACT_VERSION = "knowledge-provider-contract-v1"
EXPECTED_MANIFEST_VERSION = "provider-integration-manifest-v1"
EXPECTED_COMPONENT_ROLE = "knowledge_data_plane"


@dataclass(frozen=True)
class DeployedProviderSmokeCheck:
    name: str
    endpoint: str
    status: str
    passed: bool
    http_status_code: int | None = None
    details: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(frozen=True)
class DeployedProviderSmokeReport:
    id: str
    generated_at: str
    base_url: str
    status: str
    provider: dict[str, Any]
    handoff: dict[str, Any]
    checks: list[DeployedProviderSmokeCheck]
    operation_notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def run_deployed_provider_smoke(
    base_url: str,
    *,
    provider_api_key: str | None = None,
    timeout_seconds: float = 5.0,
    client: httpx.Client | None = None,
) -> DeployedProviderSmokeReport:
    normalized_base_url = _normalize_base_url(base_url)
    if client is not None:
        return _run_smoke_with_client(
            client,
            base_url=normalized_base_url,
            provider_api_key=provider_api_key,
        )

    with httpx.Client(
        base_url=normalized_base_url,
        timeout=timeout_seconds,
        follow_redirects=True,
    ) as http_client:
        return _run_smoke_with_client(
            http_client,
            base_url=normalized_base_url,
            provider_api_key=provider_api_key,
        )


def deployed_provider_smoke_report_to_dict(
    report: DeployedProviderSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_deployed_provider_smoke_markdown(
    report: DeployedProviderSmokeReport,
) -> str:
    lines = [
        "# Deployed Provider Smoke Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Base URL: `{report.base_url}`",
        f"- Provider: `{report.provider.get('provider_id', 'unknown')}`",
        f"- Contract: `{report.provider.get('contract_version', 'unknown')}`",
        f"- Handoff Status: `{report.handoff.get('status', 'unknown')}`",
        "",
        "## Checks",
        "",
        "| Check | Endpoint | Status | HTTP | Details |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        details = _compact_check_details(check)
        lines.append(
            f"| `{check.name}` | `{check.endpoint}` | `{check.status}` | "
            f"`{check.http_status_code or 'n/a'}` | {details} |"
        )
    lines.extend(["", "## Operation Notes", ""])
    lines.extend(f"- {note}" for note in report.operation_notes)
    lines.append("")
    return "\n".join(lines)


def export_deployed_provider_smoke_report(
    output_dir: Path = Path("docs/integration/deployed-provider-smoke"),
    *,
    base_url: str = "http://127.0.0.1:8020",
    provider_api_key: str | None = None,
    timeout_seconds: float = 5.0,
    client: httpx.Client | None = None,
) -> DeployedProviderSmokeReport:
    report = run_deployed_provider_smoke(
        base_url,
        provider_api_key=provider_api_key,
        timeout_seconds=timeout_seconds,
        client=client,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "deployed-provider-smoke.json"
    markdown_path = output_dir / "deployed-provider-smoke.md"
    exported_report = DeployedProviderSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        base_url=report.base_url,
        status=report.status,
        provider=report.provider,
        handoff=report.handoff,
        checks=report.checks,
        operation_notes=report.operation_notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            deployed_provider_smoke_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_deployed_provider_smoke_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _run_smoke_with_client(
    client: httpx.Client,
    *,
    base_url: str,
    provider_api_key: str | None,
) -> DeployedProviderSmokeReport:
    auth_headers = _auth_headers(provider_api_key)
    health_check, health = _get_json(client, "/health")
    manifest_check, manifest = _get_json(
        client,
        "/api/provider/manifest",
        headers=auth_headers,
    )
    preflight_check, preflight = _get_json(
        client,
        "/api/provider/preflight",
        headers=auth_headers,
    )
    source_bindings_check, source_bindings = _get_json(
        client,
        "/api/provider/source-bindings",
        headers=auth_headers,
    )
    handoff_check, handoff = _get_json(
        client,
        "/api/provider/handoff",
        headers=auth_headers,
    )

    checks = [
        _validate_health(health_check, health),
        _validate_manifest(manifest_check, manifest),
        _validate_preflight(preflight_check, preflight),
        _validate_source_bindings(source_bindings_check, source_bindings),
        _validate_handoff(handoff_check, handoff),
    ]
    return DeployedProviderSmokeReport(
        id=DEPLOYED_PROVIDER_SMOKE_REPORT_ID,
        generated_at=datetime.now(UTC).isoformat(),
        base_url=base_url,
        status=_overall_status(checks),
        provider=_provider_summary(manifest),
        handoff=_handoff_summary(handoff),
        checks=checks,
        operation_notes=_operation_notes(provider_api_key=provider_api_key),
    )


def _get_json(
    client: httpx.Client,
    path: str,
    *,
    headers: dict[str, str] | None = None,
) -> tuple[DeployedProviderSmokeCheck, dict[str, Any]]:
    endpoint = f"GET {path}"
    try:
        response = client.get(path, headers=headers)
    except httpx.HTTPError as error:
        return (
            DeployedProviderSmokeCheck(
                name=_check_name(path),
                endpoint=endpoint,
                status="blocked",
                passed=False,
                error=f"{error.__class__.__name__}: {error}",
            ),
            {},
        )

    if response.status_code != 200:
        return (
            DeployedProviderSmokeCheck(
                name=_check_name(path),
                endpoint=endpoint,
                status="blocked",
                passed=False,
                http_status_code=response.status_code,
                error=f"Unexpected HTTP status {response.status_code}.",
            ),
            {},
        )

    try:
        payload = response.json()
    except ValueError as error:
        return (
            DeployedProviderSmokeCheck(
                name=_check_name(path),
                endpoint=endpoint,
                status="blocked",
                passed=False,
                http_status_code=response.status_code,
                error=f"{error.__class__.__name__}: {error}",
            ),
            {},
        )

    if not isinstance(payload, dict):
        return (
            DeployedProviderSmokeCheck(
                name=_check_name(path),
                endpoint=endpoint,
                status="blocked",
                passed=False,
                http_status_code=response.status_code,
                error=f"Expected JSON object, got {type(payload).__name__}.",
            ),
            {},
        )

    return (
        DeployedProviderSmokeCheck(
            name=_check_name(path),
            endpoint=endpoint,
            status="ready",
            passed=True,
            http_status_code=response.status_code,
        ),
        payload,
    )


def _validate_health(
    check: DeployedProviderSmokeCheck,
    payload: dict[str, Any],
) -> DeployedProviderSmokeCheck:
    if not check.passed:
        return check
    provider_status = payload.get("status")
    service = payload.get("service")
    passed = service == EXPECTED_PROVIDER_ID and provider_status in {"ok", "degraded"}
    status = "ready" if provider_status == "ok" else "review"
    if not passed:
        status = "blocked"
    return _replace_check(
        check,
        status=status,
        passed=passed,
        details={
            "service": service,
            "provider_status": provider_status,
            "rag_status": (payload.get("rag") or {}).get("status"),
            "answer_status": (payload.get("answer") or {}).get("status"),
            "graph_status": (payload.get("graph") or {}).get("status"),
        },
        error=None if passed else "Health response does not match expected provider.",
    )


def _validate_manifest(
    check: DeployedProviderSmokeCheck,
    payload: dict[str, Any],
) -> DeployedProviderSmokeCheck:
    if not check.passed:
        return check
    passed = (
        payload.get("provider_id") == EXPECTED_PROVIDER_ID
        and payload.get("contract_version") == EXPECTED_CONTRACT_VERSION
        and payload.get("manifest_version") == EXPECTED_MANIFEST_VERSION
        and payload.get("component_role") == EXPECTED_COMPONENT_ROLE
    )
    return _replace_check(
        check,
        status="ready" if passed else "blocked",
        passed=passed,
        details=_provider_summary(payload),
        error=None if passed else "Manifest identity or contract is incompatible.",
    )


def _validate_preflight(
    check: DeployedProviderSmokeCheck,
    payload: dict[str, Any],
) -> DeployedProviderSmokeCheck:
    if not check.passed:
        return check
    checks = payload.get("checks", [])
    bindable = payload.get("bindable") is True
    return _replace_check(
        check,
        status="ready" if bindable else "blocked",
        passed=bindable,
        details={
            "bindable": bindable,
            "contract_version": payload.get("contract_version"),
            "check_count": len(checks) if isinstance(checks, list) else 0,
        },
        error=None if bindable else "Provider preflight is not bindable.",
    )


def _validate_handoff(
    check: DeployedProviderSmokeCheck,
    payload: dict[str, Any],
) -> DeployedProviderSmokeCheck:
    if not check.passed:
        return check
    handoff_status = payload.get("status")
    passed = handoff_status in {"ready", "review"}
    status = handoff_status if handoff_status in {"ready", "review"} else "blocked"
    return _replace_check(
        check,
        status=status,
        passed=passed,
        details=_handoff_summary(payload),
        error=None if passed else "Provider handoff evidence is blocked or invalid.",
    )


def _validate_source_bindings(
    check: DeployedProviderSmokeCheck,
    payload: dict[str, Any],
) -> DeployedProviderSmokeCheck:
    if not check.passed:
        return check
    source_binding_status = payload.get("status")
    passed = source_binding_status in {"ready", "review"}
    status = (
        source_binding_status
        if source_binding_status in {"ready", "review"}
        else "blocked"
    )
    return _replace_check(
        check,
        status=status,
        passed=passed,
        details=_source_bindings_summary(payload),
        error=(
            None
            if passed
            else "Provider source binding evidence is blocked or invalid."
        ),
    )


def _replace_check(
    check: DeployedProviderSmokeCheck,
    *,
    status: str,
    passed: bool,
    details: dict[str, Any],
    error: str | None,
) -> DeployedProviderSmokeCheck:
    return DeployedProviderSmokeCheck(
        name=check.name,
        endpoint=check.endpoint,
        status=status,
        passed=passed,
        http_status_code=check.http_status_code,
        details=details,
        error=error,
    )


def _overall_status(checks: list[DeployedProviderSmokeCheck]) -> str:
    statuses = {check.status for check in checks}
    if any(not check.passed for check in checks) or "blocked" in statuses:
        return "blocked"
    if statuses - {"ready"}:
        return "review"
    return "ready"


def _provider_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "provider_id": payload.get("provider_id"),
        "provider_name": payload.get("provider_name"),
        "provider_version": payload.get("provider_version"),
        "contract_version": payload.get("contract_version"),
        "manifest_version": payload.get("manifest_version"),
        "component_role": payload.get("component_role"),
    }


def _handoff_summary(payload: dict[str, Any]) -> dict[str, Any]:
    artifacts = payload.get("evidence_artifacts", [])
    return {
        "id": payload.get("id"),
        "status": payload.get("status"),
        "artifact_count": len(artifacts) if isinstance(artifacts, list) else 0,
    }


def _source_bindings_summary(payload: dict[str, Any]) -> dict[str, Any]:
    sources = payload.get("sources", [])
    source_count = len(sources) if isinstance(sources, list) else 0
    bindable_count = sum(
        1
        for source in sources
        if isinstance(source, dict) and source.get("bindable") is True
    )
    return {
        "id": payload.get("id"),
        "status": payload.get("status"),
        "source_count": source_count,
        "bindable_source_count": bindable_count,
    }


def _operation_notes(*, provider_api_key: str | None) -> list[str]:
    notes = [
        "This probe validates an already-running provider over HTTP.",
        "It only calls health, manifest, preflight, source binding, and handoff discovery endpoints.",
        "External deployment owners still manage TLS, reverse proxy policy, managed secrets, registration, heartbeat governance, audit policy, and source-to-agent binding.",
    ]
    if provider_api_key:
        notes.append(
            "Provider API credentials were supplied to protected /api discovery endpoints and were not written to this report."
        )
    else:
        notes.append(
            "No provider API credentials were supplied; this is only expected for local or intentionally open deployments."
        )
    return notes


def _auth_headers(provider_api_key: str | None) -> dict[str, str]:
    if not provider_api_key:
        return {}
    return {
        "Authorization": f"Bearer {provider_api_key}",
        "X-Provider-Api-Key": provider_api_key,
    }


def _normalize_base_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if not normalized:
        raise ValueError("base_url must not be empty")
    return normalized


def _check_name(path: str) -> str:
    return {
        "/health": "health_readiness",
        "/api/provider/manifest": "provider_manifest",
        "/api/provider/preflight": "provider_preflight",
        "/api/provider/source-bindings": "provider_source_bindings",
        "/api/provider/handoff": "provider_handoff",
    }.get(path, path.strip("/").replace("/", "_") or "root")


def _compact_check_details(check: DeployedProviderSmokeCheck) -> str:
    if check.error:
        return f"`{check.error}`"
    compact = {
        key: value
        for key, value in check.details.items()
        if value is not None
    }
    return f"`{json.dumps(compact, ensure_ascii=False, sort_keys=True)}`"
