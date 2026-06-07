from pathlib import Path
from types import SimpleNamespace

from app.services.parser_artifact_local_ingestion_loop import (
    export_parser_artifact_local_ingestion_loop_report,
    run_parser_artifact_local_ingestion_loop,
)


def test_parser_artifact_local_ingestion_loop_go_writes_summary(tmp_path):
    artifact_path = tmp_path / "artifact.json"
    artifact_path.write_text("{}", encoding="utf-8")

    report = export_parser_artifact_local_ingestion_loop_report(
        artifact_path=artifact_path,
        output_dir=tmp_path / "loop",
        artifact_boundary_exporter=_artifact_boundary_exporter("go"),
        ingestion_loop_exporter=_ingestion_loop_exporter("go"),
    )

    assert report.decision == "go"
    assert report.reason_code == "parser_artifact_local_ingestion_ready"
    assert report.source_id == "company_profile_2025_trial"
    assert report.artifact_id == "company_profile_pdf_pages_1_5"
    assert [step.id for step in report.steps] == [
        "parser_artifact_boundary",
        "approved_source_ingestion_loop",
    ]
    assert report.summary["artifact_materialized"] is True
    assert report.summary["approved_source_ingestion_decision"] == "go"
    assert report.summary["source_binding_status"] == "not_created"
    assert report.summary["runtime_promotion_status"] == "keep_runtime_defaults"
    assert report.summary["graph_execution_status"] == "not_executed"
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert "- Decision: `go`" in report.markdown_path.read_text(encoding="utf-8")


def test_parser_artifact_local_ingestion_loop_reviews_before_ingestion(tmp_path):
    report = run_parser_artifact_local_ingestion_loop(
        artifact_path=tmp_path / "artifact.json",
        output_dir=tmp_path / "loop",
        artifact_boundary_exporter=_artifact_boundary_exporter(
            "review",
            reason_code="artifact_missing_citation_anchors",
        ),
        ingestion_loop_exporter=_should_not_run,
    )

    assert report.decision == "review"
    assert report.reason_code == "parser_artifact_boundary_review"
    assert [step.id for step in report.steps] == ["parser_artifact_boundary"]
    assert report.steps[0].reason_code == "artifact_missing_citation_anchors"


def test_parser_artifact_local_ingestion_loop_blocks_on_raw_artifact(tmp_path):
    report = run_parser_artifact_local_ingestion_loop(
        artifact_path=tmp_path / "company.pdf",
        output_dir=tmp_path / "loop",
        artifact_boundary_exporter=_artifact_boundary_exporter(
            "blocked",
            reason_code="normalized_parser_artifact_required",
        ),
        ingestion_loop_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "parser_artifact_boundary_blocked"
    assert "does_not_parse_raw_pdf" in report.non_goals
    assert report.summary["raw_parser_execution_status"] == "not_executed"


def test_parser_artifact_local_ingestion_loop_blocks_when_ingestion_blocks(tmp_path):
    report = run_parser_artifact_local_ingestion_loop(
        artifact_path=tmp_path / "artifact.json",
        output_dir=tmp_path / "loop",
        artifact_boundary_exporter=_artifact_boundary_exporter("go"),
        ingestion_loop_exporter=_ingestion_loop_exporter(
            "blocked",
            reason_code="ingestion_preflight_blocked",
        ),
    )

    assert report.decision == "blocked"
    assert report.reason_code == "approved_source_ingestion_loop_blocked"
    assert [step.id for step in report.steps] == [
        "parser_artifact_boundary",
        "approved_source_ingestion_loop",
    ]
    assert report.steps[-1].reason_code == "ingestion_preflight_blocked"


def _artifact_boundary_exporter(decision, *, reason_code=None):
    def exporter(*, output_dir, artifact_path, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        markdown_path = output_dir / "parser-derived-source.md"
        overlay_path = output_dir / "parser-derived-source-overlay.json"
        json_path = output_dir / "normalized-parser-artifact-boundary.json"
        report_path = output_dir / "normalized-parser-artifact-boundary.md"
        json_path.write_text("{}", encoding="utf-8")
        report_path.write_text("# artifact\n", encoding="utf-8")
        if decision == "go":
            markdown_path.write_text("# 公司简介\n\n公司主营业务包括工程咨询。", encoding="utf-8")
            overlay_path.write_text("{}", encoding="utf-8")
        return SimpleNamespace(
            decision=decision,
            reason_code=reason_code or f"artifact_{decision}",
            artifact_id="company_profile_pdf_pages_1_5",
            source_id="company_profile_2025_trial",
            title="公司简介 2025 trial",
            parser_id="external-pdf-markdown-v1",
            original_file_path="D:/xwechat_files/company_profile.pdf",
            content_sha256="1" * 64,
            markdown_artifact_path=markdown_path if decision == "go" else None,
            source_overlay_path=overlay_path if decision == "go" else None,
            json_path=json_path,
            markdown_path=report_path,
            summary={
                "text_block_count": 2 if decision == "go" else 1,
                "citation_anchor_count": 2 if decision == "go" else 0,
                "raw_parser_execution_status": "not_executed",
            },
            recommended_actions=[f"artifact_{decision}_action"],
            non_goals=["does_not_parse_raw_pdf"],
        )

    return exporter


def _ingestion_loop_exporter(decision, *, reason_code=None):
    def exporter(*, output_dir, markdown_path, source_id, title, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "local-approved-source-ingestion-loop.json"
        report_path = output_dir / "local-approved-source-ingestion-loop.md"
        json_path.write_text("{}", encoding="utf-8")
        report_path.write_text("# ingestion\n", encoding="utf-8")
        return SimpleNamespace(
            decision=decision,
            reason_code=reason_code or f"ingestion_{decision}",
            source_id=source_id,
            title=title,
            markdown_path=Path(markdown_path),
            query="公司主营业务是什么？",
            top_k=3,
            json_path=json_path,
            markdown_path_out=report_path,
            steps=[],
            summary={
                "explicit_ingestion_job_created": decision == "go",
                "index_status": "ready" if decision == "go" else "blocked",
            },
            recommended_actions=[f"ingestion_{decision}_action"],
            non_goals=["does_not_execute_graphrag"],
        )

    return exporter


def _should_not_run(**kwargs):
    raise AssertionError("step should not run")
