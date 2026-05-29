from fastapi.testclient import TestClient
from datetime import UTC, datetime, timedelta

from app.main import create_app
from app.config import Settings
from app.models.contracts import EvidenceDocument, IndexLifecycleJob, IndexStatusResponse
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


def test_answer_returns_index_not_ready_for_llamaindex(monkeypatch, tmp_path):
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
        "/api/rag/answer",
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


def test_retrieval_returns_index_not_ready_before_qdrant_query(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "qdrant")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    monkeypatch.setenv("EMBEDDING_VECTOR_SIZE", "3")

    def fail_if_called(**kwargs):
        raise AssertionError("Qdrant retrieval should not run before index readiness passes")

    monkeypatch.setattr(
        "app.services.qdrant_vector_store.query_qdrant_documents_for_text",
        fail_if_called,
    )
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


def test_retrieval_calls_qdrant_after_source_index_is_ready(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "qdrant")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    monkeypatch.setenv("EMBEDDING_VECTOR_SIZE", "3")
    settings = Settings(
        rag_retrieval_backend="qdrant",
        rag_source_dir=source_dir,
        rag_index_dir=index_dir,
        embedding_vector_size=3,
    )
    IndexLifecycleStore(settings).write_source_status(IndexStatusResponse(
        source_id="refund_policy_docs",
        status="ready",
        backend="qdrant",
        indexed_at="2026-05-28T00:00:00+00:00",
        latest_job_id="idx_qdrant_ready",
    ))
    calls = []

    def fake_query(**kwargs):
        calls.append(kwargs)
        return [
            EvidenceDocument(
                source_id="refund_policy_docs",
                document_id="refund_policy_2026",
                title="售后退款规则",
                snippet="客户三天未发货可以申请退款。",
                score=0.91,
                citation="refund_policy_2026#chunk-1",
            )
        ]

    monkeypatch.setattr(
        "app.services.qdrant_vector_store.create_qdrant_client",
        lambda settings: object(),
    )
    monkeypatch.setattr(
        "app.services.qdrant_vector_store.query_qdrant_documents_for_text",
        fake_query,
    )
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
    assert body["ok"] is True
    assert body["result"]["documents"][0]["citation"] == "refund_policy_2026#chunk-1"
    assert calls[0]["source_ids"] == ["refund_policy_docs"]


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
    assert len(all_jobs) == 2
    assert all(job["status"] == "completed" for job in all_jobs)


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


def test_ingestion_job_list_is_paginated(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    (source_dir / "logistics_faq.md").write_text("logistics docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"})
    client.post("/api/ingestion/jobs", json={"source_id": "logistics_faq"})

    first_page = client.get("/api/ingestion/jobs?limit=1&offset=0").json()
    second_page = client.get("/api/ingestion/jobs?limit=1&offset=1").json()

    assert first_page["ok"] is True
    assert first_page["total"] == 2
    assert first_page["limit"] == 1
    assert first_page["offset"] == 0
    assert first_page["has_more"] is True
    assert len(first_page["jobs"]) == 1
    assert second_page["total"] == 2
    assert second_page["offset"] == 1
    assert second_page["has_more"] is False
    assert len(second_page["jobs"]) == 1


