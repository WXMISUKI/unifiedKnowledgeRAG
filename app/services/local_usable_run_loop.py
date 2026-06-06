import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx


LOCAL_USABLE_RUN_LOOP_REPORT_ID = "local-usable-run-loop-v1"
DEFAULT_BASE_URL = "http://127.0.0.1:8020"
DEFAULT_QUERY = "客户三天未发货能否退款？"
DEFAULT_SOURCE_ID = "refund_policy_docs"
DEFAULT_TOP_K = 3
OUTPUT_JSON_FILENAME = "local-usable-run-loop.json"
OUTPUT_MARKDOWN_FILENAME = "local-usable-run-loop.md"


@dataclass(frozen=True)
class LocalRunLoopCheck:
    name: str
    endpoint: str
    status: str
    passed: bool
    http_status_code: int | None = None
    details: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(frozen=True)
class LocalUsableRunLoopReport:
    id: str
    generated_at: str
    base_url: str
    decision: str
    reason_code: str
    query: str
    source_id: str
    top_k: int
    summary: dict[str, Any]
    checks: list[LocalRunLoopCheck]
    recommended_actions: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def run_local_usable_run_loop(
    base_url: str = DEFAULT_BASE_URL,
    *,
    query: str = DEFAULT_QUERY,
    source_id: str = DEFAULT_SOURCE_ID,
    top_k: int = DEFAULT_TOP_K,
    provider_api_key: str | None = None,
    timeout_seconds: float = 5.0,
    client: httpx.Client | None = None,
) -> LocalUsableRunLoopReport:
    normalized_base_url = _normalize_base_url(base_url)
    if client is not None:
        return _run_with_client(
            client,
            base_url=normalized_base_url,
            query=query,
            source_id=source_id,
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
            query=query,
            source_id=source_id,
            top_k=top_k,
            provider_api_key=provider_api_key,
        )


