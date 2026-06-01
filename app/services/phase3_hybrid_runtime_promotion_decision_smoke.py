import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE3_HYBRID_RUNTIME_PROMOTION_DECISION_SMOKE_ID = (
    "phase3-hybrid-runtime-promotion-decision-smoke-v1"
)


@dataclass(frozen=True)
class Phase3HybridRuntimePromotionDecisionSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    checks: list[dict[str, Any]]
    summary: dict[str, int]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase3_hybrid_runtime_promotion_decision_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase3HybridRuntimePromotionDecisionSmokeReport:
    readiness_path = (
        base_dir
        / "docs/benchmark/chinese-seed/hybrid-runtime-promotion/"
        "phase3-hybrid-runtime-promotion-decision-readiness.json"
    )
    checks = [
        _file_check(
            check_id="hybrid_runtime_promotion_contract_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/hybrid-runtime-promotion/"
            "phase3-hybrid-runtime-promotion-decision-contract.md",
            required=True,
        ),
        _json_check(
            check_id="hybrid_runtime_promotion_readiness_present",
            path=readiness_path,
            required=True,
        ),
        _json_check(
            check_id="phase3_retrieval_promotion_readiness_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/retrieval-promotion-readiness/"
            "phase3-retrieval-promotion-readiness.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_candidate_runtime_diagnostics_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/"
            "phase3-candidate-runtime-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_candidate_latency_diagnostics_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/"
            "phase3-candidate-latency-resource-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_hybrid_calibration_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/"
            "phase3-hybrid-fusion-threshold-calibration.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_hybrid_cross_case_fp_fn_smoke_present",
            path=base_dir
            / "docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_aggregation_relation_negative_control_smoke_present",
            path=base_dir
            / "docs/smoke/aggregation-relation-negative-control/"
            "phase3-aggregation-relation-negative-control-smoke.json",
            required=True,
        ),
        _json_check(
            check_id="phase6_bge_artifact_readiness_present",
            path=base_dir
            / "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json",
            required=True,
        ),
        _json_check(
            check_id="phase6_bge_comparison_diagnostics_present",
            path=base_dir
            / "docs/operations/bge-m3-comparison-readiness/"
            "phase6-bge-m3-vs-mock-fixture-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="phase6_bge_comparison_smoke_present",
            path=base_dir / "docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json",
            required=True,
        ),
        _json_check(
            check_id="phase6_qdrant_vector_store_readiness_present",
            path=base_dir
            / "docs/operations/qdrant-vector-store-readiness/"
            "phase6-qdrant-vector-store-readiness.json",
            required=True,
        ),
        _json_check(
            check_id="phase6_qdrant_backup_restore_smoke_present",
            path=base_dir
            / "docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json",
            required=True,
        ),
        _json_check(
            check_id="phase6_private_network_promotion_readiness_present",
            path=base_dir
            / "docs/operations/private-network-promotion/"
            "phase6-qdrant-bge-private-network-promotion-readiness.json",
            required=True,
        ),
        _json_check(
            check_id="phase6_private_network_promotion_smoke_present",
            path=base_dir
            / "docs/smoke/private-network-promotion/"
            "phase6-qdrant-bge-private-network-promotion-smoke.json",
            required=True,
        ),
        _readiness_gate_visibility_check(readiness_path),
    ]
    passed = sum(1 for check in checks if check["passed"] is True)
    total = len(checks)
    failed = total - passed
    status = "ready" if failed == 0 else "review"
    return Phase3HybridRuntimePromotionDecisionSmokeReport(
        id=PHASE3_HYBRID_RUNTIME_PROMOTION_DECISION_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_runtime_defaults",
        checks=checks,
        summary={"total_checks": total, "passed_checks": passed, "failed_checks": failed},
        notes=[
            "This smoke validates hybrid runtime promotion decision evidence-chain completeness only.",
            "It does not run retrieval execution, model download, deployment automation, or runtime promotion.",
            "Use it before final Phase 3 hybrid runtime promotion decision review.",
        ],
    )


