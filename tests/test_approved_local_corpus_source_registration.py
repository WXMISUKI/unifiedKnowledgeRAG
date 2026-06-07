import json

from fastapi.testclient import TestClient

from app.main import create_app
from app.services import (
    document_retriever,
    source_catalog,
    source_document_manifest,
    source_package,
)
from app.services.approved_local_corpus_source_registration import (
    ApprovedLocalSource,
    build_approved_local_corpus_source_registration,
    get_approved_local_source,
    list_approved_local_sources,
    register_approved_local_corpus_source,
)


def test_registers_ready_handoff_and_materializes_source(tmp_path):
    markdown_path = tmp_path / "company.md"
    markdown_path.write_text("# 公司简介\n\n公司主营业务包括智能制造和能源服务。", encoding="utf-8")
    overlay_path = tmp_path / "overlay.json"
    overlay_path.write_text(
        json.dumps(
            {
                "owner": "local_trial",
                "domain": "company_profile",
                "language": "zh-CN",
                "sensitivity": "local_private_trial",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    handoff_path = tmp_path / "handoff.json"
    _write_handoff(
        handoff_path,
        markdown_path=markdown_path,
        overlay_path=overlay_path,
    )

    result = register_approved_local_corpus_source(
        handoff_path=handoff_path,
        registry_path=tmp_path / "registry" / "approved_sources.json",
        source_dir=tmp_path / "sources",
        output_dir=tmp_path / "out",
    )

    assert result.status == "registered"
    assert result.registration_status == "registered"
    assert result.materialized_source_path.read_text(encoding="utf-8") == (
        markdown_path.read_text(encoding="utf-8")
    )
    assert result.source.domain == "company_profile"
    assert result.source.content_sha256
    assert result.json_path.exists()
    assert result.markdown_path.exists()

    sources = list_approved_local_sources(result.registry_path)
    assert [source.source_id for source in sources] == ["company_profile_2025_trial"]
    assert get_approved_local_source(
        "company_profile_2025_trial",
        result.registry_path,
    ).title == "公司简介 2025 trial"


def test_blocks_non_ready_handoff_without_writing_registry(tmp_path):
    markdown_path = tmp_path / "company.md"
    markdown_path.write_text("公司主营业务包括智能制造。", encoding="utf-8")
    handoff_path = tmp_path / "handoff.json"
    _write_handoff(handoff_path, markdown_path=markdown_path, status="review")
    registry_path = tmp_path / "registry" / "approved_sources.json"

    result = build_approved_local_corpus_source_registration(
        handoff_path=handoff_path,
        registry_path=registry_path,
        source_dir=tmp_path / "sources",
    )

    assert result.status == "blocked"
    assert result.reason_code == "handoff_not_ready_for_registration"
    assert not registry_path.exists()


def test_blocks_missing_markdown_without_writing_registry(tmp_path):
    handoff_path = tmp_path / "handoff.json"
    _write_handoff(handoff_path, markdown_path=tmp_path / "missing.md")
    registry_path = tmp_path / "registry" / "approved_sources.json"

    result = build_approved_local_corpus_source_registration(
        handoff_path=handoff_path,
        registry_path=registry_path,
        source_dir=tmp_path / "sources",
    )

    assert result.status == "blocked"
    assert result.reason_code == "handoff_markdown_missing"
    assert not registry_path.exists()


def test_approved_source_is_visible_in_catalog_package_and_manifest(
    monkeypatch,
    tmp_path,
):
    approved_source = _approved_source(tmp_path)
    _patch_approved_source(monkeypatch, approved_source)

    catalog_ids = [source.id for source in source_catalog.list_knowledge_bases()]
    package = source_package.get_source_package("company_profile_2025_trial")
    manifest = source_document_manifest.get_source_document_manifest(
        "company_profile_2025_trial"
    )

    assert "company_profile_2025_trial" in catalog_ids
    assert source_catalog.knowledge_base_exists("company_profile_2025_trial")
    assert package.domain == "company_profile"
    assert manifest.ok is True
    document = manifest.result.documents[0]
    assert document.source_file_status == "present"
    assert document.drift_status == "in_sync"
    assert document.chunk_manifest[0].citation == "company_profile_2025_trial#chunk-1"


def test_approved_source_retrieve_and_answer_smoke(monkeypatch, tmp_path):
    approved_source = _approved_source(tmp_path)
    _patch_approved_source(monkeypatch, approved_source)
    client = TestClient(create_app())

    retrieve_response = client.post(
        "/api/rag/retrieve",
        json={
            "query": "公司主营业务是什么？",
            "knowledge_base_ids": ["company_profile_2025_trial"],
            "top_k": 3,
        },
    )
    answer_response = client.post(
        "/api/rag/answer",
        json={
            "query": "公司主营业务是什么？",
            "knowledge_base_ids": ["company_profile_2025_trial"],
            "top_k": 3,
        },
    )

    retrieve_payload = retrieve_response.json()
    answer_payload = answer_response.json()
    assert retrieve_payload["ok"] is True
    assert retrieve_payload["result"]["documents"][0]["source_id"] == (
        "company_profile_2025_trial"
    )
    assert retrieve_payload["result"]["documents"][0]["citation"] == (
        "company_profile_2025_trial#chunk-1"
    )
    assert answer_payload["ok"] is True
    assert answer_payload["result"]["answer_status"] == "answered"
    assert answer_payload["result"]["citations"] == ["company_profile_2025_trial#chunk-1"]


def _write_handoff(
    path,
    *,
    markdown_path,
    overlay_path=None,
    status="ready_for_caller_review",
) -> None:
    path.write_text(
        json.dumps(
            {
                "status": status,
                "reason_code": "trial_go_ready_for_caller_review",
                "source_id": "company_profile_2025_trial",
                "title": "公司简介 2025 trial",
                "registration_status": "not_registered",
                "caller_next_action": "review_trial_artifacts_before_formal_binding",
                "artifacts": {
                    "trial_report": str(path.parent / "trial.json"),
                    "markdown": str(markdown_path),
                    "overlay": str(overlay_path) if overlay_path else None,
                    "chunks": str(path.parent / "chunks.json"),
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def _approved_source(tmp_path) -> ApprovedLocalSource:
    source_path = tmp_path / "company_profile_2025_trial.md"
    source_text = "公司主营业务包括智能制造、能源服务和企业数字化解决方案。"
    source_path.write_text(source_text, encoding="utf-8")
    return ApprovedLocalSource(
        source_id="company_profile_2025_trial",
        title="公司简介 2025 trial",
        owner="local_trial",
        version="2026-06-07",
        domain="company_profile",
        language="zh-CN",
        sensitivity="local_private_trial",
        source_path=str(source_path),
        document_id="company_profile_2025_trial",
        citation_prefix="company_profile_2025_trial",
        registration_status="registered",
        handoff_path=str(tmp_path / "handoff.json"),
        content_sha256=__import__("hashlib").sha256(
            source_text.encode("utf-8")
        ).hexdigest(),
        supported_formats=["markdown"],
        default_chunking_strategy="markdown-paragraph-v1",
        citation_granularity="chunk",
        metadata={"registered_from": "test"},
    )


def _patch_approved_source(monkeypatch, approved_source):
    monkeypatch.setattr(
        source_catalog,
        "list_approved_local_sources",
        lambda: [approved_source],
    )
    monkeypatch.setattr(
        source_catalog,
        "get_approved_local_source",
        lambda source_id: approved_source
        if source_id == approved_source.source_id
        else None,
    )
    monkeypatch.setattr(
        source_package,
        "get_approved_local_source",
        lambda source_id: approved_source
        if source_id == approved_source.source_id
        else None,
    )
    monkeypatch.setattr(
        source_document_manifest,
        "get_approved_local_source",
        lambda source_id: approved_source
        if source_id == approved_source.source_id
        else None,
    )
    monkeypatch.setattr(
        document_retriever,
        "list_approved_local_sources",
        lambda: [approved_source],
    )
    monkeypatch.setattr(
        document_retriever,
        "get_approved_local_source",
        lambda source_id: approved_source
        if source_id == approved_source.source_id
        else None,
    )
