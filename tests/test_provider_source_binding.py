from hashlib import sha256
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.models.contracts import SourceDocumentManifest
from app.services import ingestion_preflight, source_document_manifest, source_package
from app.services.provider_source_binding import (
    build_provider_source_binding_summary,
    export_provider_source_binding_summary,
    render_provider_source_binding_summary_markdown,
)


def test_provider_source_binding_summary_marks_default_sources_bindable():
    report = build_provider_source_binding_summary()

    assert report.id == "provider-source-binding-summary-v1"
    assert report.status == "ready"
    assert report.provider["provider_id"] == "unifiedKnowledgeProvider"
    rows = {source.source_id: source for source in report.sources}
    assert set(rows) == {"refund_policy_docs", "logistics_faq"}
    for row in rows.values():
        assert row.status == "ready"
        assert row.bindable is True
        assert row.source_domain in {"after_sales_policy", "logistics_support"}
        assert row.language == "zh-CN"
        assert row.sensitivity == "internal"
        assert row.supported_formats == ["markdown"]
        assert row.citation_granularity == "section"
        assert row.retrieval_backend == "fixture"
        assert row.backend_status == "ready"
        assert row.index_status == "ready"
        assert row.document_count == 1
        assert row.citation_anchor_count > 0
        assert row.chunk_manifest_count == row.citation_anchor_count
        assert row.parser_ready_document_count == 1
        assert row.unsupported_document_count == 0
        assert row.drift_statuses == ["in_sync"]
        assert row.ingestion_preflight_status == "ready"
        assert row.recommended_action == "bind_source_from_control_plane"
    assert any("read-only" in note for note in report.operation_notes)


def test_provider_source_binding_endpoint_and_manifest_discovery():
    client = TestClient(create_app())

    manifest_response = client.get("/api/provider/manifest")
    summary_response = client.get("/api/provider/source-bindings")

    assert manifest_response.status_code == 200
    assert manifest_response.json()["endpoints"]["source_bindings"] == (
        "/api/provider/source-bindings"
    )
    assert summary_response.status_code == 200
    body = summary_response.json()
    assert body["id"] == "provider-source-binding-summary-v1"
    assert body["status"] == "ready"
    assert {source["source_id"] for source in body["sources"]} == {
        "refund_policy_docs",
        "logistics_faq",
    }
    refund_source = next(
        source
        for source in body["sources"]
        if source["source_id"] == "refund_policy_docs"
    )
    assert refund_source["citation_anchor_count"] == 7
    assert refund_source["chunk_manifest_count"] == 7
    assert refund_source["parser_ready_document_count"] == 1
    assert refund_source["unsupported_document_count"] == 0
    assert refund_source["source_domain"] == "after_sales_policy"
    assert refund_source["language"] == "zh-CN"
    assert refund_source["sensitivity"] == "internal"
    assert refund_source["supported_formats"] == ["markdown"]
    assert refund_source["citation_granularity"] == "section"


def test_provider_source_binding_blocks_drifted_source(monkeypatch, tmp_path):
    source_file = tmp_path / "refund.md"
    source_file.write_text("# Refund\n\nupdated policy", encoding="utf-8")
    manifest = SourceDocumentManifest(
        document_id="refund_policy_2026",
        title="售后退款规则",
        source_path=str(source_file),
        format="markdown",
        version="2026-05-28",
        chunking_strategy="markdown-paragraph-v1",
        citation_anchors=["refund_policy_2026#section-1"],
        expected_content_sha256="not-the-current-hash",
    )
    monkeypatch.setitem(
        source_document_manifest.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [manifest],
    )
    monkeypatch.setitem(
        ingestion_preflight.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [manifest],
    )

    report = build_provider_source_binding_summary()
    row = next(
        source
        for source in report.sources
        if source.source_id == "refund_policy_docs"
    )

    assert report.status == "blocked"
    assert row.status == "blocked"
    assert row.bindable is False
    assert row.drift_statuses == ["changed"]
    assert row.citation_anchor_count == 1
    assert row.chunk_manifest_count == 1
    assert row.parser_ready_document_count == 1
    assert row.unsupported_document_count == 0
    assert row.recommended_action == "run_ingestion_job_before_binding"
    assert "fingerprint changed" in row.reasons[0]


