from fastapi.testclient import TestClient

from app.main import create_app
from app.services.index_lifecycle import clear_local_jobs_for_tests


def test_ingestion_job_indexes_llamaindex_source(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    clear_local_jobs_for_tests()
    client = TestClient(create_app())

    response = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"})

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["job"]["source_id"] == "refund_policy_docs"
    assert body["job"]["status"] == "completed"
    assert body["job"]["completed_at"] is not None

    status_response = client.get("/api/indexes/refund_policy_docs/status")
    status = status_response.json()
    assert status["status"] == "ready"
    assert status["backend"] == "llamaindex"
    assert status["latest_job_id"] == body["job"]["job_id"]


def test_ingestion_job_rejects_unknown_source(monkeypatch, tmp_path):
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(tmp_path / "sources"))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    response = client.post("/api/ingestion/jobs", json={"source_id": "missing_docs"})

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["error"]["code"] == "UNKNOWN_KNOWLEDGE_BASE"


def test_index_status_reports_not_indexed_before_job(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("fixture", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    response = client.get("/api/indexes/refund_policy_docs/status")

    assert response.status_code == 200
    body = response.json()
    assert body["source_id"] == "refund_policy_docs"
    assert body["status"] == "not_indexed"
    assert body["reason"] == "No explicit source index marker found."


def test_retrieval_returns_index_not_ready_for_llamaindex(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    response = client.post(
        "/api/rag/retrieve",
        json={
            "query": "三天未发货",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 1,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["error"]["code"] == "INDEX_NOT_READY"


def test_catalog_reports_index_lifecycle_metadata(monkeypatch):
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "fixture")
    client = TestClient(create_app())

    response = client.get("/api/catalog")

    assert response.status_code == 200
    source = response.json()["knowledge_bases"][0]
    assert source["index_status"] == "ready"
    assert source["index_reason"] == "Fixture backend does not require an explicit persisted index."
