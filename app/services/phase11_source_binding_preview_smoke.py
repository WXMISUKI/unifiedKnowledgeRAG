import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_ID = "phase11-source-binding-preview-smoke-v1"
SOURCE_BINDING_SUMMARY_PATH = Path(
    "docs/integration/source-bindings/provider-source-bindings.json"
)
PHASE10_READINESS_PATH = Path(
    "docs/integration/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-readiness.json"
)
SMOKE_JSON_FILENAME = "phase11-source-binding-preview-smoke.json"
SMOKE_MARKDOWN_FILENAME = "phase11-source-binding-preview-smoke.md"


@dataclass(frozen=True)
class Phase11SourceBindingCheck:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase11SourceBindingPreviewSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase11SourceBindingCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase11_source_binding_preview_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase11SourceBindingPreviewSmokeReport:
    source_binding_payload = _read_json_if_present(base_dir / SOURCE_BINDING_SUMMARY_PATH)
    phase10_readiness = _read_json_if_present(base_dir / PHASE10_READINESS_PATH)
    checks = [
        _source_binding_summary_ready_check(source_binding_payload),
        _source_binding_owner_check(phase10_readiness),
        _bindable_count_positive_check(source_binding_payload),
    ]
    status = "ready" if all(check.status == "ready" for check in checks) else "blocked"
    return Phase11SourceBindingPreviewSmokeReport(
        id=PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_source_binding_preview_only",
        summary={
            "total_checks": len(checks),
            "passed_checks": sum(1 for check in checks if check.status == "ready"),
            "failed_checks": sum(1 for check in checks if check.status == "blocked"),
        },
        checks=checks,
        notes=[
            "This smoke validates source-binding preview compatibility for MyPrivateAgent integration review.",
            "It does not create source-to-agent bindings.",
        ],
    )


def phase11_source_binding_preview_smoke_report_to_dict(
    report: Phase11SourceBindingPreviewSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase11_source_binding_preview_smoke_markdown(
    report: Phase11SourceBindingPreviewSmokeReport,
) -> str:
    lines = [
        "# Phase 11 Source Binding Preview Smoke",
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


def export_phase11_source_binding_preview_smoke_report(
    output_dir: Path = Path("docs/smoke/myprivateagent-local-provider-integration"),
    *,
    base_dir: Path = Path("."),
) -> Phase11SourceBindingPreviewSmokeReport:
    report = build_phase11_source_binding_preview_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / SMOKE_JSON_FILENAME
    markdown_path = output_dir / SMOKE_MARKDOWN_FILENAME
    exported = Phase11SourceBindingPreviewSmokeReport(
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
            phase11_source_binding_preview_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase11_source_binding_preview_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _source_binding_summary_ready_check(
    payload: dict[str, Any] | None,
) -> Phase11SourceBindingCheck:
    status = _normalize_status(_dict_value(payload, "status", "blocked"))
    passed = status == "ready"
    return _bool_check(
        id="source_binding_summary_ready",
        path=SOURCE_BINDING_SUMMARY_PATH,
        passed=passed,
        summary_true="source_binding_status=ready",
        summary_false=f"source_binding_status={status}",
        fail_action="regenerate_provider_source_bindings",
    )


def _source_binding_owner_check(
    payload: dict[str, Any] | None,
) -> Phase11SourceBindingCheck:
    summary = _dict_value(payload, "summary", {})
    owner = _dict_value(summary, "source_binding_policy_owner", "unknown")
    passed = owner == "caller"
    return _bool_check(
        id="source_binding_policy_owner",
        path=PHASE10_READINESS_PATH,
        passed=passed,
        summary_true="source_binding_policy_owner=caller",
        summary_false=f"source_binding_policy_owner={owner}",
        fail_action="review_phase10_source_binding_boundary",
    )


def _bindable_count_positive_check(
    payload: dict[str, Any] | None,
) -> Phase11SourceBindingCheck:
    bindable = int(_dict_value(payload, "bindable_source_count", 0) or 0)
    total = int(_dict_value(payload, "total_source_count", 0) or 0)
    passed = bindable > 0 and total >= bindable
    return _bool_check(
        id="bindable_source_count_positive",
        path=SOURCE_BINDING_SUMMARY_PATH,
        passed=passed,
        summary_true=f"bindable_sources={bindable}/{total}",
        summary_false=f"bindable_sources={bindable}/{total}",
        fail_action="review_source_binding_readiness",
    )


def _bool_check(
    *,
    id: str,
    path: Path,
    passed: bool,
    summary_true: str,
    summary_false: str,
    fail_action: str,
) -> Phase11SourceBindingCheck:
    return Phase11SourceBindingCheck(
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
