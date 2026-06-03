import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE12_LOCAL_RAG_INTEGRATION_HARDENING_SMOKE_ID = (
    "phase12-local-rag-integration-hardening-smoke-v1"
)
PHASE12_PROFILE_PATH = Path(
    "docs/integration/myprivateagent-local-rag-integration-hardening/"
    "phase12-local-rag-integration-hardening-profile.json"
)
PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
PROVIDER_HANDOFF_BUNDLE_PATH = Path("docs/integration/provider-handoff/provider-handoff-bundle.json")
PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH = Path(
    "docs/smoke/myprivateagent-local-provider-integration/"
    "phase11-source-binding-preview-smoke.json"
)
PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH = Path(
    "docs/smoke/myprivateagent-local-provider-integration/"
    "phase11-rag-retrieve-consumption-smoke.json"
)
SMOKE_JSON_FILENAME = "phase12-local-rag-integration-hardening-smoke.json"
SMOKE_MARKDOWN_FILENAME = "phase12-local-rag-integration-hardening-smoke.md"


@dataclass(frozen=True)
class Phase12LocalRagIntegrationSmokeCheck:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase12LocalRagIntegrationHardeningSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase12LocalRagIntegrationSmokeCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase12_local_rag_integration_hardening_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase12LocalRagIntegrationHardeningSmokeReport:
    profile_payload = _read_json_if_present(base_dir / PHASE12_PROFILE_PATH)
    contract_smoke_payload = _read_json_if_present(
        base_dir / PROVIDER_CONTRACT_SMOKE_PATH
    )
    handoff_payload = _read_json_if_present(base_dir / PROVIDER_HANDOFF_BUNDLE_PATH)
    source_binding_payload = _read_json_if_present(
        base_dir / PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH
    )
    rag_retrieve_payload = _read_json_if_present(
        base_dir / PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH
    )
    checks = [
        _profile_present_check(profile_payload),
        _manifest_smoke_check(contract_smoke_payload),
        _contract_smoke_check(contract_smoke_payload),
        _handoff_consistency_check(handoff_payload),
        _source_binding_preview_readiness_check(source_binding_payload),
        _rag_retrieve_consumption_readiness_check(rag_retrieve_payload),
    ]
    status = "ready" if all(check.status == "ready" for check in checks) else "blocked"
    return Phase12LocalRagIntegrationHardeningSmokeReport(
        id=PHASE12_LOCAL_RAG_INTEGRATION_HARDENING_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="confirm_local_rag_integration_hardening",
        summary={
            "total_checks": len(checks),
            "passed_checks": sum(1 for check in checks if check.status == "ready"),
            "failed_checks": sum(1 for check in checks if check.status != "ready"),
            "handoff_artifact_count": len(
                _get_evidence_artifacts(handoff_payload) if handoff_payload is not None else []
            ),
        },
        checks=checks,
        notes=[
            "Smoke is read-only and for local MyPrivateAgent integration hardening review.",
            "No runtime execution changes and no source-to-agent binding mutation are performed.",
        ],
    )


