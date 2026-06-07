import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from app.main import create_app


PARSER_DERIVED_CORPUS_QUALITY_BASELINE_ID = (
    "parser-derived-corpus-retrieval-quality-baseline-v1"
)
DEFAULT_SOURCE_ID = "company_profile_2025_trial"
DEFAULT_TOP_K = 3
DEFAULT_CASE_FILE = Path(
    "docs/local-run/parser-derived-corpus-retrieval-quality-baseline/company-profile-quality-cases.json"
)
DEFAULT_OUTPUT_DIR = Path("docs/local-run/parser-derived-corpus-retrieval-quality-baseline")
OUTPUT_JSON_FILENAME = "parser-derived-corpus-retrieval-quality-baseline.json"
OUTPUT_MARKDOWN_FILENAME = "parser-derived-corpus-retrieval-quality-baseline.md"


@dataclass(frozen=True)
class ParserDerivedQualityCase:
    id: str
    query: str
    expected_mode: str
    expected_source_id: str | None
    expected_citation: str | None
    category: str
    description: str


@dataclass(frozen=True)
class ParserDerivedQualityCaseResult:
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
    expected_citation: str | None = None
    returned_source_ids: list[str] = field(default_factory=list)
    returned_citations: list[str] = field(default_factory=list)
    answer_citations: list[str] = field(default_factory=list)
    invalid_citations: list[str] = field(default_factory=list)
    category: str = ""


@dataclass(frozen=True)
class ParserDerivedCorpusRetrievalQualityBaselineReport:
    id: str
    generated_at: str
    source_id: str
    decision: str
    reason_code: str
    top_k: int
    case_file: Path | None
    summary: dict[str, Any]
    cases: list[ParserDerivedQualityCaseResult]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_parser_derived_corpus_retrieval_quality_baseline(
    *,
    source_id: str = DEFAULT_SOURCE_ID,
    case_file: Path = DEFAULT_CASE_FILE,
    cases: list[ParserDerivedQualityCase] | None = None,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    client: TestClient | None = None,
) -> ParserDerivedCorpusRetrievalQualityBaselineReport:
    report = run_parser_derived_corpus_retrieval_quality_baseline(
        source_id=source_id,
        case_file=case_file,
        cases=cases,
        top_k=top_k,
        client=client,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = ParserDerivedCorpusRetrievalQualityBaselineReport(
        id=report.id,
        generated_at=report.generated_at,
        source_id=report.source_id,
        decision=report.decision,
        reason_code=report.reason_code,
        top_k=report.top_k,
        case_file=report.case_file,
        summary=report.summary,
        cases=report.cases,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            parser_derived_quality_baseline_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_parser_derived_quality_baseline_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_parser_derived_corpus_retrieval_quality_baseline(
    *,
    source_id: str = DEFAULT_SOURCE_ID,
    case_file: Path | None = DEFAULT_CASE_FILE,
    cases: list[ParserDerivedQualityCase] | None = None,
    top_k: int = DEFAULT_TOP_K,
    client: TestClient | None = None,
) -> ParserDerivedCorpusRetrievalQualityBaselineReport:
    active_client = client or TestClient(create_app())
    active_cases = cases if cases is not None else _load_cases(case_file)
    readiness_blocker = _source_readiness_blocker(active_client, source_id)
    if readiness_blocker is not None:
        return _report(
            source_id=source_id,
            top_k=top_k,
            case_file=case_file,
            cases=[readiness_blocker],
            decision="blocked",
            reason_code="parser_derived_source_not_ready",
        )

    results = [
        _run_case(active_client, source_id=source_id, case=case, top_k=top_k)
        for case in active_cases
    ]
    decision, reason_code = _decision(results)
    return _report(
        source_id=source_id,
        top_k=top_k,
        case_file=case_file,
        cases=results,
        decision=decision,
        reason_code=reason_code,
    )


def parser_derived_quality_baseline_report_to_dict(
    report: ParserDerivedCorpusRetrievalQualityBaselineReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.case_file is not None:
        payload["case_file"] = str(report.case_file)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_parser_derived_quality_baseline_markdown(
    report: ParserDerivedCorpusRetrievalQualityBaselineReport,
) -> str:
    lines = [
        "# Parser-Derived Corpus Retrieval Quality Baseline",
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
            "## Cases",
            "",
            "| Case | Expected | Status | Reason | Returned Citations |",
            "|---|---|---|---|---|",
        ]
    )
    for case in report.cases:
        lines.append(
            f"| `{case.id}` | `{case.expected_mode}` | `{case.status}` | "
            f"`{case.reason_code}` | `{', '.join(case.returned_citations)}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _source_readiness_blocker(
    client: TestClient,
    source_id: str,
) -> ParserDerivedQualityCaseResult | None:
    sources_response = client.get("/api/rag/sources")
    if sources_response.status_code != 200:
        return _blocked_case("catalog_visibility", "catalog_http_error")
    sources = sources_response.json().get("knowledge_bases", [])
    if not any(source.get("id") == source_id for source in sources):
        return _blocked_case("catalog_visibility", "source_not_registered")

    manifest_response = client.get(f"/api/rag/sources/{source_id}/documents")
    if manifest_response.status_code != 200:
        return _blocked_case("source_manifest", "manifest_http_error")
    manifest = manifest_response.json()
    if not manifest.get("ok") or not manifest.get("result", {}).get("documents"):
        return _blocked_case("source_manifest", "manifest_not_ready")
    return None


def _run_case(
    client: TestClient,
    *,
    source_id: str,
    case: ParserDerivedQualityCase,
    top_k: int,
) -> ParserDerivedQualityCaseResult:
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
        citation_hit = case.expected_citation in set(returned_citations)
        answer_hit = answer_status == "answered" and case.expected_citation in set(answer_citations)
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
    case: ParserDerivedQualityCase,
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
) -> ParserDerivedQualityCaseResult:
    return ParserDerivedQualityCaseResult(
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
        expected_citation=case.expected_citation,
        returned_source_ids=returned_source_ids or [],
        returned_citations=returned_citations or [],
        answer_citations=answer_citations or [],
        invalid_citations=invalid_citations or [],
        category=case.category,
    )


def _blocked_case(case_id: str, reason_code: str) -> ParserDerivedQualityCaseResult:
    return ParserDerivedQualityCaseResult(
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


def _decision(cases: list[ParserDerivedQualityCaseResult]) -> tuple[str, str]:
    if any(case.status == "blocked" for case in cases):
        return "blocked", "parser_derived_corpus_quality_blocked"
    if any(case.status == "review" for case in cases):
        return "review", "parser_derived_corpus_quality_needs_review"
    return "go", "parser_derived_corpus_quality_baseline_go"


def _report(
    *,
    source_id: str,
    top_k: int,
    case_file: Path | None,
    cases: list[ParserDerivedQualityCaseResult],
    decision: str,
    reason_code: str,
) -> ParserDerivedCorpusRetrievalQualityBaselineReport:
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
        if case.expected_citation in set(case.returned_citations)
    )
    empty_pass_count = sum(
        1
        for case in expected_empty
        if case.status == "ready" and case.retrieve_count == 0 and not case.answer_citations
    )
    invalid_citation_count = sum(len(case.invalid_citations) for case in cases)
    review_case_ids = [case.id for case in cases if case.status == "review"]
    blocked_case_ids = [case.id for case in cases if case.status == "blocked"]
    return ParserDerivedCorpusRetrievalQualityBaselineReport(
        id=PARSER_DERIVED_CORPUS_QUALITY_BASELINE_ID,
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
            "runtime_promotion_status": "keep_runtime_defaults",
            "source_binding_status": "not_created",
            "graph_execution_status": "not_executed",
            "final_decision": decision,
        },
        cases=cases,
        recommended_actions=_recommended_actions(decision),
        non_goals=_non_goals(),
    )


