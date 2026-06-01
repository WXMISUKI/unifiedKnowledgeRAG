import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE9_LOCAL_CONSUMPTION_SMOKE_ID = "phase9-myprivateagent-local-consumption-smoke-v1"
PHASE9_READINESS_PATH = Path(
    "docs/integration/myprivateagent-local-consumption/"
    "phase9-myprivateagent-local-consumption-readiness.json"
)
PHASE9_CONTRACT_PATH = Path(
    "docs/integration/myprivateagent-local-consumption/"
    "phase9-myprivateagent-local-consumption-contract.md"
)
PROVIDER_INTEGRATION_PROBE_PATH = Path(
    "docs/integration/provider-binding/provider-integration-probe.json"
)
PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
SOURCE_BINDING_SUMMARY_PATH = Path(
    "docs/integration/source-bindings/provider-source-bindings.json"
)
PHASE4_CALLER_SMOKE_PATH = Path(
    "docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json"
)
SMOKE_JSON_FILENAME = "phase9-myprivateagent-local-consumption-smoke.json"
SMOKE_MARKDOWN_FILENAME = "phase9-myprivateagent-local-consumption-smoke.md"


@dataclass(frozen=True)
class Phase9LocalConsumptionSmokeCheck:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase9LocalConsumptionSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase9LocalConsumptionSmokeCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase9_myprivateagent_local_consumption_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase9LocalConsumptionSmokeReport:
    readiness_payload = _read_json_if_present(base_dir / PHASE9_READINESS_PATH)
    probe_payload = _read_json_if_present(base_dir / PROVIDER_INTEGRATION_PROBE_PATH)
    provider_smoke_payload = _read_json_if_present(base_dir / PROVIDER_CONTRACT_SMOKE_PATH)
    source_binding_payload = _read_json_if_present(base_dir / SOURCE_BINDING_SUMMARY_PATH)
    phase4_payload = _read_json_if_present(base_dir / PHASE4_CALLER_SMOKE_PATH)
    contract_text = _read_text_if_present(base_dir / PHASE9_CONTRACT_PATH)

    checks = [
        _artifact_check(
            id="phase9_local_consumption_readiness",
            path=PHASE9_READINESS_PATH,
            payload=readiness_payload,
            required=True,
            missing_action="regenerate_phase9_local_consumption_readiness",
        ),
        _contract_content_check(contract_text),
        _control_plane_compatibility_check(probe_payload),
        _graph_boundary_planned_check(provider_smoke_payload),
        _source_binding_readiness_check(source_binding_payload),
        _phase4_caller_smoke_check(phase4_payload),
        _runtime_promotion_boundary_check(readiness_payload),
    ]

    status = "ready" if all(check.status == "ready" for check in checks) else "blocked"
    return Phase9LocalConsumptionSmokeReport(
        id=PHASE9_LOCAL_CONSUMPTION_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_runtime_defaults",
        summary={
            "total_checks": len(checks),
            "passed_checks": sum(1 for check in checks if check.status == "ready"),
            "failed_checks": sum(1 for check in checks if check.status == "blocked"),
            "readiness_status": _normalize_status(_dict_value(readiness_payload, "status", "review")),
            "local_consumption_state": _dict_value(
                readiness_payload, "local_consumption_state", "review"
            ),
            "local_handoff_ready": bool(
                _dict_value(_dict_value(readiness_payload, "summary", {}), "local_handoff_ready", False)
            ),
            "runtime_promotion_ready": bool(
                _dict_value(
                    _dict_value(readiness_payload, "summary", {}),
                    "runtime_promotion_ready",
                    False,
                )
            ),
        },
        checks=checks,
        notes=[
            "This smoke is local read-only consumer-side evidence.",
            "It validates MyPrivateAgent local-consumption contract alignment from existing artifacts.",
            "It does not mutate source bindings or promote runtime defaults.",
        ],
    )


