import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from app.main import create_app


APPROVED_LOCAL_CORPUS_ACCEPTANCE_SMOKE_ID = (
    "approved-local-corpus-acceptance-smoke-v1"
)
DEFAULT_SOURCE_ID = "company_profile_2025_trial"
DEFAULT_TOP_K = 3
DEFAULT_OUTPUT_DIR = Path("docs/local-run/approved-local-corpus-acceptance")
OUTPUT_JSON_FILENAME = "approved-local-corpus-acceptance-smoke.json"
OUTPUT_MARKDOWN_FILENAME = "approved-local-corpus-acceptance-smoke.md"


@dataclass(frozen=True)
class AcceptanceCase:
    id: str
    query: str
    expected_mode: str
    description: str


@dataclass(frozen=True)
class AcceptanceCaseResult:
    id: str
    query: str
    expected_mode: str
    status: str
    reason_code: str
    retrieve_ok: bool
    retrieve_count: int
    answer_ok: bool
    answer_status: str | None
    citations: list[str] = field(default_factory=list)
    allowed_citations: list[str] = field(default_factory=list)
    invalid_citations: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ApprovedLocalCorpusAcceptanceSmokeReport:
    id: str
    generated_at: str
    source_id: str
    decision: str
    reason_code: str
    summary: dict[str, Any]
    cases: list[AcceptanceCaseResult]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


DEFAULT_CASES = [
    AcceptanceCase(
        id="business_scope",
        query="公司主营业务是什么？",
        expected_mode="answerable",
        description="Main business scope should be answerable from company profile.",
    ),
    AcceptanceCase(
        id="qualifications",
        query="公司有哪些资质？",
        expected_mode="answerable",
        description="Company qualifications should be answerable from company profile.",
    ),
    AcceptanceCase(
        id="organization",
        query="公司组织机构包括哪些部门？",
        expected_mode="answerable",
        description="Organization departments should be answerable from company profile.",
    ),
    AcceptanceCase(
        id="project_scale",
        query="公司完成过哪些工程规模？",
        expected_mode="answerable",
        description="Historical engineering scale should be answerable from company profile.",
    ),
    AcceptanceCase(
        id="negative_refund_policy",
        query="售后退款凭证规则",
        expected_mode="insufficient_evidence",
        description="Unrelated refund policy should not be answered from company profile.",
    ),
]


