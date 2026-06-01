import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE6_BGE_M3_VS_MOCK_FIXTURE_DIAGNOSTICS_ID = (
    "phase6-bge-m3-vs-mock-fixture-diagnostics-v1"
)
FIXTURE_BASELINE_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json"
)
BGE_CANDIDATE_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json"
)
PHASE3_LATENCY_DIAGNOSTICS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/"
    "phase3-candidate-latency-resource-diagnostics.json"
)
PHASE3_RUNTIME_DIAGNOSTICS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/"
    "phase3-candidate-runtime-diagnostics.json"
)
PHASE6_ARTIFACT_READINESS_PATH = Path(
    "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json"
)
DEPLOYMENT_READINESS_PATH = Path(
    "docs/operations/deployment-readiness/deployment-readiness.json"
)


@dataclass(frozen=True)
class Phase6BgeM3ComparisonSignal:
    id: str
    status: str
    summary: str
    recommended_action: str
    evidence_path: str | None = None


@dataclass(frozen=True)
class Phase6BgeM3VsMockFixtureDiagnosticsReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    baseline_profile: dict[str, Any]
    candidate_profile: dict[str, Any]
    quality_delta: dict[str, Any]
    linkage: dict[str, Any]
    signals: list[Phase6BgeM3ComparisonSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase6_bge_m3_vs_mock_fixture_diagnostics_report(
    *,
    base_dir: Path = Path("."),
) -> Phase6BgeM3VsMockFixtureDiagnosticsReport:
    baseline_payload = _read_json_if_present(base_dir / FIXTURE_BASELINE_PATH)
    candidate_payload = _read_json_if_present(base_dir / BGE_CANDIDATE_PATH)
    latency_payload = _read_json_if_present(base_dir / PHASE3_LATENCY_DIAGNOSTICS_PATH)
    runtime_payload = _read_json_if_present(base_dir / PHASE3_RUNTIME_DIAGNOSTICS_PATH)
    artifact_payload = _read_json_if_present(base_dir / PHASE6_ARTIFACT_READINESS_PATH)
    deployment_payload = _read_json_if_present(base_dir / DEPLOYMENT_READINESS_PATH)

    baseline_profile = _benchmark_profile(baseline_payload)
    candidate_profile = _benchmark_profile(candidate_payload)
    quality_delta = _quality_delta(baseline_profile, candidate_profile)
    linkage = _linkage_snapshot(
        latency_payload=latency_payload,
        runtime_payload=runtime_payload,
        artifact_payload=artifact_payload,
        deployment_payload=deployment_payload,
    )
    signals = _build_signals(
        baseline_profile=baseline_profile,
        candidate_profile=candidate_profile,
        quality_delta=quality_delta,
        linkage=linkage,
    )
    summary = _summary(signals)
    status = _overall_status(signals)
    if (
        not baseline_profile["present"]
        or not linkage["artifact_readiness_present"]
        or not linkage["deployment_readiness_present"]
    ):
        status = "blocked"

    return Phase6BgeM3VsMockFixtureDiagnosticsReport(
        id=PHASE6_BGE_M3_VS_MOCK_FIXTURE_DIAGNOSTICS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_runtime_defaults",
        summary=summary,
        baseline_profile=baseline_profile,
        candidate_profile=candidate_profile,
        quality_delta=quality_delta,
        linkage=linkage,
        signals=signals,
        notes=[
            "This report is local read-only comparison evidence and does not change runtime defaults.",
            "Candidate deltas are interpreted as review guidance, not direct promotion approval.",
            "Use matching benchmark fixture scope when comparing baseline and candidate evidence.",
        ],
    )


def phase6_bge_m3_vs_mock_fixture_diagnostics_report_to_dict(
    report: Phase6BgeM3VsMockFixtureDiagnosticsReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase6_bge_m3_vs_mock_fixture_diagnostics_markdown(
    report: Phase6BgeM3VsMockFixtureDiagnosticsReport,
) -> str:
    lines = [
        "# Phase 6 BGE-M3 vs Mock/Fixture Diagnostics",
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
        "## Baseline vs Candidate",
        "",
        "| Field | Baseline | Candidate | Delta |",
        "|---|---|---|---|",
        (
            f"| Hit Rate | `{report.baseline_profile['hit_rate']:.4f}` | "
            f"`{report.candidate_profile['hit_rate']:.4f}` | "
            f"`{report.quality_delta['hit_rate_delta']:.4f}` |"
        ),
        (
            f"| Citation Match Rate | `{report.baseline_profile['citation_match_rate']:.4f}` | "
            f"`{report.candidate_profile['citation_match_rate']:.4f}` | "
            f"`{report.quality_delta['citation_match_rate_delta']:.4f}` |"
        ),
        (
            f"| Empty Handling Rate | `{report.baseline_profile['empty_handling_rate']:.4f}` | "
            f"`{report.candidate_profile['empty_handling_rate']:.4f}` | "
            f"`{report.quality_delta['empty_handling_rate_delta']:.4f}` |"
        ),
        (
            f"| Average Latency (ms) | `{report.baseline_profile['average_latency_ms']:.4f}` | "
            f"`{report.candidate_profile['average_latency_ms']:.4f}` | "
            f"`{report.quality_delta['average_latency_ms_delta']:.4f}` |"
        ),
        "",
        "## Linkage",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Artifact Readiness Present | `{report.linkage['artifact_readiness_present']}` |",
        f"| Artifact Readiness Status | `{report.linkage['artifact_readiness_status']}` |",
        f"| Deployment Readiness Present | `{report.linkage['deployment_readiness_present']}` |",
        f"| Deployment Readiness Status | `{report.linkage['deployment_readiness_status']}` |",
        f"| Runtime Diagnostics Present | `{report.linkage['runtime_diagnostics_present']}` |",
        f"| Runtime Diagnostics Status | `{report.linkage['runtime_diagnostics_status']}` |",
        f"| Latency Diagnostics Present | `{report.linkage['latency_diagnostics_present']}` |",
        f"| Latency Diagnostics Status | `{report.linkage['latency_diagnostics_status']}` |",
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


def export_phase6_bge_m3_vs_mock_fixture_diagnostics_report(
    output_dir: Path = Path("docs/operations/bge-m3-comparison-readiness"),
    *,
    base_dir: Path = Path("."),
) -> Phase6BgeM3VsMockFixtureDiagnosticsReport:
    report = build_phase6_bge_m3_vs_mock_fixture_diagnostics_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase6-bge-m3-vs-mock-fixture-diagnostics.json"
    markdown_path = output_dir / "phase6-bge-m3-vs-mock-fixture-diagnostics.md"
    exported = Phase6BgeM3VsMockFixtureDiagnosticsReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        baseline_profile=report.baseline_profile,
        candidate_profile=report.candidate_profile,
        quality_delta=report.quality_delta,
        linkage=report.linkage,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase6_bge_m3_vs_mock_fixture_diagnostics_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase6_bge_m3_vs_mock_fixture_diagnostics_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_signals(
    *,
    baseline_profile: dict[str, Any],
    candidate_profile: dict[str, Any],
    quality_delta: dict[str, Any],
    linkage: dict[str, Any],
) -> list[Phase6BgeM3ComparisonSignal]:
    signals: list[Phase6BgeM3ComparisonSignal] = []
    signals.append(
        _signal(
            id="baseline_profile_presence",
            ready=baseline_profile["present"],
            summary=f"present={baseline_profile['present']}; total_cases={baseline_profile['total_cases']}",
            ready_action="no_action_required",
            review_action="regenerate_fixture_baseline_evidence",
            evidence_path=str(FIXTURE_BASELINE_PATH),
        )
    )
    signals.append(
        _signal(
            id="candidate_profile_presence",
            ready=candidate_profile["present"],
            summary=f"present={candidate_profile['present']}; total_cases={candidate_profile['total_cases']}",
            ready_action="no_action_required",
            review_action="regenerate_bge_m3_candidate_evidence",
            evidence_path=str(BGE_CANDIDATE_PATH),
        )
    )
    signals.append(
        _signal(
            id="comparison_metric_schema",
            ready=baseline_profile["has_core_metrics"] and candidate_profile["has_core_metrics"],
            summary=(
                f"baseline_core_metrics={baseline_profile['has_core_metrics']}; "
                f"candidate_core_metrics={candidate_profile['has_core_metrics']}"
            ),
            ready_action="no_action_required",
            review_action="align_baseline_and_candidate_metric_schema",
            evidence_path=str(BGE_CANDIDATE_PATH),
        )
    )
    signals.append(
        _signal(
            id="artifact_readiness_linkage",
            ready=linkage["artifact_readiness_present"]
            and linkage["artifact_readiness_status"] == "ready",
            summary=(
                f"artifact_present={linkage['artifact_readiness_present']}; "
                f"artifact_status={linkage['artifact_readiness_status']}"
            ),
            ready_action="no_action_required",
            review_action="review_bge_m3_artifact_readiness",
            evidence_path=str(PHASE6_ARTIFACT_READINESS_PATH),
        )
    )
    signals.append(
        _signal(
            id="runtime_and_latency_diagnostics_linkage",
            ready=linkage["runtime_diagnostics_present"]
            and linkage["latency_diagnostics_present"],
            summary=(
                f"runtime_status={linkage['runtime_diagnostics_status']}; "
                f"latency_status={linkage['latency_diagnostics_status']}"
            ),
            ready_action="no_action_required",
            review_action="regenerate_phase3_runtime_and_latency_diagnostics",
            evidence_path=str(PHASE3_RUNTIME_DIAGNOSTICS_PATH),
        )
    )
    signals.append(
        _signal(
            id="quality_non_regression_visibility",
            ready=quality_delta["comparable"]
            and quality_delta["hit_rate_delta"] >= 0.0
            and quality_delta["citation_match_rate_delta"] >= 0.0,
            summary=(
                f"hit_rate_delta={quality_delta['hit_rate_delta']:.4f}; "
                f"citation_match_rate_delta={quality_delta['citation_match_rate_delta']:.4f}; "
                f"empty_handling_rate_delta={quality_delta['empty_handling_rate_delta']:.4f}"
            ),
            ready_action="no_action_required",
            review_action="expand_candidate_cases_and_review_fp_fn",
            evidence_path=str(BGE_CANDIDATE_PATH),
        )
    )
    signals.append(
        _signal(
            id="deployment_linkage_visibility",
            ready=linkage["deployment_readiness_present"],
            summary=(
                f"deployment_present={linkage['deployment_readiness_present']}; "
                f"deployment_status={linkage['deployment_readiness_status']}"
            ),
            ready_action="no_action_required",
            review_action="regenerate_deployment_readiness",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    return signals


def _benchmark_profile(payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return {
            "present": False,
            "total_cases": 0,
            "hit_rate": 0.0,
            "citation_match_rate": 0.0,
            "empty_handling_rate": 0.0,
            "average_latency_ms": 0.0,
            "has_core_metrics": False,
        }
    report = payload.get("report") if isinstance(payload, dict) else {}
    summary = report.get("summary") if isinstance(report, dict) else {}
    cases = report.get("cases") if isinstance(report, dict) else []
    if not isinstance(summary, dict):
        summary = {}
    if not isinstance(cases, list):
        cases = []
    latencies = [
        float(case.get("latency_ms"))
        for case in cases
        if isinstance(case, dict) and isinstance(case.get("latency_ms"), int | float)
    ]
    return {
        "present": True,
        "total_cases": _int_value(summary.get("total_cases"), fallback=len(cases)),
        "hit_rate": _float_value(summary.get("hit_rate"), fallback=0.0),
        "citation_match_rate": _float_value(summary.get("citation_match_rate"), fallback=0.0),
        "empty_handling_rate": _float_value(summary.get("empty_handling_rate"), fallback=0.0),
        "average_latency_ms": (sum(latencies) / len(latencies)) if latencies else 0.0,
        "has_core_metrics": all(
            key in summary for key in ("hit_rate", "citation_match_rate", "empty_handling_rate")
        ),
    }


def _quality_delta(
    baseline_profile: dict[str, Any],
    candidate_profile: dict[str, Any],
) -> dict[str, Any]:
    comparable = baseline_profile["present"] and candidate_profile["present"]
    if not comparable:
        return {
            "comparable": False,
            "hit_rate_delta": 0.0,
            "citation_match_rate_delta": 0.0,
            "empty_handling_rate_delta": 0.0,
            "average_latency_ms_delta": 0.0,
        }
    return {
        "comparable": True,
        "hit_rate_delta": round(
            candidate_profile["hit_rate"] - baseline_profile["hit_rate"],
            4,
        ),
        "citation_match_rate_delta": (
            round(
                candidate_profile["citation_match_rate"]
                - baseline_profile["citation_match_rate"],
                4,
            )
        ),
        "empty_handling_rate_delta": (
            round(
                candidate_profile["empty_handling_rate"]
                - baseline_profile["empty_handling_rate"],
                4,
            )
        ),
        "average_latency_ms_delta": (
            round(
                candidate_profile["average_latency_ms"]
                - baseline_profile["average_latency_ms"],
                4,
            )
        ),
    }


def _linkage_snapshot(
    *,
    latency_payload: dict[str, Any] | None,
    runtime_payload: dict[str, Any] | None,
    artifact_payload: dict[str, Any] | None,
    deployment_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "latency_diagnostics_present": latency_payload is not None,
        "latency_diagnostics_status": _status_value(latency_payload),
        "runtime_diagnostics_present": runtime_payload is not None,
        "runtime_diagnostics_status": _status_value(runtime_payload),
        "artifact_readiness_present": artifact_payload is not None,
        "artifact_readiness_status": _status_value(artifact_payload),
        "deployment_readiness_present": deployment_payload is not None,
        "deployment_readiness_status": _status_value(deployment_payload),
    }


def _summary(signals: list[Phase6BgeM3ComparisonSignal]) -> dict[str, Any]:
    return {
        "total_signals": len(signals),
        "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
        "review_signals": sum(1 for signal in signals if signal.status == "review"),
        "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
        "open_signal_ids": [
            signal.id for signal in signals if signal.status in {"review", "blocked"}
        ],
    }


def _overall_status(signals: list[Phase6BgeM3ComparisonSignal]) -> str:
    if any(signal.status == "blocked" for signal in signals):
        return "blocked"
    if any(signal.status == "review" for signal in signals):
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
) -> Phase6BgeM3ComparisonSignal:
    return Phase6BgeM3ComparisonSignal(
        id=id,
        status="ready" if ready else "review",
        summary=summary,
        recommended_action=ready_action if ready else review_action,
        evidence_path=evidence_path,
    )


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _status_value(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "missing"
    status = payload.get("status", "review")
    return str(status) if isinstance(status, str) else "review"


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback


def _float_value(value: Any, *, fallback: float) -> float:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int | float):
        return float(value)
    return fallback
