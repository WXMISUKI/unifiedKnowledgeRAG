import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE6_QDRANT_BGE_PRIVATE_NETWORK_PROMOTION_SMOKE_ID = (
    "phase6-qdrant-bge-private-network-promotion-smoke-v1"
)


@dataclass(frozen=True)
class Phase6PrivateNetworkPromotionSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    checks: list[dict[str, Any]]
    summary: dict[str, int]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase6_qdrant_bge_private_network_promotion_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase6PrivateNetworkPromotionSmokeReport:
    checks = [
        _file_check(
            check_id="private_network_review_contract_present",
            path=base_dir
            / "docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-review-contract.md",
            required=True,
        ),
        _json_check(
            check_id="private_network_promotion_readiness_present",
            path=base_dir
            / "docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.json",
            required=True,
        ),
        _json_check(
            check_id="qdrant_vector_store_readiness_present",
            path=base_dir
            / "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json",
            required=True,
        ),
        _json_check(
            check_id="qdrant_backup_restore_smoke_present",
            path=base_dir
            / "docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json",
            required=True,
        ),
        _json_check(
            check_id="bge_artifact_readiness_present",
            path=base_dir
            / "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json",
            required=True,
        ),
        _json_check(
            check_id="bge_comparison_diagnostics_present",
            path=base_dir
            / "docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="bge_comparison_smoke_present",
            path=base_dir
            / "docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_runtime_diagnostics_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_latency_diagnostics_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="deployment_readiness_present",
            path=base_dir / "docs/operations/deployment-readiness/deployment-readiness.json",
            required=True,
        ),
    ]
    passed = sum(1 for check in checks if check["passed"] is True)
    total = len(checks)
    failed = total - passed
    status = "ready" if failed == 0 else "review"
    return Phase6PrivateNetworkPromotionSmokeReport(
        id=PHASE6_QDRANT_BGE_PRIVATE_NETWORK_PROMOTION_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_runtime_defaults",
        checks=checks,
        summary={"total_checks": total, "passed_checks": passed, "failed_checks": failed},
        notes=[
            "This smoke report validates private-network promotion evidence-chain completeness only.",
            "It does not run retrieval execution, model download, deployment automation, or runtime promotion.",
            "Use it before manual private-network candidate promotion review.",
        ],
    )


def phase6_qdrant_bge_private_network_promotion_smoke_report_to_dict(
    report: Phase6PrivateNetworkPromotionSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase6_qdrant_bge_private_network_promotion_smoke_markdown(
    report: Phase6PrivateNetworkPromotionSmokeReport,
) -> str:
    lines = [
        "# Phase 6 Private-Network Promotion Smoke",
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


def export_phase6_qdrant_bge_private_network_promotion_smoke_report(
    output_dir: Path = Path("docs/smoke/private-network-promotion"),
    *,
    base_dir: Path = Path("."),
) -> Phase6PrivateNetworkPromotionSmokeReport:
    report = build_phase6_qdrant_bge_private_network_promotion_smoke_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = (
        output_dir / "phase6-qdrant-bge-private-network-promotion-smoke.json"
    )
    markdown_path = (
        output_dir / "phase6-qdrant-bge-private-network-promotion-smoke.md"
    )
    exported = Phase6PrivateNetworkPromotionSmokeReport(
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
            phase6_qdrant_bge_private_network_promotion_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase6_qdrant_bge_private_network_promotion_smoke_markdown(exported),
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
