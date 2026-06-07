import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any


APPROVED_LOCAL_SOURCE_REGISTRATION_ID = "approved-local-corpus-source-registration-v1"
DEFAULT_HANDOFF_PATH = Path(
    "docs/local-run/corpus-caller-handoff/local-corpus-caller-handoff.json"
)
DEFAULT_REGISTRY_PATH = Path("app/data/local_sources/approved_sources.json")
DEFAULT_SOURCE_DIR = Path("app/data/sources")
DEFAULT_OUTPUT_DIR = Path("docs/local-run/approved-local-source-registration")
OUTPUT_JSON_FILENAME = "approved-local-source-registration.json"
OUTPUT_MARKDOWN_FILENAME = "approved-local-source-registration.md"
SOURCE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


@dataclass(frozen=True)
class ApprovedLocalSource:
    source_id: str
    title: str
    owner: str
    version: str
    domain: str
    language: str
    sensitivity: str
    source_path: str
    document_id: str
    citation_prefix: str
    registration_status: str
    handoff_path: str
    content_sha256: str
    supported_formats: list[str]
    default_chunking_strategy: str
    citation_granularity: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ApprovedLocalSourceRegistrationResult:
    id: str
    generated_at: str
    status: str
    reason_code: str
    source_id: str | None
    title: str | None
    registration_status: str
    handoff_path: Path
    registry_path: Path
    materialized_source_path: Path | None
    source: ApprovedLocalSource | None
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def register_approved_local_corpus_source(
    *,
    handoff_path: Path = DEFAULT_HANDOFF_PATH,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    source_dir: Path = DEFAULT_SOURCE_DIR,
    output_dir: Path | None = DEFAULT_OUTPUT_DIR,
) -> ApprovedLocalSourceRegistrationResult:
    result = build_approved_local_corpus_source_registration(
        handoff_path=handoff_path,
        registry_path=registry_path,
        source_dir=source_dir,
    )
    if output_dir is None:
        return result

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = ApprovedLocalSourceRegistrationResult(
        id=result.id,
        generated_at=result.generated_at,
        status=result.status,
        reason_code=result.reason_code,
        source_id=result.source_id,
        title=result.title,
        registration_status=result.registration_status,
        handoff_path=result.handoff_path,
        registry_path=result.registry_path,
        materialized_source_path=result.materialized_source_path,
        source=result.source,
        summary=result.summary,
        recommended_actions=result.recommended_actions,
        non_goals=result.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            approved_local_source_registration_result_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_approved_local_source_registration_markdown(exported),
        encoding="utf-8",
    )
    return exported


