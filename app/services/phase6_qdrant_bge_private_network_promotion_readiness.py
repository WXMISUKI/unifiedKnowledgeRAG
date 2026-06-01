import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE6_QDRANT_BGE_PRIVATE_NETWORK_PROMOTION_READINESS_ID = (
    "phase6-qdrant-bge-private-network-promotion-readiness-v1"
)

CONTRACT_PATH = Path(
    "docs/operations/private-network-promotion/"
    "phase6-qdrant-bge-private-network-promotion-review-contract.md"
)
QDRANT_READINESS_PATH = Path(
    "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json"
)
QDRANT_BACKUP_SMOKE_PATH = Path(
    "docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json"
)
BGE_ARTIFACT_READINESS_PATH = Path(
    "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json"
)
BGE_COMPARISON_DIAGNOSTICS_PATH = Path(
    "docs/operations/bge-m3-comparison-readiness/"
    "phase6-bge-m3-vs-mock-fixture-diagnostics.json"
)
BGE_COMPARISON_SMOKE_PATH = Path(
    "docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json"
)
PHASE3_RUNTIME_DIAGNOSTICS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/"
    "phase3-candidate-runtime-diagnostics.json"
)
PHASE3_LATENCY_DIAGNOSTICS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/"
    "phase3-candidate-latency-resource-diagnostics.json"
)
PHASE3_FP_FN_REVIEW_PATH = Path(
    "docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json"
)
PHASE3_HYBRID_CALIBRATION_PATH = Path(
    "docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/"
    "phase3-hybrid-fusion-threshold-calibration.json"
)
DEPLOYMENT_READINESS_PATH = Path(
    "docs/operations/deployment-readiness/deployment-readiness.json"
)
DEPLOYED_SMOKE_PATH = Path(
    "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
)


@dataclass(frozen=True)
class Phase6PrivateNetworkPromotionSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase6QdrantBgePrivateNetworkPromotionReadinessReport:
    id: str
    generated_at: str
    status: str
    promotion_review_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase6PrivateNetworkPromotionSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase6_qdrant_bge_private_network_promotion_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase6QdrantBgePrivateNetworkPromotionReadinessReport:
    signals = [
        _contract_signal(base_dir),
        _required_artifact_signal(
            id="qdrant_vector_store_readiness",
            path=QDRANT_READINESS_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase6_qdrant_vector_store_readiness",
        ),
        _required_artifact_signal(
            id="qdrant_backup_restore_smoke",
            path=QDRANT_BACKUP_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase6_qdrant_backup_restore_smoke",
        ),
        _required_artifact_signal(
            id="bge_m3_artifact_readiness",
            path=BGE_ARTIFACT_READINESS_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase6_bge_m3_artifact_readiness",
        ),
        _required_artifact_signal(
            id="bge_m3_comparison_diagnostics",
            path=BGE_COMPARISON_DIAGNOSTICS_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase6_bge_m3_comparison_diagnostics",
        ),
        _required_artifact_signal(
            id="bge_m3_comparison_smoke",
            path=BGE_COMPARISON_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase6_bge_m3_comparison_smoke",
        ),
        _required_artifact_signal(
            id="phase3_runtime_diagnostics",
            path=PHASE3_RUNTIME_DIAGNOSTICS_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase3_runtime_diagnostics",
        ),
        _required_artifact_signal(
            id="phase3_latency_diagnostics",
            path=PHASE3_LATENCY_DIAGNOSTICS_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase3_latency_diagnostics",
        ),
        _required_artifact_signal(
            id="deployment_readiness",
            path=DEPLOYMENT_READINESS_PATH,
            base_dir=base_dir,
            missing_action="refresh_deployment_readiness",
        ),
        _optional_artifact_signal(
            id="phase3_fp_fn_review",
            path=PHASE3_FP_FN_REVIEW_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase3_fp_fn_review",
        ),
        _optional_artifact_signal(
            id="phase3_hybrid_calibration",
            path=PHASE3_HYBRID_CALIBRATION_PATH,
            base_dir=base_dir,
            missing_action="refresh_phase3_hybrid_calibration",
        ),
        _optional_artifact_signal(
            id="deployed_provider_smoke",
            path=DEPLOYED_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="run_deployed_provider_smoke_after_deployment",
        ),
    ]

    required_missing = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    review_present = any(signal.status == "review" for signal in signals)
    optional_blocked = any((not signal.required) and signal.status == "blocked" for signal in signals)

    if required_missing:
        status = "blocked"
        promotion_review_state = "blocked"
    elif review_present or optional_blocked:
        status = "review"
        promotion_review_state = "review"
    else:
        status = "ready"
        promotion_review_state = "ready_for_private_network_candidate"

    return Phase6QdrantBgePrivateNetworkPromotionReadinessReport(
        id=PHASE6_QDRANT_BGE_PRIVATE_NETWORK_PROMOTION_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        promotion_review_state=promotion_review_state,
        decision="keep_runtime_defaults",
        summary=_summary(signals),
        signals=signals,
        notes=[
            "This report is local read-only promotion review evidence.",
            "Use it to decide whether private-network candidate review can proceed.",
            "Even when ready_for_private_network_candidate, runtime defaults remain unchanged until separate promotion approval.",
        ],
    )