def phase3_hybrid_runtime_promotion_decision_smoke_report_to_dict(
    report: Phase3HybridRuntimePromotionDecisionSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_hybrid_runtime_promotion_decision_smoke_markdown(
    report: Phase3HybridRuntimePromotionDecisionSmokeReport,
) -> str:
    lines = [
        "# Phase 3 Hybrid Runtime Promotion Decision Smoke",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Checks",
        "",
        "| Check | Passed | Summary | Recommended Action |",
        "|---|---|---|---|",
    ]
    for check in report.checks:
        lines.append(
            f"| `{check['id']}` | `{check['passed']}` | {check['summary']} | `{check['recommended_action']}` |"
        )
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Total checks: `{report.summary['total_checks']}`",
            f"- Passed checks: `{report.summary['passed_checks']}`",
            f"- Failed checks: `{report.summary['failed_checks']}`",
            "",
            "## Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase3_hybrid_runtime_promotion_decision_smoke_report(
    output_dir: Path = Path("docs/smoke/hybrid-runtime-promotion"),
    *,
    base_dir: Path = Path("."),
) -> Phase3HybridRuntimePromotionDecisionSmokeReport:
    report = build_phase3_hybrid_runtime_promotion_decision_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3-hybrid-runtime-promotion-decision-smoke.json"
    markdown_path = output_dir / "phase3-hybrid-runtime-promotion-decision-smoke.md"
    exported = Phase3HybridRuntimePromotionDecisionSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        checks=report.checks,
        summary=report.summary,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_hybrid_runtime_promotion_decision_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_hybrid_runtime_promotion_decision_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _file_check(*, check_id: str, path: Path, required: bool) -> dict[str, Any]:
    present = path.exists()
    return {
        "id": check_id,
        "path": str(path),
        "required": required,
        "passed": present,
        "summary": "present" if present else "missing",
        "recommended_action": "no_action_required" if present else "restore_required_evidence",
    }


def _json_check(*, check_id: str, path: Path, required: bool) -> dict[str, Any]:
    if not path.exists():
        return {
            "id": check_id,
            "path": str(path),
            "required": required,
            "passed": False,
            "summary": "missing",
            "recommended_action": "regenerate_required_evidence",
        }
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return {
            "id": check_id,
            "path": str(path),
            "required": required,
            "passed": True,
            "summary": "json_parse_ok",
            "recommended_action": "no_action_required",
        }
    except json.JSONDecodeError as error:
        return {
            "id": check_id,
            "path": str(path),
            "required": required,
            "passed": False,
            "summary": f"invalid_json: {error.msg}",
            "recommended_action": "regenerate_required_evidence",
        }


def _readiness_gate_visibility_check(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "id": "hybrid_runtime_promotion_readiness_gate_visibility",
            "path": str(path),
            "required": True,
            "passed": False,
            "summary": "readiness_missing",
            "recommended_action": "regenerate_phase3_hybrid_runtime_promotion_decision_readiness",
        }
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return {
            "id": "hybrid_runtime_promotion_readiness_gate_visibility",
            "path": str(path),
            "required": True,
            "passed": False,
            "summary": f"invalid_json: {error.msg}",
            "recommended_action": "regenerate_phase3_hybrid_runtime_promotion_decision_readiness",
        }
    summary = payload.get("summary") if isinstance(payload, dict) else None
    open_gate_ids = summary.get("open_gate_ids") if isinstance(summary, dict) else None
    decision = payload.get("decision") if isinstance(payload, dict) else None
    review_state = payload.get("review_state") if isinstance(payload, dict) else None
    passed = (
        isinstance(open_gate_ids, list)
        and decision in {
            "keep_runtime_defaults",
            "promote_to_candidate_default",
            "blocked",
        }
        and review_state in {"ready", "review", "blocked"}
    )
    return {
        "id": "hybrid_runtime_promotion_readiness_gate_visibility",
        "path": str(path),
        "required": True,
        "passed": passed,
        "summary": (
            f"decision={decision}; review_state={review_state}; "
            f"open_gate_count={len(open_gate_ids) if isinstance(open_gate_ids, list) else 0}"
        ),
        "recommended_action": (
            "no_action_required"
            if passed
            else "regenerate_phase3_hybrid_runtime_promotion_decision_readiness"
        ),
    }