def phase12_local_rag_integration_hardening_smoke_report_to_dict(
    report: Phase12LocalRagIntegrationHardeningSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase12_local_rag_integration_hardening_smoke_markdown(
    report: Phase12LocalRagIntegrationHardeningSmokeReport,
) -> str:
    lines = [
        "# Phase 12 Local RAG Integration Hardening Smoke",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        lines.append(f"| {key} | `{rendered}` |")
    lines.extend(
        [
            "",
            "## Checks",
            "",
            "| Check | Required | Status | Summary | Recommended Action |",
            "|---|---|---|---|---|",
        ]
    )
    for check in report.checks:
        lines.append(
            f"| `{check.id}` | `{check.required}` | `{check.status}` | "
            f"{check.summary} | `{check.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase12_local_rag_integration_hardening_smoke_report(
    output_dir: Path = Path("docs/smoke/myprivateagent-local-rag-integration-hardening"),
    *,
    base_dir: Path = Path("."),
) -> Phase12LocalRagIntegrationHardeningSmokeReport:
    report = build_phase12_local_rag_integration_hardening_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / SMOKE_JSON_FILENAME
    markdown_path = output_dir / SMOKE_MARKDOWN_FILENAME
    exported = Phase12LocalRagIntegrationHardeningSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        checks=report.checks,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase12_local_rag_integration_hardening_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase12_local_rag_integration_hardening_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _profile_present_check(
    payload: dict[str, Any] | None,
) -> Phase12LocalRagIntegrationSmokeCheck:
    return _bool_check(
        id="phase12_local_rag_integration_hardening_profile_present",
        path=PHASE12_PROFILE_PATH,
        passed=payload is not None,
        summary_true="phase12_profile_present=true",
        summary_false="phase12_profile_present=false",
        fail_action="run_or_regenerate_phase12_local_rag_integration_hardening_profile",
    )


def _manifest_smoke_check(
    payload: dict[str, Any] | None,
) -> Phase12LocalRagIntegrationSmokeCheck:
    if payload is None:
        return _bool_check(
            id="provider_contract_manifest_check",
            path=PROVIDER_CONTRACT_SMOKE_PATH,
            passed=False,
            summary_true="provider_contract_manifest_passed=true",
            summary_false="provider_contract_smoke_missing",
            fail_action="regenerate_provider_contract_smoke",
        )
    checks = _dict_value(payload, "checks", [])
    manifest_check = _find_check_item(checks, "provider_integration_manifest")
    manifest_passed = bool(manifest_check and manifest_check.get("passed"))
    return _bool_check(
        id="provider_contract_manifest_check",
        path=PROVIDER_CONTRACT_SMOKE_PATH,
        passed=manifest_passed,
        summary_true="provider_contract_manifest_passed=true",
        summary_false="provider_contract_manifest_passed=false",
        fail_action="review_provider_contract_smoke_for_manifest",
    )


def _contract_smoke_check(
    payload: dict[str, Any] | None,
) -> Phase12LocalRagIntegrationSmokeCheck:
    passed = bool(payload is not None and payload.get("passed"))
    return _bool_check(
        id="provider_contract_smoke_ready",
        path=PROVIDER_CONTRACT_SMOKE_PATH,
        passed=passed,
        summary_true="provider_contract_smoke_passed=true",
        summary_false="provider_contract_smoke_passed=false",
        fail_action="regenerate_provider_contract_smoke",
    )


def _handoff_consistency_check(
    payload: dict[str, Any] | None,
) -> Phase12LocalRagIntegrationSmokeCheck:
    if payload is None:
        return _bool_check(
            id="provider_handoff_consistency",
            path=PROVIDER_HANDOFF_BUNDLE_PATH,
            passed=False,
            summary_true="provider_handoff_consistent=true",
            summary_false="provider_handoff_bundle_missing",
            fail_action="regenerate_provider_handoff_bundle",
        )
    status = _normalize_status(payload.get("status"))
    if status != "ready":
        return _bool_check(
            id="provider_handoff_consistency",
            path=PROVIDER_HANDOFF_BUNDLE_PATH,
            passed=False,
            summary_true="provider_handoff_consistent=true",
            summary_false=f"provider_handoff_status={status}",
            fail_action="resolve_provider_handoff_issue",
        )
    required_artifacts = {
        "provider_contract_smoke",
        "phase11_source_binding_preview_smoke",
        "phase11_rag_retrieve_consumption_smoke",
        "phase11_provider_discovery_smoke",
    }
    present_artifacts = {
        item.get("id")
        for item in _get_evidence_artifacts(payload)
        if isinstance(item, dict) and "id" in item
    }
    missing_artifacts = sorted(required_artifacts - present_artifacts)
    if missing_artifacts:
        return _bool_check(
            id="provider_handoff_consistency",
            path=PROVIDER_HANDOFF_BUNDLE_PATH,
            passed=False,
            summary_true="provider_handoff_consistent=true",
            summary_false=f"missing_artifacts={missing_artifacts}",
            fail_action="run_or_regenerate_phase11_provider_integration_artifacts",
        )
    inconsistent = [
        item for item in _get_evidence_artifacts(payload)
        if isinstance(item, dict) and item.get("id") in required_artifacts and item.get("status") != "ready"
    ]
    if inconsistent:
        return _bool_check(
            id="provider_handoff_consistency",
            path=PROVIDER_HANDOFF_BUNDLE_PATH,
            passed=False,
            summary_true="provider_handoff_consistent=true",
            summary_false=f"non_ready_required_artifacts={ [item.get('id') for item in inconsistent] }",
            fail_action="review_handoff_artifact_status",
        )
    return _bool_check(
        id="provider_handoff_consistency",
        path=PROVIDER_HANDOFF_BUNDLE_PATH,
        passed=True,
        summary_true="provider_handoff_consistent=true",
        summary_false="provider_handoff_consistent=false",
        fail_action="no_action_required",
    )


def _source_binding_preview_readiness_check(
    payload: dict[str, Any] | None,
) -> Phase12LocalRagIntegrationSmokeCheck:
    status = _normalize_status(payload.get("status")) if isinstance(payload, dict) else "blocked"
    return _bool_check(
        id="phase11_source_binding_preview_readiness",
        path=PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH,
        passed=status == "ready",
        summary_true="phase11_source_binding_preview_smoke_ready=true",
        summary_false=f"phase11_source_binding_preview_smoke_status={status}",
        fail_action="regenerate_phase11_source_binding_preview_smoke",
    )


def _rag_retrieve_consumption_readiness_check(
    payload: dict[str, Any] | None,
) -> Phase12LocalRagIntegrationSmokeCheck:
    status = _normalize_status(payload.get("status")) if isinstance(payload, dict) else "blocked"
    return _bool_check(
        id="phase11_rag_retrieve_consumption_readiness",
        path=PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH,
        passed=status == "ready",
        summary_true="phase11_rag_retrieve_consumption_smoke_ready=true",
        summary_false=f"phase11_rag_retrieve_consumption_smoke_status={status}",
        fail_action="regenerate_phase11_rag_retrieve_consumption_smoke",
    )


def _bool_check(
    *,
    id: str,
    path: Path,
    passed: bool,
    summary_true: str,
    summary_false: str,
    fail_action: str,
) -> Phase12LocalRagIntegrationSmokeCheck:
    return Phase12LocalRagIntegrationSmokeCheck(
        id=id,
        required=True,
        status="ready" if passed else "blocked",
        summary=summary_true if passed else summary_false,
        recommended_action="no_action_required" if passed else fail_action,
        evidence_path=str(path),
    )


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "blocked"


def _find_check_item(payload_checks: Any, name: str) -> dict[str, Any] | None:
    if not isinstance(payload_checks, list):
        return None
    for item in payload_checks:
        if isinstance(item, dict) and item.get("name") == name:
            return item
    return None


def _get_evidence_artifacts(payload: dict[str, Any] | None) -> list[Any]:
    if not isinstance(payload, dict):
        return []
    artifacts = payload.get("evidence_artifacts", [])
    return artifacts if isinstance(artifacts, list) else []
