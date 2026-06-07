from pathlib import Path
from types import SimpleNamespace

from app.services.local_approved_source_ingestion_loop import (
    export_local_approved_source_ingestion_loop_report,
    run_local_approved_source_ingestion_loop,
)


def test_ingestion_loop_go_writes_summary(tmp_path):
    markdown_path = tmp_path / "company.md"
    markdown_path.write_text("公司主营业务包括交通工程咨询监理。", encoding="utf-8")

    report = export_local_approved_source_ingestion_loop_report(
        markdown_path=markdown_path,
        source_id="company_profile_trial",
        title="公司简介 trial",
        query="公司主营业务是什么？",
        output_dir=tmp_path / "loop",
        onboarding_exporter=_onboarding_exporter("go"),
        preflight_getter=_preflight_getter("ready"),
        ingestion_job_creator=_ingestion_job_creator("completed"),
        index_status_getter=_index_status_getter("ready"),
        acceptance_exporter=_acceptance_exporter("go"),
    )

    assert report.decision == "go"
    assert report.reason_code == "local_approved_source_ingestion_ready"
    assert [step.id for step in report.steps] == [
        "document_source_onboarding",
        "ingestion_preflight",
        "ingestion_job",
        "index_status",
        "acceptance_smoke",
    ]
    assert report.summary["explicit_ingestion_job_created"] is True
    assert report.summary["source_binding_status"] == "not_created"
    assert report.summary["runtime_promotion_status"] == "keep_runtime_defaults"
    assert report.summary["graph_execution_status"] == "not_executed"
    assert report.json_path.exists()
    assert report.markdown_path_out.exists()
    assert "- Decision: `go`" in report.markdown_path_out.read_text(encoding="utf-8")


def test_ingestion_loop_blocks_when_onboarding_blocks(tmp_path):
    report = run_local_approved_source_ingestion_loop(
        markdown_path=tmp_path / "missing.md",
        output_dir=tmp_path / "loop",
        onboarding_exporter=_onboarding_exporter("blocked", reason_code="markdown_file_missing"),
        preflight_getter=_should_not_run,
        ingestion_job_creator=_should_not_run,
        index_status_getter=_should_not_run,
        acceptance_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "onboarding_blocked"
    assert [step.id for step in report.steps] == ["document_source_onboarding"]
    assert report.steps[0].reason_code == "markdown_file_missing"


def test_ingestion_loop_blocks_when_preflight_not_ready(tmp_path):
    report = run_local_approved_source_ingestion_loop(
        markdown_path=tmp_path / "company.md",
        output_dir=tmp_path / "loop",
        onboarding_exporter=_onboarding_exporter("go"),
        preflight_getter=_preflight_getter("blocked"),
        ingestion_job_creator=_should_not_run,
        index_status_getter=_should_not_run,
        acceptance_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "ingestion_preflight_blocked"
    assert report.steps[-1].id == "ingestion_preflight"


def test_ingestion_loop_blocks_when_job_fails(tmp_path):
    report = run_local_approved_source_ingestion_loop(
        markdown_path=tmp_path / "company.md",
        output_dir=tmp_path / "loop",
        onboarding_exporter=_onboarding_exporter("go"),
        preflight_getter=_preflight_getter("ready"),
        ingestion_job_creator=_ingestion_job_creator("failed"),
        index_status_getter=_should_not_run,
        acceptance_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "ingestion_job_blocked"
    assert report.steps[-1].status == "failed"


def test_ingestion_loop_reviews_when_acceptance_reviews(tmp_path):
    report = run_local_approved_source_ingestion_loop(
        markdown_path=tmp_path / "company.md",
        output_dir=tmp_path / "loop",
        onboarding_exporter=_onboarding_exporter("go"),
        preflight_getter=_preflight_getter("ready"),
        ingestion_job_creator=_ingestion_job_creator("completed"),
        index_status_getter=_index_status_getter("ready"),
        acceptance_exporter=_acceptance_exporter("review", reason_code="acceptance_needs_review"),
    )

    assert report.decision == "review"
    assert report.reason_code == "acceptance_smoke_review"
    assert report.steps[-1].id == "acceptance_smoke"


def test_ingestion_loop_non_goals_preserve_lightweight_boundary(tmp_path):
    report = run_local_approved_source_ingestion_loop(
        markdown_path=tmp_path / "company.md",
        output_dir=tmp_path / "loop",
        onboarding_exporter=_onboarding_exporter("go"),
        preflight_getter=_preflight_getter("ready"),
        ingestion_job_creator=_ingestion_job_creator("completed"),
        index_status_getter=_index_status_getter("ready"),
        acceptance_exporter=_acceptance_exporter("go"),
    )

    assert "does_not_parse_raw_pdf_as_supported_ingestion" in report.non_goals
    assert "does_not_start_ocr_services" in report.non_goals
    assert "does_not_call_myprivateagent" in report.non_goals
    assert "does_not_create_source_to_agent_binding" in report.non_goals
    assert "does_not_execute_graphrag" in report.non_goals


def _onboarding_exporter(decision, *, reason_code=None):
    def exporter(*, output_dir, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "local-document-source-onboarding.json"
        markdown_path = output_dir / "local-document-source-onboarding.md"
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# onboarding\n", encoding="utf-8")
        return SimpleNamespace(
            decision=decision,
            reason_code=reason_code or f"onboarding_{decision}",
            json_path=json_path,
            markdown_path_out=markdown_path,
            summary={"decision": decision},
        )

    return exporter


def _preflight_getter(status):
    def getter(source_id, **kwargs):
        return SimpleNamespace(
            ok=True,
            result=SimpleNamespace(
                source_id=source_id,
                status=status,
                retrieval_backend="fixture",
                index_status="ready",
                latest_index_job_id=None,
                documents=[object()] if status == "ready" else [],
                recommended_action="run_ingestion_job" if status == "ready" else "review_ingestion_preflight",
            ),
        )

    return getter


def _ingestion_job_creator(status):
    def creator(source_id, **kwargs):
        return True, SimpleNamespace(
            job_id="idx_test",
            source_id=source_id,
            status=status,
            requested_at="2026-06-07T00:00:00+00:00",
            completed_at="2026-06-07T00:00:01+00:00" if status in {"completed", "failed"} else None,
            error=SimpleNamespace(code="INDEX_BUILD_FAILED") if status == "failed" else None,
        ), None

    return creator


def _index_status_getter(status):
    def getter(source_id, **kwargs):
        return SimpleNamespace(
            source_id=source_id,
            status=status,
            backend="fixture",
            indexed_at="2026-06-07T00:00:01+00:00" if status == "ready" else None,
            latest_job_id="idx_test" if status == "ready" else None,
            reason="ready" if status == "ready" else "not ready",
            error=None,
        )

    return getter


def _acceptance_exporter(decision, *, reason_code=None):
    def exporter(*, output_dir, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "approved-local-corpus-acceptance-smoke.json"
        markdown_path = output_dir / "approved-local-corpus-acceptance-smoke.md"
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# acceptance\n", encoding="utf-8")
        return SimpleNamespace(
            decision=decision,
            reason_code=reason_code or f"acceptance_{decision}",
            json_path=json_path,
            markdown_path=markdown_path,
            summary={"decision": decision},
        )

    return exporter


def _should_not_run(**kwargs):
    raise AssertionError("step should not run")

