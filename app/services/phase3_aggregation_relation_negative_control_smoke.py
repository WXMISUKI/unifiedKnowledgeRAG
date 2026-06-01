import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE3_AGGREGATION_RELATION_NEGATIVE_CONTROL_SMOKE_ID = (
    "phase3-aggregation-relation-negative-control-smoke-v1"
)
PHASE3_AGGREGATION_CANDIDATE_PATH = Path(
    "docs/benchmark/chinese-seed/multi-chunk-aggregation-candidates/"
    "qdrant-bge-m3-hybrid-multi-chunk-aggregation.json"
)
PHASE3_AGGREGATION_NEGATIVE_CONTROL_PATH = Path(
    "docs/benchmark/chinese-seed/multi-chunk-aggregation-negative-controls/"
    "qdrant-bge-m3-hybrid-multi-chunk-aggregation.json"
)
PHASE3_RELATION_AWARE_GRADING_PATH = Path(
    "docs/benchmark/chinese-seed/relation-aware-aggregation-grading/"
    "relation-aware-aggregation-grading.json"
)


@dataclass(frozen=True)
class Phase3AggregationRelationNegativeControlSmokeCheck:
    id: str
    status: str
    summary: str
    recommended_action: str
    evidence_path: str | None = None


@dataclass(frozen=True)
class Phase3AggregationRelationNegativeControlSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    source_paths: dict[str, str]
    checks: list[Phase3AggregationRelationNegativeControlSmokeCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase3_aggregation_relation_negative_control_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase3AggregationRelationNegativeControlSmokeReport:
    aggregation_payload = _read_json_if_present(base_dir / PHASE3_AGGREGATION_CANDIDATE_PATH)
    negative_payload = _read_json_if_present(base_dir / PHASE3_AGGREGATION_NEGATIVE_CONTROL_PATH)
    relation_payload = _read_json_if_present(base_dir / PHASE3_RELATION_AWARE_GRADING_PATH)

    checks = [
        _check_aggregation_positive_control(aggregation_payload),
        _check_aggregation_negative_control(negative_payload),
        _check_relation_aware_labeling(relation_payload),
        _check_relation_aware_summary(relation_payload),
    ]
    summary = _summary(checks, relation_payload=relation_payload)
    return Phase3AggregationRelationNegativeControlSmokeReport(
        id=PHASE3_AGGREGATION_RELATION_NEGATIVE_CONTROL_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(checks),
        decision="keep_runtime_defaults",
        summary=summary,
        source_paths={
            "aggregation_candidate": str(PHASE3_AGGREGATION_CANDIDATE_PATH),
            "aggregation_negative_control": str(PHASE3_AGGREGATION_NEGATIVE_CONTROL_PATH),
            "relation_aware_grading": str(PHASE3_RELATION_AWARE_GRADING_PATH),
        },
        checks=checks,
        notes=[
            "This smoke reuses existing aggregation and relation-aware grading evidence.",
            "It is read-only and does not execute retrieval backends.",
            "Smoke readiness reflects negative-control visibility, not runtime promotion approval.",
        ],
    )


def phase3_aggregation_relation_negative_control_smoke_report_to_dict(
    report: Phase3AggregationRelationNegativeControlSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_aggregation_relation_negative_control_smoke_markdown(
    report: Phase3AggregationRelationNegativeControlSmokeReport,
) -> str:
    lines = [
        "# Phase 3 Aggregation Relation Negative-Control Smoke Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Aggregation Candidate Source: `{report.source_paths['aggregation_candidate']}`",
        f"- Aggregation Negative-Control Source: `{report.source_paths['aggregation_negative_control']}`",
        f"- Relation-Aware Grading Source: `{report.source_paths['relation_aware_grading']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Checks | `{report.summary['total_checks']}` |",
        f"| Passed Checks | `{report.summary['passed_checks']}` |",
        f"| Failed Checks | `{report.summary['failed_checks']}` |",
        f"| Open Check IDs | `{json.dumps(report.summary['open_check_ids'])}` |",
        "",
        "## Checks",
        "",
        "| Check | Status | Summary | Recommended Action |",
        "|---|---|---|---|",
    ]
    for check in report.checks:
        lines.append(
            f"| `{check.id}` | `{check.status}` | {check.summary} | `{check.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase3_aggregation_relation_negative_control_smoke_report(
    output_dir: Path = Path("docs/smoke/aggregation-relation-negative-control"),
    *,
    base_dir: Path = Path("."),
) -> Phase3AggregationRelationNegativeControlSmokeReport:
    report = build_phase3_aggregation_relation_negative_control_smoke_report(
        base_dir=base_dir,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3-aggregation-relation-negative-control-smoke.json"
    markdown_path = output_dir / "phase3-aggregation-relation-negative-control-smoke.md"
    exported = Phase3AggregationRelationNegativeControlSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        source_paths=report.source_paths,
        checks=report.checks,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_aggregation_relation_negative_control_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_aggregation_relation_negative_control_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _check_aggregation_positive_control(
    aggregation_payload: dict[str, Any] | None,
) -> Phase3AggregationRelationNegativeControlSmokeCheck:
    if aggregation_payload is None:
        return Phase3AggregationRelationNegativeControlSmokeCheck(
            id="aggregation_positive_control",
            status="blocked",
            summary="Aggregation candidate evidence is missing.",
            recommended_action="regenerate_multi_chunk_aggregation_evidence",
            evidence_path=str(PHASE3_AGGREGATION_CANDIDATE_PATH),
        )
    report = aggregation_payload.get("report") if isinstance(aggregation_payload, dict) else None
    summary = report.get("summary") if isinstance(report, dict) else {}
    cases = report.get("cases") if isinstance(report, dict) else []
    case_map = {case.get("id"): case for case in cases if isinstance(case, dict)}
    split_case = case_map.get("split-chunk-refund-policy-and-form")
    passed = bool(split_case and split_case.get("hit_at_k") is True and split_case.get("citation_match") is True)
    return _check(
        id="aggregation_positive_control",
        passed=passed,
        summary=(
            f"backend={_dict_value(summary, 'backend', 'unknown')}; "
            f"total_cases={_int_value(summary.get('total_cases'), fallback=0)}; "
            f"hit_rate={_float_value(summary.get('hit_rate'), fallback=0.0):.4f}; "
            f"citation_match_rate={_float_value(summary.get('citation_match_rate'), fallback=0.0):.4f}; "
            f"split_case_hit_at_k={bool(split_case.get('hit_at_k')) if split_case else False}"
        ),
        ready_action="no_action_required",
        review_action="regenerate_multi_chunk_aggregation_evidence",
        evidence_path=str(PHASE3_AGGREGATION_CANDIDATE_PATH),
    )


def _check_aggregation_negative_control(
    negative_payload: dict[str, Any] | None,
) -> Phase3AggregationRelationNegativeControlSmokeCheck:
    if negative_payload is None:
        return Phase3AggregationRelationNegativeControlSmokeCheck(
            id="aggregation_negative_control",
            status="blocked",
            summary="Negative-control evidence is missing.",
            recommended_action="regenerate_multi_chunk_aggregation_negative_control",
            evidence_path=str(PHASE3_AGGREGATION_NEGATIVE_CONTROL_PATH),
        )
    report = negative_payload.get("report") if isinstance(negative_payload, dict) else None
    summary = report.get("summary") if isinstance(report, dict) else {}
    cases = report.get("cases") if isinstance(report, dict) else []
    case_map = {case.get("id"): case for case in cases if isinstance(case, dict)}
    negative_case = case_map.get("multi-chunk-empty-unsupported-form-policy-link")
    passed = bool(
        negative_case
        and negative_case.get("hit_at_k") is False
        and negative_case.get("citation_match") is False
        and negative_case.get("empty_query_handling") is False
    )
    return _check(
        id="aggregation_negative_control",
        passed=passed,
        summary=(
            f"backend={_dict_value(summary, 'backend', 'unknown')}; "
            f"total_cases={_int_value(summary.get('total_cases'), fallback=0)}; "
            f"hit_rate={_float_value(summary.get('hit_rate'), fallback=0.0):.4f}; "
            f"citation_match_rate={_float_value(summary.get('citation_match_rate'), fallback=0.0):.4f}; "
            f"empty_handling_rate={_float_value(summary.get('empty_handling_rate'), fallback=0.0):.4f}; "
            f"negative_case_hit_at_k={bool(negative_case.get('hit_at_k')) if negative_case else False}"
        ),
        ready_action="no_action_required",
        review_action="regenerate_multi_chunk_aggregation_negative_control",
        evidence_path=str(PHASE3_AGGREGATION_NEGATIVE_CONTROL_PATH),
    )


def _check_relation_aware_labeling(
    relation_payload: dict[str, Any] | None,
) -> Phase3AggregationRelationNegativeControlSmokeCheck:
    if relation_payload is None:
        return Phase3AggregationRelationNegativeControlSmokeCheck(
            id="relation_aware_labeling",
            status="blocked",
            summary="Relation-aware grading evidence is missing.",
            recommended_action="regenerate_relation_aware_aggregation_grading",
            evidence_path=str(PHASE3_RELATION_AWARE_GRADING_PATH),
        )
    results = relation_payload.get("results") if isinstance(relation_payload, dict) else []
    if not isinstance(results, list) or not results:
        return Phase3AggregationRelationNegativeControlSmokeCheck(
            id="relation_aware_labeling",
            status="blocked",
            summary="Relation-aware grading results are unavailable.",
            recommended_action="regenerate_relation_aware_aggregation_grading",
            evidence_path=str(PHASE3_RELATION_AWARE_GRADING_PATH),
        )
    result = results[0] if isinstance(results[0], dict) else {}
    cases = result.get("cases", []) if isinstance(result, dict) else []
    relation_case = next(
        (
            case
            for case in cases
            if isinstance(case, dict)
            and case.get("case_id") == "multi-chunk-empty-unsupported-form-policy-link"
        ),
        None,
    )
    passed = bool(relation_case and relation_case.get("grading_label") == "relation_unsupported")
    return _check(
        id="relation_aware_labeling",
        passed=passed,
        summary=(
            f"candidate={_dict_value(result.get('candidate', {}), 'id', 'unknown')}; "
            f"label={(relation_case or {}).get('grading_label', 'missing')}; "
            f"reason={(relation_case or {}).get('grading_reason', 'missing')}"
        ),
        ready_action="no_action_required",
        review_action="regenerate_relation_aware_aggregation_grading",
        evidence_path=str(PHASE3_RELATION_AWARE_GRADING_PATH),
    )


def _check_relation_aware_summary(
    relation_payload: dict[str, Any] | None,
) -> Phase3AggregationRelationNegativeControlSmokeCheck:
    if relation_payload is None:
        return Phase3AggregationRelationNegativeControlSmokeCheck(
            id="relation_aware_summary",
            status="blocked",
            summary="Relation-aware grading summary is missing.",
            recommended_action="regenerate_relation_aware_aggregation_grading",
            evidence_path=str(PHASE3_RELATION_AWARE_GRADING_PATH),
        )
    results = relation_payload.get("results") if isinstance(relation_payload, dict) else []
    result = results[0] if isinstance(results, list) and results and isinstance(results[0], dict) else {}
    total_cases = _int_value(result.get("total_cases"), fallback=0)
    expected_empty_pass_rate = _float_value(
        result.get("expected_empty_pass_rate"),
        fallback=0.0,
    )
    relation_unsupported_count = _int_value(
        result.get("relation_unsupported_count"),
        fallback=0,
    )
    unexpected_evidence_count = _int_value(
        result.get("unexpected_evidence_count"),
        fallback=0,
    )
    passed = (
        total_cases > 0
        and expected_empty_pass_rate == 1.0
        and relation_unsupported_count >= 1
        and unexpected_evidence_count == 0
    )
    return _check(
        id="relation_aware_summary",
        passed=passed,
        summary=(
            f"total_cases={total_cases}; "
            f"answer_bearing_rate={_float_value(result.get('answer_bearing_rate'), fallback=0.0):.4f}; "
            f"relation_unsupported_count={relation_unsupported_count}; "
            f"unexpected_evidence_count={unexpected_evidence_count}; "
            f"expected_empty_pass_rate={expected_empty_pass_rate:.4f}"
        ),
        ready_action="no_action_required",
        review_action="regenerate_relation_aware_aggregation_grading",
        evidence_path=str(PHASE3_RELATION_AWARE_GRADING_PATH),
    )


def _check(
    *,
    id: str,
    passed: bool,
    summary: str,
    ready_action: str,
    review_action: str,
    evidence_path: str | None,
) -> Phase3AggregationRelationNegativeControlSmokeCheck:
    return Phase3AggregationRelationNegativeControlSmokeCheck(
        id=id,
        status="ready" if passed else "review",
        summary=summary,
        recommended_action=ready_action if passed else review_action,
        evidence_path=evidence_path,
    )


def _summary(
    checks: list[Phase3AggregationRelationNegativeControlSmokeCheck],
    *,
    relation_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    summary = {
        "total_checks": len(checks),
        "passed_checks": sum(1 for check in checks if check.status == "ready"),
        "failed_checks": sum(1 for check in checks if check.status == "review"),
        "open_check_ids": [check.id for check in checks if check.status != "ready"],
    }
    if isinstance(relation_payload, dict):
        results = relation_payload.get("results", [])
        result = results[0] if isinstance(results, list) and results and isinstance(results[0], dict) else {}
        summary["relation_unsupported_count"] = _int_value(
            result.get("relation_unsupported_count"),
            fallback=0,
        )
        summary["expected_empty_pass_rate"] = _float_value(
            result.get("expected_empty_pass_rate"),
            fallback=0.0,
        )
    return summary


def _overall_status(checks: list[Phase3AggregationRelationNegativeControlSmokeCheck]) -> str:
    if any(check.status == "blocked" for check in checks):
        return "blocked"
    if any(check.status == "review" for check in checks):
        return "review"
    return "ready"


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


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
