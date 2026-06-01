import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE3_HYBRID_FUSION_THRESHOLD_CALIBRATION_ID = (
    "phase3-hybrid-fusion-threshold-calibration-v1"
)
HYBRID_EXACT_TERM_PATH = Path(
    "docs/benchmark/chinese-seed/exact-term-candidates/"
    "qdrant-bge-m3-hybrid-exact-term-smoke.json"
)
HYBRID_EMPTY_STRESS_PATH = Path(
    "docs/benchmark/chinese-seed/hybrid-empty-stress/"
    "qdrant-bge-m3-hybrid-empty-stress.json"
)
HYBRID_GATE_PATHS = [
    Path(
        "docs/benchmark/chinese-seed/hybrid-gating-candidates/"
        "qdrant-bge-m3-hybrid-exact-identifier-gate.json"
    ),
    Path(
        "docs/benchmark/chinese-seed/hybrid-gating-candidates-expanded/"
        "qdrant-bge-m3-hybrid-exact-identifier-gate.json"
    ),
    Path(
        "docs/benchmark/chinese-seed/noisy-identifier-gating-candidates/"
        "qdrant-bge-m3-hybrid-alias-identifier-gate.json"
    ),
    Path(
        "docs/benchmark/chinese-seed/split-chunk-gating-candidates/"
        "qdrant-bge-m3-hybrid-exact-identifier-gate.json"
    ),
]
THRESHOLD_RECOMMENDATION_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-candidates/"
    "qdrant-bge-m3-threshold-recommendation.json"
)
THRESHOLD_SWEEP_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-candidates/"
    "qdrant-bge-m3-threshold-sweep.json"
)
PHASE3_FP_FN_REVIEW_PATH = Path(
    "docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json"
)
DEPLOYMENT_READINESS_PATH = Path("docs/operations/deployment-readiness/deployment-readiness.json")


@dataclass(frozen=True)
class Phase3HybridCalibrationSignal:
    id: str
    status: str
    summary: str
    recommended_action: str
    evidence_path: str | None = None


