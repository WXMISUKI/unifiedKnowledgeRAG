import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE3_HYBRID_RUNTIME_PROMOTION_DECISION_READINESS_ID = (
    "phase3-hybrid-runtime-promotion-decision-readiness-v1"
)

CONTRACT_PATH = Path(
    "docs/benchmark/chinese-seed/hybrid-runtime-promotion/"
    "phase3-hybrid-runtime-promotion-decision-contract.md"
)
PHASE3_READINESS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-promotion-readiness/"
    "phase3-retrieval-promotion-readiness.json"
)
PHASE3_RUNTIME_DIAGNOSTICS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/"
    "phase3-candidate-runtime-diagnostics.json"
)
PHASE3_LATENCY_DIAGNOSTICS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/"
    "phase3-candidate-latency-resource-diagnostics.json"
)
PHASE3_HYBRID_CALIBRATION_PATH = Path(
    "docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/"
    "phase3-hybrid-fusion-threshold-calibration.json"
)
PHASE3_HYBRID_FP_FN_SMOKE_PATH = Path(
    "docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.json"
)
PHASE3_AGGREGATION_RELATION_SMOKE_PATH = Path(
    "docs/smoke/aggregation-relation-negative-control/"
    "phase3-aggregation-relation-negative-control-smoke.json"
)
PHASE6_BGE_ARTIFACT_READINESS_PATH = Path(
    "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json"
)
PHASE6_BGE_COMPARISON_DIAGNOSTICS_PATH = Path(
    "docs/operations/bge-m3-comparison-readiness/"
    "phase6-bge-m3-vs-mock-fixture-diagnostics.json"
)
PHASE6_BGE_COMPARISON_SMOKE_PATH = Path(
    "docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json"
)
PHASE6_QDRANT_READINESS_PATH = Path(
    "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json"
)
PHASE6_QDRANT_BACKUP_SMOKE_PATH = Path(
    "docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json"
)
PHASE6_PRIVATE_NETWORK_READINESS_PATH = Path(
    "docs/operations/private-network-promotion/"
    "phase6-qdrant-bge-private-network-promotion-readiness.json"
)
PHASE6_PRIVATE_NETWORK_SMOKE_PATH = Path(
    "docs/smoke/private-network-promotion/"
    "phase6-qdrant-bge-private-network-promotion-smoke.json"
)
DEPLOYED_SMOKE_PATH = Path(
    "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
)


@dataclass(frozen=True)
class Phase3HybridRuntimePromotionSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase3HybridRuntimePromotionDecisionReadinessReport:
    id: str
    generated_at: str
    status: str
    review_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase3HybridRuntimePromotionSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase3_hybrid_runtime_promotion_decision_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase3HybridRuntimePromotionDecisionReadinessReport:
    signals = [
        _contract_signal(base_dir),
        _required_artifact_signal(
            id="phase3_retrieval_promotion_readiness",
            path=PHASE3_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase3_retrieval_promotion_readiness",
        ),
        _required_artifact_signal(
            id="phase3_candidate_runtime_diagnostics",
            path=PHASE3_RUNTIME_DIAGNOSTICS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase3_candidate_runtime_diagnostics",
        ),
        _required_artifact_signal(
            id="phase3_candidate_latency_resource_diagnostics",
            path=PHASE3_LATENCY_DIAGNOSTICS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase3_candidate_latency_resource_diagnostics",
        ),
        _required_artifact_signal(
            id="phase3_hybrid_fusion_threshold_calibration",
            path=PHASE3_HYBRID_CALIBRATION_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase3_hybrid_fusion_threshold_calibration",
        ),
        _required_artifact_signal(
            id="phase3_hybrid_cross_case_fp_fn_smoke",
            path=PHASE3_HYBRID_FP_FN_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase3_hybrid_cross_case_fp_fn_smoke",
        ),
        _required_artifact_signal(
            id="phase3_aggregation_relation_negative_control_smoke",
            path=PHASE3_AGGREGATION_RELATION_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase3_aggregation_relation_negative_control_smoke",
        ),
        _required_artifact_signal(
            id="phase6_bge_m3_artifact_readiness",
            path=PHASE6_BGE_ARTIFACT_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_bge_m3_artifact_readiness",
        ),
        _required_artifact_signal(
            id="phase6_bge_m3_vs_mock_fixture_diagnostics",
            path=PHASE6_BGE_COMPARISON_DIAGNOSTICS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_bge_m3_vs_mock_fixture_diagnostics",
        ),
        _required_artifact_signal(
            id="phase6_bge_m3_comparison_smoke",
            path=PHASE6_BGE_COMPARISON_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_bge_m3_comparison_smoke",
        ),
        _required_artifact_signal(
            id="phase6_qdrant_vector_store_readiness",
            path=PHASE6_QDRANT_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_qdrant_vector_store_readiness",
        ),
        _required_artifact_signal(
            id="phase6_qdrant_backup_restore_smoke",
            path=PHASE6_QDRANT_BACKUP_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_qdrant_backup_restore_smoke",
        ),
        _required_artifact_signal(
            id="phase6_qdrant_bge_private_network_promotion_readiness",
            path=PHASE6_PRIVATE_NETWORK_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_qdrant_bge_private_network_promotion_readiness",
        ),
        _required_artifact_signal(
            id="phase6_qdrant_bge_private_network_promotion_smoke",
            path=PHASE6_PRIVATE_NETWORK_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_qdrant_bge_private_network_promotion_smoke",
        ),
        _optional_artifact_signal(
            id="deployed_provider_smoke",
            path=DEPLOYED_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="run_deployed_provider_smoke_after_deployment",
        ),
    ]

    required_blocked = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    required_review = any(
        signal.required and signal.status == "review" for signal in signals
    )
    optional_review = any(
        (not signal.required) and signal.status in {"review", "blocked"}
        for signal in signals
    )

    if required_blocked:
        status = "blocked"
        review_state = "blocked"
        decision = "blocked"
    elif required_review or optional_review:
        status = "review"
        review_state = "review"
        decision = "keep_runtime_defaults"
    else:
        status = "ready"
        review_state = "ready"
        decision = "promote_to_candidate_default"

    return Phase3HybridRuntimePromotionDecisionReadinessReport(
        id=PHASE3_HYBRID_RUNTIME_PROMOTION_DECISION_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        review_state=review_state,
        decision=decision,
        summary=_summary(signals),
        signals=signals,
        notes=[
            "This report is local read-only promotion review evidence.",
            "It consolidates Phase 3 and Phase 6 bridge prerequisites for final hybrid runtime promotion review.",
            "Unless all required gates are ready, keep_runtime_defaults is the expected decision.",
        ],
    )


