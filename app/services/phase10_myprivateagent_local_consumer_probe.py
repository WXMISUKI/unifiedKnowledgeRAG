import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE10_LOCAL_CONSUMER_PROBE_ID = "phase10-myprivateagent-local-consumer-probe-v1"
PHASE10_READINESS_PATH = Path(
    "docs/integration/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-readiness.json"
)
PHASE10_CONTRACT_PATH = Path(
    "docs/integration/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-verification-contract.md"
)
PROVIDER_HANDOFF_BUNDLE_PATH = Path(
    "docs/integration/provider-handoff/provider-handoff-bundle.json"
)
PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
PHASE4_CALLER_CONSUMPTION_SMOKE_PATH = Path(
    "docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json"
)
PROBE_JSON_FILENAME = "phase10-myprivateagent-local-consumer-probe.json"
PROBE_MARKDOWN_FILENAME = "phase10-myprivateagent-local-consumer-probe.md"


@dataclass(frozen=True)
class Phase10LocalConsumerProbeCheck:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase10LocalConsumerProbeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase10LocalConsumerProbeCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase10_myprivateagent_local_consumer_probe_report(
    *,
    base_dir: Path = Path("."),
) -> Phase10LocalConsumerProbeReport:
    readiness_payload = _read_json_if_present(base_dir / PHASE10_READINESS_PATH)
    contract_text = _read_text_if_present(base_dir / PHASE10_CONTRACT_PATH)
    handoff_payload = _read_json_if_present(base_dir / PROVIDER_HANDOFF_BUNDLE_PATH)
    provider_smoke_payload = _read_json_if_present(base_dir / PROVIDER_CONTRACT_SMOKE_PATH)
    phase4_smoke_payload = _read_json_if_present(base_dir / PHASE4_CALLER_CONSUMPTION_SMOKE_PATH)

    checks = [
        _readiness_artifact_check(readiness_payload),
        _contract_content_check(contract_text),
        _local_access_mode_check(readiness_payload),
        _handoff_contains_phase10_check(handoff_payload),
        _evidence_pack_caller_smoke_check(phase4_smoke_payload),
        _graph_boundary_check(provider_smoke_payload, readiness_payload),
        _runtime_promotion_boundary_check(readiness_payload),
    ]
    status = "ready" if all(check.status == "ready" for check in checks) else "blocked"
    summary = _dict_value(readiness_payload, "summary", {})
    return Phase10LocalConsumerProbeReport(
        id=PHASE10_LOCAL_CONSUMER_PROBE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_provider_side_consumer_probe_review",
        summary={
            "total_checks": len(checks),
            "passed_checks": sum(1 for check in checks if check.status == "ready"),
            "failed_checks": sum(1 for check in checks if check.status == "blocked"),
            "readiness_status": _normalize_status(_dict_value(readiness_payload, "status", "review")),
            "local_consumer_state": _dict_value(readiness_payload, "local_consumer_state", "review"),
            "local_provider_url": _dict_value(summary, "local_provider_url", "http://127.0.0.1:8020"),
            "api_key_mode": _dict_value(summary, "api_key_mode", "not_configured_local_dev"),
            "runtime_promotion_status": _dict_value(summary, "runtime_promotion_status", "keep_runtime_defaults"),
        },
        checks=checks,
        notes=[
            "This probe is caller-shaped but provider-side and read-only.",
            "It validates local consumer evidence alignment without running a live MyPrivateAgent integration.",
            "It does not create source bindings, execute GraphRAG, or promote runtime defaults.",
        ],
    )


