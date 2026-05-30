from app.models.contracts import SourceDocumentManifest
from app.services import source_document_manifest
from app.services.source_document_manifest import (
    get_source_document_manifest,
)


def test_source_document_manifest_reports_changed_file(monkeypatch, tmp_path):
    source_file = tmp_path / "source.md"
    source_file.write_text("changed source", encoding="utf-8")
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
                expected_content_sha256="0" * 64,
            )
        ],
    )

    response = get_source_document_manifest("refund_policy_docs")

    document = response.result.documents[0]
    assert document.source_file_status == "present"
    assert document.content_sha256 is not None
    assert document.expected_content_sha256 == "0" * 64
    assert document.content_byte_size == len("changed source".encode("utf-8"))
    assert document.drift_status == "changed"


def test_source_document_manifest_reports_missing_file(monkeypatch, tmp_path):
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
                expected_content_sha256="0" * 64,
            )
        ],
    )

    response = get_source_document_manifest("logistics_faq")

    document = response.result.documents[0]
    assert document.source_file_status == "missing"
    assert document.content_sha256 is None
    assert document.content_byte_size is None
    assert document.drift_status == "missing"


def test_source_document_manifest_reports_unchecked_without_expected_hash(
    monkeypatch,
    tmp_path,
):
    source_file = tmp_path / "source.md"
    source_file.write_text("unchecked source", encoding="utf-8")
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
            )
        ],
    )

    response = get_source_document_manifest("refund_policy_docs")

    document = response.result.documents[0]
    assert document.source_file_status == "present"
    assert document.expected_content_sha256 is None
    assert document.drift_status == "unchecked"
