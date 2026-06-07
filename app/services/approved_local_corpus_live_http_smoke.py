import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx

from app.services.approved_local_corpus_acceptance_smoke import (
    AcceptanceCase,
    AcceptanceCaseResult,
    DEFAULT_CASES,
    DEFAULT_SOURCE_ID,
    DEFAULT_TOP_K,
)


APPROVED_LOCAL_CORPUS_LIVE_HTTP_SMOKE_ID = (
    "approved-local-corpus-live-http-smoke-v1"
)
DEFAULT_BASE_URL = "http://127.0.0.1:8020"
DEFAULT_TIMEOUT_SECONDS = 5.0
DEFAULT_OUTPUT_DIR = Path("docs/local-run/approved-local-corpus-live-http")
OUTPUT_JSON_FILENAME = "approved-local-corpus-live-http-smoke.json"
OUTPUT_MARKDOWN_FILENAME = "approved-local-corpus-live-http-smoke.md"


@dataclass(frozen=True)
class ApprovedLocalCorpusLiveHttpSmokeReport:
    id: str
    generated_at: str
    base_url: str
    source_id: str
    top_k: int
    decision: str
    reason_code: str
    transport_mode: str
    api_key_supplied: bool
    summary: dict[str, Any]
    cases: list[AcceptanceCaseResult]
    recommended_actions: list[str] = field(default_factory=list)
    non_goals: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_approved_local_corpus_live_http_smoke(
    *,
    base_url: str = DEFAULT_BASE_URL,
    source_id: str = DEFAULT_SOURCE_ID,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    case_file: Path | None = None,
    top_k: int = DEFAULT_TOP_K,
    provider_api_key: str | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    client: httpx.Client | None = None,
) -> ApprovedLocalCorpusLiveHttpSmokeReport:
    report = run_approved_local_corpus_live_http_smoke(
        base_url=base_url,
        source_id=source_id,
        cases=_load_cases(case_file),
        top_k=top_k,
        provider_api_key=provider_api_key,
        timeout_seconds=timeout_seconds,
        client=client,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = ApprovedLocalCorpusLiveHttpSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        base_url=report.base_url,
        source_id=report.source_id,
        top_k=report.top_k,
        decision=report.decision,
        reason_code=report.reason_code,
        transport_mode=report.transport_mode,
        api_key_supplied=report.api_key_supplied,
        summary=report.summary,
        cases=report.cases,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            approved_local_corpus_live_http_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_approved_local_corpus_live_http_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_approved_local_corpus_live_http_smoke(
    *,
    base_url: str = DEFAULT_BASE_URL,
    source_id: str = DEFAULT_SOURCE_ID,
    cases: list[AcceptanceCase] | None = None,
    top_k: int = DEFAULT_TOP_K,
    provider_api_key: str | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    client: httpx.Client | None = None,
) -> ApprovedLocalCorpusLiveHttpSmokeReport:
    normalized_base_url = _normalize_base_url(base_url)
    if client is not None:
        return _run_with_client(
            client,
            base_url=normalized_base_url,
            source_id=source_id,
            cases=cases or DEFAULT_CASES,
            top_k=top_k,
            provider_api_key=provider_api_key,
        )

    with httpx.Client(
        base_url=normalized_base_url,
        timeout=timeout_seconds,
        follow_redirects=True,
    ) as http_client:
        return _run_with_client(
            http_client,
            base_url=normalized_base_url,
            source_id=source_id,
            cases=cases or DEFAULT_CASES,
            top_k=top_k,
            provider_api_key=provider_api_key,
        )


def approved_local_corpus_live_http_smoke_report_to_dict(
    report: ApprovedLocalCorpusLiveHttpSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_approved_local_corpus_live_http_smoke_markdown(
    report: ApprovedLocalCorpusLiveHttpSmokeReport,
) -> str:
    lines = [
        "# Approved Local Corpus Live HTTP Smoke",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Base URL: `{report.base_url}`",
        f"- Source ID: `{report.source_id}`",
        f"- Transport: `{report.transport_mode}`",
        f"- API Key Supplied: `{report.api_key_supplied}`",
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
            "| Case | Expected | Status | Reason | Retrieve | Answer | Citations | Invalid |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for case in report.cases:
        lines.append(
            f"| `{case.id}` | `{case.expected_mode}` | `{case.status}` | "
            f"`{case.reason_code}` | `{case.retrieve_count}` | "
            f"`{case.answer_status or 'n/a'}` | `{len(case.citations)}` | "
            f"`{len(case.invalid_citations)}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _run_with_client(
    client: httpx.Client,
    *,
    base_url: str,
    source_id: str,
    cases: list[AcceptanceCase],
    top_k: int,
    provider_api_key: str | None,
) -> ApprovedLocalCorpusLiveHttpSmokeReport:
    headers = _auth_headers(provider_api_key)
    catalog_result = _catalog_source_check(client, source_id, headers=headers)
    manifest_result = _manifest_check(client, source_id, headers=headers)

    if catalog_result is not None or manifest_result is not None:
        case_results = [
            result
            for result in [catalog_result, manifest_result]
            if result is not None
        ]
        return _report(
            base_url=base_url,
            source_id=source_id,
            top_k=top_k,
            cases=case_results,
            decision="blocked",
            reason_code=_blocked_reason(case_results),
            api_key_supplied=provider_api_key is not None,
        )

    case_results = [
        _run_case(client, source_id=source_id, case=case, top_k=top_k, headers=headers)
        for case in cases
    ]
    decision, reason_code = _decision(case_results)
    return _report(
        base_url=base_url,
        source_id=source_id,
        top_k=top_k,
        cases=case_results,
        decision=decision,
        reason_code=reason_code,
        api_key_supplied=provider_api_key is not None,
    )


def _catalog_source_check(
    client: httpx.Client,
    source_id: str,
    *,
    headers: dict[str, str],
) -> AcceptanceCaseResult | None:
    response, error = _get(client, "/api/rag/sources", headers=headers)
    if error is not None:
        return _blocked_case("catalog_visibility", "catalog_http_error", error)
    if response is None or response.status_code != 200:
        return _blocked_case(
            "catalog_visibility",
            "catalog_http_error",
            _http_status_note(response),
        )
    payload, error = _json_object(response)
    if error is not None:
        return _blocked_case("catalog_visibility", "catalog_invalid_json", error)
    sources = payload.get("knowledge_bases", [])
    if not any(source.get("id") == source_id for source in sources):
        return _blocked_case("catalog_visibility", "source_not_registered")
    return None


def _manifest_check(
    client: httpx.Client,
    source_id: str,
    *,
    headers: dict[str, str],
) -> AcceptanceCaseResult | None:
    response, error = _get(
        client,
        f"/api/rag/sources/{source_id}/documents",
        headers=headers,
    )
    if error is not None:
        return _blocked_case("source_manifest", "manifest_http_error", error)
    if response is None or response.status_code != 200:
        return _blocked_case(
            "source_manifest",
            "manifest_http_error",
            _http_status_note(response),
        )
    payload, error = _json_object(response)
    if error is not None:
        return _blocked_case("source_manifest", "manifest_invalid_json", error)
    if not payload.get("ok"):
        return _blocked_case("source_manifest", "manifest_not_ok")
    documents = payload.get("result", {}).get("documents", [])
    if not documents:
        return _blocked_case("source_manifest", "manifest_documents_missing")
    return None


def _run_case(
    client: httpx.Client,
    *,
    source_id: str,
    case: AcceptanceCase,
    top_k: int,
    headers: dict[str, str],
) -> AcceptanceCaseResult:
    payload = {
        "query": case.query,
        "knowledge_base_ids": [source_id],
        "top_k": top_k,
    }
    retrieve_response, retrieve_error = _post(
        client,
        "/api/rag/retrieve",
        headers=headers,
        payload=payload,
    )
    answer_response, answer_error = _post(
        client,
        "/api/rag/answer",
        headers=headers,
        payload=payload,
    )
    if retrieve_error is not None or answer_error is not None:
        return _case_result(
            case=case,
            status="blocked",
            reason_code="rag_http_error",
            retrieve_ok=False,
            answer_ok=False,
            notes=[note for note in [retrieve_error, answer_error] if note],
        )
    if (
        retrieve_response is None
        or answer_response is None
        or retrieve_response.status_code != 200
        or answer_response.status_code != 200
    ):
        return _case_result(
            case=case,
            status="blocked",
            reason_code="rag_http_error",
            retrieve_ok=False,
            answer_ok=False,
            notes=[
                _http_status_note(retrieve_response),
                _http_status_note(answer_response),
            ],
        )

    retrieve, retrieve_json_error = _json_object(retrieve_response)
    answer, answer_json_error = _json_object(answer_response)
    if retrieve_json_error is not None or answer_json_error is not None:
        return _case_result(
            case=case,
            status="blocked",
            reason_code="rag_invalid_json",
            retrieve_ok=False,
            answer_ok=False,
            notes=[
                note for note in [retrieve_json_error, answer_json_error] if note
            ],
        )

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
        return "blocked", _blocked_reason(cases)
    if any(case.status == "review" for case in cases):
        return "review", "live_http_acceptance_needs_review"
    return "go", "approved_local_corpus_live_http_accepted"


def _blocked_reason(cases: list[AcceptanceCaseResult]) -> str:
    if any("ConnectError" in " ".join(case.notes) for case in cases):
        return "local_provider_unreachable"
    first_blocked = next((case for case in cases if case.status == "blocked"), None)
    if first_blocked is None:
        return "live_http_acceptance_blocked"
    return first_blocked.reason_code


def _report(
    *,
    base_url: str,
    source_id: str,
    top_k: int,
    cases: list[AcceptanceCaseResult],
    decision: str,
    reason_code: str,
    api_key_supplied: bool,
) -> ApprovedLocalCorpusLiveHttpSmokeReport:
    return ApprovedLocalCorpusLiveHttpSmokeReport(
        id=APPROVED_LOCAL_CORPUS_LIVE_HTTP_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        base_url=base_url,
        source_id=source_id,
        top_k=top_k,
        decision=decision,
        reason_code=reason_code,
        transport_mode="live_http",
        api_key_supplied=api_key_supplied,
        summary={
            "case_count": len(cases),
            "ready_case_count": sum(1 for case in cases if case.status == "ready"),
            "review_case_count": sum(1 for case in cases if case.status == "review"),
            "blocked_case_count": sum(
                1 for case in cases if case.status == "blocked"
            ),
            "invalid_citation_count": sum(
                len(case.invalid_citations) for case in cases
            ),
            "transport_mode": "live_http",
            "api_key_supplied": api_key_supplied,
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        cases=cases,
        recommended_actions=_recommended_actions(decision, reason_code),
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
    notes: list[str] | None = None,
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
        notes=[note for note in notes or [] if note],
    )


def _blocked_case(
    case_id: str,
    reason_code: str,
    note: str | None = None,
) -> AcceptanceCaseResult:
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
        notes=[note] if note else [],
    )


def _get(
    client: httpx.Client,
    path: str,
    *,
    headers: dict[str, str],
) -> tuple[httpx.Response | None, str | None]:
    try:
        return client.get(path, headers=headers), None
    except httpx.HTTPError as error:
        return None, f"{error.__class__.__name__}: {error}"


def _post(
    client: httpx.Client,
    path: str,
    *,
    headers: dict[str, str],
    payload: dict[str, Any],
) -> tuple[httpx.Response | None, str | None]:
    try:
        return client.post(path, headers=headers, json=payload), None
    except httpx.HTTPError as error:
        return None, f"{error.__class__.__name__}: {error}"


def _json_object(response: httpx.Response) -> tuple[dict[str, Any], str | None]:
    try:
        payload = response.json()
    except ValueError as error:
        return {}, f"{error.__class__.__name__}: {error}"
    if not isinstance(payload, dict):
        return {}, f"Expected JSON object, got {type(payload).__name__}."
    return payload, None


def _http_status_note(response: httpx.Response | None) -> str:
    if response is None:
        return "No HTTP response."
    return f"Unexpected HTTP status {response.status_code}."


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


def _auth_headers(provider_api_key: str | None) -> dict[str, str]:
    if not provider_api_key:
        return {}
    return {
        "Authorization": f"Bearer {provider_api_key}",
        "X-Provider-Api-Key": provider_api_key,
    }


def _normalize_base_url(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if not normalized:
        raise ValueError("base_url must not be empty")
    return normalized


def _recommended_actions(decision: str, reason_code: str) -> list[str]:
    if decision == "go":
        return [
            "use_registered_local_corpus_for_myprivateagent_http_trial",
            "keep_source_to_agent_binding_in_caller_control_plane",
            "move_next_trial_work_to_myprivateagent_repository",
        ]
    if reason_code == "local_provider_unreachable":
        return [
            "start_local_provider_with_uvicorn_app_main_app_reload_port_8020",
            "rerun_approved_local_corpus_live_http_smoke",
        ]
    if decision == "review":
        return [
            "review_company_profile_page_range_markdown_or_queries",
            "rerun_live_http_smoke_after_corpus_adjustment",
        ]
    return [
        "fix_blocked_catalog_manifest_http_or_citation_contract",
        "rerun_live_http_smoke_after_provider_fix",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_start_server",
        "does_not_register_sources",
        "does_not_create_source_to_agent_binding",
        "does_not_create_formal_ingestion_job",
        "does_not_start_ocr_services",
        "does_not_promote_retrieval_backend",
        "does_not_run_myprivateagent_orchestration",
        "does_not_call_vector_databases",
        "does_not_execute_graphrag",
    ]


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
