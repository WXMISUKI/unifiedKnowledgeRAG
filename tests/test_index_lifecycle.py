from fastapi.testclient import TestClient

from app.main import create_app
from app.config import Settings
from app.services.index_lifecycle import clear_local_jobs_for_tests, get_index_status
from app.services.index_lifecycle_store import IndexLifecycleStore


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
    clear_local_jobs_for_tests(Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
    ))
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

    store = IndexLifecycleStore(Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
    ))
    assert store.jobs_path.exists()
    assert store.sources_path.exists()
    assert store.latest_job_for_source("refund_policy_docs").job_id == body["job"]["job_id"]
    assert store.read_source_status("refund_policy_docs").latest_job_id == body["job"]["job_id"]


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


def test_index_status_survives_process_restart_style_reload(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    client = TestClient(create_app())

    job = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"}).json()["job"]

    fresh_settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=index_dir,
    )
    reloaded_status = get_index_status("refund_policy_docs", fresh_settings)

    assert reloaded_status.status == "ready"
    assert reloaded_status.latest_job_id == job["job_id"]
    assert reloaded_status.indexed_at is not None


def test_source_status_manifest_is_canonical(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    client = TestClient(create_app())

    client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"})

    assert (index_dir / "sources.json").exists()
    assert not (index_dir / "refund_policy_docs.index.json").exists()
    status = client.get("/api/indexes/refund_policy_docs/status").json()
    assert status["status"] == "ready"


def test_ingestion_jobs_can_be_listed_and_filtered(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    (source_dir / "logistics_faq.md").write_text("logistics docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    first = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"}).json()["job"]
    second = client.post("/api/ingestion/jobs", json={"source_id": "logistics_faq"}).json()["job"]

    all_jobs = client.get("/api/ingestion/jobs").json()["jobs"]
    refund_jobs = client.get("/api/ingestion/jobs?source_id=refund_policy_docs").json()["jobs"]
    completed_jobs = client.get("/api/ingestion/jobs?status=completed").json()["jobs"]

    assert first["job_id"] in {job["job_id"] for job in all_jobs}
    assert second["job_id"] in {job["job_id"] for job in all_jobs}
    assert {job["source_id"] for job in refund_jobs} == {"refund_policy_docs"}
    assert {job["status"] for job in completed_jobs} == {"completed"}


def test_ingestion_job_detail_and_missing_error(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    job = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"}).json()["job"]

    detail = client.get(f"/api/ingestion/jobs/{job['job_id']}").json()
    missing = client.get("/api/ingestion/jobs/missing-job").json()

    assert detail["ok"] is True
    assert detail["job"]["job_id"] == job["job_id"]
    assert missing["ok"] is False
    assert missing["error"]["code"] == "JOB_NOT_FOUND"


def test_failed_ingestion_job_can_be_retried(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    client = TestClient(create_app())

    failed = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"}).json()["job"]
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    retry = client.post(f"/api/ingestion/jobs/{failed['job_id']}/retry").json()

    assert failed["status"] == "failed"
    assert retry["ok"] is True
    assert retry["job"]["job_id"] != failed["job_id"]
    assert retry["job"]["source_id"] == "refund_policy_docs"
    assert retry["job"]["status"] == "completed"


def test_non_failed_ingestion_job_retry_is_rejected(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    completed = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"}).json()["job"]
    retry = client.post(f"/api/ingestion/jobs/{completed['job_id']}/retry").json()

    assert completed["status"] == "completed"
    assert retry["ok"] is False
    assert retry["error"]["code"] == "JOB_RETRY_NOT_ALLOWED"
