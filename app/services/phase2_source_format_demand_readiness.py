import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE2_SOURCE_FORMAT_DEMAND_READINESS_ID = "phase2-source-format-demand-readiness-v1"
PHASE2_SOURCE_BINDING_SUMMARY_PATH = Path(
    "docs/integration/source-bindings/provider-source-bindings.json"
)
PHASE2_PARSER_EXPANSION_DEMAND_CONTRACT_PATH = Path(
    "docs/operations/source-format-demand/phase2-parser-expansion-demand-contract.md"
)
PHASE2_SOURCE_FORMAT_DEMAND_READINESS_JSON = "phase2-source-format-demand-readiness.json"
PHASE2_SOURCE_FORMAT_DEMAND_READINESS_MARKDOWN = (
    "phase2-source-format-demand-readiness.md"
)
PHASE2_DEFERRED_FORMATS = ["pdf", "word", "excel", "ocr", "table-structure"]


@dataclass(frozen=True)
class Phase2SourceFormatDemandReadinessArtifact:
    id: str
    category: str
    path: str
    status: str
    summary: str
    present: bool
    required: bool
    recommended_action: str


@dataclass(frozen=True)
class Phase2SourceFormatDemandReadinessReport:
    id: str
    generated_at: str
    status: str
    decision: str
    baseline_parser: str
    deferred_formats: list[str]
    contract_path: str
    source_binding_path: str
    summary: dict[str, Any]
    open_gate_ids: list[str]
    supporting_evidence: list[Phase2SourceFormatDemandReadinessArtifact]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase2_source_format_demand_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase2SourceFormatDemandReadinessReport:
    contract_artifact = _build_contract_artifact(base_dir)
    source_binding_artifact, source_binding_payload = _build_source_binding_artifact(
        base_dir
    )
    summary = _summary_from_payload(source_binding_payload)
    demand_signal = bool(summary["format_expansion_demand_signal"])
    open_gate_ids = _open_gate_ids(demand_signal)
    status = _overall_status(
        contract_artifact=contract_artifact,
        source_binding_artifact=source_binding_artifact,
        demand_signal=demand_signal,
    )
    supporting_evidence = [contract_artifact, source_binding_artifact]
    return Phase2SourceFormatDemandReadinessReport(
        id=PHASE2_SOURCE_FORMAT_DEMAND_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_markdown_baseline",
        baseline_parser="markdown",
        deferred_formats=PHASE2_DEFERRED_FORMATS,
        contract_path=str(PHASE2_PARSER_EXPANSION_DEMAND_CONTRACT_PATH),
        source_binding_path=str(PHASE2_SOURCE_BINDING_SUMMARY_PATH),
        summary=summary,
        open_gate_ids=open_gate_ids,
        supporting_evidence=supporting_evidence,
        notes=[
            "This report is local, read-only evidence for Phase 2 parser-expansion demand review.",
            "It uses source-binding evidence to summarize real format demand without enabling non-Markdown runtime parsing.",
            "It does not change ingestion defaults, retrieval defaults, deployment ownership boundaries, or GraphRAG boundaries.",
        ],
    )


