from types import SimpleNamespace

from app.services.local_enterprise_corpus_ingestion_qa_loop import (
    export_local_enterprise_corpus_ingestion_qa_loop_report,
    run_local_enterprise_corpus_ingestion_qa_loop,
)


def test_enterprise_corpus_loop_go_for_markdown_input(tmp_path):
    source_file = tmp_path / "company.md"
    source_file.write_text("# 公司简介\n\n公司主营业务包括交通工程咨询监理。", encoding="utf-8")

    report = export_local_enterprise_corpus_ingestion_qa_loop_report(
        input_path=source_file,
        source_id="company_profile_trial",
        title="公司简介 trial",
        query="公司主营业务是什么？",
        output_dir=tmp_path / "out",
        ingestion_loop_exporter=_ingestion_exporter("go"),
    )

    assert report.decision == "go"
    assert report.reason_code == "local_enterprise_corpus_qa_ready"
    assert report.input_format == "markdown"
    assert report.materialized_markdown_path == source_file.resolve()
    assert report.summary["source_binding_status"] == "not_created"
    assert report.summary["runtime_promotion_status"] == "keep_runtime_defaults"
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert "Local Enterprise Corpus Ingestion QA Loop" in report.markdown_path.read_text(encoding="utf-8")


def test_enterprise_corpus_loop_materializes_txt_input(tmp_path):
    source_file = tmp_path / "company.txt"
    source_file.write_text("公司主营业务包括试验检测服务。", encoding="utf-8")
    calls = []

    report = run_local_enterprise_corpus_ingestion_qa_loop(
        input_path=source_file,
        source_id="company_txt_trial",
        title="公司文本 trial",
        output_dir=tmp_path / "out",
        ingestion_loop_exporter=_recording_ingestion_exporter(calls, "go"),
    )

    assert report.decision == "go"
    assert report.input_format == "txt"
    assert report.materialized_markdown_path.suffix == ".md"
    assert report.materialized_markdown_path.exists()
    assert calls[0]["markdown_path"] == report.materialized_markdown_path
    assert "公司主营业务包括试验检测服务" in report.materialized_markdown_path.read_text(encoding="utf-8")


def test_enterprise_corpus_loop_blocks_missing_input(tmp_path):
    report = run_local_enterprise_corpus_ingestion_qa_loop(
        input_path=tmp_path / "missing.md",
        output_dir=tmp_path / "out",
        ingestion_loop_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "input_file_missing"
    assert report.summary["input_status"] == "missing"


def test_enterprise_corpus_loop_blocks_raw_pdf_with_recovery_actions(tmp_path):
    source_file = tmp_path / "company.pdf"
    source_file.write_bytes(b"%PDF-1.7")

    report = run_local_enterprise_corpus_ingestion_qa_loop(
        input_path=source_file,
        output_dir=tmp_path / "out",
        ingestion_loop_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "raw_pdf_requires_parser_artifact"
    assert "convert_pdf_to_markdown_with_parser_or_ocr" in report.recommended_actions
    assert "does_not_start_ocr_services" in report.non_goals


def test_enterprise_corpus_loop_blocks_unsupported_format(tmp_path):
    source_file = tmp_path / "company.docx"
    source_file.write_bytes(b"docx")

    report = run_local_enterprise_corpus_ingestion_qa_loop(
        input_path=source_file,
        output_dir=tmp_path / "out",
        ingestion_loop_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "unsupported_input_format"


def test_enterprise_corpus_loop_reviews_when_downstream_reviews(tmp_path):
    source_file = tmp_path / "company.md"
    source_file.write_text("公司主营业务包括交通工程。", encoding="utf-8")

    report = run_local_enterprise_corpus_ingestion_qa_loop(
        input_path=source_file,
        output_dir=tmp_path / "out",
        ingestion_loop_exporter=_ingestion_exporter("review", reason_code="acceptance_smoke_review"),
    )

    assert report.decision == "review"
    assert report.reason_code == "downstream_acceptance_smoke_review"
    assert report.downstream["decision"] == "review"


def test_enterprise_corpus_loop_blocks_when_downstream_blocks(tmp_path):
    source_file = tmp_path / "company.md"
    source_file.write_text("公司主营业务包括交通工程。", encoding="utf-8")

    report = run_local_enterprise_corpus_ingestion_qa_loop(
        input_path=source_file,
        output_dir=tmp_path / "out",
        ingestion_loop_exporter=_ingestion_exporter("blocked", reason_code="ingestion_preflight_blocked"),
    )

    assert report.decision == "blocked"
    assert report.reason_code == "downstream_ingestion_preflight_blocked"


def test_enterprise_corpus_loop_preserves_lightweight_boundary(tmp_path):
    source_file = tmp_path / "company.md"
    source_file.write_text("公司主营业务包括交通工程。", encoding="utf-8")

    report = run_local_enterprise_corpus_ingestion_qa_loop(
        input_path=source_file,
        output_dir=tmp_path / "out",
        ingestion_loop_exporter=_ingestion_exporter("go"),
    )

    assert "does_not_call_myprivateagent" in report.non_goals
    assert "does_not_create_source_to_agent_binding" in report.non_goals
    assert "does_not_start_ocr_services" in report.non_goals
    assert "does_not_execute_graphrag" in report.non_goals


def _ingestion_exporter(decision, *, reason_code=None):
    def exporter(*, output_dir, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "local-approved-source-ingestion-loop.json"
        markdown_path = output_dir / "local-approved-source-ingestion-loop.md"
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# downstream\n", encoding="utf-8")
        return SimpleNamespace(
            decision=decision,
            reason_code=reason_code or f"downstream_{decision}",
            source_id=kwargs.get("source_id"),
            title=kwargs.get("title"),
            query=kwargs.get("query"),
            top_k=kwargs.get("top_k"),
            json_path=json_path,
            markdown_path_out=markdown_path,
            summary={
                "final_decision": decision,
                "source_binding_status": "not_created",
                "runtime_promotion_status": "keep_runtime_defaults",
                "graph_execution_status": "not_executed",
            },
        )

    return exporter


def _recording_ingestion_exporter(calls, decision):
    def exporter(*, markdown_path, output_dir, **kwargs):
        calls.append({"markdown_path": markdown_path, "output_dir": output_dir, **kwargs})
        return _ingestion_exporter(decision)(markdown_path=markdown_path, output_dir=output_dir, **kwargs)

    return exporter


def _should_not_run(**kwargs):
    raise AssertionError("downstream ingestion loop should not run")
