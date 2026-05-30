import json

from app.config import Settings
from app.models.contracts import (
    IndexLifecycleJob,
    IndexStatusResponse,
    SourceDocumentManifest,
)
from app.services import source_document_manifest
from app.services.index_lifecycle_store import IndexLifecycleStore
from app.services.reindex_readiness import (
    build_reindex_readiness_report,
    export_reindex_readiness_report,
    render_reindex_readiness_markdown,
)


def test_reindex_readiness_reports_fixture_sources_as_optional():
    report = build_reindex_readiness_report()

    assert report.id == "reindex-readiness-v1"
    assert report.status == "ready"
    assert report.retrieval_backend == "fixture"
    assert {source["source_id"] for source in report.sources} == {
        "refund_policy_docs",
        "logistics_faq",
    }
    assert {source["recommended_action"] for source in report.sources} == {
        "reindex_optional"
    }
    assert {source["source_fingerprint_status"] for source in report.sources} == {
        "in_sync"
    }
    assert report.job_summary == {
        "total_latest_jobs": 0,
        "status_counts": {},
    }
    assert any("read-only" in note for note in report.operation_notes)


def test_reindex_readiness_blocks_missing_source_file(tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
    )

    report = build_reindex_readiness_report(settings)

    assert report.status == "blocked"
    missing = next(
        source for source in report.sources if source["source_id"] == "logistics_faq"
    )
    assert missing["source_file_status"] == "missing"
    assert missing["recommended_action"] == "restore_source_file_before_reindex"
    assert missing["source_fingerprint_status"] == "in_sync"


def test_reindex_readiness_includes_latest_job_and_status_counts(tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    (source_dir / "logistics_faq.md").write_text("logistics docs", encoding="utf-8")
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
    )
    store = IndexLifecycleStore(settings)
    store.append_job(
        IndexLifecycleJob(
            job_id="idx_refund_completed",
            source_id="refund_policy_docs",
            status="completed",
            requested_at="2026-05-30T00:00:00+00:00",
            completed_at="2026-05-30T00:01:00+00:00",
        )
    )
    store.append_job(
        IndexLifecycleJob(
            job_id="idx_logistics_failed",
            source_id="logistics_faq",
            status="failed",
            requested_at="2026-05-30T00:02:00+00:00",
        )
    )
    store.write_source_status(
        IndexStatusResponse(
            source_id="refund_policy_docs",
            status="ready",
            backend="llamaindex",
            indexed_at="2026-05-30T00:01:00+00:00",
            latest_job_id="idx_refund_completed",
        )
    )

    report = build_reindex_readiness_report(settings)

    assert report.status == "review"
    assert report.job_summary == {
        "total_latest_jobs": 2,
        "status_counts": {"completed": 1, "failed": 1},
    }
    refund = next(
        source for source in report.sources if source["source_id"] == "refund_policy_docs"
    )
    logistics = next(
        source for source in report.sources if source["source_id"] == "logistics_faq"
    )
    assert refund["latest_job"]["job_id"] == "idx_refund_completed"
    assert refund["recommended_action"] == "reindex_optional"
    assert logistics["latest_job"]["job_id"] == "idx_logistics_failed"
    assert logistics["recommended_action"] == "run_ingestion_job"


def test_reindex_readiness_recommends_ingestion_for_changed_source(
    monkeypatch,
    tmp_path,
):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    refund_file = source_dir / "refund_policy_docs.md"
    logistics_file = source_dir / "logistics_faq.md"
    refund_file.write_text("changed refund docs", encoding="utf-8")
    logistics_file.write_text("logistics docs", encoding="utf-8")
    monkeypatch.setitem(
        source_document_manifest.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [
            SourceDocumentManifest(
                document_id="refund_policy_2026",
                title="售后退款规则",
                source_path=str(refund_file),
                format="markdown",
                version="2026-05-28",
                chunking_strategy="markdown-paragraph-v1",
                expected_content_sha256="0" * 64,
            )
        ],
    )
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
    )
    store = IndexLifecycleStore(settings)
    store.write_source_status(
        IndexStatusResponse(
            source_id="refund_policy_docs",
            status="ready",
            backend="llamaindex",
            indexed_at="2026-05-30T00:01:00+00:00",
        )
    )

    report = build_reindex_readiness_report(settings)

    refund = next(
        source for source in report.sources if source["source_id"] == "refund_policy_docs"
    )
    assert report.status == "review"
    assert refund["source_fingerprint_status"] == "changed"
    assert refund["recommended_action"] == "run_ingestion_job"
    assert refund["document_fingerprints"][0]["drift_status"] == "changed"


def test_reindex_readiness_reviews_unchecked_source_fingerprint(
    monkeypatch,
    tmp_path,
):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    refund_file = source_dir / "refund_policy_docs.md"
    logistics_file = source_dir / "logistics_faq.md"
    refund_file.write_text("unchecked refund docs", encoding="utf-8")
    logistics_file.write_text("logistics docs", encoding="utf-8")
    monkeypatch.setitem(
        source_document_manifest.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [
            SourceDocumentManifest(
                document_id="refund_policy_2026",
                title="售后退款规则",
                source_path=str(refund_file),
                format="markdown",
                version="2026-05-28",
                chunking_strategy="markdown-paragraph-v1",
            )
        ],
    )
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
    )

    report = build_reindex_readiness_report(settings)

    refund = next(
        source for source in report.sources if source["source_id"] == "refund_policy_docs"
    )
    assert report.status == "review"
    assert refund["source_fingerprint_status"] == "unchecked"
    assert refund["recommended_action"] == "review_source_fingerprint"


def test_export_reindex_readiness_writes_json_and_markdown(tmp_path):
    report = export_reindex_readiness_report(output_dir=tmp_path / "reindex")

    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == "reindex-readiness-v1"
    assert payload["json_path"] == str(report.json_path)
    assert "# Reindex Readiness Plan" in markdown
    assert "| Source | Source File | Index Status | Fingerprint | Latest Job | Recommended Action |" in markdown
    assert "reindex_optional" in render_reindex_readiness_markdown(report)