@dataclass(frozen=True)
class Phase3HybridFusionThresholdCalibrationReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    calibration: dict[str, Any]
    signals: list[Phase3HybridCalibrationSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase3_hybrid_fusion_threshold_calibration_report(
    *,
    base_dir: Path = Path("."),
) -> Phase3HybridFusionThresholdCalibrationReport:
    hybrid_exact_term = _read_json_if_present(base_dir / HYBRID_EXACT_TERM_PATH)
    hybrid_empty_stress = _read_json_if_present(base_dir / HYBRID_EMPTY_STRESS_PATH)
    hybrid_gate_payloads = [
        _read_json_if_present(base_dir / gate_path)
        for gate_path in HYBRID_GATE_PATHS
    ]
    threshold_recommendation = _read_json_if_present(base_dir / THRESHOLD_RECOMMENDATION_PATH)
    threshold_sweep = _read_json_if_present(base_dir / THRESHOLD_SWEEP_PATH)
    fp_fn_review = _read_json_if_present(base_dir / PHASE3_FP_FN_REVIEW_PATH)
    deployment_readiness = _read_json_if_present(base_dir / DEPLOYMENT_READINESS_PATH)

    calibration = _build_calibration(
        hybrid_exact_term=hybrid_exact_term,
        threshold_recommendation=threshold_recommendation,
        threshold_sweep=threshold_sweep,
        deployment_readiness=deployment_readiness,
    )
    signals = _build_signals(
        hybrid_exact_term=hybrid_exact_term,
        hybrid_empty_stress=hybrid_empty_stress,
        hybrid_gate_payloads=hybrid_gate_payloads,
        threshold_recommendation=threshold_recommendation,
        threshold_sweep=threshold_sweep,
        fp_fn_review=fp_fn_review,
        deployment_readiness=deployment_readiness,
        calibration=calibration,
    )
    summary = _summary(signals)
    return Phase3HybridFusionThresholdCalibrationReport(
        id=PHASE3_HYBRID_FUSION_THRESHOLD_CALIBRATION_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(signals),
        decision="keep_runtime_defaults",
        summary=summary,
        calibration=calibration,
        signals=signals,
        notes=[
            "This report is local, read-only candidate calibration evidence for Phase 3 promotion review.",
            "Hybrid retrieval in these artifacts uses RRF fusion and score filtering is disabled for fusion scores.",
            "Dense threshold recommendations and runtime thresholds are not direct promotion instructions for hybrid RRF runtime defaults.",
        ],
    )


def phase3_hybrid_fusion_threshold_calibration_report_to_dict(
    report: Phase3HybridFusionThresholdCalibrationReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_hybrid_fusion_threshold_calibration_markdown(
    report: Phase3HybridFusionThresholdCalibrationReport,
) -> str:
    lines = [
        "# Phase 3 Hybrid Fusion Threshold Calibration",
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
        f"| Total Signals | `{report.summary['total_signals']}` |",
        f"| Ready Signals | `{report.summary['ready_signals']}` |",
        f"| Review Signals | `{report.summary['review_signals']}` |",
        f"| Blocked Signals | `{report.summary['blocked_signals']}` |",
        f"| Open Signal IDs | `{json.dumps(report.summary['open_signal_ids'])}` |",
        "",
        "## Calibration",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Fusion Mode | `{report.calibration['fusion_mode']}` |",
        f"| Score Filter Mode | `{report.calibration['score_filter_mode']}` |",
        f"| Dense Selected Threshold | `{report.calibration['selected_dense_threshold']}` |",
        f"| Runtime Threshold | `{report.calibration['runtime_threshold']}` |",
        f"| Threshold Delta | `{report.calibration['threshold_delta']}` |",
        f"| Sweep Threshold Count | `{report.calibration['sweep_threshold_count']}` |",
        f"| Sweep Best Empty Handling Rate | `{report.calibration['sweep_best_empty_handling_rate']}` |",
        f"| Hybrid Exact-Term Hit Rate | `{report.calibration['hybrid_exact_term_hit_rate']}` |",
        f"| Hybrid Empty-Stress Empty Handling Rate | `{report.calibration['hybrid_empty_stress_empty_handling_rate']}` |",
        "",
        "## Signals",
        "",
        "| Signal | Status | Summary | Recommended Action |",
        "|---|---|---|---|",
    ]
    for signal in report.signals:
        lines.append(
            f"| `{signal.id}` | `{signal.status}` | {signal.summary} | "
            f"`{signal.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase3_hybrid_fusion_threshold_calibration_report(
    output_dir: Path = Path(
        "docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration"
    ),
    *,
    base_dir: Path = Path("."),
) -> Phase3HybridFusionThresholdCalibrationReport:
    report = build_phase3_hybrid_fusion_threshold_calibration_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3-hybrid-fusion-threshold-calibration.json"
    markdown_path = output_dir / "phase3-hybrid-fusion-threshold-calibration.md"
    exported = Phase3HybridFusionThresholdCalibrationReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        calibration=report.calibration,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_hybrid_fusion_threshold_calibration_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_hybrid_fusion_threshold_calibration_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_calibration(
    *,
    hybrid_exact_term: dict[str, Any] | None,
    threshold_recommendation: dict[str, Any] | None,
    threshold_sweep: dict[str, Any] | None,
    deployment_readiness: dict[str, Any] | None,
) -> dict[str, Any]:
    metadata = _dict_value(hybrid_exact_term, "metadata", {})
    exact_term_summary = _nested_summary(hybrid_exact_term)
    recommendation_threshold = _float_value(
        _dict_value(threshold_recommendation, "selected_threshold", None),
        fallback=0.0,
    )
    runtime_config = _dict_value(deployment_readiness, "runtime_config", {})
    runtime_threshold = _float_value(
        _dict_value(runtime_config, "rag_score_threshold", None),
        fallback=0.0,
    )
    sweep_rows = _dict_value(threshold_sweep, "summary", [])
    if not isinstance(sweep_rows, list):
        sweep_rows = []
    sweep_best_empty = max(
        (
            _float_value(_dict_value(row, "empty_handling_rate", None), fallback=0.0)
            for row in sweep_rows
            if isinstance(row, dict)
        ),
        default=0.0,
    )
    return {
        "fusion_mode": _dict_value(metadata, "fusion", "unknown"),
        "score_filter_mode": _dict_value(metadata, "score_filter", "unknown"),
        "selected_dense_threshold": recommendation_threshold,
        "runtime_threshold": runtime_threshold,
        "threshold_delta": round(recommendation_threshold - runtime_threshold, 4),
        "sweep_threshold_count": len(sweep_rows),
        "sweep_best_empty_handling_rate": round(sweep_best_empty, 4),
        "hybrid_exact_term_hit_rate": round(
            _float_value(_dict_value(exact_term_summary, "hit_rate", None), fallback=0.0),
            4,
        ),
        "hybrid_exact_term_total_cases": _int_value(
            _dict_value(exact_term_summary, "total_cases", None),
            fallback=0,
        ),
        "hybrid_empty_stress_empty_handling_rate": 0.0,
    }


def _build_signals(
    *,
    hybrid_exact_term: dict[str, Any] | None,
    hybrid_empty_stress: dict[str, Any] | None,
    hybrid_gate_payloads: list[dict[str, Any] | None],
    threshold_recommendation: dict[str, Any] | None,
    threshold_sweep: dict[str, Any] | None,
    fp_fn_review: dict[str, Any] | None,
    deployment_readiness: dict[str, Any] | None,
    calibration: dict[str, Any],
) -> list[Phase3HybridCalibrationSignal]:
    signals: list[Phase3HybridCalibrationSignal] = []
    exact_term_summary = _nested_summary(hybrid_exact_term)
    exact_term_hit_rate = _float_value(
        _dict_value(exact_term_summary, "hit_rate", None),
        fallback=0.0,
    )
    signals.append(
        _signal(
            id="hybrid_exact_term_positive_control",
            ready=hybrid_exact_term is not None and exact_term_hit_rate >= 1.0,
            summary=(
                f"hit_rate={exact_term_hit_rate:.4f}; "
                f"total_cases={_int_value(_dict_value(exact_term_summary, 'total_cases', None), fallback=0)}"
            ),
            ready_action="no_action_required",
            review_action="regenerate_hybrid_exact_term_evidence",
            evidence_path=str(HYBRID_EXACT_TERM_PATH),
        )
    )
    empty_summary = _nested_summary(hybrid_empty_stress)
    empty_handling_rate = _float_value(
        _dict_value(empty_summary, "empty_handling_rate", None),
        fallback=0.0,
    )
    calibration["hybrid_empty_stress_empty_handling_rate"] = round(empty_handling_rate, 4)
    signals.append(
        _signal(
            id="hybrid_empty_stress_negative_control",
            ready=hybrid_empty_stress is not None and empty_handling_rate >= 1.0,
            summary=(
                f"empty_handling_rate={empty_handling_rate:.4f}; "
                f"total_cases={_int_value(_dict_value(empty_summary, 'total_cases', None), fallback=0)}"
            ),
            ready_action="no_action_required",
            review_action="review_empty_false_positive_risk",
            evidence_path=str(HYBRID_EMPTY_STRESS_PATH),
        )
    )
    present_gate_count = sum(1 for payload in hybrid_gate_payloads if payload is not None)
    signals.append(
        _signal(
            id="hybrid_gate_coverage_bundle",
            ready=present_gate_count == len(HYBRID_GATE_PATHS),
            summary=f"present_gate_artifacts={present_gate_count}/{len(HYBRID_GATE_PATHS)}",
            ready_action="no_action_required",
            review_action="regenerate_hybrid_gate_evidence_bundle",
            evidence_path="; ".join(str(path) for path in HYBRID_GATE_PATHS),
        )
    )
    selected_dense_threshold = _float_value(
        _dict_value(threshold_recommendation, "selected_threshold", None),
        fallback=0.0,
    )
    thresholds = _dict_value(threshold_sweep, "thresholds", [])
    threshold_count = len(thresholds) if isinstance(thresholds, list) else 0
    signals.append(
        _signal(
            id="dense_threshold_sweep_context",
            ready=threshold_recommendation is not None and threshold_sweep is not None,
            summary=(
                f"selected_dense_threshold={selected_dense_threshold:.4f}; "
                f"sweep_threshold_count={threshold_count}"
            ),
            ready_action="no_action_required",
            review_action="regenerate_dense_threshold_evidence",
            evidence_path=f"{THRESHOLD_RECOMMENDATION_PATH}; {THRESHOLD_SWEEP_PATH}",
        )
    )
    fp_count = _int_value(_dict_value(fp_fn_review, "false_positive_count", None), fallback=0)
    fn_count = _int_value(_dict_value(fp_fn_review, "false_negative_count", None), fallback=0)
    signals.append(
        _signal(
            id="cross_case_fp_fn_context",
            ready=fp_fn_review is not None and fp_count == 0 and fn_count == 0,
            summary=f"false_positive_count={fp_count}; false_negative_count={fn_count}",
            ready_action="no_action_required",
            review_action="continue_cross_case_fp_fn_review",
            evidence_path=str(PHASE3_FP_FN_REVIEW_PATH),
        )
    )
    runtime_config = _dict_value(deployment_readiness, "runtime_config", {})
    runtime_threshold = _float_value(
        _dict_value(runtime_config, "rag_score_threshold", None),
        fallback=0.0,
    )
    signals.append(
        _signal(
            id="runtime_threshold_alignment",
            ready=(
                deployment_readiness is not None
                and abs(selected_dense_threshold - runtime_threshold) < 1e-9
                and str(calibration.get("score_filter_mode", "")).startswith("enabled")
            ),
            summary=(
                f"selected_dense_threshold={selected_dense_threshold:.4f}; "
                f"runtime_threshold={runtime_threshold:.4f}; "
                f"fusion={calibration.get('fusion_mode', 'unknown')}; "
                f"score_filter={calibration.get('score_filter_mode', 'unknown')}"
            ),
            ready_action="no_action_required",
            review_action="keep_runtime_defaults_until_hybrid_runtime_calibration",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    return signals


def _summary(signals: list[Phase3HybridCalibrationSignal]) -> dict[str, Any]:
    return {
        "total_signals": len(signals),
        "ready_signals": sum(1 for item in signals if item.status == "ready"),
        "review_signals": sum(1 for item in signals if item.status == "review"),
        "blocked_signals": sum(1 for item in signals if item.status == "blocked"),
        "open_signal_ids": [
            item.id for item in signals if item.status in {"review", "blocked"}
        ],
    }


def _overall_status(signals: list[Phase3HybridCalibrationSignal]) -> str:
    if any(item.status == "blocked" for item in signals):
        return "blocked"
    if any(item.status == "review" for item in signals):
        return "review"
    return "ready"


def _signal(
    *,
    id: str,
    ready: bool,
    summary: str,
    ready_action: str,
    review_action: str,
    evidence_path: str | None = None,
) -> Phase3HybridCalibrationSignal:
    status = "ready" if ready else "review"
    return Phase3HybridCalibrationSignal(
        id=id,
        status=status,
        summary=summary,
        recommended_action=ready_action if ready else review_action,
        evidence_path=evidence_path,
    )


def _nested_summary(payload: dict[str, Any] | None) -> dict[str, Any]:
    report = _dict_value(payload, "report", {})
    summary = _dict_value(report, "summary", {})
    if isinstance(summary, dict):
        return summary
    return {}


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)


def _float_value(value: Any, *, fallback: float) -> float:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int | float):
        return float(value)
    return fallback


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback
