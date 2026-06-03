import json
from pathlib import Path

from app.services.phase12d_pgvector_live_probe_readiness import (
    build_phase12d_pgvector_live_probe_readiness_report,
    export_phase12d_pgvector_live_probe_readiness_report,
    render_phase12d_pgvector_live_probe_readiness_markdown,
)


def test_build_phase12d_pgvector_live_probe_readiness_defaults_to_blocked_without_configuration(
    monkeypatch,
):
    for env_name in [
        "PGVECTOR_DATABASE_URL",
        "PGVECTOR_SCHEMA",
        "PGVECTOR_TABLE",
        "PGVECTOR_INDEX_NAME",
        "PGVECTOR_VECTOR_SIZE",
        "PGVECTOR_PROBE_TIMEOUT_SECONDS",
    ]:
        monkeypatch.delenv(env_name, raising=False)

    report = build_phase12d_pgvector_live_probe_readiness_report()

    assert report.id == "phase12d-pgvector-live-probe-readiness-v1"
    assert report.status == "blocked"
    assert report.decision == "keep_current_default"
    assert report.summary["strategy_verdict"] == "continue_provider_first_with_candidate_backends"
    assert report.summary["pgvector_database_url_present"] is False
    assert report.summary["candidate_backend_id"] == "pgvector"
    assert any(signal.id == "pgvector_configuration" for signal in report.signals)
    assert any(family.id == "pgvector_probe_gate" for family in report.candidate_families)


def test_build_phase12d_pgvector_live_probe_readiness_is_ready_with_fake_driver(
    monkeypatch,
):
    monkeypatch.setenv(
        "PGVECTOR_DATABASE_URL",
        "postgresql://user:password@localhost:5432/unifiedKnowledgeRAG",
    )
    monkeypatch.setenv("PGVECTOR_SCHEMA", "public")
    monkeypatch.setenv("PGVECTOR_TABLE", "knowledge_chunks")
    monkeypatch.setenv("PGVECTOR_INDEX_NAME", "knowledge_chunks_embedding_idx")
    monkeypatch.setenv("PGVECTOR_VECTOR_SIZE", "1024")
    monkeypatch.setenv("PGVECTOR_PROBE_TIMEOUT_SECONDS", "5")
    monkeypatch.setattr(
        "app.services.phase12d_pgvector_live_probe_readiness.import_module",
        lambda name: _fake_psycopg_module()
        if name == "psycopg"
        else __import__(name),
    )

    report = build_phase12d_pgvector_live_probe_readiness_report(
        base_dir=Path(__file__).resolve().parents[1]
    )

    assert report.status == "ready"
    assert report.decision == "eligible_for_promotion_review"
    assert report.summary["pgvector_database_url_present"] is True
    assert report.summary["pgvector_driver_available"] is True
    assert report.summary["pgvector_connection_status"] == "ready"
    assert report.summary["pgvector_extension_installed"] is True
    assert report.summary["pgvector_schema_exists"] is True
    assert report.summary["pgvector_table_exists"] is True
    assert report.summary["pgvector_index_exists"] is True
    assert report.summary["pgvector_server_version"] == "PostgreSQL 16.3"


def test_export_phase12d_pgvector_live_probe_readiness_writes_outputs(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setenv(
        "PGVECTOR_DATABASE_URL",
        "postgresql://user:password@localhost:5432/unifiedKnowledgeRAG",
    )
    monkeypatch.setenv("PGVECTOR_SCHEMA", "public")
    monkeypatch.setenv("PGVECTOR_TABLE", "knowledge_chunks")
    monkeypatch.setenv("PGVECTOR_INDEX_NAME", "knowledge_chunks_embedding_idx")
    monkeypatch.setenv("PGVECTOR_VECTOR_SIZE", "1024")
    monkeypatch.setenv("PGVECTOR_PROBE_TIMEOUT_SECONDS", "5")
    monkeypatch.setattr(
        "app.services.phase12d_pgvector_live_probe_readiness.import_module",
        lambda name: _fake_psycopg_module()
        if name == "psycopg"
        else __import__(name),
    )

    report = export_phase12d_pgvector_live_probe_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=Path(__file__).resolve().parents[1],
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["summary"]["candidate_backend_id"] == "pgvector"
    assert "# Phase 12d PGVector Live Probe Readiness" in markdown
    assert render_phase12d_pgvector_live_probe_readiness_markdown(report) == markdown


class _FakeCursor:
    def __init__(self):
        self._results = iter(
            [
                ("PostgreSQL 16.3",),
                (True,),
                ("public.knowledge_chunks",),
                (True,),
                (True,),
            ]
        )

    def execute(self, *args, **kwargs):
        return None

    def fetchone(self):
        return next(self._results)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeConnection:
    def __init__(self):
        self.closed = False

    def cursor(self):
        return _FakeCursor()

    def close(self):
        self.closed = True


class _FakePsycopgModule:
    def connect(self, database_url, connect_timeout=None):
        assert database_url.startswith("postgresql://")
        assert connect_timeout == 5
        return _FakeConnection()


def _fake_psycopg_module():
    return _FakePsycopgModule()
