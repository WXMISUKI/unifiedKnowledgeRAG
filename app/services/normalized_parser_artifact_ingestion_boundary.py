import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any


NORMALIZED_PARSER_ARTIFACT_BOUNDARY_ID = "normalized-parser-artifact-ingestion-boundary-v1"
DEFAULT_ARTIFACT_PATH = Path(
    "docs/local-run/parser-artifacts/company-profile-parser-artifact.json"
)
DEFAULT_OUTPUT_DIR = Path("docs/local-run/normalized-parser-artifact-boundary")
OUTPUT_JSON_FILENAME = "normalized-parser-artifact-boundary.json"
OUTPUT_MARKDOWN_FILENAME = "normalized-parser-artifact-boundary.md"
MATERIALIZED_MARKDOWN_FILENAME = "parser-derived-source.md"
SOURCE_OVERLAY_FILENAME = "parser-derived-source-overlay.json"
RAW_DOCUMENT_SUFFIXES = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".png", ".jpg", ".jpeg"}
SOURCE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


@dataclass(frozen=True)
class NormalizedParserArtifactBoundaryReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    artifact_path: Path
    artifact_id: str | None
    source_id: str | None
    title: str | None
    parser_id: str | None
    original_file_path: str | None
    content_sha256: str | None
    markdown_artifact_path: Path | None
    source_overlay_path: Path | None
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_normalized_parser_artifact_ingestion_boundary_report(
    *,
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> NormalizedParserArtifactBoundaryReport:
    report = run_normalized_parser_artifact_ingestion_boundary(
        artifact_path=artifact_path,
        output_dir=output_dir,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = NormalizedParserArtifactBoundaryReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        artifact_path=report.artifact_path,
        artifact_id=report.artifact_id,
        source_id=report.source_id,
        title=report.title,
        parser_id=report.parser_id,
        original_file_path=report.original_file_path,
        content_sha256=report.content_sha256,
        markdown_artifact_path=report.markdown_artifact_path,
        source_overlay_path=report.source_overlay_path,
        summary=report.summary,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            normalized_parser_artifact_boundary_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_normalized_parser_artifact_boundary_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_normalized_parser_artifact_ingestion_boundary(
    *,
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> NormalizedParserArtifactBoundaryReport:
    normalized_artifact_path = artifact_path.expanduser()
    if normalized_artifact_path.suffix.lower() in RAW_DOCUMENT_SUFFIXES:
        return _report(
            decision="blocked",
            reason_code="normalized_parser_artifact_required",
            artifact_path=normalized_artifact_path,
            summary={
                "input_status": "raw_document_not_supported",
                "materialized_markdown_status": "not_written",
            },
            recommended_actions=[
                "run_external_parser_or_ocr_to_produce_normalized_artifact_json",
                "rerun_parser_artifact_boundary_with_artifact_json",
            ],
        )

    artifact, error = _read_artifact(normalized_artifact_path)
    if error is not None or artifact is None:
        return _report(
            decision="blocked",
            reason_code=error or "artifact_unreadable",
            artifact_path=normalized_artifact_path,
            summary={
                "input_status": "missing_or_unreadable",
                "materialized_markdown_status": "not_written",
            },
            recommended_actions=[
                "provide_normalized_parser_artifact_json",
                "rerun_parser_artifact_boundary",
            ],
        )

    identity_error = _validate_identity(artifact)
    if identity_error is not None:
        return _report_from_artifact(
            artifact=artifact,
            artifact_path=normalized_artifact_path,
            decision="blocked",
            reason_code=identity_error,
            summary={"materialized_markdown_status": "not_written"},
            recommended_actions=["fix_parser_artifact_identity_fields"],
        )

    text_blocks = _text_blocks(artifact)
    if not text_blocks:
        return _report_from_artifact(
            artifact=artifact,
            artifact_path=normalized_artifact_path,
            decision="blocked",
            reason_code="artifact_has_no_text_blocks",
            summary={
                "text_block_count": 0,
                "citation_anchor_count": 0,
                "materialized_markdown_status": "not_written",
            },
            recommended_actions=["rerun_external_parser_with_text_output"],
        )

    citation_count = _citation_anchor_count(text_blocks)
    if citation_count == 0:
        return _report_from_artifact(
            artifact=artifact,
            artifact_path=normalized_artifact_path,
            decision="review",
            reason_code="artifact_missing_citation_anchors",
            summary={
                "text_block_count": len(text_blocks),
                "citation_anchor_count": 0,
                "materialized_markdown_status": "not_written",
            },
            recommended_actions=["add_stable_citation_anchors_to_parser_artifact"],
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_artifact_path = output_dir / MATERIALIZED_MARKDOWN_FILENAME
    source_overlay_path = output_dir / SOURCE_OVERLAY_FILENAME
    markdown_text = _render_materialized_markdown(artifact, text_blocks)
    markdown_artifact_path.write_text(markdown_text, encoding="utf-8")
    content_sha = sha256(markdown_text.encode("utf-8")).hexdigest()
    source_overlay_path.write_text(
        json.dumps(
            _source_overlay_payload(artifact, content_sha, markdown_artifact_path),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return _report_from_artifact(
        artifact=artifact,
        artifact_path=normalized_artifact_path,
        decision="go",
        reason_code="parser_artifact_ready_for_local_onboarding",
        markdown_artifact_path=markdown_artifact_path,
        source_overlay_path=source_overlay_path,
        content_sha256=content_sha,
        summary={
            "text_block_count": len(text_blocks),
            "citation_anchor_count": citation_count,
            "materialized_markdown_status": "written",
            "source_overlay_status": "written",
        },
        recommended_actions=[
            "run_local_document_source_onboarding_with_materialized_markdown",
            "run_local_approved_source_ingestion_loop_after_onboarding",
        ],
    )


def normalized_parser_artifact_boundary_report_to_dict(
    report: NormalizedParserArtifactBoundaryReport,
) -> dict[str, Any]:
    payload = asdict(report)
    for key in [
        "artifact_path",
        "markdown_artifact_path",
        "source_overlay_path",
        "json_path",
        "markdown_path",
    ]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_normalized_parser_artifact_boundary_markdown(
    report: NormalizedParserArtifactBoundaryReport,
) -> str:
    lines = [
        "# Normalized Parser Artifact Boundary",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Artifact Path: `{report.artifact_path}`",
        f"- Artifact ID: `{report.artifact_id}`",
        f"- Source ID: `{report.source_id}`",
        f"- Parser ID: `{report.parser_id}`",
        f"- Materialized Markdown: `{report.markdown_artifact_path}`",
        f"- Source Overlay: `{report.source_overlay_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _read_artifact(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, "artifact_missing"
    if path.suffix.lower() != ".json":
        return None, "artifact_must_be_json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, "artifact_invalid_json"
    if not isinstance(payload, dict):
        return None, "artifact_invalid_shape"
    return payload, None


def _validate_identity(artifact: dict[str, Any]) -> str | None:
    required = ["artifact_id", "source_id", "title"]
    for key in required:
        if not _string_or_none(artifact.get(key)):
            return f"artifact_missing_{key}"
    source_id = str(artifact["source_id"])
    if not SOURCE_ID_PATTERN.match(source_id):
        return "artifact_invalid_source_id"
    parser = artifact.get("parser")
    if not isinstance(parser, dict) or not _string_or_none(parser.get("parser_id")):
        return "artifact_missing_parser_id"
    original_file = artifact.get("original_file")
    if not isinstance(original_file, dict) or not _string_or_none(original_file.get("path")):
        return "artifact_missing_original_file_path"
    return None


def _text_blocks(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    raw_blocks = artifact.get("text_blocks")
    if not isinstance(raw_blocks, list):
        return []
    blocks: list[dict[str, Any]] = []
    for raw_block in raw_blocks:
        if not isinstance(raw_block, dict):
            continue
        text = _string_or_none(raw_block.get("text"))
        if text:
            blocks.append({**raw_block, "text": text})
    return blocks


def _citation_anchor_count(text_blocks: list[dict[str, Any]]) -> int:
    return sum(1 for block in text_blocks if _string_or_none(block.get("citation")))


def _render_materialized_markdown(
    artifact: dict[str, Any],
    text_blocks: list[dict[str, Any]],
) -> str:
    original_file = artifact.get("original_file") if isinstance(artifact.get("original_file"), dict) else {}
    parser = artifact.get("parser") if isinstance(artifact.get("parser"), dict) else {}
    lines = [
        f"# {artifact['title']}",
        "",
        "<!--",
        f"artifact_id: {artifact['artifact_id']}",
        f"source_id: {artifact['source_id']}",
        f"parser_id: {parser.get('parser_id')}",
        f"original_file: {original_file.get('path')}",
        "-->",
        "",
    ]
    for index, block in enumerate(text_blocks, start=1):
        block_id = _string_or_none(block.get("block_id")) or f"block-{index}"
        lines.append(f"## {block_id}")
        citation = _string_or_none(block.get("citation"))
        if citation:
            lines.append(f"<!-- citation: {citation} -->")
        lines.extend(["", str(block["text"]).strip(), ""])
    return "\n".join(lines).rstrip() + "\n"


def _source_overlay_payload(
    artifact: dict[str, Any],
    content_sha: str,
    markdown_artifact_path: Path,
) -> dict[str, Any]:
    parser = artifact.get("parser") if isinstance(artifact.get("parser"), dict) else {}
    original_file = artifact.get("original_file") if isinstance(artifact.get("original_file"), dict) else {}
    return {
        "source_id": artifact["source_id"],
        "title": artifact["title"],
        "owner": artifact.get("owner") or "local_parser_artifact",
        "domain": artifact.get("domain") or "local_business_corpus",
        "language": artifact.get("language") or "zh-CN",
        "sensitivity": artifact.get("sensitivity") or "local_private",
        "markdown_path": str(markdown_artifact_path),
        "content_sha256": content_sha,
        "parser_artifact": {
            "artifact_id": artifact["artifact_id"],
            "parser_id": parser.get("parser_id"),
            "parser_version": parser.get("parser_version"),
            "parsed_at": parser.get("parsed_at"),
            "original_file_path": original_file.get("path"),
            "original_file_sha256": original_file.get("sha256"),
            "page_range": original_file.get("page_range"),
        },
        "runtime_promotion_status": "keep_runtime_defaults",
        "source_binding_status": "not_created",
        "graph_execution_status": "not_executed",
    }


def _report_from_artifact(
    *,
    artifact: dict[str, Any],
    artifact_path: Path,
    decision: str,
    reason_code: str,
    summary: dict[str, Any],
    recommended_actions: list[str],
    markdown_artifact_path: Path | None = None,
    source_overlay_path: Path | None = None,
    content_sha256: str | None = None,
) -> NormalizedParserArtifactBoundaryReport:
    parser = artifact.get("parser") if isinstance(artifact.get("parser"), dict) else {}
    original_file = artifact.get("original_file") if isinstance(artifact.get("original_file"), dict) else {}
    return _report(
        decision=decision,
        reason_code=reason_code,
        artifact_path=artifact_path,
        artifact_id=_string_or_none(artifact.get("artifact_id")),
        source_id=_string_or_none(artifact.get("source_id")),
        title=_string_or_none(artifact.get("title")),
        parser_id=_string_or_none(parser.get("parser_id")),
        original_file_path=_string_or_none(original_file.get("path")),
        content_sha256=content_sha256 or _string_or_none(original_file.get("sha256")),
        markdown_artifact_path=markdown_artifact_path,
        source_overlay_path=source_overlay_path,
        summary=summary,
        recommended_actions=recommended_actions,
    )


def _report(
    *,
    decision: str,
    reason_code: str,
    artifact_path: Path,
    summary: dict[str, Any],
    recommended_actions: list[str],
    artifact_id: str | None = None,
    source_id: str | None = None,
    title: str | None = None,
    parser_id: str | None = None,
    original_file_path: str | None = None,
    content_sha256: str | None = None,
    markdown_artifact_path: Path | None = None,
    source_overlay_path: Path | None = None,
) -> NormalizedParserArtifactBoundaryReport:
    return NormalizedParserArtifactBoundaryReport(
        id=NORMALIZED_PARSER_ARTIFACT_BOUNDARY_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        artifact_path=artifact_path,
        artifact_id=artifact_id,
        source_id=source_id,
        title=title,
        parser_id=parser_id,
        original_file_path=original_file_path,
        content_sha256=content_sha256,
        markdown_artifact_path=markdown_artifact_path,
        source_overlay_path=source_overlay_path,
        summary={
            "final_decision": decision,
            "runtime_promotion_status": "keep_runtime_defaults",
            "source_binding_status": "not_created",
            "raw_parser_execution_status": "not_executed",
            "ocr_service_status": "not_started",
            "ingestion_job_status": "not_created",
            "vector_database_status": "not_called",
            "graph_execution_status": "not_executed",
            **summary,
        },
        recommended_actions=recommended_actions,
        non_goals=_non_goals(),
    )


def _non_goals() -> list[str]:
    return [
        "does_not_parse_raw_pdf",
        "does_not_start_ocr_services",
        "does_not_call_paddleocr_or_parser_engines",
        "does_not_create_source_to_agent_binding",
        "does_not_call_myprivateagent",
        "does_not_create_ingestion_job",
        "does_not_promote_retrieval_backend",
        "does_not_call_vector_databases",
        "does_not_execute_graphrag",
    ]


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