def _load_cases(case_file: Path | None) -> list[ParserDerivedQualityCase]:
    if case_file is None:
        return []
    payload = json.loads(case_file.read_text(encoding="utf-8"))
    return [
        ParserDerivedQualityCase(
            id=str(item["id"]),
            query=str(item["query"]),
            expected_mode=str(item["expected_mode"]),
            expected_source_id=(
                str(item["expected_source_id"])
                if item.get("expected_source_id") is not None
                else None
            ),
            expected_citation=(
                str(item["expected_citation"])
                if item.get("expected_citation") is not None
                else None
            ),
            category=str(item.get("category") or ""),
            description=str(item.get("description") or ""),
        )
        for item in payload
    ]


def _recommended_actions(decision: str) -> list[str]:
    if decision == "go":
        return [
            "use_quality_baseline_as_stage4_candidate_backend_input",
            "keep_runtime_defaults_until_candidate_backend_review_passes",
        ]
    if decision == "review":
        return [
            "review_parser_derived_markdown_chunks_citations_or_queries",
            "rerun_quality_baseline_before_backend_candidate_review",
        ]
    return [
        "fix_parser_derived_source_registration_manifest_or_rag_contract",
        "rerun_quality_baseline_after_source_readiness_is_restored",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_parse_raw_pdf",
        "does_not_start_ocr_services",
        "does_not_create_ingestion_jobs",
        "does_not_call_myprivateagent",
        "does_not_create_source_to_agent_binding",
        "does_not_mutate_chat_runtime",
        "does_not_promote_qdrant_pgvector_bge_m3_hybrid_or_rerankers",
        "does_not_execute_graphrag",
    ]


def _rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 1.0
    return round(numerator / denominator, 4)


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