def export_approved_local_corpus_acceptance_smoke(
    *,
    source_id: str = DEFAULT_SOURCE_ID,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    case_file: Path | None = None,
    top_k: int = DEFAULT_TOP_K,
    client: TestClient | None = None,
) -> ApprovedLocalCorpusAcceptanceSmokeReport:
    report = run_approved_local_corpus_acceptance_smoke(
        source_id=source_id,
        cases=_load_cases(case_file),
        top_k=top_k,
        client=client,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = ApprovedLocalCorpusAcceptanceSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        source_id=report.source_id,
        decision=report.decision,
        reason_code=report.reason_code,
        summary=report.summary,
        cases=report.cases,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            approved_local_corpus_acceptance_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_approved_local_corpus_acceptance_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_approved_local_corpus_acceptance_smoke(
    *,
    source_id: str = DEFAULT_SOURCE_ID,
    cases: list[AcceptanceCase] | None = None,
    top_k: int = DEFAULT_TOP_K,
    client: TestClient | None = None,
) -> ApprovedLocalCorpusAcceptanceSmokeReport:
    active_client = client or TestClient(create_app())
    active_cases = cases or DEFAULT_CASES
    catalog_result = _catalog_source_check(active_client, source_id)
    manifest_result = _manifest_check(active_client, source_id)

    if catalog_result is not None or manifest_result is not None:
        case_results = [
            result
            for result in [catalog_result, manifest_result]
            if result is not None
        ]
        return _report(
            source_id=source_id,
            cases=case_results,
            decision="blocked",
            reason_code="approved_source_not_ready_for_acceptance",
        )

    case_results = [
        _run_case(active_client, source_id=source_id, case=case, top_k=top_k)
        for case in active_cases
    ]
    decision, reason_code = _decision(case_results)
    return _report(
        source_id=source_id,
        cases=case_results,
        decision=decision,
        reason_code=reason_code,
    )


def approved_local_corpus_acceptance_smoke_report_to_dict(
    report: ApprovedLocalCorpusAcceptanceSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_approved_local_corpus_acceptance_smoke_markdown(
    report: ApprovedLocalCorpusAcceptanceSmokeReport,
) -> str:
    lines = [
        "# Approved Local Corpus Acceptance Smoke",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source ID: `{report.source_id}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Expected | Status | Retrieve | Answer | Citations | Invalid |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for case in report.cases:
        lines.append(
            f"| `{case.id}` | `{case.expected_mode}` | `{case.status}` | "
            f"`{case.retrieve_count}` | `{case.answer_status or 'n/a'}` | "
            f"`{len(case.citations)}` | `{len(case.invalid_citations)}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _catalog_source_check(client: TestClient, source_id: str) -> AcceptanceCaseResult | None:
    response = client.get("/api/rag/sources")
    if response.status_code != 200:
        return _blocked_case("catalog_visibility", "catalog_http_error")
    payload = response.json()
    sources = payload.get("knowledge_bases", [])
    if not any(source.get("id") == source_id for source in sources):
        return _blocked_case("catalog_visibility", "source_not_registered")
    return None


def _manifest_check(client: TestClient, source_id: str) -> AcceptanceCaseResult | None:
    response = client.get(f"/api/rag/sources/{source_id}/documents")
    if response.status_code != 200:
        return _blocked_case("source_manifest", "manifest_http_error")
    payload = response.json()
    if not payload.get("ok"):
        return _blocked_case("source_manifest", "manifest_not_ok")
    documents = payload.get("result", {}).get("documents", [])
    if not documents:
        return _blocked_case("source_manifest", "manifest_documents_missing")
    return None


def _run_case(
    client: TestClient,
    *,
    source_id: str,
    case: AcceptanceCase,
    top_k: int,
) -> AcceptanceCaseResult:
    retrieve_payload = {
        "query": case.query,
        "knowledge_base_ids": [source_id],
        "top_k": top_k,
    }
    retrieve_response = client.post("/api/rag/retrieve", json=retrieve_payload)
    answer_response = client.post("/api/rag/answer", json=retrieve_payload)
    if retrieve_response.status_code != 200 or answer_response.status_code != 200:
        return _case_result(
            case=case,
            status="blocked",
            reason_code="rag_http_error",
            retrieve_ok=False,
            answer_ok=False,
        )

    retrieve = retrieve_response.json()
    answer = answer_response.json()
    retrieve_ok = retrieve.get("ok") is True
    answer_ok = answer.get("ok") is True
    documents = retrieve.get("result", {}).get("documents", []) if retrieve_ok else []
    answer_result = answer.get("result", {}) if answer_ok else {}
    citations = list(answer_result.get("citations") or [])
    allowed_citations = [document.get("citation") for document in documents]
    invalid_citations = [
        citation for citation in citations if citation not in set(allowed_citations)
    ]
    answer_status = answer_result.get("answer_status")
    if invalid_citations:
        status = "blocked"
        reason_code = "answer_citation_outside_retrieval_allowlist"
    elif not retrieve_ok or not answer_ok:
        status = "blocked"
        reason_code = "rag_contract_not_ok"
    elif case.expected_mode == "answerable":
        if documents and answer_status == "answered" and citations:
            status = "ready"
            reason_code = "answerable_case_passed"
        else:
            status = "review"
            reason_code = "expected_answerable_evidence_missing"
    else:
        if not documents and answer_status == "insufficient_evidence" and not citations:
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
        citations=citations,
        allowed_citations=allowed_citations,
        invalid_citations=invalid_citations,
    )


def _decision(cases: list[AcceptanceCaseResult]) -> tuple[str, str]:
    if any(case.status == "blocked" for case in cases):
        return "blocked", "acceptance_blocked"
    if any(case.status == "review" for case in cases):
        return "review", "acceptance_needs_review"
    return "go", "approved_local_corpus_accepted"


def _report(
    *,
    source_id: str,
    cases: list[AcceptanceCaseResult],
    decision: str,
    reason_code: str,
) -> ApprovedLocalCorpusAcceptanceSmokeReport:
    return ApprovedLocalCorpusAcceptanceSmokeReport(
        id=APPROVED_LOCAL_CORPUS_ACCEPTANCE_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        source_id=source_id,
        decision=decision,
        reason_code=reason_code,
        summary={
            "case_count": len(cases),
            "ready_case_count": sum(1 for case in cases if case.status == "ready"),
            "review_case_count": sum(1 for case in cases if case.status == "review"),
            "blocked_case_count": sum(1 for case in cases if case.status == "blocked"),
            "invalid_citation_count": sum(
                len(case.invalid_citations) for case in cases
            ),
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        cases=cases,
        recommended_actions=_recommended_actions(decision),
        non_goals=_non_goals(),
    )


def _case_result(
    *,
    case: AcceptanceCase,
    status: str,
    reason_code: str,
    retrieve_ok: bool,
    retrieve_count: int = 0,
    answer_ok: bool,
    answer_status: str | None = None,
    citations: list[str] | None = None,
    allowed_citations: list[str] | None = None,
    invalid_citations: list[str] | None = None,
) -> AcceptanceCaseResult:
    return AcceptanceCaseResult(
        id=case.id,
        query=case.query,
        expected_mode=case.expected_mode,
        status=status,
        reason_code=reason_code,
        retrieve_ok=retrieve_ok,
        retrieve_count=retrieve_count,
        answer_ok=answer_ok,
        answer_status=answer_status,
        citations=citations or [],
        allowed_citations=allowed_citations or [],
        invalid_citations=invalid_citations or [],
    )


def _blocked_case(case_id: str, reason_code: str) -> AcceptanceCaseResult:
    return AcceptanceCaseResult(
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


def _load_cases(case_file: Path | None) -> list[AcceptanceCase]:
    if case_file is None:
        return DEFAULT_CASES
    payload = json.loads(case_file.read_text(encoding="utf-8"))
    return [
        AcceptanceCase(
            id=str(item["id"]),
            query=str(item["query"]),
            expected_mode=str(item["expected_mode"]),
            description=str(item.get("description", "")),
        )
        for item in payload
    ]


def _recommended_actions(decision: str) -> list[str]:
    if decision == "go":
        return [
            "use_registered_local_corpus_for_myprivateagent_trial",
            "keep_source_to_agent_binding_in_caller_control_plane",
        ]
    if decision == "review":
        return [
            "review_company_profile_page_range_markdown_or_queries",
            "rerun_acceptance_smoke_after_corpus_adjustment",
        ]
    return [
        "register_approved_local_corpus_source_first",
        "fix_blocked_catalog_manifest_or_citation_contract",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_register_sources",
        "does_not_create_source_to_agent_binding",
        "does_not_create_formal_ingestion_job",
        "does_not_start_ocr_services",
        "does_not_promote_retrieval_backend",
        "does_not_run_myprivateagent_orchestration",
        "does_not_call_vector_databases",
        "does_not_execute_graphrag",
    ]
