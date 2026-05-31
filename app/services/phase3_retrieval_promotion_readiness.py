import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE3_RETRIEVAL_PROMOTION_READINESS_ID = "phase3-retrieval-promotion-readiness-v1"
PHASE3_GAP_MATRIX_PATH = (
    "docs/benchmark/chinese-seed/retrieval-promotion-readiness/"
    "phase3-retrieval-promotion-gap-matrix.md"
)
PHASE3_RETRIEVAL_PROMOTION_READINESS_JSON = (
    "phase3-retrieval-promotion-readiness.json"
)
PHASE3_RETRIEVAL_PROMOTION_READINESS_MARKDOWN = (
    "phase3-retrieval-promotion-readiness.md"
)


@dataclass(frozen=True)
class Phase3RetrievalPromotionGate:
    id: str
    title: str
    status: str
    evidence_paths: list[str]
    evidence_present: bool
    summary: str
    open_gap: str
    next_evidence: str
    promotion_position: str
    recommended_action: str


@dataclass(frozen=True)
class Phase3SupportingEvidenceItem:
    id: str
    category: str
    path: str
    status: str
    summary: str
    present: bool
    required: bool
    recommended_action: str


@dataclass(frozen=True)
class Phase3RetrievalPromotionReadinessReport:
    id: str
    generated_at: str
    status: str
    decision: str
    gap_matrix_path: str
    summary: dict[str, int]
    gates: list[Phase3RetrievalPromotionGate]
    supporting_evidence: list[Phase3SupportingEvidenceItem]
    open_gates: list[str]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase3_retrieval_promotion_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase3RetrievalPromotionReadinessReport:
    gates = [
        _build_qdrant_gate(base_dir),
        _build_bge_m3_gate(base_dir),
        _build_hybrid_retrieval_gate(base_dir),
        _build_hybrid_gating_gate(base_dir),
        _build_aggregation_gate(base_dir),
        _build_relation_aware_gate(base_dir),
        _build_deployed_smoke_gate(base_dir),
    ]
    supporting_evidence = [
        _build_supporting_seed_baseline(base_dir),
        _build_supporting_fp_fn_review(base_dir),
    ]
    open_gates = [gate.id for gate in gates if gate.status != "ready"]
    summary = {
        "total_gates": len(gates),
        "ready_gates": sum(1 for gate in gates if gate.status == "ready"),
        "review_gates": sum(1 for gate in gates if gate.status == "review"),
        "candidate_gates": sum(1 for gate in gates if gate.status == "candidate"),
        "blocked_gates": sum(1 for gate in gates if gate.status == "blocked"),
        "supporting_evidence_ready": sum(
            1 for item in supporting_evidence if item.status == "ready"
        ),
        "open_gates": len(open_gates),
    }
    return Phase3RetrievalPromotionReadinessReport(
        id=PHASE3_RETRIEVAL_PROMOTION_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(gates),
        decision="keep_runtime_defaults",
        gap_matrix_path=PHASE3_GAP_MATRIX_PATH,
        summary=summary,
        gates=gates,
        supporting_evidence=supporting_evidence,
        open_gates=open_gates,
        notes=[
            "This report is local, read-only evidence for Phase 3 promotion review.",
            "It complements the human-readable gap matrix and does not change runtime defaults.",
        ],
    )