def export_local_usable_run_loop_report(
    output_dir: Path = Path("docs/local-run"),
    *,
    base_url: str = DEFAULT_BASE_URL,
    query: str = DEFAULT_QUERY,
    source_id: str = DEFAULT_SOURCE_ID,
    top_k: int = DEFAULT_TOP_K,
    provider_api_key: str | None = None,
    timeout_seconds: float = 5.0,
    client: httpx.Client | None = None,
) -> LocalUsableRunLoopReport:
    report = run_local_usable_run_loop(
        base_url=base_url,
        query=query,
        source_id=source_id,
        top_k=top_k,
        provider_api_key=provider_api_key,
        timeout_seconds=timeout_seconds,
        client=client,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported_report = LocalUsableRunLoopReport(
        id=report.id,
        generated_at=report.generated_at,
        base_url=report.base_url,
        decision=report.decision,
        reason_code=report.reason_code,
        query=report.query,
        source_id=report.source_id,
        top_k=report.top_k,
        summary=report.summary,
        checks=report.checks,
        recommended_actions=report.recommended_actions,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            local_usable_run_loop_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_local_usable_run_loop_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def local_usable_run_loop_report_to_dict(
    report: LocalUsableRunLoopReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_local_usable_run_loop_markdown(report: LocalUsableRunLoopReport) -> str:
    lines = [
        "# Local Usable Run Loop",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Base URL: `{report.base_url}`",
        f"- Query: `{report.query}`",
        f"- Source ID: `{report.source_id}`",
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
            "## Checks",
            "",
            "| Check | Endpoint | Status | HTTP | Details |",
            "|---|---|---|---|---|",
        ]
    )
    for check in report.checks:
        details = check.error or _format_value(check.details)
        lines.append(
            f"| `{check.name}` | `{check.endpoint}` | `{check.status}` | "
            f"`{check.http_status_code or 'n/a'}` | `{details}` |"
        )

    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    return "\n".join(lines).rstrip() + "\n"


def _run_with_client(
    client: httpx.Client,
    *,
    base_url: str,
    query: str,
    source_id: str,
    top_k: int,
    provider_api_key: str | None,
) -> LocalUsableRunLoopReport:
    auth_headers = _auth_headers(provider_api_key)
    live_check, live_payload = _get_json(client, "/live")
    ready_check, ready_payload = _get_json(
        client,
        "/ready",
        allowed_status_codes={200, 503},
    )
    health_check, health_payload = _get_json(client, "/health")
    manifest_check, manifest_payload = _get_json(
        client,
        "/api/provider/manifest",
        headers=auth_headers,
    )
    preflight_check, preflight_payload = _get_json(
        client,
        "/api/provider/preflight",
        headers=auth_headers,
    )
    retrieve_check, retrieve_payload = _post_json(
        client,
        "/api/rag/retrieve",
        headers=auth_headers,
        payload={
            "query": query,
            "knowledge_base_ids": [source_id],
            "top_k": top_k,
        },
    )
    answer_check, answer_payload = _post_json(
        client,
        "/api/rag/answer",
        headers=auth_headers,
        payload={
            "query": query,
            "knowledge_base_ids": [source_id],
            "top_k": top_k,
        },
    )

    checks = [
        _validate_live(live_check, live_payload),
        _validate_ready(ready_check, ready_payload),
        _validate_health(health_check, health_payload),
        _validate_manifest(manifest_check, manifest_payload),
        _validate_preflight(preflight_check, preflight_payload),
    ]
    retrieve_validated = _validate_retrieve(retrieve_check, retrieve_payload)
    checks.append(retrieve_validated)
    checks.append(_validate_answer(answer_check, answer_payload, retrieve_payload))

    decision, reason_code = _decision(checks)
    return LocalUsableRunLoopReport(
        id=LOCAL_USABLE_RUN_LOOP_REPORT_ID,
        generated_at=datetime.now(UTC).isoformat(),
        base_url=base_url,
        decision=decision,
        reason_code=reason_code,
        query=query,
        source_id=source_id,
        top_k=top_k,
        summary=_summary(
            decision=decision,
            checks=checks,
            retrieve_payload=retrieve_payload,
            answer_payload=answer_payload,
        ),
        checks=checks,
        recommended_actions=_recommended_actions(decision, reason_code),
        notes=_notes(provider_api_key=provider_api_key),
    )


def _get_json(
    client: httpx.Client,
    path: str,
    *,
    headers: dict[str, str] | None = None,
    allowed_status_codes: set[int] | None = None,
) -> tuple[LocalRunLoopCheck, dict[str, Any]]:
    endpoint = f"GET {path}"
    allowed = allowed_status_codes or {200}
    try:
        response = client.get(path, headers=headers)
    except httpx.HTTPError as error:
        return _blocked_check(path, endpoint, f"{error.__class__.__name__}: {error}"), {}
    return _response_json(path, endpoint, response, allowed_status_codes=allowed)


def _post_json(
    client: httpx.Client,
    path: str,
    *,
    payload: dict[str, Any],
    headers: dict[str, str] | None = None,
) -> tuple[LocalRunLoopCheck, dict[str, Any]]:
    endpoint = f"POST {path}"
    try:
        response = client.post(path, headers=headers, json=payload)
    except httpx.HTTPError as error:
        return _blocked_check(path, endpoint, f"{error.__class__.__name__}: {error}"), {}
    return _response_json(path, endpoint, response, allowed_status_codes={200})


def _response_json(
    path: str,
    endpoint: str,
    response: httpx.Response,
    *,
    allowed_status_codes: set[int],
) -> tuple[LocalRunLoopCheck, dict[str, Any]]:
    if response.status_code not in allowed_status_codes:
        return (
            LocalRunLoopCheck(
                name=_check_name(path),
                endpoint=endpoint,
                status="blocked",
                passed=False,
                http_status_code=response.status_code,
                error=f"Unexpected HTTP status {response.status_code}.",
            ),
            {},
        )
    try:
        payload = response.json()
    except ValueError as error:
        return (
            LocalRunLoopCheck(
                name=_check_name(path),
                endpoint=endpoint,
                status="blocked",
                passed=False,
                http_status_code=response.status_code,
                error=f"{error.__class__.__name__}: {error}",
            ),
            {},
        )
    if not isinstance(payload, dict):
        return (
            LocalRunLoopCheck(
                name=_check_name(path),
                endpoint=endpoint,
                status="blocked",
                passed=False,
                http_status_code=response.status_code,
                error=f"Expected JSON object, got {type(payload).__name__}.",
            ),
            {},
        )
    return (
        LocalRunLoopCheck(
            name=_check_name(path),
            endpoint=endpoint,
            status="ready",
            passed=True,
            http_status_code=response.status_code,
        ),
        payload,
    )


def _validate_live(check: LocalRunLoopCheck, payload: dict[str, Any]) -> LocalRunLoopCheck:
    if not check.passed:
        return check
    status = payload.get("status")
    service = payload.get("service")
    passed = service == "unifiedKnowledgeProvider" and status in {"ok", "live"}
    return _replace_check(
        check,
        status="ready" if passed else "blocked",
        passed=passed,
        details={"service": service, "status": status},
        error=None if passed else "Live probe does not match expected provider.",
    )


def _validate_ready(check: LocalRunLoopCheck, payload: dict[str, Any]) -> LocalRunLoopCheck:
    if not check.passed:
        return check
    provider_status = payload.get("status")
    passed = provider_status in {"ok", "degraded"}
    status = "ready" if provider_status == "ok" else "review"
    return _replace_check(
        check,
        status=status if passed else "blocked",
        passed=passed,
        details={"status": provider_status},
        error=None if passed else "Ready probe returned an invalid readiness body.",
    )


def _validate_health(check: LocalRunLoopCheck, payload: dict[str, Any]) -> LocalRunLoopCheck:
    if not check.passed:
        return check
    provider_status = payload.get("status")
    service = payload.get("service")
    passed = service == "unifiedKnowledgeProvider" and provider_status in {"ok", "degraded"}
    status = "ready" if provider_status == "ok" else "review"
    return _replace_check(
        check,
        status=status if passed else "blocked",
        passed=passed,
        details={
            "service": service,
            "status": provider_status,
            "rag_status": (payload.get("rag") or {}).get("status"),
            "answer_status": (payload.get("answer") or {}).get("status"),
        },
        error=None if passed else "Health response does not match expected provider.",
    )


def _validate_manifest(check: LocalRunLoopCheck, payload: dict[str, Any]) -> LocalRunLoopCheck:
    if not check.passed:
        return check
    passed = (
        payload.get("provider_id") == "unifiedKnowledgeProvider"
        and payload.get("contract_version") == "knowledge-provider-contract-v1"
    )
    return _replace_check(
        check,
        status="ready" if passed else "blocked",
        passed=passed,
        details={
            "provider_id": payload.get("provider_id"),
            "contract_version": payload.get("contract_version"),
            "manifest_version": payload.get("manifest_version"),
        },
        error=None if passed else "Provider manifest is incompatible.",
    )


def _validate_preflight(check: LocalRunLoopCheck, payload: dict[str, Any]) -> LocalRunLoopCheck:
    if not check.passed:
        return check
    bindable = payload.get("bindable") is True
    return _replace_check(
        check,
        status="ready" if bindable else "blocked",
        passed=bindable,
        details={
            "bindable": bindable,
            "contract_version": payload.get("contract_version"),
            "check_count": len(payload.get("checks", [])) if isinstance(payload.get("checks"), list) else 0,
        },
        error=None if bindable else "Provider preflight is not bindable.",
    )


def _validate_retrieve(check: LocalRunLoopCheck, payload: dict[str, Any]) -> LocalRunLoopCheck:
    if not check.passed:
        return check
    result = _dict_value(payload.get("result"))
    metadata = _dict_value(result.get("metadata"))
    evidence_pack = _dict_value(metadata.get("evidence_pack"))
    documents = result.get("documents") if isinstance(result.get("documents"), list) else []
    allowed_citations = evidence_pack.get("allowed_citations")
    allowed_citations = allowed_citations if isinstance(allowed_citations, list) else []
    if payload.get("ok") is not True:
        return _replace_check(
            check,
            status="blocked",
            passed=False,
            details={"ok": payload.get("ok"), "error": payload.get("error")},
            error="RAG retrieve returned ok=false.",
        )
    evidence_status = evidence_pack.get("status")
    if evidence_status != "answerable" or not documents or not allowed_citations:
        return _replace_check(
            check,
            status="review",
            passed=True,
            details={
                "ok": True,
                "document_count": len(documents),
                "evidence_pack_status": evidence_status,
                "allowed_citation_count": len(allowed_citations),
            },
            error=None,
        )
    return _replace_check(
        check,
        status="ready",
        passed=True,
        details={
            "ok": True,
            "document_count": len(documents),
            "evidence_pack_status": evidence_status,
            "allowed_citation_count": len(allowed_citations),
        },
        error=None,
    )


def _validate_answer(
    check: LocalRunLoopCheck,
    payload: dict[str, Any],
    retrieve_payload: dict[str, Any],
) -> LocalRunLoopCheck:
    if not check.passed:
        return check
    if payload.get("ok") is not True:
        return _replace_check(
            check,
            status="blocked",
            passed=False,
            details={"ok": payload.get("ok"), "error": payload.get("error")},
            error="RAG answer returned ok=false.",
        )
    result = _dict_value(payload.get("result"))
    citations = result.get("citations") if isinstance(result.get("citations"), list) else []
    answer_status = result.get("answer_status")
    allowed_citations = _allowed_citations_from_retrieve(retrieve_payload)
    invalid_citations = [
        citation
        for citation in citations
        if isinstance(citation, str) and citation not in allowed_citations
    ]
    if invalid_citations:
        return _replace_check(
            check,
            status="blocked",
            passed=False,
            details={
                "answer_status": answer_status,
                "citation_count": len(citations),
                "invalid_citations": invalid_citations,
            },
            error="Answer citations are outside retrieve allowlist.",
        )
    if answer_status != "answered" or not citations:
        return _replace_check(
            check,
            status="review",
            passed=True,
            details={
                "answer_status": answer_status,
                "citation_count": len(citations),
            },
            error=None,
        )
    return _replace_check(
        check,
        status="ready",
        passed=True,
        details={
            "answer_status": answer_status,
            "citation_count": len(citations),
        },
        error=None,
    )


def _replace_check(
    check: LocalRunLoopCheck,
    *,
    status: str,
    passed: bool,
    details: dict[str, Any],
    error: str | None,
) -> LocalRunLoopCheck:
    return LocalRunLoopCheck(
        name=check.name,
        endpoint=check.endpoint,
        status=status,
        passed=passed,
        http_status_code=check.http_status_code,
        details=details,
        error=error,
    )


def _decision(checks: list[LocalRunLoopCheck]) -> tuple[str, str]:
    if any(not check.passed or check.status == "blocked" for check in checks):
        first_blocked = next(
            check for check in checks if not check.passed or check.status == "blocked"
        )
        if first_blocked.error and "ConnectError" in first_blocked.error:
            return "blocked", "local_provider_unreachable"
        return "blocked", f"{first_blocked.name}_blocked"
    if any(check.status == "review" for check in checks):
        first_review = next(check for check in checks if check.status == "review")
        if first_review.name == "rag_retrieve":
            return "review", "retrieval_evidence_needs_review"
        if first_review.name == "rag_answer":
            return "review", "answer_output_needs_review"
        return "review", f"{first_review.name}_needs_review"
    return "go", "local_provider_usable"


def _summary(
    *,
    decision: str,
    checks: list[LocalRunLoopCheck],
    retrieve_payload: dict[str, Any],
    answer_payload: dict[str, Any],
) -> dict[str, Any]:
    result = _dict_value(retrieve_payload.get("result"))
    metadata = _dict_value(result.get("metadata"))
    evidence_pack = _dict_value(metadata.get("evidence_pack"))
    answer_result = _dict_value(answer_payload.get("result"))
    return {
        "decision": decision,
        "ready_checks": sum(1 for check in checks if check.status == "ready"),
        "review_checks": sum(1 for check in checks if check.status == "review"),
        "blocked_checks": sum(1 for check in checks if check.status == "blocked"),
        "retrieve_document_count": len(result.get("documents", [])) if isinstance(result.get("documents"), list) else 0,
        "retrieve_evidence_pack_status": evidence_pack.get("status"),
        "retrieve_allowed_citation_count": len(evidence_pack.get("allowed_citations", [])) if isinstance(evidence_pack.get("allowed_citations"), list) else 0,
        "answer_status": answer_result.get("answer_status"),
        "answer_citation_count": len(answer_result.get("citations", [])) if isinstance(answer_result.get("citations"), list) else 0,
        "runtime_promotion_status": "keep_runtime_defaults",
        "backend_promotion_status": "not_promoted_by_local_run_loop",
        "graph_execution_status": "not_executed",
    }


def _recommended_actions(decision: str, reason_code: str) -> list[str]:
    if decision == "go":
        return [
            "use_http_127_0_0_1_8020_as_local_provider_url",
            "connect_myprivateagent_to_local_provider_when_needed",
            "keep_runtime_defaults_unchanged",
        ]
    if reason_code == "local_provider_unreachable":
        return [
            "start_local_provider_with_uvicorn_app_main_app_reload_port_8020",
            "rerun_export_local_usable_run_loop",
        ]
    if decision == "review":
        return [
            "review_query_source_id_and_fixture_corpus",
            "confirm_default_source_refund_policy_docs_is_available",
            "rerun_local_run_loop_after_adjustment",
        ]
    return [
        "inspect_blocked_check_error_in_local_run_report",
        "fix_provider_contract_or_local_runtime_issue",
        "rerun_local_run_loop_after_fix",
    ]


def _notes(*, provider_api_key: str | None) -> list[str]:
    notes = [
        "This report validates an already-running local provider service.",
        "It does not start uvicorn, download models, start Docker/Qdrant/pgvector, rebuild indexes, create source bindings, promote retrieval defaults, or execute GraphRAG.",
        "The default query and source are fixture-friendly local smoke inputs, not production corpus approval.",
    ]
    if provider_api_key:
        notes.append("Provider API key was supplied for /api calls and is not written to the report.")
    else:
        notes.append("No provider API key was supplied; this is expected for default local development.")
    return notes


def _allowed_citations_from_retrieve(payload: dict[str, Any]) -> set[str]:
    result = _dict_value(payload.get("result"))
    metadata = _dict_value(result.get("metadata"))
    evidence_pack = _dict_value(metadata.get("evidence_pack"))
    allowed = evidence_pack.get("allowed_citations")
    if not isinstance(allowed, list):
        return set()
    return {citation for citation in allowed if isinstance(citation, str)}


def _blocked_check(path: str, endpoint: str, error: str) -> LocalRunLoopCheck:
    return LocalRunLoopCheck(
        name=_check_name(path),
        endpoint=endpoint,
        status="blocked",
        passed=False,
        error=error,
    )


def _dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


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


def _check_name(path: str) -> str:
    return {
        "/live": "live_probe",
        "/ready": "ready_probe",
        "/health": "health_readiness",
        "/api/provider/manifest": "provider_manifest",
        "/api/provider/preflight": "provider_preflight",
        "/api/rag/retrieve": "rag_retrieve",
        "/api/rag/answer": "rag_answer",
    }.get(path, path.strip("/").replace("/", "_") or "root")


def _format_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