def test_provider_source_binding_coverage_counts_are_informational(
    monkeypatch,
    tmp_path,
):
    source_file = tmp_path / "refund.md"
    content = "# Refund\n\nupdated policy"
    source_file.write_text(content, encoding="utf-8")
    manifest = SourceDocumentManifest(
        document_id="refund_policy_2026",
        title="售后退款规则",
        source_path=str(source_file),
        format="markdown",
        version="2026-05-28",
        chunking_strategy="markdown-paragraph-v1",
        citation_anchors=["refund_policy_2026#section-1"],
        expected_content_sha256=sha256(source_file.read_bytes()).hexdigest(),
    )
    monkeypatch.setitem(
        source_document_manifest.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [manifest],
    )
    monkeypatch.setitem(
        ingestion_preflight.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [manifest],
    )

    report = build_provider_source_binding_summary()
    row = next(
        source
        for source in report.sources
        if source.source_id == "refund_policy_docs"
    )

    assert row.status == "ready"
    assert row.bindable is True
    assert row.source_domain == "after_sales_policy"
    assert row.sensitivity == "internal"
    assert row.citation_anchor_count == 1
    assert row.chunk_manifest_count == 1
    assert row.parser_ready_document_count == 1


def test_provider_source_binding_package_context_is_informational(monkeypatch):
    monkeypatch.setitem(
        source_package.SOURCE_PACKAGES,
        "refund_policy_docs",
        {
            "domain": "finance_policy",
            "language": "zh-CN",
            "sensitivity": "restricted",
            "supported_formats": ["markdown"],
            "default_chunking_strategy": "markdown-paragraph-v1",
            "citation_granularity": "section",
            "allowed_parser_statuses": ["ready"],
        },
    )

    report = build_provider_source_binding_summary()
    row = next(
        source
        for source in report.sources
        if source.source_id == "refund_policy_docs"
    )

    assert row.status == "ready"
    assert row.bindable is True
    assert row.source_domain == "finance_policy"
    assert row.sensitivity == "restricted"


def test_provider_source_binding_blocks_not_ready_index(tmp_path):
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_index_dir=tmp_path / "indexes",
    )

    report = build_provider_source_binding_summary(settings)

    assert report.status == "blocked"
    rows = {source.source_id: source for source in report.sources}
    assert rows["refund_policy_docs"].index_status == "not_indexed"
    assert rows["refund_policy_docs"].status == "blocked"
    assert rows["refund_policy_docs"].recommended_action == (
        "run_ingestion_job_before_binding"
    )


def test_provider_source_binding_summary_is_read_only(monkeypatch):
    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("source binding summary must remain read-only")

    monkeypatch.setattr("app.routers.rag.retrieve_documents", fail_if_called)
    monkeypatch.setattr("app.routers.rag.answer_documents", fail_if_called)
    monkeypatch.setattr("app.routers.graph.query_graph", fail_if_called)
    monkeypatch.setattr("app.routers.ingestion.create_job", fail_if_called)

    response = TestClient(create_app()).get("/api/provider/source-bindings")

    assert response.status_code == 200
    assert response.json()["id"] == "provider-source-binding-summary-v1"


def test_provider_source_binding_export_writes_json_and_markdown(tmp_path):
    report = export_provider_source_binding_summary(output_dir=tmp_path / "bindings")

    assert report.status == "ready"
    assert report.json_path is not None
    assert report.markdown_path is not None
    json_path = Path(report.json_path)
    markdown_path = Path(report.markdown_path)
    assert json_path.exists()
    assert markdown_path.exists()
    payload = json_path.read_text(encoding="utf-8")
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "provider-source-binding-summary-v1" in payload
    assert "source_domain" in payload
    assert "sensitivity" in payload
    assert "citation_anchor_count" in payload
    assert "chunk_manifest_count" in payload
    assert "# Provider Source Binding Summary" in markdown
    assert "Domain" in markdown
    assert "Sensitivity" in markdown
    assert "Citations" in markdown
    assert "Chunks" in markdown
    assert "bind_source_from_control_plane" in markdown


def test_provider_source_binding_markdown_summarizes_sources():
    report = build_provider_source_binding_summary()

    markdown = render_provider_source_binding_summary_markdown(report)

    assert "| Source | Status | Bindable | Domain | Language | Sensitivity | Formats | Citation Granularity | Backend | Index | Documents | Citations | Chunks | Parser Ready | Unsupported | Drift | Preflight | Recommended Action |" in markdown
    assert "`refund_policy_docs`" in markdown
    assert "`after_sales_policy`" in markdown
    assert "`bind_source_from_control_plane`" in markdown