def test_ingestion_job_filtered_total_uses_latest_logical_jobs(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"})

    completed = client.get("/api/ingestion/jobs?status=completed").json()
    running = client.get("/api/ingestion/jobs?status=running").json()

    assert completed["total"] == 1
    assert len(completed["jobs"]) == 1
    assert completed["jobs"][0]["status"] == "completed"
    assert running["total"] == 0
    assert running["jobs"] == []


def test_ingestion_job_retention_compacts_latest_logical_jobs(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    (source_dir / "logistics_faq.md").write_text("logistics docs", encoding="utf-8")
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    client = TestClient(create_app())

    first = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"}).json()["job"]
    second = client.post("/api/ingestion/jobs", json={"source_id": "logistics_faq"}).json()["job"]

    response = client.post(
        "/api/ingestion/jobs/retention/compact",
        json={"keep_latest": 1},
    )
    jobs = client.get("/api/ingestion/jobs").json()
    lines = (index_dir / "jobs.jsonl").read_text(encoding="utf-8").splitlines()

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["result"] == {
        "before_count": 2,
        "after_count": 1,
        "removed_count": 1,
        "keep_latest": 1,
    }
    assert jobs["total"] == 1
    assert jobs["jobs"][0]["job_id"] in {first["job_id"], second["job_id"]}
    assert len(lines) == 1


def test_running_ingestion_job_can_be_canceled(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=index_dir,
    )
    IndexLifecycleStore(settings).append_job(IndexLifecycleJob(
        job_id="idx_running_cancel",
        source_id="refund_policy_docs",
        status="running",
        requested_at=datetime.now(UTC).isoformat(),
    ))
    client = TestClient(create_app())

    response = client.post(
        "/api/ingestion/jobs/idx_running_cancel/cancel",
        json={"reason": "operator stop"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["job"]["status"] == "canceled"
    assert body["job"]["error"]["code"] == "JOB_CANCELED"
    status = client.get("/api/indexes/refund_policy_docs/status").json()
    assert status["status"] == "canceled"
    assert status["latest_job_id"] == "idx_running_cancel"


def test_terminal_ingestion_job_cancel_is_rejected(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    completed = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"}).json()["job"]
    response = client.post(
        f"/api/ingestion/jobs/{completed['job_id']}/cancel",
        json={"reason": "too late"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["error"]["code"] == "JOB_CANCEL_NOT_ALLOWED"


def test_stale_running_jobs_are_recovered_as_failed(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=index_dir,
    )
    store = IndexLifecycleStore(settings)
    store.append_job(IndexLifecycleJob(
        job_id="idx_old_running",
        source_id="refund_policy_docs",
        status="running",
        requested_at=(datetime.now(UTC) - timedelta(hours=2)).isoformat(),
    ))
    store.append_job(IndexLifecycleJob(
        job_id="idx_fresh_running",
        source_id="logistics_faq",
        status="running",
        requested_at=datetime.now(UTC).isoformat(),
    ))
    client = TestClient(create_app())

    response = client.post(
        "/api/ingestion/jobs/recovery/stale-running",
        json={"max_age_seconds": 3600},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["result"]["recovered_count"] == 1
    assert body["result"]["recovered_job_ids"] == ["idx_old_running"]
    old_job = client.get("/api/ingestion/jobs/idx_old_running").json()["job"]
    fresh_job = client.get("/api/ingestion/jobs/idx_fresh_running").json()["job"]
    assert old_job["status"] == "failed"
    assert old_job["error"]["code"] == "STALE_RUNNING_JOB"
    assert fresh_job["status"] == "running"


def test_stale_recovered_job_can_be_retried(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=index_dir,
    )
    IndexLifecycleStore(settings).append_job(IndexLifecycleJob(
        job_id="idx_retry_after_stale",
        source_id="refund_policy_docs",
        status="running",
        requested_at=(datetime.now(UTC) - timedelta(hours=2)).isoformat(),
    ))
    client = TestClient(create_app())

    client.post(
        "/api/ingestion/jobs/recovery/stale-running",
        json={"max_age_seconds": 3600},
    )
    retry = client.post("/api/ingestion/jobs/idx_retry_after_stale/retry").json()

    assert retry["ok"] is True
    assert retry["job"]["source_id"] == "refund_policy_docs"
    assert retry["job"]["status"] == "completed"


def test_queued_ingestion_job_does_not_build_immediately(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    response = client.post(
        "/api/ingestion/jobs",
        json={"source_id": "refund_policy_docs", "run_mode": "queued"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["job"]["status"] == "queued"
    status = client.get("/api/indexes/refund_policy_docs/status").json()
    assert status["status"] == "not_indexed"


def test_run_next_queued_ingestion_job_completes(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    queued = client.post(
        "/api/ingestion/jobs",
        json={"source_id": "refund_policy_docs", "run_mode": "queued"},
    ).json()["job"]
    response = client.post("/api/ingestion/jobs/queue/run-next")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["job"]["job_id"] == queued["job_id"]
    assert body["job"]["status"] == "completed"
    status = client.get("/api/indexes/refund_policy_docs/status").json()
    assert status["status"] == "ready"
    assert status["latest_job_id"] == queued["job_id"]


def test_run_next_queued_ingestion_job_failure(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    queued = client.post(
        "/api/ingestion/jobs",
        json={"source_id": "refund_policy_docs", "run_mode": "queued"},
    ).json()["job"]
    response = client.post("/api/ingestion/jobs/queue/run-next")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["job"]["job_id"] == queued["job_id"]
    assert body["job"]["status"] == "failed"
    assert body["job"]["error"]["code"] == "INDEX_BUILD_FAILED"


def test_run_next_queued_ingestion_job_empty_queue(monkeypatch, tmp_path):
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(tmp_path / "sources"))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    response = client.post("/api/ingestion/jobs/queue/run-next")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["error"]["code"] == "INGESTION_QUEUE_EMPTY"


def test_sync_ingestion_job_remains_default(monkeypatch, tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text("refund docs", encoding="utf-8")
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "llamaindex")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(tmp_path / "index"))
    client = TestClient(create_app())

    response = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"})

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["job"]["status"] == "completed"


def test_ingestion_job_indexes_qdrant_source(monkeypatch, tmp_path):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    fake_client = FakeQdrantClient(collection_exists=False)
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    index_dir = tmp_path / "index"
    monkeypatch.setenv("RAG_RETRIEVAL_BACKEND", "qdrant")
    monkeypatch.setenv("RAG_SOURCE_DIR", str(source_dir))
    monkeypatch.setenv("RAG_INDEX_DIR", str(index_dir))
    monkeypatch.setenv("QDRANT_URL", ":memory:")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "mock")
    monkeypatch.setenv("EMBEDDING_VECTOR_SIZE", "3")
    monkeypatch.setattr(
        "app.services.qdrant_vector_store.create_qdrant_client",
        lambda settings: fake_client,
    )
    client = TestClient(create_app())

    response = client.post("/api/ingestion/jobs", json={"source_id": "refund_policy_docs"})

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["job"]["status"] == "completed"
    assert fake_client.upserts

    status = client.get("/api/indexes/refund_policy_docs/status").json()
    assert status["status"] == "ready"
    assert status["backend"] == "qdrant"
    assert status["latest_job_id"] == body["job"]["job_id"]
