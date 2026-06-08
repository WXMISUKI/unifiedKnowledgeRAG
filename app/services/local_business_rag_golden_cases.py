import json
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from app.main import create_app


LOCAL_BUSINESS_RAG_GOLDEN_CASES_ID = "local-business-rag-golden-cases-v1"
REAL_BUSINESS_CORPUS_GOLDEN_CASES_ID = "real-business-corpus-golden-cases-v1"
DEFAULT_SOURCE_ID = "company_profile_2025_trial"
DEFAULT_TOP_K = 3
DEFAULT_CASE_FILE = Path(
    "docs/local-run/business-rag-golden-cases/company-profile-golden-cases.json"
)
DEFAULT_AGGREGATE_CASE_FILE = Path(
    "docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.fixture.json"
)
DEFAULT_OUTPUT_DIR = Path("docs/local-run/business-rag-golden-cases")
OUTPUT_JSON_FILENAME = "local-business-rag-golden-cases.json"
OUTPUT_MARKDOWN_FILENAME = "local-business-rag-golden-cases.md"
AGGREGATE_OUTPUT_JSON_FILENAME = "real-business-corpus-golden-cases.json"
AGGREGATE_OUTPUT_MARKDOWN_FILENAME = "real-business-corpus-golden-cases.md"

MIN_CHUNK_COUNT = 1
MAX_TINY_CHUNK_RATIO = 0.45
MIN_CITATION_COVERAGE_RATIO = 0.8
MIN_PAGE_COVERAGE_COUNT = 1
TINY_CHUNK_CHAR_THRESHOLD = 20
NOISY_CHUNK_CHAR_THRESHOLD = 6
MAX_NOISY_SAMPLES = 8


@dataclass(frozen=True)
class LocalBusinessGoldenCase:
    id: str
    query: str
    expected_mode: str
    expected_source_id: str | None
    expected_citation_prefix: str | None
    business_question_type: str
    description: str


@dataclass(frozen=True)
class RealBusinessGoldenCase:
    id: str
    source_id: str
    query: str
    expected_mode: str
    expected_citation_prefix: str | None
    business_question_type: str
    failure_mode: str
    risk_level: str
    description: str


@dataclass(frozen=True)
class LocalBusinessGoldenCaseResult:
    id: str
    query: str
    expected_mode: str
    status: str
    reason_code: str
    retrieve_ok: bool
    retrieve_count: int
    answer_ok: bool
    answer_status: str | None
    expected_source_id: str | None = None
    expected_citation_prefix: str | None = None
    business_question_type: str = ""
    returned_source_ids: list[str] = field(default_factory=list)
    returned_citations: list[str] = field(default_factory=list)
    answer_citations: list[str] = field(default_factory=list)
    invalid_citations: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ChunkQualityDiagnostics:
    status: str
    reason_code: str
    total_chunk_count: int
    tiny_chunk_count: int
    tiny_chunk_ratio: float
    citation_anchor_count: int
    citation_coverage_ratio: float
    page_coverage_count: int
    page_ids: list[str]
    noisy_chunk_samples: list[dict[str, Any]]
    thresholds: dict[str, Any]