def phase9_myprivateagent_local_consumption_smoke_report_to_dict(
    report: Phase9LocalConsumptionSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase9_myprivateagent_local_consumption_smoke_markdown(
    report: Phase9LocalConsumptionSmokeReport,
) -> str:
    lines = [
        "# Phase 9 MyPrivateAgent Local Consumption Smoke",
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
        f"| Total Checks | `{report.summary['total_checks']}` |",
        f"| Passed Checks | `{report.summary['passed_checks']}` |",
        f"| Failed Checks | `{report.summary['failed_checks']}` |",
        f"| Readiness Status | `{report.summary['readiness_status']}` |",
        f"| Local Consumption State | `{report.summary['local_consumption_state']}` |",
        f"| Local Handoff Ready | `{report.summary['local_handoff_ready']}` |",
        f"| Runtime Promotion Ready | `{report.summary['runtime_promotion_ready']}` |",
        "",
        "## Checks",
        "",
        "| Check | Required | Status | Summary | Recommended Action |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        lines.append(
            f"| `{check.id}` | `{check.required}` | `{check.status}` | "
            f"{check.summary} | `{check.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase9_myprivateagent_local_consumption_smoke_report(
    output_dir: Path = Path("docs/smoke/myprivateagent-local-consumption"),
    *,
    base_dir: Path = Path("."),
) -> Phase9LocalConsumptionSmokeReport:
    report = build_phase9_myprivateagent_local_consumption_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / SMOKE_JSON_FILENAME
    markdown_path = output_dir / SMOKE_MARKDOWN_FILENAME
    exported = Phase9LocalConsumptionSmokeReport(
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
            phase9_myprivateagent_local_consumption_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase9_myprivateagent_local_consumption_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _artifact_check(
    *,
    id: str,
    path: Path,
    payload: dict[str, Any] | None,
    required: bool,
    missing_action: str,
) -> Phase9LocalConsumptionSmokeCheck:
    if not isinstance(payload, dict):
        return Phase9LocalConsumptionSmokeCheck(
            id=id,
            required=required,
            status="blocked",
            summary="artifact_present=false",
            recommended_action=missing_action,
            evidence_path=str(path),
        )
    status = _normalize_status(payload.get("status", "review"))
    return Phase9LocalConsumptionSmokeCheck(
        id=id,
        required=required,
        status="ready" if status in {"ready", "review"} else "blocked",
        summary=f"artifact_present=true; status={status}",
        recommended_action="no_action_required" if status in {"ready", "review"} else "review_evidence_notes",
        evidence_path=str(path),
    )


def _contract_content_check(contract_text: str | None) -> Phase9LocalConsumptionSmokeCheck:
    required_tokens = [
        "http://127.0.0.1:8020",
        "PROVIDER_API_KEY",
        "MyPrivateAgent",
        "source-to-agent binding",
    ]
    if not contract_text:
        return Phase9LocalConsumptionSmokeCheck(
            id="phase9_contract_content",
            required=True,
            status="blocked",
            summary="contract_present=false",
            recommended_action="restore_phase9_local_consumption_contract",
            evidence_path=str(PHASE9_CONTRACT_PATH),
        )
    missing = [token for token in required_tokens if token not in contract_text]
    if missing:
        return Phase9LocalConsumptionSmokeCheck(
            id="phase9_contract_content",
            required=True,
            status="blocked",
            summary=f"missing_tokens={','.join(missing)}",
            recommended_action="update_phase9_local_consumption_contract",
            evidence_path=str(PHASE9_CONTRACT_PATH),
        )
    return Phase9LocalConsumptionSmokeCheck(
        id="phase9_contract_content",
        required=True,
        status="ready",
        summary="contract_required_tokens_present=true",
        recommended_action="no_action_required",
        evidence_path=str(PHASE9_CONTRACT_PATH),
    )


def _control_plane_compatibility_check(
    payload: dict[str, Any] | None,
) -> Phase9LocalConsumptionSmokeCheck:
    if not isinstance(payload, dict):
        return Phase9LocalConsumptionSmokeCheck(
            id="control_plane_compatibility",
            required=True,
            status="blocked",
            summary="integration_probe_present=false",
            recommended_action="regenerate_provider_integration_probe",
            evidence_path=str(PROVIDER_INTEGRATION_PROBE_PATH),
        )
    checks = payload.get("checks", [])
    compatible = False
    if isinstance(checks, list):
        for check in checks:
            if not isinstance(check, dict):
                continue
            if check.get("name") != "manifest_identity":
                continue
            details = _dict_value(check, "details", {})
            planes = _dict_value(details, "compatible_control_planes", [])
            if isinstance(planes, list) and "MyPrivateAgent" in planes:
                compatible = True
                break
    return Phase9LocalConsumptionSmokeCheck(
        id="control_plane_compatibility",
        required=True,
        status="ready" if compatible else "blocked",
        summary=f"myprivateagent_compatible={compatible}",
        recommended_action="no_action_required" if compatible else "review_evidence_notes",
        evidence_path=str(PROVIDER_INTEGRATION_PROBE_PATH),
    )


def _graph_boundary_planned_check(
    payload: dict[str, Any] | None,
) -> Phase9LocalConsumptionSmokeCheck:
    if not isinstance(payload, dict):
        return Phase9LocalConsumptionSmokeCheck(
            id="graph_planned_boundary",
            required=True,
            status="blocked",
            summary="provider_contract_smoke_present=false",
            recommended_action="regenerate_provider_contract_smoke",
            evidence_path=str(PROVIDER_CONTRACT_SMOKE_PATH),
        )
    checks = payload.get("checks", [])
    graph_planned = False
    if isinstance(checks, list):
        for check in checks:
            if not isinstance(check, dict):
                continue
            if check.get("name") != "graph_planned_boundary":
                continue
            if bool(check.get("passed")):
                graph_planned = True
                break
    return Phase9LocalConsumptionSmokeCheck(
        id="graph_planned_boundary",
        required=True,
        status="ready" if graph_planned else "blocked",
        summary=f"graph_boundary_check_passed={graph_planned}",
        recommended_action="no_action_required" if graph_planned else "review_evidence_notes",
        evidence_path=str(PROVIDER_CONTRACT_SMOKE_PATH),
    )


def _source_binding_readiness_check(
    payload: dict[str, Any] | None,
) -> Phase9LocalConsumptionSmokeCheck:
    if not isinstance(payload, dict):
        return Phase9LocalConsumptionSmokeCheck(
            id="source_binding_readiness",
            required=False,
            status="review",
            summary="source_binding_summary_present=false",
            recommended_action="regenerate_provider_source_bindings",
            evidence_path=str(SOURCE_BINDING_SUMMARY_PATH),
        )
    status = _normalize_status(payload.get("status", "review"))
    return Phase9LocalConsumptionSmokeCheck(
        id="source_binding_readiness",
        required=False,
        status="ready" if status in {"ready", "review"} else "blocked",
        summary=(
            f"status={status}; bindable_sources={payload.get('bindable_source_count', 0)}/"
            f"{payload.get('total_source_count', 0)}"
        ),
        recommended_action="no_action_required" if status in {"ready", "review"} else "review_evidence_notes",
        evidence_path=str(SOURCE_BINDING_SUMMARY_PATH),
    )


def _phase4_caller_smoke_check(payload: dict[str, Any] | None) -> Phase9LocalConsumptionSmokeCheck:
    if not isinstance(payload, dict):
        return Phase9LocalConsumptionSmokeCheck(
            id="phase4_caller_consumption_smoke",
            required=False,
            status="review",
            summary="phase4_caller_smoke_present=false",
            recommended_action="regenerate_phase4_caller_consumption_smoke",
            evidence_path=str(PHASE4_CALLER_SMOKE_PATH),
        )
    status = _normalize_status(payload.get("status", "review"))
    return Phase9LocalConsumptionSmokeCheck(
        id="phase4_caller_consumption_smoke",
        required=False,
        status="ready" if status in {"ready", "review"} else "blocked",
        summary=f"status={status}",
        recommended_action="no_action_required" if status in {"ready", "review"} else "review_evidence_notes",
        evidence_path=str(PHASE4_CALLER_SMOKE_PATH),
    )


def _runtime_promotion_boundary_check(
    readiness_payload: dict[str, Any] | None,
) -> Phase9LocalConsumptionSmokeCheck:
    if not isinstance(readiness_payload, dict):
        return Phase9LocalConsumptionSmokeCheck(
            id="runtime_promotion_boundary",
            required=True,
            status="blocked",
            summary="readiness_present=false",
            recommended_action="regenerate_phase9_local_consumption_readiness",
            evidence_path=str(PHASE9_READINESS_PATH),
        )
    summary = _dict_value(readiness_payload, "summary", {})
    runtime_ready = bool(_dict_value(summary, "runtime_promotion_ready", False))
    decision = str(_dict_value(readiness_payload, "decision", "keep_local_consumption_review"))
    passed = not runtime_ready and decision != "confirm_runtime_promotion"
    return Phase9LocalConsumptionSmokeCheck(
        id="runtime_promotion_boundary",
        required=True,
        status="ready" if passed else "blocked",
        summary=f"runtime_promotion_ready={runtime_ready}; decision={decision}",
        recommended_action="no_action_required" if passed else "review_evidence_notes",
        evidence_path=str(PHASE9_READINESS_PATH),
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
