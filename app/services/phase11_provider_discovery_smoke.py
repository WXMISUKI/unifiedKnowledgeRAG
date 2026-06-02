import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE11_PROVIDER_DISCOVERY_SMOKE_ID = "phase11-provider-discovery-smoke-v1"
PHASE11_PROFILE_PATH = Path(
    "docs/integration/myprivateagent-local-provider-integration/"
    "phase11-local-provider-integration-profile.json"
)
PROVIDER_INTEGRATION_PROBE_PATH = Path(
    "docs/integration/provider-binding/provider-integration-probe.json"
)
PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
PROVIDER_HANDOFF_BUNDLE_PATH = Path(
    "docs/integration/provider-handoff/provider-handoff-bundle.json"
)
SMOKE_JSON_FILENAME = "phase11-provider-discovery-smoke.json"
SMOKE_MARKDOWN_FILENAME = "phase11-provider-discovery-smoke.md"


@dataclass(frozen=True)
class Phase11DiscoveryCheck:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase11ProviderDiscoverySmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase11DiscoveryCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase11_provider_discovery_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase11ProviderDiscoverySmokeReport:
    profile_payload = _read_json_if_present(base_dir / PHASE11_PROFILE_PATH)
    probe_payload = _read_json_if_present(base_dir / PROVIDER_INTEGRATION_PROBE_PATH)
    contract_smoke_payload = _read_json_if_present(base_dir / PROVIDER_CONTRACT_SMOKE_PATH)
    handoff_payload = _read_json_if_present(base_dir / PROVIDER_HANDOFF_BUNDLE_PATH)

    checks = [
        _profile_presence_check(profile_payload),
        _integration_probe_bindable_check(probe_payload),
        _contract_smoke_check(contract_smoke_payload),
        _handoff_row_check(handoff_payload),
    ]
    status = "ready" if all(check.status == "ready" for check in checks) else "blocked"
    return Phase11ProviderDiscoverySmokeReport(
        id=PHASE11_PROVIDER_DISCOVERY_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_discovery_read_only",
        summary={
            "total_checks": len(checks),
            "passed_checks": sum(1 for check in checks if check.status == "ready"),
            "failed_checks": sum(1 for check in checks if check.status == "blocked"),
        },
        checks=checks,
        notes=[
            "Discovery smoke validates MyPrivateAgent-style provider discovery evidence alignment.",
            "It does not call mutating endpoints or start external services.",
        ],
    )


def phase11_provider_discovery_smoke_report_to_dict(
    report: Phase11ProviderDiscoverySmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase11_provider_discovery_smoke_markdown(
    report: Phase11ProviderDiscoverySmokeReport,
) -> str:
    lines = [
        "# Phase 11 Provider Discovery Smoke",
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
        lines.append(f"| {key} | `{value}` |")
    lines.extend(["", "## Checks", "", "| Check | Required | Status | Summary | Recommended Action |", "|---|---|---|---|---|"])
    for check in report.checks:
        lines.append(
            f"| `{check.id}` | `{check.required}` | `{check.status}` | {check.summary} | `{check.recommended_action}` |"
        )
    lines.append("")
    return "\n".join(lines)


def export_phase11_provider_discovery_smoke_report(
    output_dir: Path = Path("docs/smoke/myprivateagent-local-provider-integration"),
    *,
    base_dir: Path = Path("."),
) -> Phase11ProviderDiscoverySmokeReport:
    report = build_phase11_provider_discovery_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / SMOKE_JSON_FILENAME
    markdown_path = output_dir / SMOKE_MARKDOWN_FILENAME
    exported = Phase11ProviderDiscoverySmokeReport(
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
            phase11_provider_discovery_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase11_provider_discovery_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _profile_presence_check(payload: dict[str, Any] | None) -> Phase11DiscoveryCheck:
    return _bool_check(
        id="phase11_profile_present",
        path=PHASE11_PROFILE_PATH,
        passed=isinstance(payload, dict),
        summary_true="profile_present=true",
        summary_false="profile_present=false",
        fail_action="regenerate_phase11_local_provider_integration_profile",
    )


def _integration_probe_bindable_check(payload: dict[str, Any] | None) -> Phase11DiscoveryCheck:
    bindable = isinstance(payload, dict) and bool(payload.get("bindable", False))
    return _bool_check(
        id="provider_integration_probe_bindable",
        path=PROVIDER_INTEGRATION_PROBE_PATH,
        passed=bindable,
        summary_true="bindable=true",
        summary_false="bindable=false",
        fail_action="review_provider_integration_probe",
    )


def _contract_smoke_check(payload: dict[str, Any] | None) -> Phase11DiscoveryCheck:
    passed = isinstance(payload, dict) and bool(payload.get("passed", False))
    return _bool_check(
        id="provider_contract_smoke_passed",
        path=PROVIDER_CONTRACT_SMOKE_PATH,
        passed=passed,
        summary_true="contract_smoke_passed=true",
        summary_false="contract_smoke_passed=false",
        fail_action="regenerate_provider_contract_smoke",
    )


def _handoff_row_check(payload: dict[str, Any] | None) -> Phase11DiscoveryCheck:
    has_row = False
    if isinstance(payload, dict):
        artifacts = payload.get("evidence_artifacts", [])
        if isinstance(artifacts, list):
            has_row = any(
                isinstance(artifact, dict)
                and artifact.get("id") == "phase11_local_provider_integration_profile"
                for artifact in artifacts
            )
    return _bool_check(
        id="handoff_has_phase11_profile_row",
        path=PROVIDER_HANDOFF_BUNDLE_PATH,
        passed=has_row,
        summary_true="phase11_profile_row_present=true",
        summary_false="phase11_profile_row_present=false",
        fail_action="wire_phase11_into_provider_handoff_bundle",
    )


def _bool_check(
    *,
    id: str,
    path: Path,
    passed: bool,
    summary_true: str,
    summary_false: str,
    fail_action: str,
) -> Phase11DiscoveryCheck:
    return Phase11DiscoveryCheck(
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
