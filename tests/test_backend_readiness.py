from fastapi.testclient import TestClient

from app.main import create_app


def test_health_reports_fixture_backend_readiness(monkeypatch):
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "fixture")
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["rag"]["backend"] == "fixture"
    assert body["rag"]["backend_status"] == "ready"
    assert body["rag"]["index_status"] == "ready"


def test_health_reports_degraded_llamaindex_backend(monkeypatch, tmp_path):
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(tmp_path / "missing-sources"))
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "degraded"
    assert body["rag"]["backend"] == "llamaindex"
    assert body["rag"]["backend_status"] == "degraded"
    assert "Source directory not found" in body["rag"]["reason"]


def test_catalog_reports_backend_metadata(monkeypatch):
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "fixture")
    client = TestClient(create_app())

    response = client.get("/api/catalog")

    assert response.status_code == 200
    source = response.json()["knowledge_bases"][0]
    assert source["retrieval_backend"] == "fixture"
    assert source["backend_status"] == "ready"
    assert source["index_status"] == "ready"
