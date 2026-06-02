import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_ID = (
    "phase11-rag-retrieve-consumption-smoke-v1"
)
PHASE4_CALLER_CONSUMPTION_SMOKE_PATH = Path(
    "docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json"
)
PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
PHASE10_PROBE_PATH = Path(
    "docs/smoke/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-probe.json"
)
SMOKE_JSON_FILENAME = "phase11-rag-retrieve-consumption-smoke.json"
SMOKE_MARKDOWN_FILENAME = "phase11-rag-retrieve-consumption-smoke.md"


@dataclass(frozen=True)
class Phase11RetrieveCheck:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase11RagRetrieveConsumptionSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase11RetrieveCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase11_rag_retrieve_consumption_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase11RagRetrieveConsumptionSmokeReport:
    phase4_smoke = _read_json_if_present(base_dir / PHASE4_CALLER_CONSUMPTION_SMOKE_PATH)
    contract_smoke = _read_json_if_present(base_dir / PROVIDER_CONTRACT_SMOKE_PATH)
    phase10_probe = _read_json_if_present(base_dir / PHASE10_PROBE_PATH)
    checks = [
        _phase4_caller_smoke_check(phase4_smoke),
        _provider_contract_smoke_check(contract_smoke),
        _phase10_probe_runtime_boundary_check(phase10_probe),
    ]
    status = "ready" if all(check.status == "ready" for check in checks) else "blocked"
    return Phase11RagRetrieveConsumptionSmokeReport(
        id=PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_caller_consumption_fail_closed",
        summary={
            "total_checks": len(checks),
            "passed_checks": sum(1 for check in checks if check.status == "ready"),
            "failed_checks": sum(1 for check in checks if check.status == "blocked"),
        },
        checks=checks,
        notes=[
            "This smoke confirms retrieval-consumption evidence compatibility for MyPrivateAgent-style consumption.",
            "It relies on existing provider and caller evidence; no runtime execution changes are applied.",
        ],
    )


def phase11_rag_retrieve_consumption_smoke_report_to_dict(
    report: Phase11RagRetrieveConsumptionSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase11_rag_retrieve_consumption_smoke_markdown(
    report: Phase11RagRetrieveConsumptionSmokeReport,
) -> str:
    lines = [
        "# Phase 11 RAG Retrieve Consumption Smoke",
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


def export_phase11_rag_retrieve_consumption_smoke_report(
    output_dir: Path = Path("docs/smoke/myprivateagent-local-provider-integration"),
    *,
    base_dir: Path = Path("."),
) -> Phase11RagRetrieveConsumptionSmokeReport:
    report = build_phase11_rag_retrieve_consumption_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / SMOKE_JSON_FILENAME
    markdown_path = output_dir / SMOKE_MARKDOWN_FILENAME
    exported = Phase11RagRetrieveConsumptionSmokeReport(
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
            phase11_rag_retrieve_consumption_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase11_rag_retrieve_consumption_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _phase4_caller_smoke_check(payload: dict[str, Any] | None) -> Phase11RetrieveCheck:
    status = _normalize_status(_dict_value(payload, "status", "blocked"))
    passed = status == "ready"
    return _bool_check(
        id="phase4_caller_consumption_ready",
        path=PHASE4_CALLER_CONSUMPTION_SMOKE_PATH,
        passed=passed,
        summary_true="phase4_caller_consumption_status=ready",
        summary_false=f"phase4_caller_consumption_status={status}",
        fail_action="regenerate_phase4_caller_consumption_smoke",
    )


def _provider_contract_smoke_check(payload: dict[str, Any] | None) -> Phase11RetrieveCheck:
    passed = isinstance(payload, dict) and bool(payload.get("passed", False))
    return _bool_check(
        id="provider_contract_smoke_ready",
        path=PROVIDER_CONTRACT_SMOKE_PATH,
        passed=passed,
        summary_true="provider_contract_smoke_passed=true",
        summary_false="provider_contract_smoke_passed=false",
        fail_action="regenerate_provider_contract_smoke",
    )


def _phase10_probe_runtime_boundary_check(payload: dict[str, Any] | None) -> Phase11RetrieveCheck:
    passed = False
    if isinstance(payload, dict):
        summary = payload.get("summary", {})
        if isinstance(summary, dict):
            passed = (
                summary.get("runtime_promotion_status", "keep_runtime_defaults")
                == "keep_runtime_defaults"
            )
    return _bool_check(
        id="phase10_runtime_boundary_preserved",
        path=PHASE10_PROBE_PATH,
        passed=passed,
        summary_true="runtime_promotion_status=keep_runtime_defaults",
        summary_false="runtime_promotion_boundary_not_preserved",
        fail_action="review_phase10_probe_runtime_boundary",
    )


def _bool_check(
    *,
    id: str,
    path: Path,
    passed: bool,
    summary_true: str,
    summary_false: str,
    fail_action: str,
) -> Phase11RetrieveCheck:
    return Phase11RetrieveCheck(
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


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "blocked"


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)