def build_approved_local_corpus_source_registration(
    *,
    handoff_path: Path = DEFAULT_HANDOFF_PATH,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    source_dir: Path = DEFAULT_SOURCE_DIR,
) -> ApprovedLocalSourceRegistrationResult:
    normalized_handoff_path = handoff_path.expanduser().resolve()
    normalized_registry_path = registry_path.expanduser()
    normalized_source_dir = source_dir.expanduser()

    handoff, error = _read_json(normalized_handoff_path)
    if error is not None or handoff is None:
        return _blocked_result(
            handoff_path=normalized_handoff_path,
            registry_path=normalized_registry_path,
            reason_code=error or "handoff_missing",
            summary={"handoff_status": "missing_or_unreadable"},
            recommended_actions=["export_local_corpus_caller_handoff_first"],
        )

    source_id = _string_or_none(handoff.get("source_id"))
    title = _string_or_none(handoff.get("title"))
    if not source_id or not SOURCE_ID_PATTERN.match(source_id):
        return _blocked_result(
            handoff_path=normalized_handoff_path,
            registry_path=normalized_registry_path,
            source_id=source_id,
            title=title,
            reason_code="invalid_source_id",
            summary={"source_id": source_id},
            recommended_actions=["rerun_local_corpus_caller_handoff_with_valid_source_id"],
        )

    if handoff.get("status") != "ready_for_caller_review":
        return _blocked_result(
            handoff_path=normalized_handoff_path,
            registry_path=normalized_registry_path,
            source_id=source_id,
            title=title,
            reason_code="handoff_not_ready_for_registration",
            summary={"handoff_status": handoff.get("status")},
            recommended_actions=["fix_or_review_local_corpus_handoff_before_registration"],
        )

    if handoff.get("registration_status") != "not_registered":
        return _blocked_result(
            handoff_path=normalized_handoff_path,
            registry_path=normalized_registry_path,
            source_id=source_id,
            title=title,
            reason_code="handoff_registration_status_not_eligible",
            summary={"handoff_registration_status": handoff.get("registration_status")},
            recommended_actions=["review_existing_registration_state_before_retry"],
        )

    markdown_path = _markdown_path_from_handoff(handoff, normalized_handoff_path)
    if markdown_path is None or not markdown_path.exists():
        return _blocked_result(
            handoff_path=normalized_handoff_path,
            registry_path=normalized_registry_path,
            source_id=source_id,
            title=title,
            reason_code="handoff_markdown_missing",
            summary={"markdown_path": str(markdown_path) if markdown_path else None},
            recommended_actions=["rerun_pdf_or_business_corpus_trial_before_registration"],
        )
    if markdown_path.suffix.lower() not in {".md", ".markdown"}:
        return _blocked_result(
            handoff_path=normalized_handoff_path,
            registry_path=normalized_registry_path,
            source_id=source_id,
            title=title,
            reason_code="unsupported_markdown_format",
            summary={"markdown_path": str(markdown_path)},
            recommended_actions=["provide_markdown_corpus_before_registration"],
        )

    materialized_source_path = normalized_source_dir / f"{source_id}.md"
    normalized_source_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(markdown_path, materialized_source_path)
    content_bytes = materialized_source_path.read_bytes()
    content_sha256 = sha256(content_bytes).hexdigest()
    overlay = _read_overlay(handoff, normalized_handoff_path)
    source = ApprovedLocalSource(
        source_id=source_id,
        title=title or source_id,
        owner=_string_or_none(overlay.get("owner")) or "local_approved",
        version=datetime.now(UTC).date().isoformat(),
        domain=_string_or_none(overlay.get("domain")) or "local_business_corpus",
        language=_string_or_none(overlay.get("language")) or "zh-CN",
        sensitivity=_string_or_none(overlay.get("sensitivity")) or "local_private",
        source_path=str(materialized_source_path),
        document_id=source_id,
        citation_prefix=source_id,
        registration_status="registered",
        handoff_path=str(normalized_handoff_path),
        content_sha256=content_sha256,
        supported_formats=["markdown"],
        default_chunking_strategy="markdown-paragraph-v1",
        citation_granularity="chunk",
        metadata={
            "registered_from": "local_corpus_caller_handoff",
            "trial_report": handoff.get("artifacts", {}).get("trial_report"),
            "caller_next_action": handoff.get("caller_next_action"),
            "runtime_promotion_status": "keep_runtime_defaults",
        },
    )
    _upsert_approved_source(normalized_registry_path, source)
    return ApprovedLocalSourceRegistrationResult(
        id=APPROVED_LOCAL_SOURCE_REGISTRATION_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status="registered",
        reason_code="approved_local_source_registered",
        source_id=source.source_id,
        title=source.title,
        registration_status="registered",
        handoff_path=normalized_handoff_path,
        registry_path=normalized_registry_path,
        materialized_source_path=materialized_source_path,
        source=source,
        summary={
            "source_id": source.source_id,
            "registry_status": "written",
            "materialized_source_status": "written",
            "content_sha256": content_sha256,
            "default_source_catalog_status": "extended_with_approved_local_source",
            "runtime_promotion_status": "keep_runtime_defaults",
            "source_binding_status": "not_created",
            "graph_execution_status": "not_executed",
        },
        recommended_actions=[
            "verify_registered_source_with_rag_sources",
            "run_retrieve_and_answer_smoke_for_registered_source",
            "keep_source_to_agent_binding_in_caller_control_plane",
        ],
        non_goals=_non_goals(),
    )


def list_approved_local_sources(
    registry_path: Path = DEFAULT_REGISTRY_PATH,
) -> list[ApprovedLocalSource]:
    payload = _read_registry(registry_path)
    return [
        _source_from_dict(item)
        for item in payload.get("sources", [])
        if item.get("registration_status") == "registered"
    ]


def get_approved_local_source(
    source_id: str,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
) -> ApprovedLocalSource | None:
    return next(
        (
            source
            for source in list_approved_local_sources(registry_path)
            if source.source_id == source_id
        ),
        None,
    )


def approved_local_source_registration_result_to_dict(
    result: ApprovedLocalSourceRegistrationResult,
) -> dict[str, Any]:
    return {
        "id": result.id,
        "generated_at": result.generated_at,
        "status": result.status,
        "reason_code": result.reason_code,
        "source_id": result.source_id,
        "title": result.title,
        "registration_status": result.registration_status,
        "handoff_path": str(result.handoff_path),
        "registry_path": str(result.registry_path),
        "materialized_source_path": (
            str(result.materialized_source_path)
            if result.materialized_source_path is not None
            else None
        ),
        "source": asdict(result.source) if result.source is not None else None,
        "summary": result.summary,
        "recommended_actions": result.recommended_actions,
        "non_goals": result.non_goals,
        "json_path": str(result.json_path) if result.json_path is not None else None,
        "markdown_path": (
            str(result.markdown_path) if result.markdown_path is not None else None
        ),
    }


