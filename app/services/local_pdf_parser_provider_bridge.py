import base64
import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable

import httpx

from app.services.approved_local_corpus_acceptance_smoke import DEFAULT_TOP_K
from app.services.local_business_corpus_trial import DEFAULT_QUERY, DEFAULT_SOURCE_ID, DEFAULT_TITLE
from app.services.parser_artifact_local_ingestion_loop import (
    export_parser_artifact_local_ingestion_loop_report,
)


LOCAL_PDF_PARSER_PROVIDER_BRIDGE_ID = "local-pdf-parser-provider-bridge-v1"
DEFAULT_PDF_PATH = Path(
    r"D:\xwechat_files\wxid_pc6sc451nt9022_dea0\msg\file\2026-06\公司简介2025年10月27日(1).pdf"
)
DEFAULT_PROVIDER_URL = "http://127.0.0.1:8080"
DEFAULT_PROVIDER_PATH = "/ocr"
DEFAULT_OUTPUT_DIR = Path("docs/local-run/local-pdf-parser-provider-bridge")
OUTPUT_JSON_FILENAME = "local-pdf-parser-provider-bridge.json"
OUTPUT_MARKDOWN_FILENAME = "local-pdf-parser-provider-bridge.md"
PARSER_ARTIFACT_FILENAME = "local-pdf-parser-artifact.json"
DEFAULT_MAX_PAGES = 5


@dataclass(frozen=True)
class LocalPdfParserProviderBridgeStep:
    id: str
    status: str
    reason_code: str
    artifacts: dict[str, str | None]
    summary: dict[str, Any]