@dataclass(frozen=True)
class LocalBusinessRagGoldenCasesReport:
    id: str
    generated_at: str
    source_id: str
    decision: str
    reason_code: str
    top_k: int
    case_file: Path | None
    summary: dict[str, Any]
    chunk_quality: ChunkQualityDiagnostics
    cases: list[LocalBusinessGoldenCaseResult]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class RealBusinessCorpusGoldenCasesReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    top_k: int
    case_file: Path | None
    summary: dict[str, Any]
    source_reports: list[LocalBusinessRagGoldenCasesReport]
    failure_mode_summary: dict[str, int]
    risk_level_summary: dict[str, int]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_local_business_rag_golden_cases(
    *,
    source_id: str = DEFAULT_SOURCE_ID,
    case_file: Path = DEFAULT_CASE_FILE,
    cases: list[LocalBusinessGoldenCase] | None = None,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    client: TestClient | None = None,
) -> LocalBusinessRagGoldenCasesReport:
    report = run_local_business_rag_golden_cases(
        source_id=source_id,
        case_file=case_file,
        cases=cases,
        top_k=top_k,
        client=client,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = LocalBusinessRagGoldenCasesReport(
        id=report.id,
        generated_at=report.generated_at,
        source_id=report.source_id,
        decision=report.decision,
        reason_code=report.reason_code,
        top_k=report.top_k,
        case_file=report.case_file,
        summary=report.summary,
        chunk_quality=report.chunk_quality,
        cases=report.cases,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            local_business_rag_golden_cases_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_local_business_rag_golden_cases_markdown(exported),
        encoding="utf-8",
    )
    return exported


def export_real_business_corpus_golden_cases(
    *,
    case_file: Path = DEFAULT_AGGREGATE_CASE_FILE,
    cases: list[RealBusinessGoldenCase] | None = None,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    client: TestClient | None = None,
) -> RealBusinessCorpusGoldenCasesReport:
    report = run_real_business_corpus_golden_cases(
        case_file=case_file,
        cases=cases,
        top_k=top_k,
        client=client,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / AGGREGATE_OUTPUT_JSON_FILENAME
    markdown_path = output_dir / AGGREGATE_OUTPUT_MARKDOWN_FILENAME
    exported = RealBusinessCorpusGoldenCasesReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        top_k=report.top_k,
        case_file=report.case_file,
        summary=report.summary,
        source_reports=report.source_reports,
        failure_mode_summary=report.failure_mode_summary,
        risk_level_summary=report.risk_level_summary,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            real_business_corpus_golden_cases_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_real_business_corpus_golden_cases_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_real_business_corpus_golden_cases(
    *,
    case_file: Path | None = DEFAULT_AGGREGATE_CASE_FILE,
    cases: list[RealBusinessGoldenCase] | None = None,
    top_k: int = DEFAULT_TOP_K,
    client: TestClient | None = None,
) -> RealBusinessCorpusGoldenCasesReport:
    active_client = client or TestClient(create_app())
    active_cases = cases if cases is not None else _load_aggregate_cases(case_file)
    grouped_cases = _group_real_business_cases_by_source(active_cases)
    source_reports = [
        run_local_business_rag_golden_cases(
            source_id=source_id,
            case_file=None,
            cases=[
                LocalBusinessGoldenCase(
                    id=case.id,
                    query=case.query,
                    expected_mode=case.expected_mode,
                    expected_source_id=case.source_id
                    if case.expected_mode == "answerable"
                    else None,
                    expected_citation_prefix=case.expected_citation_prefix,
                    business_question_type=case.business_question_type,
                    description=case.description,
                )
                for case in source_cases
            ],
            top_k=top_k,
            client=active_client,
        )
        for source_id, source_cases in sorted(grouped_cases.items())
    ]
    decision, reason_code = _aggregate_decision(source_reports)
    return _aggregate_report(
        case_file=case_file,
        cases=active_cases,
        source_reports=source_reports,
        top_k=top_k,
        decision=decision,
        reason_code=reason_code,
    )


def run_local_business_rag_golden_cases(
    *,
    source_id: str = DEFAULT_SOURCE_ID,
    case_file: Path | None = DEFAULT_CASE_FILE,
    cases: list[LocalBusinessGoldenCase] | None = None,
    top_k: int = DEFAULT_TOP_K,
    client: TestClient | None = None,
) -> LocalBusinessRagGoldenCasesReport:
    active_client = client or TestClient(create_app())
    active_cases = cases if cases is not None else _load_cases(case_file)
    manifest = _load_manifest(active_client, source_id)
    if manifest is None:
        blocked_case = _blocked_case("source_manifest", "source_manifest_not_ready")
        chunk_quality = _blocked_chunk_quality("source_manifest_not_ready")
        return _report(
            source_id=source_id,
            top_k=top_k,
            case_file=case_file,
            cases=[blocked_case],
            chunk_quality=chunk_quality,
            decision="blocked",
            reason_code="local_business_rag_baseline_blocked",
        )

    chunk_quality = _build_chunk_quality(manifest)
    case_results = [
        _run_case(active_client, source_id=source_id, case=case, top_k=top_k)
        for case in active_cases
    ]
    decision, reason_code = _decision(case_results, chunk_quality)
    return _report(
        source_id=source_id,
        top_k=top_k,
        case_file=case_file,
        cases=case_results,
        chunk_quality=chunk_quality,
        decision=decision,
        reason_code=reason_code,
    )


def local_business_rag_golden_cases_report_to_dict(
    report: LocalBusinessRagGoldenCasesReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.case_file is not None:
        payload["case_file"] = str(report.case_file)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def real_business_corpus_golden_cases_report_to_dict(
    report: RealBusinessCorpusGoldenCasesReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.case_file is not None:
        payload["case_file"] = str(report.case_file)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_local_business_rag_golden_cases_markdown(
    report: LocalBusinessRagGoldenCasesReport,
) -> str:
    lines = [
        "# Local Business RAG Golden Cases",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source ID: `{report.source_id}`",
        f"- Case File: `{report.case_file}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(
        [
            "",
            "## Chunk Quality",
            "",
            "| Metric | Value |",
            "|---|---|",
        ]
    )
    chunk_payload = asdict(report.chunk_quality)
    for key, value in chunk_payload.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Type | Expected | Status | Reason | Returned Citations |",
            "|---|---|---|---|---|---|",
        ]
    )
    for case in report.cases:
        lines.append(
            f"| `{case.id}` | `{case.business_question_type}` | "
            f"`{case.expected_mode}` | `{case.status}` | `{case.reason_code}` | "
            f"`{', '.join(case.returned_citations)}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def render_real_business_corpus_golden_cases_markdown(
    report: RealBusinessCorpusGoldenCasesReport,
) -> str:
    lines = [
        "# Real Business Corpus Golden Cases",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Case File: `{report.case_file}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(
        [
            "",
            "## Failure Modes",
            "",
            "| Failure Mode | Count |",
            "|---|---|",
        ]
    )
    for key, value in sorted(report.failure_mode_summary.items()):
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Source Reports",
            "",
            "| Source | Decision | Cases | Hit Rate | Citation Match | Empty Handling | Chunk Quality |",
            "|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for source_report in report.source_reports:
        lines.append(
            f"| `{source_report.source_id}` | `{source_report.decision}` | "
            f"`{source_report.summary['case_count']}` | "
            f"`{source_report.summary['hit_rate']}` | "
            f"`{source_report.summary['citation_match_rate']}` | "
            f"`{source_report.summary['empty_handling_rate']}` | "
            f"`{source_report.chunk_quality.status}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _load_manifest(client: TestClient, source_id: str) -> dict[str, Any] | None:
    sources_response = client.get("/api/rag/sources")
    if sources_response.status_code != 200:
        return None
    sources = sources_response.json().get("knowledge_bases", [])
    if not any(source.get("id") == source_id for source in sources):
        return None

    manifest_response = client.get(f"/api/rag/sources/{source_id}/documents")
    if manifest_response.status_code != 200:
        return None
    payload = manifest_response.json()
    if not payload.get("ok"):
        return None
    documents = payload.get("result", {}).get("documents", [])
    if not documents:
        return None
    return payload


def _build_chunk_quality(manifest: dict[str, Any]) -> ChunkQualityDiagnostics:
    documents = manifest.get("result", {}).get("documents", [])
    chunks: list[dict[str, Any]] = []
    citation_anchors: set[str] = set()
    page_ids: set[str] = set()
    for document in documents:
        citation_anchors.update(str(anchor) for anchor in document.get("citation_anchors") or [])
        for chunk in document.get("chunk_manifest") or []:
            chunks.append(chunk)
            citation = str(chunk.get("citation") or "")
            if citation:
                citation_anchors.add(citation)
            preview = str(chunk.get("text_preview") or "")
            page_ids.update(_extract_page_ids(preview))

    total = len(chunks)
    tiny_chunks = [chunk for chunk in chunks if _chunk_char_count(chunk) < TINY_CHUNK_CHAR_THRESHOLD]
    noisy_samples = _noisy_samples(chunks)
    citation_coverage = _rate(len(citation_anchors), total)
    tiny_ratio = _rate(len(tiny_chunks), total)
    status = "ready"
    reasons: list[str] = []
    if total < MIN_CHUNK_COUNT:
        status = "blocked"
        reasons.append("chunk_manifest_empty")
    if tiny_ratio > MAX_TINY_CHUNK_RATIO:
        status = "review" if status != "blocked" else status
        reasons.append("tiny_chunk_ratio_high")
    if citation_coverage < MIN_CITATION_COVERAGE_RATIO:
        status = "review" if status != "blocked" else status
        reasons.append("citation_coverage_low")
    if len(page_ids) < MIN_PAGE_COVERAGE_COUNT:
        status = "review" if status != "blocked" else status
        reasons.append("page_coverage_missing")

    return ChunkQualityDiagnostics(
        status=status,
        reason_code=";".join(reasons) if reasons else "chunk_quality_ready",
        total_chunk_count=total,
        tiny_chunk_count=len(tiny_chunks),
        tiny_chunk_ratio=tiny_ratio,
        citation_anchor_count=len(citation_anchors),
        citation_coverage_ratio=citation_coverage,
        page_coverage_count=len(page_ids),
        page_ids=sorted(page_ids),
        noisy_chunk_samples=noisy_samples,
        thresholds=_thresholds(),
    )


def _run_case(
    client: TestClient,
    *,
    source_id: str,
    case: LocalBusinessGoldenCase,
    top_k: int,
) -> LocalBusinessGoldenCaseResult:
    payload = {
        "query": case.query,
        "knowledge_base_ids": [source_id],
        "top_k": top_k,
    }
    retrieve_response = client.post("/api/rag/retrieve", json=payload)
    answer_response = client.post("/api/rag/answer", json=payload)
    if retrieve_response.status_code != 200 or answer_response.status_code != 200:
        return _case_result(case=case, status="blocked", reason_code="rag_http_error")

    retrieve = retrieve_response.json()
    answer = answer_response.json()
    retrieve_ok = retrieve.get("ok") is True
    answer_ok = answer.get("ok") is True
    if not retrieve_ok or not answer_ok:
        return _case_result(
            case=case,
            status="blocked",
            reason_code="rag_contract_not_ok",
            retrieve_ok=retrieve_ok,
            answer_ok=answer_ok,
        )

    documents = retrieve.get("result", {}).get("documents", [])
    answer_result = answer.get("result", {})
    returned_citations = [str(document.get("citation")) for document in documents]
    returned_source_ids = [str(document.get("source_id")) for document in documents]
    answer_citations = [str(citation) for citation in answer_result.get("citations") or []]
    invalid_citations = [
        citation for citation in answer_citations if citation not in set(returned_citations)
    ]
    answer_status = answer_result.get("answer_status")

    if invalid_citations:
        status = "blocked"
        reason_code = "answer_citation_outside_retrieval_allowlist"
    elif case.expected_mode == "answerable":
        source_hit = case.expected_source_id in set(returned_source_ids)
        citation_hit = _has_prefix(returned_citations, case.expected_citation_prefix)
        answer_hit = (
            answer_status == "answered"
            and _has_prefix(answer_citations, case.expected_citation_prefix)
        )
        if source_hit and citation_hit and answer_hit:
            status = "ready"
            reason_code = "answerable_case_passed"
        else:
            status = "review"
            reason_code = "expected_answerable_evidence_missing"
    else:
        if not documents and answer_status == "insufficient_evidence" and not answer_citations:
            status = "ready"
            reason_code = "negative_control_passed"
        else:
            status = "review"
            reason_code = "negative_control_returned_evidence"

    return _case_result(
        case=case,
        status=status,
        reason_code=reason_code,
        retrieve_ok=retrieve_ok,
        retrieve_count=len(documents),
        answer_ok=answer_ok,
        answer_status=answer_status,
        returned_source_ids=returned_source_ids,
        returned_citations=returned_citations,
        answer_citations=answer_citations,
        invalid_citations=invalid_citations,
    )


def _case_result(
    *,
    case: LocalBusinessGoldenCase,
    status: str,
    reason_code: str,
    retrieve_ok: bool = False,
    retrieve_count: int = 0,
    answer_ok: bool = False,
    answer_status: str | None = None,
    returned_source_ids: list[str] | None = None,
    returned_citations: list[str] | None = None,
    answer_citations: list[str] | None = None,
    invalid_citations: list[str] | None = None,
) -> LocalBusinessGoldenCaseResult:
    return LocalBusinessGoldenCaseResult(
        id=case.id,
        query=case.query,
        expected_mode=case.expected_mode,
        status=status,
        reason_code=reason_code,
        retrieve_ok=retrieve_ok,
        retrieve_count=retrieve_count,
        answer_ok=answer_ok,
        answer_status=answer_status,
        expected_source_id=case.expected_source_id,
        expected_citation_prefix=case.expected_citation_prefix,
        business_question_type=case.business_question_type,
        returned_source_ids=returned_source_ids or [],
        returned_citations=returned_citations or [],
        answer_citations=answer_citations or [],
        invalid_citations=invalid_citations or [],
    )


def _blocked_case(case_id: str, reason_code: str) -> LocalBusinessGoldenCaseResult:
    return LocalBusinessGoldenCaseResult(
        id=case_id,
        query="",
        expected_mode="provider_contract",
        status="blocked",
        reason_code=reason_code,
        retrieve_ok=False,
        retrieve_count=0,
        answer_ok=False,
        answer_status=None,
    )


def _blocked_chunk_quality(reason_code: str) -> ChunkQualityDiagnostics:
    return ChunkQualityDiagnostics(
        status="blocked",
        reason_code=reason_code,
        total_chunk_count=0,
        tiny_chunk_count=0,
        tiny_chunk_ratio=0.0,
        citation_anchor_count=0,
        citation_coverage_ratio=0.0,
        page_coverage_count=0,
        page_ids=[],
        noisy_chunk_samples=[],
        thresholds=_thresholds(),
    )


def _decision(
    cases: list[LocalBusinessGoldenCaseResult],
    chunk_quality: ChunkQualityDiagnostics,
) -> tuple[str, str]:
    if chunk_quality.status == "blocked" or any(case.status == "blocked" for case in cases):
        return "blocked", "local_business_rag_baseline_blocked"
    if chunk_quality.status == "review" or any(case.status == "review" for case in cases):
        return "review", "local_business_rag_baseline_needs_review"
    return "go", "local_business_rag_baseline_go"


def _report(
    *,
    source_id: str,
    top_k: int,
    case_file: Path | None,
    cases: list[LocalBusinessGoldenCaseResult],
    chunk_quality: ChunkQualityDiagnostics,
    decision: str,
    reason_code: str,
) -> LocalBusinessRagGoldenCasesReport:
    answerable = [case for case in cases if case.expected_mode == "answerable"]
    expected_empty = [
        case for case in cases if case.expected_mode == "insufficient_evidence"
    ]
    hit_count = sum(
        1
        for case in answerable
        if case.expected_source_id in set(case.returned_source_ids)
    )
    citation_match_count = sum(
        1
        for case in answerable
        if _has_prefix(case.returned_citations, case.expected_citation_prefix)
    )
    empty_pass_count = sum(
        1
        for case in expected_empty
        if case.status == "ready" and case.retrieve_count == 0 and not case.answer_citations
    )
    invalid_citation_count = sum(len(case.invalid_citations) for case in cases)
    review_case_ids = [case.id for case in cases if case.status == "review"]
    blocked_case_ids = [case.id for case in cases if case.status == "blocked"]
    return LocalBusinessRagGoldenCasesReport(
        id=LOCAL_BUSINESS_RAG_GOLDEN_CASES_ID,
        generated_at=datetime.now(UTC).isoformat(),
        source_id=source_id,
        decision=decision,
        reason_code=reason_code,
        top_k=top_k,
        case_file=case_file,
        summary={
            "case_count": len(cases),
            "answerable_case_count": len(answerable),
            "expected_empty_case_count": len(expected_empty),
            "hit_rate": _rate(hit_count, len(answerable)),
            "citation_match_rate": _rate(citation_match_count, len(answerable)),
            "empty_handling_rate": _rate(empty_pass_count, len(expected_empty)),
            "invalid_citation_count": invalid_citation_count,
            "review_case_ids": review_case_ids,
            "blocked_case_ids": blocked_case_ids,
            "chunk_quality_status": chunk_quality.status,
            "chunk_quality_reason": chunk_quality.reason_code,
            "runtime_promotion_status": "keep_runtime_defaults",
            "source_binding_status": "not_created",
            "graph_execution_status": "not_executed",
            "final_decision": decision,
        },
        chunk_quality=chunk_quality,
        cases=cases,
        recommended_actions=_recommended_actions(decision, chunk_quality),
        non_goals=_non_goals(),
    )


def _load_cases(case_file: Path | None) -> list[LocalBusinessGoldenCase]:
    if case_file is None:
        return []
    payload = json.loads(case_file.read_text(encoding="utf-8"))
    return [
        LocalBusinessGoldenCase(
            id=str(item["id"]),
            query=str(item["query"]),
            expected_mode=str(item["expected_mode"]),
            expected_source_id=(
                str(item["expected_source_id"])
                if item.get("expected_source_id") is not None
                else None
            ),
            expected_citation_prefix=(
                str(item["expected_citation_prefix"])
                if item.get("expected_citation_prefix") is not None
                else None
            ),
            business_question_type=str(item.get("business_question_type") or ""),
            description=str(item.get("description") or ""),
        )
        for item in payload
    ]


def _load_aggregate_cases(case_file: Path | None) -> list[RealBusinessGoldenCase]:
    if case_file is None:
        return []
    payload = json.loads(case_file.read_text(encoding="utf-8"))
    return [
        RealBusinessGoldenCase(
            id=str(item["case_id"]),
            source_id=str(item["source_id"]),
            query=str(item["query"]),
            expected_mode=str(item["expected_mode"]),
            expected_citation_prefix=(
                str(item["expected_citation_prefix"])
                if item.get("expected_citation_prefix") is not None
                else None
            ),
            business_question_type=str(item.get("business_question_type") or ""),
            failure_mode=str(item.get("failure_mode") or "unclassified"),
            risk_level=str(item.get("risk_level") or "medium"),
            description=str(item.get("description") or ""),
        )
        for item in payload
    ]


def _group_real_business_cases_by_source(
    cases: list[RealBusinessGoldenCase],
) -> dict[str, list[RealBusinessGoldenCase]]:
    grouped: dict[str, list[RealBusinessGoldenCase]] = {}
    for case in cases:
        grouped.setdefault(case.source_id, []).append(case)
    return grouped


def _aggregate_decision(
    source_reports: list[LocalBusinessRagGoldenCasesReport],
) -> tuple[str, str]:
    if any(report.decision == "blocked" for report in source_reports):
        return "blocked", "real_business_corpus_baseline_blocked"
    if any(report.decision == "review" for report in source_reports):
        return "review", "real_business_corpus_baseline_needs_review"
    return "go", "real_business_corpus_baseline_go"


def _aggregate_report(
    *,
    case_file: Path | None,
    cases: list[RealBusinessGoldenCase],
    source_reports: list[LocalBusinessRagGoldenCasesReport],
    top_k: int,
    decision: str,
    reason_code: str,
) -> RealBusinessCorpusGoldenCasesReport:
    answerable_count = sum(
        report.summary["answerable_case_count"] for report in source_reports
    )
    expected_empty_count = sum(
        report.summary["expected_empty_case_count"] for report in source_reports
    )
    case_count = sum(report.summary["case_count"] for report in source_reports)
    invalid_citation_count = sum(
        report.summary["invalid_citation_count"] for report in source_reports
    )
    blocked_sources = [
        report.source_id for report in source_reports if report.decision == "blocked"
    ]
    review_sources = [
        report.source_id for report in source_reports if report.decision == "review"
    ]
    return RealBusinessCorpusGoldenCasesReport(
        id=REAL_BUSINESS_CORPUS_GOLDEN_CASES_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        top_k=top_k,
        case_file=case_file,
        summary={
            "source_count": len(source_reports),
            "case_count": case_count,
            "answerable_case_count": answerable_count,
            "expected_empty_case_count": expected_empty_count,
            "hit_rate": _weighted_rate(source_reports, "hit_rate", "answerable_case_count"),
            "citation_match_rate": _weighted_rate(
                source_reports,
                "citation_match_rate",
                "answerable_case_count",
            ),
            "empty_handling_rate": _weighted_rate(
                source_reports,
                "empty_handling_rate",
                "expected_empty_case_count",
            ),
            "invalid_citation_count": invalid_citation_count,
            "review_sources": review_sources,
            "blocked_sources": blocked_sources,
            "runtime_promotion_status": "keep_runtime_defaults",
            "source_binding_status": "not_created",
            "graph_execution_status": "not_executed",
            "final_decision": decision,
        },
        source_reports=source_reports,
        failure_mode_summary=_count_by(cases, "failure_mode"),
        risk_level_summary=_count_by(cases, "risk_level"),
        recommended_actions=_aggregate_recommended_actions(
            decision,
            failure_mode_summary=_count_by(cases, "failure_mode"),
        ),
        non_goals=_non_goals(),
    )


def _weighted_rate(
    source_reports: list[LocalBusinessRagGoldenCasesReport],
    rate_key: str,
    weight_key: str,
) -> float:
    numerator = 0.0
    denominator = 0
    for report in source_reports:
        weight = int(report.summary.get(weight_key) or 0)
        numerator += float(report.summary.get(rate_key) or 0.0) * weight
        denominator += weight
    if denominator == 0:
        return 1.0
    return round(numerator / denominator, 4)


def _count_by(cases: list[RealBusinessGoldenCase], field_name: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for case in cases:
        value = getattr(case, field_name) or "unclassified"
        counts[value] = counts.get(value, 0) + 1
    return counts


def _aggregate_recommended_actions(
    decision: str,
    *,
    failure_mode_summary: dict[str, int],
) -> list[str]:
    if decision == "go":
        return [
            "add_more_real_business_documents_or_real_failed_questions",
            "keep_advanced_rag_strategies_unpromoted_until_failures_appear",
        ]
    actions = ["review_failed_sources_and_cases_before_strategy_changes"]
    if failure_mode_summary.get("chunking"):
        actions.append("consider_chunk_merging_or_contextual_headers_candidate")
    if failure_mode_summary.get("query_mismatch"):
        actions.append("consider_query_rewrite_candidate")
    if failure_mode_summary.get("retrieval_quality"):
        actions.append("consider_rerank_or_hybrid_candidate")
    if failure_mode_summary.get("graph_use_case"):
        actions.append("open_graphrag_use_case_gate")
    if len(actions) == 1:
        actions.append("classify_real_failure_modes_before_choosing_next_gate")
    return actions


def _noisy_samples(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for chunk in chunks:
        preview = str(chunk.get("text_preview") or "")
        visible_text = _strip_citation_comment(preview)
        if (
            _chunk_char_count(chunk) < TINY_CHUNK_CHAR_THRESHOLD
            or len(_semantic_chars(visible_text)) < NOISY_CHUNK_CHAR_THRESHOLD
        ):
            samples.append(
                {
                    "chunk_id": chunk.get("chunk_id"),
                    "citation": chunk.get("citation"),
                    "char_count": _chunk_char_count(chunk),
                    "text_preview": preview[:120],
                }
            )
        if len(samples) >= MAX_NOISY_SAMPLES:
            break
    return samples


def _chunk_char_count(chunk: dict[str, Any]) -> int:
    value = chunk.get("char_count")
    if isinstance(value, int):
        return value
    return len(str(chunk.get("text_preview") or ""))


def _extract_page_ids(value: str) -> set[str]:
    return set(re.findall(r"#(page-\d+)", value))


def _strip_citation_comment(value: str) -> str:
    return re.sub(r"<!--.*?-->", "", value).strip()


def _semantic_chars(value: str) -> str:
    return "".join(re.findall(r"[A-Za-z0-9\u4e00-\u9fff]", value))


def _has_prefix(values: list[str], prefix: str | None) -> bool:
    if prefix is None:
        return True
    return any(value.startswith(prefix) for value in values)


def _recommended_actions(
    decision: str,
    chunk_quality: ChunkQualityDiagnostics,
) -> list[str]:
    if decision == "go":
        return [
            "reuse_golden_cases_before_future_rag_strategy_changes",
            "continue_testing_more_real_business_documents",
            "keep_runtime_defaults_until_candidate_evidence_passes",
        ]
    if decision == "review":
        actions = [
            "review_failed_golden_cases_or_negative_controls",
            "rerun_baseline_before_advanced_rag_candidate_review",
        ]
        if chunk_quality.status == "review":
            actions.insert(0, "review_tiny_or_noisy_chunks_before_changing_chunk_defaults")
        return actions
    return [
        "restore_approved_source_catalog_manifest_or_chunk_artifacts",
        "rerun_local_business_rag_golden_cases_after_source_readiness_is_restored",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_change_public_http_apis",
        "does_not_create_source_to_agent_binding",
        "does_not_call_myprivateagent",
        "does_not_start_or_adopt_parser_engines",
        "does_not_promote_qdrant_pgvector_bge_m3_hybrid_or_rerankers",
        "does_not_enable_query_rewrite_hyde_hype_raptor_or_self_rag",
        "does_not_execute_graphrag",
        "does_not_change_runtime_retrieval_defaults",
    ]


def _thresholds() -> dict[str, Any]:
    return {
        "min_chunk_count": MIN_CHUNK_COUNT,
        "max_tiny_chunk_ratio": MAX_TINY_CHUNK_RATIO,
        "min_citation_coverage_ratio": MIN_CITATION_COVERAGE_RATIO,
        "min_page_coverage_count": MIN_PAGE_COVERAGE_COUNT,
        "tiny_chunk_char_threshold": TINY_CHUNK_CHAR_THRESHOLD,
        "noisy_chunk_char_threshold": NOISY_CHUNK_CHAR_THRESHOLD,
    }


def _rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 1.0
    return round(numerator / denominator, 4)


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