def render_approved_local_source_registration_markdown(
    result: ApprovedLocalSourceRegistrationResult,
) -> str:
    lines = [
        "# Approved Local Source Registration",
        "",
        f"- Report: `{result.id}`",
        f"- Status: `{result.status}`",
        f"- Reason: `{result.reason_code}`",
        f"- Generated At: `{result.generated_at}`",
        f"- Source ID: `{result.source_id}`",
        f"- Title: `{result.title}`",
        f"- Registration Status: `{result.registration_status}`",
        f"- Handoff Path: `{result.handoff_path}`",
        f"- Registry Path: `{result.registry_path}`",
        f"- Materialized Source Path: `{result.materialized_source_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in result.summary.items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in result.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in result.non_goals)
    lines.append("")
    return "\n".join(lines)


def _blocked_result(
    *,
    handoff_path: Path,
    registry_path: Path,
    reason_code: str,
    summary: dict[str, Any],
    recommended_actions: list[str],
    source_id: str | None = None,
    title: str | None = None,
) -> ApprovedLocalSourceRegistrationResult:
    return ApprovedLocalSourceRegistrationResult(
        id=APPROVED_LOCAL_SOURCE_REGISTRATION_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status="blocked",
        reason_code=reason_code,
        source_id=source_id,
        title=title,
        registration_status="blocked",
        handoff_path=handoff_path,
        registry_path=registry_path,
        materialized_source_path=None,
        source=None,
        summary={
            **summary,
            "registry_status": "unchanged",
            "runtime_promotion_status": "keep_runtime_defaults",
            "source_binding_status": "not_created",
            "graph_execution_status": "not_executed",
        },
        recommended_actions=recommended_actions,
        non_goals=_non_goals(),
    )


def _read_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, "handoff_missing"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, "handoff_invalid_json"
    if not isinstance(payload, dict):
        return None, "handoff_invalid_shape"
    return payload, None


def _markdown_path_from_handoff(
    handoff: dict[str, Any],
    handoff_path: Path,
) -> Path | None:
    artifacts = handoff.get("artifacts")
    if not isinstance(artifacts, dict):
        return None
    raw_markdown_path = _string_or_none(artifacts.get("markdown"))
    if not raw_markdown_path:
        return None
    markdown_path = Path(raw_markdown_path).expanduser()
    if markdown_path.is_absolute():
        return markdown_path
    return (handoff_path.parent / markdown_path).resolve() if not markdown_path.exists() else markdown_path.resolve()


def _read_overlay(handoff: dict[str, Any], handoff_path: Path) -> dict[str, Any]:
    artifacts = handoff.get("artifacts")
    if not isinstance(artifacts, dict):
        return {}
    raw_overlay_path = _string_or_none(artifacts.get("overlay"))
    if not raw_overlay_path:
        return {}
    overlay_path = Path(raw_overlay_path).expanduser()
    if not overlay_path.is_absolute():
        overlay_path = overlay_path if overlay_path.exists() else handoff_path.parent / overlay_path
    payload, error = _read_json(overlay_path.resolve())
    if error is not None or payload is None:
        return {}
    return payload


def _upsert_approved_source(
    registry_path: Path,
    source: ApprovedLocalSource,
) -> None:
    payload = _read_registry(registry_path)
    sources = [
        item
        for item in payload.get("sources", [])
        if item.get("source_id") != source.source_id
    ]
    sources.append(asdict(source))
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(
        json.dumps(
            {
                "id": "approved-local-sources-v1",
                "updated_at": datetime.now(UTC).isoformat(),
                "sources": sorted(sources, key=lambda item: item["source_id"]),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _read_registry(registry_path: Path) -> dict[str, Any]:
    if not registry_path.exists():
        return {"id": "approved-local-sources-v1", "sources": []}
    try:
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"id": "approved-local-sources-v1", "sources": []}
    if not isinstance(payload, dict) or not isinstance(payload.get("sources"), list):
        return {"id": "approved-local-sources-v1", "sources": []}
    return payload


def _source_from_dict(item: dict[str, Any]) -> ApprovedLocalSource:
    return ApprovedLocalSource(
        source_id=str(item["source_id"]),
        title=str(item.get("title") or item["source_id"]),
        owner=str(item.get("owner") or "local_approved"),
        version=str(item.get("version") or "local"),
        domain=str(item.get("domain") or "local_business_corpus"),
        language=str(item.get("language") or "zh-CN"),
        sensitivity=str(item.get("sensitivity") or "local_private"),
        source_path=str(item.get("source_path") or ""),
        document_id=str(item.get("document_id") or item["source_id"]),
        citation_prefix=str(item.get("citation_prefix") or item["source_id"]),
        registration_status=str(item.get("registration_status") or "registered"),
        handoff_path=str(item.get("handoff_path") or ""),
        content_sha256=str(item.get("content_sha256") or ""),
        supported_formats=list(item.get("supported_formats") or ["markdown"]),
        default_chunking_strategy=str(
            item.get("default_chunking_strategy") or "markdown-paragraph-v1"
        ),
        citation_granularity=str(item.get("citation_granularity") or "chunk"),
        metadata=dict(item.get("metadata") or {}),
    )


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _non_goals() -> list[str]:
    return [
        "does_not_create_source_to_agent_binding",
        "does_not_create_formal_ingestion_job",
        "does_not_promote_retrieval_backend",
        "does_not_start_ocr_services",
        "does_not_run_myprivateagent_orchestration",
        "does_not_call_vector_databases",
        "does_not_execute_graphrag",
    ]