def phase10_myprivateagent_local_consumer_probe_report_to_dict(
    report: Phase10LocalConsumerProbeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase10_myprivateagent_local_consumer_probe_markdown(
    report: Phase10LocalConsumerProbeReport,
) -> str:
    lines = [
        "# Phase 10 MyPrivateAgent Local Consumer Probe",
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


def export_phase10_myprivateagent_local_consumer_probe_report(
    output_dir: Path = Path("docs/smoke/myprivateagent-local-consumer-verification"),
    *,
    base_dir: Path = Path("."),
) -> Phase10LocalConsumerProbeReport:
    report = build_phase10_myprivateagent_local_consumer_probe_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PROBE_JSON_FILENAME
    markdown_path = output_dir / PROBE_MARKDOWN_FILENAME
    exported = Phase10LocalConsumerProbeReport(
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
            phase10_myprivateagent_local_consumer_probe_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase10_myprivateagent_local_consumer_probe_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _readiness_artifact_check(
    payload: dict[str, Any] | None,
) -> Phase10LocalConsumerProbeCheck:
    if not isinstance(payload, dict):
        return _blocked(
            "phase10_local_consumer_readiness",
            PHASE10_READINESS_PATH,
            "readiness_present=false",
            "regenerate_phase10_local_consumer_readiness",
        )
    status = _normalize_status(payload.get("status"))
    passed = status in {"ready", "review"}
    return Phase10LocalConsumerProbeCheck(
        id="phase10_local_consumer_readiness",
        required=True,
        status="ready" if passed else "blocked",
        summary=f"readiness_present=true; status={status}",
        recommended_action="no_action_required" if passed else "review_evidence_notes",
        evidence_path=str(PHASE10_READINESS_PATH),
    )


def _contract_content_check(
    contract_text: str | None,
) -> Phase10LocalConsumerProbeCheck:
    required_tokens = [
        "http://127.0.0.1:8020",
        "PROVIDER_API_KEY",
        "GET /api/provider/manifest",
        "GET /api/provider/preflight",
        "GET /api/provider/source-bindings",
        "GET /api/provider/handoff",
        "source-to-agent binding",
        "GraphRAG",
    ]
    if not contract_text:
        return _blocked(
            "phase10_contract_content",
            PHASE10_CONTRACT_PATH,
            "contract_present=false",
            "restore_phase10_local_consumer_verification_contract",
        )
    missing = [token for token in required_tokens if token not in contract_text]
    if missing:
        return _blocked(
            "phase10_contract_content",
            PHASE10_CONTRACT_PATH,
            f"missing_tokens={','.join(missing)}",
            "update_phase10_local_consumer_verification_contract",
        )
    return Phase10LocalConsumerProbeCheck(
        id="phase10_contract_content",
        required=True,
        status="ready",
        summary="contract_required_tokens_present=true",
        recommended_action="no_action_required",
        evidence_path=str(PHASE10_CONTRACT_PATH),
    )


def _local_access_mode_check(
    readiness_payload: dict[str, Any] | None,
) -> Phase10LocalConsumerProbeCheck:
    summary = _dict_value(readiness_payload, "summary", {})
    base_url = _dict_value(summary, "local_provider_url", "")
    api_key_mode = _dict_value(summary, "api_key_mode", "")
    passed = (
        base_url == "http://127.0.0.1:8020"
        and api_key_mode in {"not_configured_local_dev", "configured_protected_api"}
    )
    return Phase10LocalConsumerProbeCheck(
        id="local_access_mode",
        required=True,
        status="ready" if passed else "blocked",
        summary=f"base_url={base_url}; api_key_mode={api_key_mode}",
        recommended_action="no_action_required" if passed else "review_local_access_contract",
        evidence_path=str(PHASE10_READINESS_PATH),
    )


def _handoff_contains_phase10_check(
    payload: dict[str, Any] | None,
) -> Phase10LocalConsumerProbeCheck:
    if not isinstance(payload, dict):
        return _blocked(
            "handoff_phase10_presence",
            PROVIDER_HANDOFF_BUNDLE_PATH,
            "handoff_present=false",
            "regenerate_provider_handoff_bundle",
        )
    artifacts = payload.get("evidence_artifacts", [])
    ids = {
        artifact.get("id")
        for artifact in artifacts
        if isinstance(artifact, dict)
    } if isinstance(artifacts, list) else set()
    expected = {
        "phase10_myprivateagent_local_consumer_readiness",
        "phase10_myprivateagent_local_consumer_probe",
    }
    missing = sorted(expected - ids)
    if missing:
        return _blocked(
            "handoff_phase10_presence",
            PROVIDER_HANDOFF_BUNDLE_PATH,
            f"missing_phase10_artifacts={','.join(missing)}",
            "wire_phase10_into_provider_handoff_bundle",
        )
    return Phase10LocalConsumerProbeCheck(
        id="handoff_phase10_presence",
        required=True,
        status="ready",
        summary="phase10_handoff_artifacts_present=true",
        recommended_action="no_action_required",
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _evidence_pack_caller_smoke_check(
    payload: dict[str, Any] | None,
) -> Phase10LocalConsumerProbeCheck:
    if not isinstance(payload, dict):
        return _blocked(
            "evidence_pack_caller_smoke",
            PHASE4_CALLER_CONSUMPTION_SMOKE_PATH,
            "phase4_caller_smoke_present=false",
            "regenerate_phase4_caller_consumption_smoke",
        )
    status = _normalize_status(payload.get("status"))
    passed = status in {"ready", "review"}
    return Phase10LocalConsumerProbeCheck(
        id="evidence_pack_caller_smoke",
        required=True,
        status="ready" if passed else "blocked",
        summary=f"status={status}",
        recommended_action="no_action_required" if passed else "review_evidence_pack_smoke",
        evidence_path=str(PHASE4_CALLER_CONSUMPTION_SMOKE_PATH),
    )


def _graph_boundary_check(
    provider_smoke_payload: dict[str, Any] | None,
    readiness_payload: dict[str, Any] | None,
) -> Phase10LocalConsumerProbeCheck:
    summary = _dict_value(readiness_payload, "summary", {})
    readiness_graph_ready = bool(_dict_value(summary, "graph_boundary_ready", False))
    checks = _dict_value(provider_smoke_payload, "checks", [])
    smoke_graph_ready = False
    if isinstance(checks, list):
        smoke_graph_ready = any(
            isinstance(check, dict)
            and check.get("name") == "graph_planned_boundary"
            and check.get("passed") is True
            for check in checks
        )
    passed = readiness_graph_ready and smoke_graph_ready
    return Phase10LocalConsumerProbeCheck(
        id="graph_planned_boundary",
        required=True,
        status="ready" if passed else "blocked",
        summary=(
            f"readiness_graph_boundary_ready={readiness_graph_ready}; "
            f"provider_smoke_graph_boundary_ready={smoke_graph_ready}"
        ),
        recommended_action="no_action_required" if passed else "regenerate_provider_contract_smoke",
        evidence_path=str(PROVIDER_CONTRACT_SMOKE_PATH),
    )


def _runtime_promotion_boundary_check(
    readiness_payload: dict[str, Any] | None,
) -> Phase10LocalConsumerProbeCheck:
    summary = _dict_value(readiness_payload, "summary", {})
    runtime_ready = bool(_dict_value(summary, "runtime_promotion_ready", False))
    runtime_status = _dict_value(summary, "runtime_promotion_status", "")
    passed = not runtime_ready and runtime_status == "keep_runtime_defaults"
    return Phase10LocalConsumerProbeCheck(
        id="runtime_promotion_boundary",
        required=True,
        status="ready" if passed else "blocked",
        summary=(
            f"runtime_promotion_ready={runtime_ready}; "
            f"runtime_promotion_status={runtime_status}"
        ),
        recommended_action="no_action_required" if passed else "review_runtime_promotion_boundary",
        evidence_path=str(PHASE10_READINESS_PATH),
    )


def _blocked(
    id: str,
    path: Path,
    summary: str,
    action: str,
) -> Phase10LocalConsumerProbeCheck:
    return Phase10LocalConsumerProbeCheck(
        id=id,
        required=True,
        status="blocked",
        summary=summary,
        recommended_action=action,
        evidence_path=str(path),
    )


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text_if_present(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "review"


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)
