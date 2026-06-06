from pathlib import Path

from app.services.pdf_derived_markdown_corpus_trial import (
    PdfExtractionResult,
    PdfTrialDocument,
    export_pdf_derived_markdown_trial_report,
    run_pdf_derived_markdown_trial,
)


def test_pdf_derived_markdown_trial_returns_go_and_writes_artifacts(tmp_path):
    pdf_path = tmp_path / "company.pdf"
    pdf_path.write_bytes(b"%PDF-1.4")

    report = export_pdf_derived_markdown_trial_report(
        pdf_path=pdf_path,
        output_dir=tmp_path / "trial",
        query="公司主营业务是什么？",
        extractor=_ready_extractor,
    )

    assert report.decision == "go"
    assert report.reason_code == "pdf_derived_markdown_usable"
    assert report.summary["extracted_pages"] == 2
    assert report.summary["retrieved_document_count"] > 0
    assert report.markdown_path is not None
    assert report.json_path is not None
    assert report.report_markdown_path is not None
    markdown = report.markdown_path.read_text(encoding="utf-8")
    report_markdown = report.report_markdown_path.read_text(encoding="utf-8")
    assert "PDF Derived Corpus Trial" in markdown
    assert "公司主营业务包括智能制造和数字化服务" in markdown
    assert "- Decision: `go`" in report_markdown


def test_pdf_derived_markdown_trial_blocks_when_pdf_is_missing(tmp_path):
    report = run_pdf_derived_markdown_trial(
        pdf_path=tmp_path / "missing.pdf",
        output_dir=tmp_path / "trial",
        extractor=_ready_extractor,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "pdf_file_missing"
    assert report.markdown_path is None
    assert "check_pdf_path_and_rerun_trial" in report.recommended_actions


def test_pdf_derived_markdown_trial_blocks_when_extractor_is_unavailable(tmp_path):
    pdf_path = tmp_path / "company.pdf"
    pdf_path.write_bytes(b"%PDF-1.4")

    report = run_pdf_derived_markdown_trial(
        pdf_path=pdf_path,
        output_dir=tmp_path / "trial",
        extractor=_blocked_extractor,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "pdf_text_extraction_unavailable"
    assert report.summary["error"] == "extractor unavailable"


def test_pdf_derived_markdown_trial_returns_review_for_weak_evidence(tmp_path):
    pdf_path = tmp_path / "company.pdf"
    pdf_path.write_bytes(b"%PDF-1.4")

    report = run_pdf_derived_markdown_trial(
        pdf_path=pdf_path,
        output_dir=tmp_path / "trial",
        query="完全不存在的问题",
        extractor=_ready_extractor,
    )

    assert report.decision == "review"
    assert report.reason_code == "derived_evidence_needs_review"
    assert report.documents == []
    assert report.citations == []


def test_pdf_derived_markdown_trial_blocks_invalid_answer_citations(monkeypatch, tmp_path):
    pdf_path = tmp_path / "company.pdf"
    pdf_path.write_bytes(b"%PDF-1.4")

    def invalid_answer(documents: list[PdfTrialDocument]) -> tuple[str, list[str]]:
        return "bad answer", ["outside#citation"]

    monkeypatch.setattr(
        "app.services.pdf_derived_markdown_corpus_trial._compose_trial_answer",
        invalid_answer,
    )

    report = run_pdf_derived_markdown_trial(
        pdf_path=pdf_path,
        output_dir=tmp_path / "trial",
        query="公司主营业务是什么？",
        extractor=_ready_extractor,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "trial_answer_citation_blocked"
    assert report.summary["invalid_citation_count"] == 1


def _ready_extractor(pdf_path: Path, max_pages: int) -> PdfExtractionResult:
    assert pdf_path.exists()
    return PdfExtractionResult(
        status="ready",
        page_count=8,
        extractor="test",
        text_by_page=[
            "公司主营业务包括智能制造和数字化服务，服务企业客户。",
            "公司简介展示了发展历程、产品能力和客户案例。",
        ][:max_pages],
    )


def _blocked_extractor(pdf_path: Path, max_pages: int) -> PdfExtractionResult:
    assert pdf_path.exists()
    assert max_pages > 0
    return PdfExtractionResult(
        status="blocked",
        extractor="test",
        error="extractor unavailable",
    )
