from fastapi.testclient import TestClient

from app.main import create_app
from app.models.contracts import SourceDocumentManifest
from app.services import source_document_manifest
from app.services.index_lifecycle import list_ingestion_jobs


def test_ingestion_preflight_reports_ready_markdown(monkeypatch, tmp_path):
    source_file = tmp_path / "source.md"
    source_file.write_text("# 标题\n\n第一段内容。\n\n第二段内容。", encoding="utf-8")
    monkeypatch.setitem(
        source_document_manifest.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [
            SourceDocumentManifest(
                document_id="refund_policy_2026",
                title="售后退款规则",
                source_path=str(source_file),
                format="markdown",
                version="2026-05-28",
                chunking_strategy="markdown-paragraph-v1",
                citation_anchors=["refund_policy_2026#section-1"],
            )
        ],
    )
    client = TestClient(create_app())

    response = client.get("/api/ingestion/sources/refund_policy_docs/preflight")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    result = body["result"]
    assert result["status"] == "ready"
    assert result["recommended_action"] == "run_ingestion_job"
    assert result["source_package"]["source_id"] == "refund_policy_docs"
    assert result["source_package"]["domain"] == "after_sales_policy"
    assert result["source_package"]["default_chunking_strategy"] == "markdown-paragraph-v1"
    document = result["documents"][0]
    assert document["format_supported"] is True
    assert document["file_status"] == "present"
    assert document["parser_status"] == "ready"
    assert document["chunk_count"] == 2
    assert len(document["chunk_preview"]) == 2
    assert document["chunk_manifest"] == [
        {
            "chunk_id": "chunk-1",
            "citation": "refund_policy_2026#section-1",
            "chunking_strategy": "markdown-paragraph-v1",
            "source_path": str(source_file),
            "char_count": 6,
            "text_preview": "第一段内容。",
        },
        {
            "chunk_id": "chunk-2",
            "citation": "refund_policy_2026#chunk-2",
            "chunking_strategy": "markdown-paragraph-v1",
            "source_path": str(source_file),
            "char_count": 6,
            "text_preview": "第二段内容。",
        },
    ]
    assert document["citation_anchor_count"] == 1
    assert document["recommended_action"] == "run_ingestion_job"


def test_ingestion_preflight_reports_missing_file(monkeypatch, tmp_path):
    missing_file = tmp_path / "missing.md"
    monkeypatch.setitem(
        source_document_manifest.SOURCE_DOCUMENT_MANIFESTS,
        "logistics_faq",
        [
            SourceDocumentManifest(
                document_id="logistics_faq_2026",
                title="物流常见问题",
                source_path=str(missing_file),
                format="markdown",
                version="2026-05-28",
                chunking_strategy="markdown-paragraph-v1",
                citation_anchors=["logistics_faq_2026#delay"],
            )
        ],
    )
    client = TestClient(create_app())

    response = client.get("/api/ingestion/sources/logistics_faq/preflight")

    body = response.json()
    assert body["ok"] is True
    result = body["result"]
    assert result["status"] == "blocked"
    assert result["recommended_action"] == "restore_source_file_before_ingestion"
    document = result["documents"][0]
    assert document["file_status"] == "missing"
    assert document["parser_status"] == "missing_source_file"
    assert document["chunk_manifest"] == []
    assert document["recommended_action"] == "restore_source_file_before_ingestion"


def test_ingestion_preflight_reports_unsupported_format(monkeypatch, tmp_path):
    source_file = tmp_path / "source.docx"
    source_file.write_bytes(b"fake docx")
    monkeypatch.setitem(
        source_document_manifest.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [
            SourceDocumentManifest(
                document_id="refund_policy_docx_2026",
                title="售后退款规则 Word",
                source_path=str(source_file),
                format="docx",
                version="2026-05-28",
                chunking_strategy="unstructured-docx-v1",
                citation_anchors=["refund_policy_docx_2026#section-1"],
            )
        ],
    )
    client = TestClient(create_app())

    response = client.get("/api/ingestion/sources/refund_policy_docs/preflight")

    body = response.json()
    assert body["result"]["status"] == "blocked"
    assert body["result"]["recommended_action"] == "add_parser_support_before_ingestion"
    document = body["result"]["documents"][0]
    assert document["format_supported"] is False
    assert document["parser_status"] == "unsupported_format"
    assert document["chunk_count"] == 0
    assert document["chunk_manifest"] == []


def test_ingestion_preflight_rejects_unknown_source():
    client = TestClient(create_app())

    response = client.get("/api/ingestion/sources/missing_docs/preflight")

    body = response.json()
    assert body["ok"] is False
    assert body["error"]["code"] == "UNKNOWN_KNOWLEDGE_BASE"
    assert body["error"]["details"] == {
        "requested_source_id": "missing_docs",
        "unknown_source_ids": ["missing_docs"],
    }


def test_ingestion_preflight_is_side_effect_free(monkeypatch, tmp_path):
    source_file = tmp_path / "source.md"
    source_file.write_text("可解析内容。", encoding="utf-8")
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    monkeypatch.setitem(
        source_document_manifest.SOURCE_DOCUMENT_MANIFESTS,
        "refund_policy_docs",
        [
            SourceDocumentManifest(
                document_id="refund_policy_2026",
                title="售后退款规则",
                source_path=str(source_file),
                format="markdown",
                version="2026-05-28",
                chunking_strategy="markdown-paragraph-v1",
                citation_anchors=["refund_policy_2026#section-1"],
            )
        ],
    )
    client = TestClient(create_app())

    response = client.get("/api/ingestion/sources/refund_policy_docs/preflight")
    jobs, total, _has_more = list_ingestion_jobs()

    assert response.status_code == 200
    assert response.json()["result"]["status"] == "ready"
    assert total == 0
    assert jobs == []
    assert not (index_dir / "jobs.jsonl").exists()
    assert not (index_dir / "sources.json").exists()