@dataclass(frozen=True)
class LocalPdfParserProviderBridgeReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    pdf_path: Path
    provider_url: str
    provider_path: str
    source_id: str
    title: str
    query: str
    top_k: int
    max_pages: int
    artifact_path: Path | None
    downstream: dict[str, Any]
    steps: list[LocalPdfParserProviderBridgeStep]
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_local_pdf_parser_provider_bridge_report(
    *,
    pdf_path: Path = DEFAULT_PDF_PATH,
    provider_url: str = DEFAULT_PROVIDER_URL,
    provider_path: str = DEFAULT_PROVIDER_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    max_pages: int = DEFAULT_MAX_PAGES,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    client: httpx.Client | None = None,
    downstream_exporter: Callable[..., Any] = export_parser_artifact_local_ingestion_loop_report,
) -> LocalPdfParserProviderBridgeReport:
    report = run_local_pdf_parser_provider_bridge(
        pdf_path=pdf_path,
        provider_url=provider_url,
        provider_path=provider_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        max_pages=max_pages,
        output_dir=output_dir,
        client=client,
        downstream_exporter=downstream_exporter,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = LocalPdfParserProviderBridgeReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        pdf_path=report.pdf_path,
        provider_url=report.provider_url,
        provider_path=report.provider_path,
        source_id=report.source_id,
        title=report.title,
        query=report.query,
        top_k=report.top_k,
        max_pages=report.max_pages,
        artifact_path=report.artifact_path,
        downstream=report.downstream,
        steps=report.steps,
        summary=report.summary,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(local_pdf_parser_provider_bridge_report_to_dict(exported), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(render_local_pdf_parser_provider_bridge_markdown(exported), encoding="utf-8")
    return exported


def run_local_pdf_parser_provider_bridge(
    *,
    pdf_path: Path = DEFAULT_PDF_PATH,
    provider_url: str = DEFAULT_PROVIDER_URL,
    provider_path: str = DEFAULT_PROVIDER_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    max_pages: int = DEFAULT_MAX_PAGES,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    client: httpx.Client | None = None,
    downstream_exporter: Callable[..., Any] = export_parser_artifact_local_ingestion_loop_report,
) -> LocalPdfParserProviderBridgeReport:
    normalized_pdf_path = pdf_path.expanduser()
    steps: list[LocalPdfParserProviderBridgeStep] = []
    if max_pages <= 0:
        return _blocked_report(
            reason_code="invalid_max_pages",
            pdf_path=normalized_pdf_path,
            provider_url=provider_url,
            provider_path=provider_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            max_pages=max_pages,
            steps=steps,
            summary={"input_status": "invalid_max_pages"},
        )
    if not normalized_pdf_path.exists():
        return _blocked_report(
            reason_code="pdf_file_missing",
            pdf_path=normalized_pdf_path,
            provider_url=provider_url,
            provider_path=provider_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            max_pages=max_pages,
            steps=steps,
            summary={"input_status": "missing"},
        )
    if normalized_pdf_path.suffix.lower() != ".pdf":
        return _blocked_report(
            reason_code="input_must_be_pdf",
            pdf_path=normalized_pdf_path,
            provider_url=provider_url,
            provider_path=provider_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            max_pages=max_pages,
            steps=steps,
            summary={"input_status": "unsupported_format"},
        )

    payload = _paddlex_ocr_payload(normalized_pdf_path, max_pages=max_pages)
    provider_payload, provider_error = _post_provider(
        provider_url=provider_url,
        provider_path=provider_path,
        payload=payload,
        client=client,
    )
    if provider_error is not None or provider_payload is None:
        steps.append(
            LocalPdfParserProviderBridgeStep(
                id="parser_provider_call",
                status="blocked",
                reason_code="parser_provider_unreachable",
                artifacts={},
                summary={"provider_error": provider_error},
            )
        )
        return _blocked_report(
            reason_code="parser_provider_unreachable",
            pdf_path=normalized_pdf_path,
            provider_url=provider_url,
            provider_path=provider_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            max_pages=max_pages,
            steps=steps,
            summary={"provider_status": "unreachable"},
        )

    if _provider_error_code(provider_payload) not in (None, "0"):
        steps.append(
            LocalPdfParserProviderBridgeStep(
                id="parser_provider_call",
                status="blocked",
                reason_code="parser_provider_error",
                artifacts={},
                summary={
                    "provider_error_code": _provider_error_code(provider_payload),
                    "provider_error_message": provider_payload.get("errorMsg"),
                },
            )
        )
        return _blocked_report(
            reason_code="parser_provider_error",
            pdf_path=normalized_pdf_path,
            provider_url=provider_url,
            provider_path=provider_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            max_pages=max_pages,
            steps=steps,
            summary={"provider_status": "error"},
        )

    text_blocks = _normalize_text_blocks(provider_payload, source_id=source_id, max_pages=max_pages)
    steps.append(
        LocalPdfParserProviderBridgeStep(
            id="parser_provider_call",
            status="go" if text_blocks else "blocked",
            reason_code="parser_provider_text_ready" if text_blocks else "parser_provider_returned_no_text",
            artifacts={},
            summary={
                "text_block_count": len(text_blocks),
                "requested_max_pages": max_pages,
                "provider_error_code": _provider_error_code(provider_payload),
            },
        )
    )
    if not text_blocks:
        return _blocked_report(
            reason_code="parser_provider_returned_no_text",
            pdf_path=normalized_pdf_path,
            provider_url=provider_url,
            provider_path=provider_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            max_pages=max_pages,
            steps=steps,
            summary={"provider_status": "no_text"},
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / "parser-artifacts" / PARSER_ARTIFACT_FILENAME
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact = _artifact_payload(
        pdf_path=normalized_pdf_path,
        provider_url=provider_url,
        provider_path=provider_path,
        source_id=source_id,
        title=title,
        max_pages=max_pages,
        text_blocks=text_blocks,
        raw_provider_payload=provider_payload,
    )
    artifact_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    steps.append(
        LocalPdfParserProviderBridgeStep(
            id="normalized_parser_artifact",
            status="go",
            reason_code="normalized_parser_artifact_written",
            artifacts={"artifact": str(artifact_path)},
            summary={
                "artifact_id": artifact["artifact_id"],
                "source_id": source_id,
                "text_block_count": len(text_blocks),
            },
        )
    )

    downstream_report = downstream_exporter(
        artifact_path=artifact_path,
        query=query,
        top_k=top_k,
        output_dir=output_dir / "parser-artifact-local-ingestion-loop",
    )
    downstream = _downstream_summary(downstream_report)
    downstream_decision = str(getattr(downstream_report, "decision", "") or "blocked")
    downstream_reason = str(getattr(downstream_report, "reason_code", "") or "downstream_unknown")
    steps.append(_downstream_step(downstream_report))
    if downstream_decision == "go":
        decision = "go"
        reason_code = "local_pdf_parser_provider_bridge_ready"
    elif downstream_decision == "review":
        decision = "review"
        reason_code = f"downstream_{downstream_reason}"
    else:
        decision = "blocked"
        reason_code = f"downstream_{downstream_reason}"

    return _report(
        decision=decision,
        reason_code=reason_code,
        pdf_path=normalized_pdf_path,
        provider_url=provider_url,
        provider_path=provider_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        max_pages=max_pages,
        artifact_path=artifact_path,
        downstream=downstream,
        steps=steps,
        summary={
            "input_status": "ready",
            "provider_status": "ready",
            "normalized_artifact_status": "written",
            "text_block_count": len(text_blocks),
            "downstream_decision": downstream_decision,
            "downstream_reason_code": downstream_reason,
        },
    )


def local_pdf_parser_provider_bridge_report_to_dict(
    report: LocalPdfParserProviderBridgeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    for key in ["pdf_path", "artifact_path", "json_path", "markdown_path"]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_local_pdf_parser_provider_bridge_markdown(report: LocalPdfParserProviderBridgeReport) -> str:
    lines = [
        "# Local PDF Parser Provider Bridge",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- PDF Path: `{report.pdf_path}`",
        f"- Provider: `{report.provider_url.rstrip('/')}{report.provider_path}`",
        f"- Source ID: `{report.source_id}`",
        f"- Title: `{report.title}`",
        f"- Max Pages: `{report.max_pages}`",
        f"- Artifact Path: `{report.artifact_path}`",
        "",
        "## Steps",
        "",
        "| Step | Status | Reason | Artifacts |",
        "|---|---|---|---|",
    ]
    for step in report.steps:
        artifacts = ", ".join(f"{key}={value}" for key, value in step.artifacts.items() if value) or "n/a"
        lines.append(f"| `{step.id}` | `{step.status}` | `{step.reason_code}` | `{artifacts}` |")
    lines.extend(["", "## Downstream", "", "| Field | Value |", "|---|---|"])
    for key, value in report.downstream.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(["", "## Summary", "", "| Metric | Value |", "|---|---|"])
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _paddlex_ocr_payload(pdf_path: Path, *, max_pages: int) -> dict[str, Any]:
    return {
        "file": base64.b64encode(pdf_path.read_bytes()).decode("ascii"),
        "fileType": 0,
        "visualize": False,
        "maxPages": max_pages,
    }


def _post_provider(
    *,
    provider_url: str,
    provider_path: str,
    payload: dict[str, Any],
    client: httpx.Client | None,
) -> tuple[dict[str, Any] | None, str | None]:
    close_client = client is None
    http_client = client or httpx.Client(base_url=provider_url.rstrip("/"), timeout=120.0)
    try:
        response = http_client.post(_normalize_path(provider_path), json=payload)
        response.raise_for_status()
        data = response.json()
    except (httpx.HTTPError, ValueError) as error:
        return None, str(error)
    finally:
        if close_client:
            http_client.close()
    return data if isinstance(data, dict) else None, None


def _provider_error_code(payload: dict[str, Any]) -> str | None:
    error_code = payload.get("errorCode")
    if error_code is None:
        return None
    return str(error_code)


def _normalize_text_blocks(payload: dict[str, Any], *, source_id: str, max_pages: int) -> list[dict[str, Any]]:
    result = payload.get("result") if isinstance(payload.get("result"), dict) else payload
    candidates = _extract_ocr_result_blocks(result, source_id=source_id)
    if not candidates:
        candidates = _extract_pages(result, source_id=source_id)
    if not candidates:
        candidates = _extract_flat_text(result, source_id=source_id)
    return [block for block in candidates if int(block["provenance"]["page"]) <= max_pages]


def _extract_ocr_result_blocks(result: dict[str, Any], *, source_id: str) -> list[dict[str, Any]]:
    ocr_results = result.get("ocrResults")
    if not isinstance(ocr_results, list):
        return []
    blocks: list[dict[str, Any]] = []
    for page_index, page_result in enumerate(ocr_results, start=1):
        if not isinstance(page_result, dict):
            continue
        pruned = page_result.get("prunedResult") if isinstance(page_result.get("prunedResult"), dict) else page_result
        texts = _list_texts(pruned.get("rec_texts") or pruned.get("texts") or pruned.get("text"))
        for offset, text in enumerate(texts, start=1):
            blocks.append(_text_block(source_id, page_index, offset, text))
    return blocks


def _extract_pages(result: dict[str, Any], *, source_id: str) -> list[dict[str, Any]]:
    pages = result.get("pages") or result.get("pageResults") or result.get("layoutParsingResults")
    if not isinstance(pages, list):
        return []
    blocks: list[dict[str, Any]] = []
    for page_index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            continue
        page_number = _positive_int(page.get("page_number") or page.get("page") or page.get("pageNo")) or page_index
        text = _first_text(page.get("text"), page.get("markdown"), page.get("md"))
        if text:
            blocks.append(_text_block(source_id, page_number, 1, text))
            continue
        pruned = page.get("prunedResult") if isinstance(page.get("prunedResult"), dict) else {}
        texts = _list_texts(pruned.get("rec_texts") or pruned.get("texts") or pruned.get("text"))
        for offset, block_text in enumerate(texts, start=1):
            blocks.append(_text_block(source_id, page_number, offset, block_text))
    return blocks


def _extract_flat_text(result: dict[str, Any], *, source_id: str) -> list[dict[str, Any]]:
    text = _first_text(result.get("text"), result.get("markdown"), result.get("md"))
    if not text:
        return []
    return [_text_block(source_id, 1, 1, text)]


def _text_block(source_id: str, page_number: int, offset: int, text: str) -> dict[str, Any]:
    return {
        "block_id": f"page-{page_number}-block-{offset}",
        "text": text.strip(),
        "citation": f"{source_id}#page-{page_number}",
        "provenance": {"page": page_number},
    }


def _artifact_payload(
    *,
    pdf_path: Path,
    provider_url: str,
    provider_path: str,
    source_id: str,
    title: str,
    max_pages: int,
    text_blocks: list[dict[str, Any]],
    raw_provider_payload: dict[str, Any],
) -> dict[str, Any]:
    digest = sha256(pdf_path.read_bytes()).hexdigest()
    safe_source_id = _safe_source_id(source_id)
    return {
        "artifact_id": f"{safe_source_id}_paddleocr_pdf_pages_1_{max_pages}",
        "source_id": source_id,
        "title": title,
        "owner": "local_pdf_parser_provider_bridge",
        "domain": "local_business_corpus",
        "language": "zh-CN",
        "sensitivity": "local_private_trial",
        "original_file": {
            "path": str(pdf_path),
            "name": pdf_path.name,
            "sha256": digest,
            "page_range": f"1-{max_pages}",
        },
        "parser": {
            "parser_id": "paddleocr-http-ocr-provider-v1",
            "parser_version": "local-trial",
            "parsed_at": datetime.now(UTC).isoformat(),
            "provider_url": provider_url.rstrip("/"),
            "provider_path": _normalize_path(provider_path),
        },
        "text_blocks": text_blocks,
        "raw_provider_summary": {
            "errorCode": raw_provider_payload.get("errorCode"),
            "has_result": isinstance(raw_provider_payload.get("result"), dict),
        },
    }


def _downstream_summary(report: Any) -> dict[str, Any]:
    return {
        "decision": getattr(report, "decision", None),
        "reason_code": getattr(report, "reason_code", None),
        "artifact_id": getattr(report, "artifact_id", None),
        "source_id": getattr(report, "source_id", None),
        "materialized_markdown_path": _path_string(getattr(report, "materialized_markdown_path", None)),
        "source_overlay_path": _path_string(getattr(report, "source_overlay_path", None)),
        "json_path": _path_string(getattr(report, "json_path", None)),
        "markdown_path": _path_string(getattr(report, "markdown_path", None)),
        "summary": dict(getattr(report, "summary", {}) or {}),
    }


def _downstream_step(report: Any) -> LocalPdfParserProviderBridgeStep:
    return LocalPdfParserProviderBridgeStep(
        id="parser_artifact_local_ingestion_loop",
        status=str(getattr(report, "decision", None)),
        reason_code=str(getattr(report, "reason_code", None)),
        artifacts={
            "json": _path_string(getattr(report, "json_path", None)),
            "markdown": _path_string(getattr(report, "markdown_path", None)),
            "materialized_markdown": _path_string(getattr(report, "materialized_markdown_path", None)),
        },
        summary=dict(getattr(report, "summary", {}) or {}),
    )


def _blocked_report(
    *,
    reason_code: str,
    pdf_path: Path,
    provider_url: str,
    provider_path: str,
    source_id: str,
    title: str,
    query: str,
    top_k: int,
    max_pages: int,
    steps: list[LocalPdfParserProviderBridgeStep],
    summary: dict[str, Any],
) -> LocalPdfParserProviderBridgeReport:
    return _report(
        decision="blocked",
        reason_code=reason_code,
        pdf_path=pdf_path,
        provider_url=provider_url,
        provider_path=provider_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        max_pages=max_pages,
        artifact_path=None,
        downstream={},
        steps=steps,
        summary=summary,
    )


def _report(
    *,
    decision: str,
    reason_code: str,
    pdf_path: Path,
    provider_url: str,
    provider_path: str,
    source_id: str,
    title: str,
    query: str,
    top_k: int,
    max_pages: int,
    artifact_path: Path | None,
    downstream: dict[str, Any],
    steps: list[LocalPdfParserProviderBridgeStep],
    summary: dict[str, Any],
) -> LocalPdfParserProviderBridgeReport:
    return LocalPdfParserProviderBridgeReport(
        id=LOCAL_PDF_PARSER_PROVIDER_BRIDGE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        pdf_path=pdf_path,
        provider_url=provider_url,
        provider_path=_normalize_path(provider_path),
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        max_pages=max_pages,
        artifact_path=artifact_path,
        downstream=downstream,
        steps=steps,
        summary={
            "final_decision": decision,
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "retrieval_backend_promotion_status": "not_changed",
            "myprivateagent_call_status": "not_called",
            "ocr_service_start_status": "not_started",
            "graph_execution_status": "not_executed",
            **summary,
        },
        recommended_actions=_recommended_actions(decision, reason_code),
        non_goals=_non_goals(),
    )


def _recommended_actions(decision: str, reason_code: str) -> list[str]:
    if decision == "go":
        return [
            "use_generated_source_id_for_local_rag_questions",
            "review_pdf_parser_quality_before_productizing_upload_flow",
            "keep_myprivateagent_as_optional_orchestrator_not_parser_middleman",
        ]
    if reason_code == "parser_provider_unreachable":
        return ["start_paddleocr_provider_and_rerun", "check_provider_url_and_path"]
    if reason_code == "parser_provider_returned_no_text":
        return ["inspect_paddleocr_raw_output", "try_layout_provider_or_smaller_page_range"]
    if reason_code in {"pdf_file_missing", "input_must_be_pdf", "invalid_max_pages"}:
        return ["fix_cli_input_and_rerun"]
    if decision == "review":
        return ["review_downstream_ingestion_result", "rerun_after_artifact_or_query_adjustment"]
    return ["inspect_bridge_or_downstream_reason_code", "rerun_local_pdf_parser_provider_bridge"]


def _non_goals() -> list[str]:
    return [
        "does_not_start_paddleocr_or_ocr_services",
        "does_not_call_myprivateagent",
        "does_not_create_source_to_agent_binding",
        "does_not_mutate_chat_runtime",
        "does_not_promote_retrieval_backend",
        "does_not_add_background_worker",
        "does_not_execute_graphrag",
    ]


def _normalize_path(path: str) -> str:
    value = str(path or "").strip() or DEFAULT_PROVIDER_PATH
    return value if value.startswith("/") else f"/{value}"


def _list_texts(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _first_text(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, dict):
            nested = _first_text(value.get("text"), value.get("markdown"), value.get("md"))
            if nested:
                return nested
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _positive_int(value: Any) -> int | None:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def _safe_source_id(source_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", source_id.strip())
    return cleaned or "local_pdf_source"


def _path_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