def phase2_source_format_demand_readiness_report_to_dict(
    report: Phase2SourceFormatDemandReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase2_source_format_demand_readiness_markdown(
    report: Phase2SourceFormatDemandReadinessReport,
) -> str:
    lines = [
        "# Phase 2 Source Format Demand Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Baseline Parser: `{report.baseline_parser}`",
        f"- Deferred Formats: `{', '.join(report.deferred_formats)}`",
        f"- Contract Doc: `{report.contract_path}`",
        f"- Source Binding Evidence: `{report.source_binding_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Sources | `{report.summary['total_sources']}` |",
        f"| Bindable Sources | `{report.summary['bindable_sources']}` |",
        f"| Markdown-Only Sources | `{report.summary['markdown_only_sources']}` |",
        f"| Non-Markdown Sources | `{report.summary['non_markdown_sources']}` |",
        f"| Parser-Ready Documents | `{report.summary['parser_ready_documents']}` |",
        f"| Unsupported Documents | `{report.summary['unsupported_documents']}` |",
        f"| Source Binding Ready | `{report.summary['source_binding_ready']}` |",
        f"| Demand Signal | `{report.summary['format_expansion_demand_signal']}` |",
        f"| Open Gate Count | `{report.summary['open_gate_count']}` |",
        "",
        "## Supporting Evidence",
        "",
        "| Evidence | Category | Status | Summary |",
        "|---|---|---|---|",
    ]
    for item in report.supporting_evidence:
        lines.append(
            f"| `{item.id}` | `{item.category}` | `{item.status}` | {item.summary} |"
        )
    lines.extend(["", "## Open Gates", ""])
    if report.open_gate_ids:
        lines.extend(f"- `{gate}`" for gate in report.open_gate_ids)
    else:
        lines.append("- `none`")
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase2_source_format_demand_readiness_report(
    output_dir: Path = Path("docs/operations/source-format-demand"),
    *,
    base_dir: Path = Path("."),
) -> Phase2SourceFormatDemandReadinessReport:
    report = build_phase2_source_format_demand_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE2_SOURCE_FORMAT_DEMAND_READINESS_JSON
    markdown_path = output_dir / PHASE2_SOURCE_FORMAT_DEMAND_READINESS_MARKDOWN
    exported_report = Phase2SourceFormatDemandReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        baseline_parser=report.baseline_parser,
        deferred_formats=report.deferred_formats,
        contract_path=report.contract_path,
        source_binding_path=report.source_binding_path,
        summary=report.summary,
        open_gate_ids=report.open_gate_ids,
        supporting_evidence=report.supporting_evidence,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase2_source_format_demand_readiness_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase2_source_format_demand_readiness_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _build_contract_artifact(
    base_dir: Path,
) -> Phase2SourceFormatDemandReadinessArtifact:
    path = base_dir / PHASE2_PARSER_EXPANSION_DEMAND_CONTRACT_PATH
    if not path.exists():
        return Phase2SourceFormatDemandReadinessArtifact(
            id="phase2_parser_expansion_demand_contract",
            category="contract",
            path=str(PHASE2_PARSER_EXPANSION_DEMAND_CONTRACT_PATH),
            status="blocked",
            summary="Phase 2 parser expansion demand contract document is missing.",
            present=False,
            required=True,
            recommended_action="regenerate_phase2_parser_expansion_demand_contract",
        )
    return Phase2SourceFormatDemandReadinessArtifact(
        id="phase2_parser_expansion_demand_contract",
        category="contract",
        path=str(PHASE2_PARSER_EXPANSION_DEMAND_CONTRACT_PATH),
        status="ready",
        summary="contract_doc_present=True",
        present=True,
        required=True,
        recommended_action="no_action_required",
    )


def _build_source_binding_artifact(
    base_dir: Path,
) -> tuple[Phase2SourceFormatDemandReadinessArtifact, dict[str, Any]]:
    path = base_dir / PHASE2_SOURCE_BINDING_SUMMARY_PATH
    if not path.exists():
        return (
            Phase2SourceFormatDemandReadinessArtifact(
                id="source_binding_summary",
                category="source-binding",
                path=str(PHASE2_SOURCE_BINDING_SUMMARY_PATH),
                status="blocked",
                summary="Source binding summary artifact is missing.",
                present=False,
                required=True,
                recommended_action="regenerate_source_binding_summary",
            ),
            {},
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    status = payload.get("status", "review")
    normalized_status = (
        status if status in {"ready", "review", "blocked"} else "review"
    )
    source_count = _int_value(
        payload.get("total_source_count"),
        fallback=len(payload.get("sources", [])),
    )
    unsupported_documents = _sum_source_int(payload.get("sources", []), "unsupported_document_count")
    non_markdown_sources = _count_non_markdown_sources(payload.get("sources", []))
    parser_ready_documents = _sum_source_int(payload.get("sources", []), "parser_ready_document_count")
    return (
        Phase2SourceFormatDemandReadinessArtifact(
            id="source_binding_summary",
            category="source-binding",
            path=str(PHASE2_SOURCE_BINDING_SUMMARY_PATH),
            status=normalized_status,
            summary=(
                f"status={status}; sources={source_count}; "
                f"parser_ready_documents={parser_ready_documents}; "
                f"unsupported_documents={unsupported_documents}; "
                f"non_markdown_sources={non_markdown_sources}"
            ),
            present=True,
            required=True,
            recommended_action=(
                "no_action_required"
                if normalized_status == "ready"
                else "review_source_binding_evidence"
            ),
        ),
        payload,
    )


def _summary_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    sources = payload.get("sources", [])
    if not isinstance(sources, list):
        sources = []
    total_sources = _int_value(payload.get("total_source_count"), fallback=len(sources))
    bindable_sources = _int_value(
        payload.get("bindable_source_count"),
        fallback=sum(
            1 for source in sources if isinstance(source, dict) and source.get("bindable") is True
        ),
    )
    markdown_only_sources = _count_markdown_only_sources(sources)
    non_markdown_sources = _count_non_markdown_sources(sources)
    parser_ready_documents = _sum_source_int(sources, "parser_ready_document_count")
    unsupported_documents = _sum_source_int(sources, "unsupported_document_count")
    source_binding_status = payload.get("status", "review")
    source_binding_ready = source_binding_status == "ready"
    format_expansion_demand_signal = (
        non_markdown_sources > 0 or unsupported_documents > 0
    )
    return {
        "total_sources": total_sources,
        "bindable_sources": bindable_sources,
        "markdown_only_sources": markdown_only_sources,
        "non_markdown_sources": non_markdown_sources,
        "parser_ready_documents": parser_ready_documents,
        "unsupported_documents": unsupported_documents,
        "source_binding_status": source_binding_status,
        "source_binding_ready": source_binding_ready,
        "source_status_counts": _dict_counts(payload.get("status_counts")),
        "recommended_action_counts": _dict_counts(
            payload.get("recommended_action_counts")
        ),
        "supported_format_counts": _supported_format_counts(sources),
        "parser_status_counts": _parser_status_counts(sources),
        "format_expansion_demand_signal": format_expansion_demand_signal,
        "open_gate_count": 4 if format_expansion_demand_signal else 0,
    }


def _open_gate_ids(demand_signal: bool) -> list[str]:
    if not demand_signal:
        return []
    return [
        "customer_like_format_benchmark",
        "parser_false_positive_false_negative_review",
        "parser_latency_resource_review",
        "parser_deployment_ownership_review",
    ]


def _overall_status(
    *,
    contract_artifact: Phase2SourceFormatDemandReadinessArtifact,
    source_binding_artifact: Phase2SourceFormatDemandReadinessArtifact,
    demand_signal: bool,
) -> str:
    if contract_artifact.status == "blocked" or source_binding_artifact.status == "blocked":
        return "blocked"
    if source_binding_artifact.status == "review":
        return "review"
    if demand_signal:
        return "review"
    return "ready"


def _sum_source_int(sources: list[Any], field_name: str) -> int:
    total = 0
    for source in sources:
        if not isinstance(source, dict):
            continue
        total += _int_value(source.get(field_name), fallback=0)
    return total


def _count_markdown_only_sources(sources: list[Any]) -> int:
    count = 0
    for source in sources:
        if not isinstance(source, dict):
            continue
        formats = _source_formats(source)
        if formats and all(fmt == "markdown" for fmt in formats):
            count += 1
    return count


def _count_non_markdown_sources(sources: list[Any]) -> int:
    count = 0
    for source in sources:
        if not isinstance(source, dict):
            continue
        formats = _source_formats(source)
        if any(fmt != "markdown" for fmt in formats):
            count += 1
    return count


def _supported_format_counts(sources: list[Any]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for source in sources:
        if not isinstance(source, dict):
            continue
        for fmt in _source_formats(source):
            counter[fmt] += 1
    return dict(sorted(counter.items()))


def _parser_status_counts(sources: list[Any]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for source in sources:
        if not isinstance(source, dict):
            continue
        parser_statuses = source.get("parser_statuses", [])
        if not isinstance(parser_statuses, list):
            continue
        for status in parser_statuses:
            if isinstance(status, str) and status:
                counter[status] += 1
    return dict(sorted(counter.items()))


def _source_formats(source: dict[str, Any]) -> list[str]:
    supported_formats = source.get("supported_formats", [])
    if not isinstance(supported_formats, list):
        return []
    formats: list[str] = []
    for item in supported_formats:
        if isinstance(item, str) and item:
            formats.append(item.lower())
    return formats


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback


def _dict_counts(value: Any) -> dict[str, int]:
    if not isinstance(value, dict):
        return {}
    counts: dict[str, int] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            continue
        normalized_value = _int_value(item, fallback=0)
        if normalized_value > 0:
            counts[key] = normalized_value
    return dict(sorted(counts.items()))
