import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings
from app.models.contracts import IndexLifecycleJob
from app.services.index_lifecycle import get_index_status
from app.services.index_lifecycle_store import IndexLifecycleStore
from app.services.source_catalog import KNOWLEDGE_BASES
from app.services.source_document_manifest import get_source_document_manifest


REINDEX_READINESS_REPORT_ID = "reindex-readiness-v1"


@dataclass(frozen=True)
class ReindexReadinessReport:
    id: str
    generated_at: str
    status: str
    retrieval_backend: str
    source_dir: str
    index_dir: str
    sources: list[dict[str, Any]]
    job_summary: dict[str, Any]
    operation_notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_reindex_readiness_report(
    settings: Settings | None = None,
) -> ReindexReadinessReport:
    settings = settings or get_settings()
    store = IndexLifecycleStore(settings)
    latest_jobs = store.list_latest_jobs()
    latest_by_source = {
        job.source_id: job
        for job in latest_jobs
    }
    source_rows = [
        _source_row(settings, latest_by_source.get(source.id), source.id)
        for source in KNOWLEDGE_BASES
    ]
    return ReindexReadinessReport(
        id=REINDEX_READINESS_REPORT_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(source_rows),
        retrieval_backend=settings.rag_retrieval_backend.lower(),
        source_dir=str(settings.rag_source_dir),
        index_dir=str(settings.rag_index_dir),
        sources=source_rows,
        job_summary=_job_summary(latest_jobs),
        operation_notes=_operation_notes(settings, source_rows),
    )


