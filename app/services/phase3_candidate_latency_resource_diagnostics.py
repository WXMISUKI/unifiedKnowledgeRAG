import json
import math
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from statistics import fmean, median
from typing import Any

from app.config import Settings, get_settings


PHASE3_CANDIDATE_LATENCY_RESOURCE_DIAGNOSTICS_ID = (
    "phase3-candidate-latency-resource-diagnostics-v1"
)
PHASE3_BASELINE_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-candidates/"
    "fixture-chinese-seed-baseline.json"
)
DEPLOYMENT_READINESS_PATH = Path("docs/operations/deployment-readiness/deployment-readiness.json")
RUNTIME_DIAGNOSTICS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/"
    "phase3-candidate-runtime-diagnostics.json"
)
DEPLOYED_SMOKE_PATH = Path(
    "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
)


@dataclass(frozen=True)
class Phase3LatencyResourceSignal:
    id: str
    status: str
    summary: str
    recommended_action: str
    evidence_path: str | None = None


@dataclass(frozen=True)
class Phase3CandidateLatencyResourceDiagnosticsReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    latency_profile: dict[str, Any]
    resource_posture: dict[str, Any]
    signals: list[Phase3LatencyResourceSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase3_candidate_latency_resource_diagnostics_report(
    settings: Settings | None = None,
    *,
    base_dir: Path = Path("."),
) -> Phase3CandidateLatencyResourceDiagnosticsReport:
    settings = settings or get_settings()
    baseline_payload = _read_json_if_present(base_dir / PHASE3_BASELINE_PATH)
    deployment_payload = _read_json_if_present(base_dir / DEPLOYMENT_READINESS_PATH)
    runtime_payload = _read_json_if_present(base_dir / RUNTIME_DIAGNOSTICS_PATH)
    deployed_smoke_payload = _read_json_if_present(base_dir / DEPLOYED_SMOKE_PATH)

    latency_profile = _build_latency_profile(baseline_payload)
    resource_posture = _build_resource_posture(
        settings=settings,
        deployment_payload=deployment_payload,
        runtime_payload=runtime_payload,
    )
    signals = _build_signals(
        baseline_payload=baseline_payload,
        deployment_payload=deployment_payload,
        runtime_payload=runtime_payload,
        deployed_smoke_payload=deployed_smoke_payload,
        latency_profile=latency_profile,
    )
    summary = _summary(signals)

    return Phase3CandidateLatencyResourceDiagnosticsReport(
        id=PHASE3_CANDIDATE_LATENCY_RESOURCE_DIAGNOSTICS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(signals),
        decision="keep_runtime_defaults",
        summary=summary,
        latency_profile=latency_profile,
        resource_posture=resource_posture,
        signals=signals,
        notes=[
            "This report is local, read-only candidate latency/resource evidence for Phase 3 promotion review.",
            "It combines benchmark latency profile evidence with deployment and runtime posture snapshots.",
            "Latency values are environment-sensitive and should be compared against matching deployment conditions.",
        ],
    )


def phase3_candidate_latency_resource_diagnostics_report_to_dict(
    report: Phase3CandidateLatencyResourceDiagnosticsReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_candidate_latency_resource_diagnostics_markdown(
    report: Phase3CandidateLatencyResourceDiagnosticsReport,
) -> str:
    lines = [
        "# Phase 3 Candidate Latency/Resource Diagnostics",
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
        "## Latency Profile",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Backend | `{report.latency_profile['backend']}` |",
        f"| Total Cases | `{report.latency_profile['total_cases']}` |",
        f"| Hit Rate | `{report.latency_profile['hit_rate']}` |",
        f"| Citation Match Rate | `{report.latency_profile['citation_match_rate']}` |",
        f"| Empty Handling Rate | `{report.latency_profile['empty_handling_rate']}` |",
        f"| Average Latency (ms) | `{report.latency_profile['average_latency_ms']}` |",
        f"| Median Latency (ms) | `{report.latency_profile['median_latency_ms']}` |",
        f"| P95 Latency (ms) | `{report.latency_profile['p95_latency_ms']}` |",
        f"| Max Latency (ms) | `{report.latency_profile['max_latency_ms']}` |",
        f"| Slowest Case | `{report.latency_profile['slowest_case_id']}` |",
        f"| Slowest Case Latency (ms) | `{report.latency_profile['slowest_case_latency_ms']}` |",
        "",
        "## Resource Posture",
        "",
        "| Setting | Value |",
        "|---|---|",
        f"| Deployment Readiness Status | `{report.resource_posture['deployment_readiness_status']}` |",
        f"| Runtime Diagnostics Status | `{report.resource_posture['runtime_diagnostics_status']}` |",
        f"| Retrieval Backend | `{report.resource_posture['rag_retrieval_backend']}` |",
        f"| Embedding Provider | `{report.resource_posture['embedding_provider']}` |",
        f"| Embedding Model | `{report.resource_posture['embedding_model']}` |",
        f"| Embedding Model Path | `{report.resource_posture['embedding_model_path']}` |",
        f"| Model Artifact Status | `{report.resource_posture['model_artifacts_status']}` |",
        f"| Provider API Key Configured | `{report.resource_posture['provider_api_key_configured']}` |",
        f"| Qdrant API Key Configured | `{report.resource_posture['qdrant_api_key_configured']}` |",
        f"| Qdrant URL | `{report.resource_posture['qdrant_url']}` |",
        f"| Qdrant Collection | `{report.resource_posture['qdrant_collection']}` |",
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


def export_phase3_candidate_latency_resource_diagnostics_report(
    output_dir: Path = Path(
        "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics"
    ),
    *,
    settings: Settings | None = None,
    base_dir: Path = Path("."),
) -> Phase3CandidateLatencyResourceDiagnosticsReport:
    report = build_phase3_candidate_latency_resource_diagnostics_report(
        settings=settings,
        base_dir=base_dir,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3-candidate-latency-resource-diagnostics.json"
    markdown_path = output_dir / "phase3-candidate-latency-resource-diagnostics.md"
    exported = Phase3CandidateLatencyResourceDiagnosticsReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        latency_profile=report.latency_profile,
        resource_posture=report.resource_posture,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_candidate_latency_resource_diagnostics_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_candidate_latency_resource_diagnostics_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_latency_profile(payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return {
            "backend": "missing",
            "total_cases": 0,
            "hit_rate": 0.0,
            "citation_match_rate": 0.0,
            "empty_handling_rate": 0.0,
            "average_latency_ms": 0.0,
            "median_latency_ms": 0.0,
            "p95_latency_ms": 0.0,
            "max_latency_ms": 0.0,
            "slowest_case_id": None,
            "slowest_case_latency_ms": 0.0,
            "empty_case_count": 0,
            "empty_case_average_latency_ms": 0.0,
            "non_empty_case_count": 0,
            "non_empty_case_average_latency_ms": 0.0,
        }
    report = payload.get("report") if isinstance(payload, dict) else None
    summary = report.get("summary") if isinstance(report, dict) else {}
    cases = report.get("cases") if isinstance(report, dict) else []
    if not isinstance(summary, dict):
        summary = {}
    if not isinstance(cases, list):
        cases = []

    latencies = [
        _float_value(case.get("latency_ms"), fallback=0.0)
        for case in cases
        if isinstance(case, dict)
    ]
    empty_latencies = [
        _float_value(case.get("latency_ms"), fallback=0.0)
        for case in cases
        if isinstance(case, dict) and _is_empty_case(case)
    ]
    non_empty_latencies = [
        _float_value(case.get("latency_ms"), fallback=0.0)
        for case in cases
        if isinstance(case, dict) and not _is_empty_case(case)
    ]
    slowest_case = max(
        (case for case in cases if isinstance(case, dict)),
        key=lambda case: _float_value(case.get("latency_ms"), fallback=0.0),
        default=None,
    )
    return {
        "backend": summary.get("backend", "unknown"),
        "total_cases": _int_value(summary.get("total_cases"), fallback=len(cases)),
        "hit_rate": _float_value(summary.get("hit_rate"), fallback=0.0),
        "citation_match_rate": _float_value(
            summary.get("citation_match_rate"),
            fallback=0.0,
        ),
        "empty_handling_rate": _float_value(
            summary.get("empty_handling_rate"),
            fallback=0.0,
        ),
        "average_latency_ms": round(fmean(latencies), 4) if latencies else 0.0,
        "median_latency_ms": round(median(latencies), 4) if latencies else 0.0,
        "p95_latency_ms": round(_percentile(latencies, 95), 4) if latencies else 0.0,
        "max_latency_ms": round(max(latencies), 4) if latencies else 0.0,
        "slowest_case_id": slowest_case.get("id") if slowest_case else None,
        "slowest_case_latency_ms": (
            round(_float_value(slowest_case.get("latency_ms"), fallback=0.0), 4)
            if slowest_case is not None
            else 0.0
        ),
        "empty_case_count": len(empty_latencies),
        "empty_case_average_latency_ms": (
            round(fmean(empty_latencies), 4) if empty_latencies else 0.0
        ),
        "non_empty_case_count": len(non_empty_latencies),
        "non_empty_case_average_latency_ms": (
            round(fmean(non_empty_latencies), 4) if non_empty_latencies else 0.0
        ),
    }


def _build_resource_posture(
    *,
    settings: Settings,
    deployment_payload: dict[str, Any] | None,
    runtime_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    deployment_runtime = (
        deployment_payload.get("runtime_config")
        if isinstance(deployment_payload, dict)
        else {}
    )
    deployment_model = (
        deployment_payload.get("model_artifacts")
        if isinstance(deployment_payload, dict)
        else {}
    )
    runtime_summary = (
        runtime_payload.get("summary") if isinstance(runtime_payload, dict) else {}
    )
    return {
        "deployment_readiness_status": (
            deployment_payload.get("status", "review")
            if isinstance(deployment_payload, dict)
            else "missing"
        ),
        "runtime_diagnostics_status": (
            runtime_payload.get("status", "review")
            if isinstance(runtime_payload, dict)
            else "missing"
        ),
        "deployment_health_status": (
            deployment_payload.get("health", {}).get("status", "unknown")
            if isinstance(deployment_payload, dict)
            else "unknown"
        ),
        "deployment_bindable": (
            bool(deployment_payload.get("preflight", {}).get("bindable", False))
            if isinstance(deployment_payload, dict)
            else False
        ),
        "rag_retrieval_backend": (
            deployment_runtime.get("rag_retrieval_backend", settings.rag_retrieval_backend)
            if isinstance(deployment_runtime, dict)
            else settings.rag_retrieval_backend
        ),
        "embedding_provider": (
            deployment_runtime.get("embedding_provider", settings.embedding_provider)
            if isinstance(deployment_runtime, dict)
            else settings.embedding_provider
        ),
        "embedding_model": (
            deployment_runtime.get("embedding_model", settings.embedding_model)
            if isinstance(deployment_runtime, dict)
            else settings.embedding_model
        ),
        "embedding_model_path": (
            deployment_runtime.get("embedding_model_path")
            if isinstance(deployment_runtime, dict)
            else None
        ),
        "model_artifacts_status": (
            deployment_model.get("status", "not_configured")
            if isinstance(deployment_model, dict)
            else "not_configured"
        ),
        "provider_api_key_configured": (
            bool(deployment_runtime.get("provider_api_key_configured", False))
            if isinstance(deployment_runtime, dict)
            else bool(settings.provider_api_key)
        ),
        "qdrant_api_key_configured": (
            bool(deployment_runtime.get("qdrant_api_key_configured", False))
            if isinstance(deployment_runtime, dict)
            else bool(settings.qdrant_api_key)
        ),
        "qdrant_url": (
            deployment_runtime.get("qdrant_url", settings.qdrant_url)
            if isinstance(deployment_runtime, dict)
            else settings.qdrant_url
        ),
        "qdrant_collection": (
            deployment_runtime.get("qdrant_collection", settings.qdrant_collection)
            if isinstance(deployment_runtime, dict)
            else settings.qdrant_collection
        ),
        "open_runtime_prerequisite_ids": (
            runtime_summary.get("open_prerequisite_ids", [])
            if isinstance(runtime_summary, dict)
            else []
        ),
    }


def _build_signals(
    *,
    baseline_payload: dict[str, Any] | None,
    deployment_payload: dict[str, Any] | None,
    runtime_payload: dict[str, Any] | None,
    deployed_smoke_payload: dict[str, Any] | None,
    latency_profile: dict[str, Any],
) -> list[Phase3LatencyResourceSignal]:
    signals: list[Phase3LatencyResourceSignal] = []
    signals.append(
        _signal(
            id="benchmark_latency_profile",
            ready=baseline_payload is not None and latency_profile["total_cases"] > 0,
            summary=(
                f"backend={latency_profile['backend']}; "
                f"total_cases={latency_profile['total_cases']}; "
                f"average_latency_ms={latency_profile['average_latency_ms']:.4f}; "
                f"median_latency_ms={latency_profile['median_latency_ms']:.4f}; "
                f"p95_latency_ms={latency_profile['p95_latency_ms']:.4f}"
            ),
            ready_action="no_action_required",
            review_action="regenerate_chinese_seed_evidence_bundle",
            evidence_path=str(PHASE3_BASELINE_PATH),
        )
    )
    deployment_status = (
        deployment_payload.get("status", "review")
        if isinstance(deployment_payload, dict)
        else "missing"
    )
    deployment_runtime = (
        deployment_payload.get("runtime_config")
        if isinstance(deployment_payload, dict)
        else {}
    )
    deployment_model = (
        deployment_payload.get("model_artifacts")
        if isinstance(deployment_payload, dict)
        else {}
    )
    signals.append(
        _signal(
            id="deployment_readiness_snapshot",
            ready=deployment_status == "ready",
            summary=(
                f"status={deployment_status}; "
                f"rag_backend={_dict_value(deployment_runtime, 'rag_retrieval_backend', 'unknown')}; "
                f"embedding_provider={_dict_value(deployment_runtime, 'embedding_provider', 'unknown')}; "
                f"model_artifacts_status={_dict_value(deployment_model, 'status', 'unknown')}"
            ),
            ready_action="no_action_required",
            review_action="review_deployment_readiness_notes",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    runtime_status = (
        runtime_payload.get("status", "review")
        if isinstance(runtime_payload, dict)
        else "missing"
    )
    runtime_summary = (
        runtime_payload.get("summary") if isinstance(runtime_payload, dict) else {}
    )
    signals.append(
        _signal(
            id="runtime_diagnostics_snapshot",
            ready=runtime_status == "ready",
            summary=(
                f"status={runtime_status}; "
                f"decision={_dict_value(runtime_payload, 'decision', 'keep_runtime_defaults')}; "
                f"open_prerequisites={_open_runtime_prerequisites(runtime_summary)}"
            ),
            ready_action="no_action_required",
            review_action="review_runtime_diagnostics_notes",
            evidence_path=str(RUNTIME_DIAGNOSTICS_PATH),
        )
    )
    signals.append(
        _signal(
            id="local_embedding_artifact",
            ready=_dict_value(deployment_model, "status", "not_configured") == "ready",
            summary=(
                f"status={_dict_value(deployment_model, 'status', 'not_configured')}; "
                f"path_exists={_dict_value(deployment_model, 'path_exists', False)}; "
                f"manifest_exists={_dict_value(deployment_model, 'manifest_exists', False)}"
            ),
            ready_action="no_action_required",
            review_action="validate_local_embedding_artifact",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    signals.append(
        _signal(
            id="provider_api_guard",
            ready=bool(_dict_value(deployment_runtime, "provider_api_key_configured", False)),
            summary=(
                f"provider_api_key_configured={bool(_dict_value(deployment_runtime, 'provider_api_key_configured', False))}"
            ),
            ready_action="no_action_required",
            review_action="configure_provider_api_key_for_deployment_review",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    if deployed_smoke_payload is None:
        signals.append(
            Phase3LatencyResourceSignal(
                id="deployed_smoke_evidence",
                status="review",
                summary="Deployed smoke evidence is not present in local workspace.",
                recommended_action="run_deployed_provider_smoke_after_deployment",
                evidence_path=str(DEPLOYED_SMOKE_PATH),
            )
        )
    else:
        smoke_status = _normalize_status(deployed_smoke_payload.get("status", "review"))
        signals.append(
            Phase3LatencyResourceSignal(
                id="deployed_smoke_evidence",
                status=smoke_status,
                summary=(
                    f"status={smoke_status}; base_url={deployed_smoke_payload.get('base_url', 'unknown')}"
                ),
                recommended_action=(
                    "no_action_required"
                    if smoke_status == "ready"
                    else "review_evidence_notes"
                ),
                evidence_path=str(DEPLOYED_SMOKE_PATH),
            )
        )
    return signals


def _summary(signals: list[Phase3LatencyResourceSignal]) -> dict[str, Any]:
    return {
        "total_signals": len(signals),
        "ready_signals": sum(1 for item in signals if item.status == "ready"),
        "review_signals": sum(1 for item in signals if item.status == "review"),
        "blocked_signals": sum(1 for item in signals if item.status == "blocked"),
        "open_signal_ids": [
            item.id for item in signals if item.status in {"review", "blocked"}
        ],
    }


def _overall_status(signals: list[Phase3LatencyResourceSignal]) -> str:
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
) -> Phase3LatencyResourceSignal:
    status = "ready" if ready else "review"
    return Phase3LatencyResourceSignal(
        id=id,
        status=status,
        summary=summary,
        recommended_action=ready_action if ready else review_action,
        evidence_path=evidence_path,
    )


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "review"


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


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)


def _open_runtime_prerequisites(summary: Any) -> int:
    if not isinstance(summary, dict):
        return 0
    open_ids = summary.get("open_prerequisite_ids", [])
    if isinstance(open_ids, list):
        return len(open_ids)
    return 0


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil((percentile / 100) * len(ordered)) - 1))
    return ordered[index]


def _is_empty_case(case: dict[str, Any]) -> bool:
    if str(case.get("category", "")).lower() == "empty":
        return True
    if case.get("empty_query_handling") is not None:
        return bool(case.get("empty_query_handling"))
    if case.get("expect_empty") is not None:
        return bool(case.get("expect_empty"))
    if case.get("expect_empty_case") is not None:
        return bool(case.get("expect_empty_case"))
    return False