def phase3_hybrid_runtime_promotion_decision_readiness_report_to_dict(
    report: Phase3HybridRuntimePromotionDecisionReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_hybrid_runtime_promotion_decision_readiness_markdown(
    report: Phase3HybridRuntimePromotionDecisionReadinessReport,
) -> str:
    lines = [
        "# Phase 3 Hybrid Runtime Promotion Decision Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Review State: `{report.review_state}`",
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


def export_phase3_hybrid_runtime_promotion_decision_readiness_report(
    output_dir: Path = Path("docs/benchmark/chinese-seed/hybrid-runtime-promotion"),
    *,
    base_dir: Path = Path("."),
) -> Phase3HybridRuntimePromotionDecisionReadinessReport:
    report = build_phase3_hybrid_runtime_promotion_decision_readiness_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3-hybrid-runtime-promotion-decision-readiness.json"
    markdown_path = output_dir / "phase3-hybrid-runtime-promotion-decision-readiness.md"
    exported = Phase3HybridRuntimePromotionDecisionReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        review_state=report.review_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_hybrid_runtime_promotion_decision_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_hybrid_runtime_promotion_decision_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _contract_signal(base_dir: Path) -> Phase3HybridRuntimePromotionSignal:
    path = base_dir / CONTRACT_PATH
    if path.exists():
        return Phase3HybridRuntimePromotionSignal(
            id="phase3_hybrid_runtime_promotion_decision_contract",
            required=True,
            status="ready",
            summary="contract_present=true",
            recommended_action="no_action_required",
            evidence_path=str(CONTRACT_PATH),
        )
    return Phase3HybridRuntimePromotionSignal(
        id="phase3_hybrid_runtime_promotion_decision_contract",
        required=True,
        status="blocked",
        summary="contract_present=false",
        recommended_action="restore_hybrid_runtime_promotion_decision_contract",
        evidence_path=str(CONTRACT_PATH),
    )


def _required_artifact_signal(
    *,
    id: str,
    path: Path,
    base_dir: Path,
    missing_action: str,
) -> Phase3HybridRuntimePromotionSignal:
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
) -> Phase3HybridRuntimePromotionSignal:
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
) -> Phase3HybridRuntimePromotionSignal:
    full_path = base_dir / path
    if not full_path.exists():
        return Phase3HybridRuntimePromotionSignal(
            id=id,
            required=required,
            status="blocked" if required else "review",
            summary="artifact_present=false",
            recommended_action=missing_action,
            evidence_path=str(path),
        )
    payload = _read_json_if_present(full_path)
    status = _normalize_status(_dict_value(payload, "status", "review"))
    decision = _dict_value(payload, "decision", "n/a")
    summary = f"artifact_present=true; status={status}; decision={decision}"
    return Phase3HybridRuntimePromotionSignal(
        id=id,
        required=required,
        status=status,
        summary=summary,
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(path),
    )


def _summary(signals: list[Phase3HybridRuntimePromotionSignal]) -> dict[str, Any]:
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
