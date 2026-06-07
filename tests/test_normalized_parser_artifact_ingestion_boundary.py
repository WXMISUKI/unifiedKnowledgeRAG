import json

from app.services.normalized_parser_artifact_ingestion_boundary import (
    export_normalized_parser_artifact_ingestion_boundary_report,
    run_normalized_parser_artifact_ingestion_boundary,
)


def test_ready_parser_artifact_materializes_markdown_and_overlay(tmp_path):
    artifact_path = tmp_path / "artifact.json"
    _write_artifact(artifact_path)

    report = export_normalized_parser_artifact_ingestion_boundary_report(
        artifact_path=artifact_path,
        output_dir=tmp_path / "out",
    )

    assert report.decision == "go"
    assert report.reason_code == "parser_artifact_ready_for_local_onboarding"
    assert report.source_id == "company_profile_2025_trial"
    assert report.summary["text_block_count"] == 2
    assert report.summary["citation_anchor_count"] == 2
    assert report.summary["raw_parser_execution_status"] == "not_executed"
    assert report.summary["ingestion_job_status"] == "not_created"
    assert report.markdown_artifact_path.exists()
    assert report.source_overlay_path.exists()
    assert report.json_path.exists()
    assert report.markdown_path.exists()

    markdown = report.markdown_artifact_path.read_text(encoding="utf-8")
    assert "# 公司简介 2025 trial" in markdown
    assert "公司主营业务包括工程咨询、试验检测和数字化服务。" in markdown
    assert "<!-- citation: company_profile_2025_trial#page-1 -->" in markdown

    overlay = json.loads(report.source_overlay_path.read_text(encoding="utf-8"))
    assert overlay["source_id"] == "company_profile_2025_trial"
    assert overlay["parser_artifact"]["artifact_id"] == "company_profile_pdf_pages_1_5"
    assert overlay["parser_artifact"]["parser_id"] == "external-pdf-markdown-v1"


def test_parser_artifact_blocks_without_text_blocks(tmp_path):
    artifact_path = tmp_path / "artifact.json"
    _write_artifact(artifact_path, text_blocks=[])

    report = run_normalized_parser_artifact_ingestion_boundary(
        artifact_path=artifact_path,
        output_dir=tmp_path / "out",
    )

    assert report.decision == "blocked"
    assert report.reason_code == "artifact_has_no_text_blocks"
    assert report.markdown_artifact_path is None
    assert report.summary["materialized_markdown_status"] == "not_written"


def test_parser_artifact_reviews_without_citation_anchors(tmp_path):
    artifact_path = tmp_path / "artifact.json"
    _write_artifact(
        artifact_path,
        text_blocks=[
            {
                "block_id": "page-1-block-1",
                "text": "公司主营业务包括工程咨询、试验检测和数字化服务。",
                "provenance": {"page": 1},
            }
        ],
    )

    report = run_normalized_parser_artifact_ingestion_boundary(
        artifact_path=artifact_path,
        output_dir=tmp_path / "out",
    )

    assert report.decision == "review"
    assert report.reason_code == "artifact_missing_citation_anchors"
    assert report.markdown_artifact_path is None
    assert report.summary["text_block_count"] == 1


def test_raw_pdf_input_is_blocked_before_provider_ingestion(tmp_path):
    pdf_path = tmp_path / "company.pdf"
    pdf_path.write_bytes(b"%PDF-1.7 fake")

    report = run_normalized_parser_artifact_ingestion_boundary(
        artifact_path=pdf_path,
        output_dir=tmp_path / "out",
    )

    assert report.decision == "blocked"
    assert report.reason_code == "normalized_parser_artifact_required"
    assert "does_not_parse_raw_pdf" in report.non_goals
    assert report.summary["raw_parser_execution_status"] == "not_executed"


def _write_artifact(path, *, text_blocks=None):
    if text_blocks is None:
        text_blocks = [
            {
                "block_id": "page-1-block-1",
                "text": "公司主营业务包括工程咨询、试验检测和数字化服务。",
                "citation": "company_profile_2025_trial#page-1",
                "provenance": {"page": 1},
            },
            {
                "block_id": "page-2-block-1",
                "text": "公司服务对象覆盖交通、市政和能源行业客户。",
                "citation": "company_profile_2025_trial#page-2",
                "provenance": {"page": 2},
            },
        ]
    path.write_text(
        json.dumps(
            {
                "artifact_id": "company_profile_pdf_pages_1_5",
                "source_id": "company_profile_2025_trial",
                "title": "公司简介 2025 trial",
                "owner": "local_trial",
                "domain": "company_profile",
                "language": "zh-CN",
                "sensitivity": "local_private_trial",
                "original_file": {
                    "path": "D:/xwechat_files/company_profile.pdf",
                    "name": "公司简介2025年10月27日(1).pdf",
                    "sha256": "0" * 64,
                    "page_range": "1-5",
                },
                "parser": {
                    "parser_id": "external-pdf-markdown-v1",
                    "parser_version": "trial",
                    "parsed_at": "2026-06-07T00:00:00+00:00",
                },
                "text_blocks": text_blocks,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