def phase6_qdrant_bge_private_network_promotion_readiness_report_to_dict(
    report: Phase6QdrantBgePrivateNetworkPromotionReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase6_qdrant_bge_private_network_promotion_readiness_markdown(
    report: Phase6QdrantBgePrivateNetworkPromotionReadinessReport,
) -> str:
    lines = [
        "# Phase 6 Qdrant+BGE Private-Network Promotion Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Promotion Review State: `{report.promotion_review_state}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Signals | `{report.summary['total_signals']}` |",
        f"| Required Signals | `{report.summary['required_signals']}` |",
        f"| Ready Signals | `{report.summary['ready_signals']}` |",
        f"| Review Signals | `{report.summary['review_signals']}` |",
        f"| Blocked Signals | `{report.summary['blocked_signals']}` |",
        f"| Open Gate IDs | `{json.dumps(report.summary['open_gate_ids'])}` |",
        "",
        "## Signals",
        "",
        "| Signal | Required | Status | Summary | Recommended Action |",
        "|---|---|---|---|---|",
    ]
    for signal in report.signals:
        lines.append(
            f"| `{signal.id}` | `{signal.required}` | `{signal.status}` | "
            f"{signal.summary} | `{signal.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase6_qdrant_bge_private_network_promotion_readiness_report(
    output_dir: Path = Path("docs/operations/private-network-promotion"),
    *,
    base_dir: Path = Path("."),
) -> Phase6QdrantBgePrivateNetworkPromotionReadinessReport:
    report = build_phase6_qdrant_bge_private_network_promotion_readiness_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = (
        output_dir / "phase6-qdrant-bge-private-network-promotion-readiness.json"
    )
    markdown_path = (
        output_dir / "phase6-qdrant-bge-private-network-promotion-readiness.md"
    )
    exported = Phase6QdrantBgePrivateNetworkPromotionReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        promotion_review_state=report.promotion_review_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase6_qdrant_bge_private_network_promotion_readiness_report_to_dict(
                exported
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase6_qdrant_bge_private_network_promotion_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _contract_signal(base_dir: Path) -> Phase6PrivateNetworkPromotionSignal:
    path = base_dir / CONTRACT_PATH
    if path.exists():
        return Phase6PrivateNetworkPromotionSignal(
            id="private_network_review_contract",
            required=True,
            status="ready",
            summary="contract_present=true",
            recommended_action="no_action_required",
            evidence_path=str(CONTRACT_PATH),
        )
    return Phase6PrivateNetworkPromotionSignal(
        id="private_network_review_contract",
        required=True,
        status="blocked",
        summary="contract_present=false",
        recommended_action="restore_private_network_review_contract",
        evidence_path=str(CONTRACT_PATH),
    )


def _required_artifact_signal(
    *,
    id: str,
    path: Path,
    base_dir: Path,
    missing_action: str,
) -> Phase6PrivateNetworkPromotionSignal:
    return _artifact_signal(
        id=id,
        required=True,
        path=path,
        base_dir=base_dir,
        missing_action=missing_action,
    )


def _optional_artifact_signal(
    *,
    id: str,
    path: Path,
    base_dir: Path,
    missing_action: str,
) -> Phase6PrivateNetworkPromotionSignal:
    return _artifact_signal(
        id=id,
        required=False,
        path=path,
        base_dir=base_dir,
        missing_action=missing_action,
    )


def _artifact_signal(
    *,
    id: str,
    required: bool,
    path: Path,
    base_dir: Path,
    missing_action: str,
) -> Phase6PrivateNetworkPromotionSignal:
    full_path = base_dir / path
    if not full_path.exists():
        return Phase6PrivateNetworkPromotionSignal(
            id=id,
            required=required,
            status="blocked" if required else "review",
            summary="artifact_present=false",
            recommended_action=missing_action,
            evidence_path=str(path),
        )
    payload = _read_json_if_present(full_path)
    status_value = _normalize_status(_dict_value(payload, "status", "review"))
    summary = (
        f"artifact_present=true; status={status_value}; "
        f"decision={_dict_value(payload, 'decision', 'n/a')}"
    )
    if required:
        recommended_action = (
            "no_action_required" if status_value == "ready" else "review_evidence_notes"
        )
    else:
        recommended_action = (
            "no_action_required" if status_value == "ready" else "review_evidence_notes"
        )
    return Phase6PrivateNetworkPromotionSignal(
        id=id,
        required=required,
        status=status_value,
        summary=summary,
        recommended_action=recommended_action,
        evidence_path=str(path),
    )


def _summary(signals: list[Phase6PrivateNetworkPromotionSignal]) -> dict[str, Any]:
    return {
        "total_signals": len(signals),
        "required_signals": sum(1 for signal in signals if signal.required),
        "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
        "review_signals": sum(1 for signal in signals if signal.status == "review"),
        "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
        "open_gate_ids": [
            signal.id for signal in signals if signal.status in {"review", "blocked"}
        ],
    }


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "review"


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)