def reindex_readiness_report_to_dict(report: ReindexReadinessReport) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_reindex_readiness_markdown(report: ReindexReadinessReport) -> str:
    lines = [
        "# Reindex Readiness Plan",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Retrieval Backend: `{report.retrieval_backend}`",
        f"- Source Dir: `{report.source_dir}`",
        f"- Index Dir: `{report.index_dir}`",
        "",
        "## Sources",
        "",
        "| Source | Source File | Index Status | Fingerprint | Latest Job | Recommended Action |",
        "|---|---|---|---|---|---|",
    ]
    for source in report.sources:
        latest_job = source["latest_job"] or {}
        latest_job_label = (
            f"{latest_job.get('job_id')} ({latest_job.get('status')})"
            if latest_job
            else "none"
        )
        lines.append(
            f"| `{source['source_id']}` | `{source['source_file_status']}` | "
            f"`{source['index_status']}` | `{source['source_fingerprint_status']}` | "
            f"`{latest_job_label}` | "
            f"`{source['recommended_action']}` |"
        )
    counts = report.job_summary["status_counts"]
    lines.extend(
        [
            "",
            "## Job Summary",
            "",
            f"- Total latest logical jobs: `{report.job_summary['total_latest_jobs']}`",
            f"- Status counts: `{json.dumps(counts, ensure_ascii=False, sort_keys=True)}`",
            "",
            "## Operation Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in report.operation_notes)
    lines.append("")
    return "\n".join(lines)


def export_reindex_readiness_report(
    output_dir: Path = Path("docs/operations/reindex-readiness"),
    *,
    settings: Settings | None = None,
) -> ReindexReadinessReport:
    report = build_reindex_readiness_report(settings=settings)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "reindex-readiness.json"
    markdown_path = output_dir / "reindex-readiness.md"
    exported_report = ReindexReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        retrieval_backend=report.retrieval_backend,
        source_dir=report.source_dir,
        index_dir=report.index_dir,
        sources=report.sources,
        job_summary=report.job_summary,
        operation_notes=report.operation_notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            reindex_readiness_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_reindex_readiness_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _source_row(
    settings: Settings,
    latest_job: IndexLifecycleJob | None,
    source_id: str,
) -> dict[str, Any]:
    source_file = settings.rag_source_dir / f"{source_id}.md"
    index_status = get_index_status(source_id, settings)
    source_file_exists = source_file.exists()
    document_fingerprints = _document_fingerprints(source_id, settings)
    source_fingerprint_status = _source_fingerprint_status(document_fingerprints)
    return {
        "source_id": source_id,
        "source_file": str(source_file),
        "source_file_status": "present" if source_file_exists else "missing",
        "source_fingerprint_status": source_fingerprint_status,
        "document_fingerprints": document_fingerprints,
        "index_status": index_status.status,
        "index_reason": index_status.reason,
        "indexed_at": index_status.indexed_at,
        "latest_job": _job_payload(latest_job),
        "recommended_action": _recommended_action(
            source_file_exists=source_file_exists,
            source_fingerprint_status=source_fingerprint_status,
            index_status=index_status.status,
        ),
    }


def _job_payload(job: IndexLifecycleJob | None) -> dict[str, Any] | None:
    if job is None:
        return None
    return {
        "job_id": job.job_id,
        "status": job.status,
        "requested_at": job.requested_at,
        "completed_at": job.completed_at,
        "error_code": job.error.code if job.error else None,
    }


def _recommended_action(
    *,
    source_file_exists: bool,
    source_fingerprint_status: str,
    index_status: str,
) -> str:
    if not source_file_exists:
        return "restore_source_file_before_reindex"
    if source_fingerprint_status in {"changed", "mixed_changed"}:
        return "run_ingestion_job"
    if source_fingerprint_status in {"unchecked", "mixed_unchecked", "unknown"}:
        return "review_source_fingerprint"
    if index_status in {"not_indexed", "failed", "canceled", "unknown"}:
        return "run_ingestion_job"
    if index_status == "ready":
        return "reindex_optional"
    return "review_index_status"


def _document_fingerprints(
    source_id: str,
    settings: Settings,
) -> list[dict[str, Any]]:
    manifest = get_source_document_manifest(source_id, settings)
    if not manifest.ok or manifest.result is None:
        return []
    return [
        {
            "document_id": document.document_id,
            "source_path": document.source_path,
            "source_file_status": document.source_file_status,
            "drift_status": document.drift_status,
            "content_sha256": document.content_sha256,
            "expected_content_sha256": document.expected_content_sha256,
            "content_byte_size": document.content_byte_size,
        }
        for document in manifest.result.documents
    ]


def _source_fingerprint_status(
    document_fingerprints: list[dict[str, Any]],
) -> str:
    statuses = {
        fingerprint.get("drift_status") or "unknown"
        for fingerprint in document_fingerprints
    }
    if not statuses:
        return "unknown"
    if statuses == {"in_sync"}:
        return "in_sync"
    if statuses == {"changed"}:
        return "changed"
    if "changed" in statuses:
        return "mixed_changed"
    if statuses == {"missing"}:
        return "missing"
    if "missing" in statuses:
        return "mixed_missing"
    if statuses == {"unchecked"}:
        return "unchecked"
    if "unchecked" in statuses:
        return "mixed_unchecked"
    return "unknown"


def _job_summary(jobs: list[IndexLifecycleJob]) -> dict[str, Any]:
    counts = Counter(job.status for job in jobs)
    return {
        "total_latest_jobs": len(jobs),
        "status_counts": dict(sorted(counts.items())),
    }


def _overall_status(sources: list[dict[str, Any]]) -> str:
    actions = {source["recommended_action"] for source in sources}
    if "restore_source_file_before_reindex" in actions:
        return "blocked"
    if actions - {"reindex_optional"}:
        return "review"
    return "ready"


def _operation_notes(
    settings: Settings,
    sources: list[dict[str, Any]],
) -> list[str]:
    notes = [
        "This plan is read-only and does not trigger ingestion or index rebuilds.",
        "Back up the index directory before production reindex operations.",
    ]
    if settings.rag_retrieval_backend.lower() == "fixture":
        notes.append("Fixture backend does not require persisted source indexes.")
    if any(source["latest_job"] is None for source in sources):
        notes.append("Some sources have no recorded ingestion job history.")
    if any(source["source_fingerprint_status"] != "in_sync" for source in sources):
        notes.append("Some source document fingerprints require review or reindex planning.")
    return notes