def phase3_retrieval_promotion_readiness_report_to_dict(
    report: Phase3RetrievalPromotionReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_retrieval_promotion_readiness_markdown(
    report: Phase3RetrievalPromotionReadinessReport,
) -> str:
    lines = [
        "# Phase 3 Retrieval Promotion Readiness Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Gap Matrix: `{report.gap_matrix_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Gates | `{report.summary['total_gates']}` |",
        f"| Ready Gates | `{report.summary['ready_gates']}` |",
        f"| Review Gates | `{report.summary['review_gates']}` |",
        f"| Candidate Gates | `{report.summary['candidate_gates']}` |",
        f"| Blocked Gates | `{report.summary['blocked_gates']}` |",
        f"| Supporting Evidence Ready | `{report.summary['supporting_evidence_ready']}` |",
        f"| Open Gates | `{report.summary['open_gates']}` |",
        "",
        "## Promotion Gates",
        "",
        "| Gate | Status | Evidence | Open Gap | Next Evidence |",
        "|---|---|---|---|---|",
    ]
    for gate in report.gates:
        evidence = ", ".join(f"`{path}`" for path in gate.evidence_paths) or "`none`"
        lines.append(
            f"| `{gate.title}` | `{gate.status}` | {evidence} | "
            f"{gate.open_gap} | {gate.next_evidence} |"
        )
    lines.extend(
        [
            "",
            "## Supporting Evidence",
            "",
            "| Evidence | Status | Summary |",
            "|---|---|---|",
        ]
    )
    for item in report.supporting_evidence:
        lines.append(
            f"| `{item.id}` | `{item.status}` | {item.summary} |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase3_retrieval_promotion_readiness_report(
    *,
    output_dir: Path = Path(
        "docs/benchmark/chinese-seed/retrieval-promotion-readiness"
    ),
    base_dir: Path = Path("."),
) -> Phase3RetrievalPromotionReadinessReport:
    report = build_phase3_retrieval_promotion_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE3_RETRIEVAL_PROMOTION_READINESS_JSON
    markdown_path = output_dir / PHASE3_RETRIEVAL_PROMOTION_READINESS_MARKDOWN
    exported_report = Phase3RetrievalPromotionReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        gap_matrix_path=report.gap_matrix_path,
        summary=report.summary,
        gates=report.gates,
        supporting_evidence=report.supporting_evidence,
        open_gates=report.open_gates,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_retrieval_promotion_readiness_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_retrieval_promotion_readiness_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _build_qdrant_gate(base_dir: Path) -> Phase3RetrievalPromotionGate:
    smoke_path = Path(
        "docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json"
    )
    recommendation_path = Path(
        "docs/benchmark/chinese-seed/retrieval-candidates/"
        "qdrant-bge-m3-threshold-recommendation.json"
    )
    smoke = _load_json(base_dir, smoke_path)
    recommendation = _load_json(base_dir, recommendation_path)
    summary_parts = []
    if smoke is not None:
        summary_parts.append(_report_summary_metrics(smoke))
    if recommendation is not None:
        selected_threshold = _safe_value(recommendation.get("selected_threshold"))
        approval_status = _safe_value(recommendation.get("approval_status"))
        summary_parts.append(
            f"threshold={selected_threshold}; approval_status={approval_status}"
        )
    summary = (
        "; ".join(summary_parts)
        if summary_parts
        else "Qdrant smoke evidence is missing."
    )
    evidence_present = smoke is not None
    status = "candidate" if evidence_present else "review"
    return Phase3RetrievalPromotionGate(
        id="qdrant_vector_store",
        title="Qdrant vector store",
        status=status,
        evidence_paths=[str(smoke_path), str(recommendation_path)],
        evidence_present=evidence_present,
        summary=summary,
        open_gap=(
            "Customer-like corpus benchmark, deployment latency, backup/restore review, "
            "private-network deployment evidence"
        ),
        next_evidence=(
            "Export customer-like Qdrant benchmark and deployment review evidence"
        ),
        promotion_position="Keep opt-in; do not change runtime default",
        recommended_action="collect_customer_like_qdrant_evidence",
    )


def _build_bge_m3_gate(base_dir: Path) -> Phase3RetrievalPromotionGate:
    candidate_path = Path(
        "docs/benchmark/chinese-seed/embedding-candidates/bge-m3-local-candidate.json"
    )
    payload = _load_json(base_dir, candidate_path)
    summary = "BGE-M3 candidate evidence is missing."
    evidence_present = payload is not None
    status = "review"
    if payload is not None:
        readiness_status = _safe_value(payload.get("readiness_status"))
        criteria = payload.get("criteria_coverage")
        summary = (
            f"readiness_status={readiness_status}; "
            f"criteria_coverage={_format_criteria_coverage(criteria)}"
        )
        if readiness_status == "baseline":
            status = "candidate"
    return Phase3RetrievalPromotionGate(
        id="bge_m3_local_embedding",
        title="BGE-M3 local embedding",
        status=status,
        evidence_paths=[str(candidate_path)],
        evidence_present=evidence_present,
        summary=summary,
        open_gap=(
            "Artifact validation, private-network deployment, quality/latency comparison, "
            "deployment readiness evidence"
        ),
        next_evidence=(
            "Validate the downloaded local model artifact and compare latency in a private network"
        ),
        promotion_position="Keep opt-in; do not change runtime default",
        recommended_action="validate_bge_m3_artifact_and_latency",
    )


def _build_hybrid_retrieval_gate(base_dir: Path) -> Phase3RetrievalPromotionGate:
    exact_path = Path(
        "docs/benchmark/chinese-seed/exact-term-candidates/"
        "qdrant-bge-m3-hybrid-exact-term-smoke.json"
    )
    empty_path = Path(
        "docs/benchmark/chinese-seed/hybrid-empty-stress/"
        "qdrant-bge-m3-hybrid-empty-stress.json"
    )
    exact_payload = _load_json(base_dir, exact_path)
    empty_payload = _load_json(base_dir, empty_path)
    summary_parts = []
    if exact_payload is not None:
        summary_parts.append(
            f"exact_term={_report_summary_metrics(exact_payload)}"
        )
    if empty_payload is not None:
        summary_parts.append(
            f"empty_stress={_report_summary_metrics(empty_payload)}"
        )
    summary = (
        "; ".join(summary_parts)
        if summary_parts
        else "Hybrid retrieval evidence is missing."
    )
    evidence_present = exact_payload is not None or empty_payload is not None
    status = "candidate" if evidence_present else "review"
    return Phase3RetrievalPromotionGate(
        id="hybrid_retrieval",
        title="Hybrid retrieval",
        status=status,
        evidence_paths=[str(exact_path), str(empty_path)],
        evidence_present=evidence_present,
        summary=summary,
        open_gap=(
            "Broader customer-like false-positive and false-negative review, score/fusion "
            "calibration, deploy review"
        ),
        next_evidence=(
            "Expand customer-like hybrid benchmark coverage and compare score/fusion strategies"
        ),
        promotion_position="Not default",
        recommended_action="collect_hybrid_promotion_evidence",
    )


def _build_hybrid_gating_gate(base_dir: Path) -> Phase3RetrievalPromotionGate:
    exact_gate_path = Path(
        "docs/benchmark/chinese-seed/hybrid-gating-candidates/"
        "qdrant-bge-m3-hybrid-exact-identifier-gate.json"
    )
    alias_gate_path = Path(
        "docs/benchmark/chinese-seed/noisy-identifier-gating-candidates/"
        "qdrant-bge-m3-hybrid-alias-identifier-gate.json"
    )
    split_gate_path = Path(
        "docs/benchmark/chinese-seed/split-chunk-gating-candidates/"
        "qdrant-bge-m3-hybrid-exact-identifier-gate.json"
    )
    exact_payload = _load_json(base_dir, exact_gate_path)
    alias_payload = _load_json(base_dir, alias_gate_path)
    split_payload = _load_json(base_dir, split_gate_path)
    summary_parts = []
    if exact_payload is not None:
        summary_parts.append(f"exact_gate={_hybrid_gate_summary(exact_payload)}")
    if alias_payload is not None:
        summary_parts.append(f"alias_gate={_hybrid_gate_summary(alias_payload)}")
    if split_payload is not None:
        summary_parts.append(f"split_gate={_hybrid_gate_summary(split_payload)}")
    summary = (
        "; ".join(summary_parts)
        if summary_parts
        else "Hybrid gating evidence is missing."
    )
    evidence_present = any(
        payload is not None
        for payload in (exact_payload, alias_payload, split_payload)
    )
    status = "candidate" if evidence_present else "review"
    return Phase3RetrievalPromotionGate(
        id="hybrid_gating",
        title="Hybrid gating",
        status=status,
        evidence_paths=[
            str(exact_gate_path),
            str(alias_gate_path),
            str(split_gate_path),
        ],
        evidence_present=evidence_present,
        summary=summary,
        open_gap=(
            "Broader alias/noisy identifier coverage, split-chunk false-negative review, "
            "gating policy ownership"
        ),
        next_evidence=(
            "Expand gating fixtures with additional alias, OCR-noise, and split-chunk cases"
        ),
        promotion_position="Evaluation only",
        recommended_action="collect_hybrid_gating_evidence",
    )


def _build_aggregation_gate(base_dir: Path) -> Phase3RetrievalPromotionGate:
    aggregation_path = Path(
        "docs/benchmark/chinese-seed/multi-chunk-aggregation-candidates/"
        "qdrant-bge-m3-hybrid-multi-chunk-aggregation.json"
    )
    negative_path = Path(
        "docs/benchmark/chinese-seed/multi-chunk-aggregation-negative-controls/"
        "qdrant-bge-m3-hybrid-multi-chunk-aggregation.json"
    )
    relation_path = Path(
        "docs/benchmark/chinese-seed/relation-aware-aggregation-grading/"
        "relation-aware-aggregation-grading.json"
    )
    aggregation_payload = _load_json(base_dir, aggregation_path)
    negative_payload = _load_json(base_dir, negative_path)
    relation_payload = _load_json(base_dir, relation_path)
    summary_parts = []
    if aggregation_payload is not None:
        summary_parts.append(
            f"aggregation={_report_summary_metrics(aggregation_payload)}"
        )
    if negative_payload is not None:
        summary_parts.append(
            f"negative_control={_report_summary_metrics(negative_payload)}"
        )
    if relation_payload is not None:
        summary_parts.append(f"relation={_relation_aware_summary(relation_payload)}")
    summary = (
        "; ".join(summary_parts)
        if summary_parts
        else "Multi-chunk aggregation evidence is missing."
    )
    evidence_present = any(
        payload is not None
        for payload in (aggregation_payload, negative_payload, relation_payload)
    )
    status = "review" if evidence_present else "review"
    return Phase3RetrievalPromotionGate(
        id="multi_chunk_aggregation",
        title="Multi-chunk aggregation",
        status=status,
        evidence_paths=[
            str(aggregation_path),
            str(negative_path),
            str(relation_path),
        ],
        evidence_present=evidence_present,
        summary=summary,
        open_gap=(
            "More relation-heavy customer-like cases, noisy top-k review, latency and "
            "citation granularity review"
        ),
        next_evidence=(
            "Expand same-document negative controls and relation-aware coverage before promoting aggregation"
        ),
        promotion_position="Keep review-only",
        recommended_action="collect_aggregation_evidence",
    )


def _build_relation_aware_gate(base_dir: Path) -> Phase3RetrievalPromotionGate:
    relation_path = Path(
        "docs/benchmark/chinese-seed/relation-aware-aggregation-grading/"
        "relation-aware-aggregation-grading.json"
    )
    payload = _load_json(base_dir, relation_path)
    summary = "Relation-aware grading evidence is missing."
    evidence_present = payload is not None
    status = "candidate" if evidence_present else "review"
    if payload is not None:
        summary = _relation_aware_summary(payload)
    return Phase3RetrievalPromotionGate(
        id="relation_aware_grading",
        title="Relation-aware grading",
        status=status,
        evidence_paths=[str(relation_path)],
        evidence_present=evidence_present,
        summary=summary,
        open_gap="Broader relation fixture coverage and production semantics review",
        next_evidence="Expand relation fixtures and decide whether deterministic grading remains sufficient",
        promotion_position="Evaluation only",
        recommended_action="expand_relation_grading_fixture",
    )


def _build_deployed_smoke_gate(base_dir: Path) -> Phase3RetrievalPromotionGate:
    smoke_path = Path(
        "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
    )
    payload = _load_json(base_dir, smoke_path)
    if payload is None:
        return Phase3RetrievalPromotionGate(
            id="deployed_smoke",
            title="Deployed smoke",
            status="review",
            evidence_paths=[str(smoke_path)],
            evidence_present=False,
            summary="Optional deployed smoke evidence is missing.",
            open_gap="Live deployed URL evidence is missing in local development",
            next_evidence="Run deployed smoke against the deployed provider URL after deployment",
            promotion_position="Run after deployment; do not block local iteration",
            recommended_action="run_deployed_provider_smoke_after_deployment",
        )
    status = _safe_status(payload.get("status"), fallback="review")
    base_url = _safe_value(payload.get("base_url"))
    handoff = payload.get("handoff")
    handoff_status = (
        _safe_value(handoff.get("status")) if isinstance(handoff, dict) else "unknown"
    )
    return Phase3RetrievalPromotionGate(
        id="deployed_smoke",
        title="Deployed smoke",
        status=status,
        evidence_paths=[str(smoke_path)],
        evidence_present=True,
        summary=f"status={status}; base_url={base_url}; handoff_status={handoff_status}",
        open_gap="Live deployed URL evidence must be collected before external binding",
        next_evidence="Re-run deployed smoke against the live base URL after deployment",
        promotion_position="Run after deployment; do not block local iteration",
        recommended_action="run_deployed_provider_smoke_after_deployment",
    )


def _build_supporting_seed_baseline(base_dir: Path) -> Phase3SupportingEvidenceItem:
    path = Path(
        "docs/benchmark/chinese-seed/retrieval-candidates/"
        "fixture-chinese-seed-baseline.json"
    )
    payload = _load_json(base_dir, path)
    if payload is None:
        return Phase3SupportingEvidenceItem(
            id="phase3_seed_retrieval_baseline",
            category="retrieval-evidence",
            path=str(path),
            status="review",
            summary="Optional Phase 3 seed baseline evidence is missing.",
            present=False,
            required=False,
            recommended_action="regenerate_phase3_seed_retrieval_baseline",
        )
    summary = payload.get("report", {}).get("summary", {})
    return Phase3SupportingEvidenceItem(
        id="phase3_seed_retrieval_baseline",
        category="retrieval-evidence",
        path=str(path),
        status="ready",
        summary=(
            f"total_cases={_safe_int(summary.get('total_cases'))}; "
            f"hit_rate={_safe_float(summary.get('hit_rate')):.4f}; "
            f"citation_match_rate={_safe_float(summary.get('citation_match_rate')):.4f}; "
            f"empty_handling_rate={_safe_float(summary.get('empty_handling_rate')):.4f}"
        ),
        present=True,
        required=False,
        recommended_action="no_action_required",
    )


def _build_supporting_fp_fn_review(base_dir: Path) -> Phase3SupportingEvidenceItem:
    path = Path("docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json")
    payload = _load_json(base_dir, path)
    if payload is None:
        return Phase3SupportingEvidenceItem(
            id="phase3_fp_fn_review",
            category="retrieval-evidence",
            path=str(path),
            status="review",
            summary="Optional Phase 3 FP/FN review evidence is missing.",
            present=False,
            required=False,
            recommended_action="regenerate_phase3_fp_fn_review",
        )
    return Phase3SupportingEvidenceItem(
        id="phase3_fp_fn_review",
        category="retrieval-evidence",
        path=str(path),
        status="ready",
        summary=(
            f"false_positive_count={_safe_int(payload.get('false_positive_count'))}; "
            f"false_negative_count={_safe_int(payload.get('false_negative_count'))}; "
            f"false_positive_rate={_safe_float(payload.get('false_positive_rate')):.4f}; "
            f"false_negative_rate={_safe_float(payload.get('false_negative_rate')):.4f}"
        ),
        present=True,
        required=False,
        recommended_action="no_action_required",
    )


def _overall_status(gates: list[Phase3RetrievalPromotionGate]) -> str:
    statuses = {gate.status for gate in gates}
    if "blocked" in statuses:
        return "blocked"
    if statuses - {"ready"}:
        return "review"
    return "ready"


def _load_json(base_dir: Path, relative_path: Path) -> dict[str, Any] | None:
    path = base_dir / relative_path
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _report_summary_metrics(payload: dict[str, Any]) -> str:
    summary = payload.get("report", {}).get("summary")
    if isinstance(summary, dict):
        return (
            f"backend={_safe_value(summary.get('backend'))}; "
            f"total_cases={_safe_int(summary.get('total_cases'))}; "
            f"hit_rate={_safe_float(summary.get('hit_rate')):.4f}; "
            f"citation_match_rate={_safe_float(summary.get('citation_match_rate')):.4f}; "
            f"empty_handling_rate={_safe_float(summary.get('empty_handling_rate')):.4f}"
        )
    summary = payload.get("summary")
    if isinstance(summary, dict):
        return (
            f"backend={_safe_value(summary.get('backend'))}; "
            f"total_cases={_safe_int(summary.get('total_cases'))}; "
            f"hit_rate={_safe_float(summary.get('hit_rate')):.4f}; "
            f"citation_match_rate={_safe_float(summary.get('citation_match_rate')):.4f}; "
            f"empty_handling_rate={_safe_float(summary.get('empty_handling_rate')):.4f}"
        )
    return "summary=unavailable"


def _format_criteria_coverage(value: Any) -> str:
    if not isinstance(value, dict):
        return "unavailable"
    ordered = []
    for key in sorted(value.keys()):
        ordered.append(f"{key}={_safe_bool(value.get(key))}")
    return ", ".join(ordered) if ordered else "unavailable"


def _hybrid_gate_summary(payload: dict[str, Any]) -> str:
    summary = payload.get("report", {}).get("summary")
    if not isinstance(summary, dict):
        return "summary=unavailable"
    return (
        f"backend={_safe_value(summary.get('backend'))}; "
        f"total_cases={_safe_int(summary.get('total_cases'))}; "
        f"hit_rate={_safe_float(summary.get('hit_rate')):.4f}; "
        f"citation_match_rate={_safe_float(summary.get('citation_match_rate')):.4f}; "
        f"empty_handling_rate={_safe_float(summary.get('empty_handling_rate')):.4f}"
    )


def _relation_aware_summary(payload: dict[str, Any]) -> str:
    results = payload.get("results")
    if not isinstance(results, list) or not results:
        return "results=unavailable"
    row = results[0]
    if not isinstance(row, dict):
        return "results=unavailable"
    return (
        f"candidate={_safe_value(row.get('candidate', {}).get('id'))}; "
        f"total_cases={_safe_int(row.get('total_cases'))}; "
        f"answer_bearing_rate={_safe_float(row.get('answer_bearing_rate')):.4f}; "
        f"related_insufficient_count={_safe_int(row.get('related_insufficient_count'))}; "
        f"relation_unsupported_count={_safe_int(row.get('relation_unsupported_count'))}; "
        f"missing_evidence_count={_safe_int(row.get('missing_evidence_count'))}; "
        f"unexpected_evidence_count={_safe_int(row.get('unexpected_evidence_count'))}; "
        f"expected_empty_pass_rate={_safe_float(row.get('expected_empty_pass_rate')):.4f}"
    )


def _safe_value(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _safe_bool(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "unknown"


def _safe_int(value: Any) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return 0


def _safe_float(value: Any) -> float:
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _safe_status(value: Any, *, fallback: str) -> str:
    if isinstance(value, str) and value in {"ready", "review", "blocked", "candidate"}:
        return value
    return fallback
