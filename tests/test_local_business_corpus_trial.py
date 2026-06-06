from app.services.local_business_corpus_trial import (
    LocalBusinessCorpusEvidence,
    export_local_business_corpus_trial_report,
    run_local_business_corpus_trial,
)


def test_local_business_corpus_trial_returns_go_and_writes_artifacts(tmp_path):
    markdown_path = tmp_path / "company.md"
    markdown_path.write_text(
        "# 公司简介\n\n公司主营业务包括交通工程咨询监理、试验检测和项目管理服务。\n\n"
        "公司拥有公路工程监理甲级和水运工程监理甲级资质。\n",
        encoding="utf-8",
    )

    report = export_local_business_corpus_trial_report(
        markdown_path=markdown_path,
        output_dir=tmp_path / "trial",
        source_id="company_profile_trial",
        title="公司简介 trial",
        query="公司主营业务是什么？",
    )

    assert report.decision == "go"
    assert report.reason_code == "local_business_corpus_usable"
    assert report.summary["chunk_count"] == 2
    assert report.summary["retrieved_evidence_count"] > 0
    assert report.overlay_path is not None
    assert report.chunks_path is not None
    assert report.json_path is not None
    assert report.report_markdown_path is not None
    overlay = report.overlay_path.read_text(encoding="utf-8")
    markdown = report.report_markdown_path.read_text(encoding="utf-8")
    assert '"formal_registration_status": "not_registered"' in overlay
    assert "- Decision: `go`" in markdown
    assert "default_source_catalog_status" in markdown


def test_local_business_corpus_trial_blocks_when_markdown_is_missing(tmp_path):
    report = run_local_business_corpus_trial(
        markdown_path=tmp_path / "missing.md",
        output_dir=tmp_path / "trial",
    )

    assert report.decision == "blocked"
    assert report.reason_code == "markdown_file_missing"
    assert report.overlay is None
    assert "check_markdown_path" in report.recommended_actions


def test_local_business_corpus_trial_blocks_when_markdown_is_empty(tmp_path):
    markdown_path = tmp_path / "empty.md"
    markdown_path.write_text("# Only heading\n\n- metadata only\n", encoding="utf-8")

    report = run_local_business_corpus_trial(
        markdown_path=markdown_path,
        output_dir=tmp_path / "trial",
    )

    assert report.decision == "blocked"
    assert report.reason_code == "markdown_content_empty"
    assert report.summary["trial_overlay_status"] == "not_written"


def test_local_business_corpus_trial_returns_review_for_weak_evidence(tmp_path):
    markdown_path = tmp_path / "company.md"
    markdown_path.write_text(
        "# 公司简介\n\n公司主营业务包括交通工程咨询监理和试验检测服务。\n",
        encoding="utf-8",
    )

    report = run_local_business_corpus_trial(
        markdown_path=markdown_path,
        output_dir=tmp_path / "trial",
        query="完全不存在的问题",
    )

    assert report.decision == "review"
    assert report.reason_code == "business_corpus_evidence_needs_review"
    assert report.evidence == []
    assert report.citations == []


def test_local_business_corpus_trial_blocks_invalid_answer_citations(
    monkeypatch,
    tmp_path,
):
    markdown_path = tmp_path / "company.md"
    markdown_path.write_text(
        "# 公司简介\n\n公司主营业务包括交通工程咨询监理和试验检测服务。\n",
        encoding="utf-8",
    )

    def invalid_answer(evidence: list[LocalBusinessCorpusEvidence]) -> tuple[str, list[str]]:
        return "bad answer", ["outside#citation"]

    monkeypatch.setattr(
        "app.services.local_business_corpus_trial._compose_trial_answer",
        invalid_answer,
    )

    report = run_local_business_corpus_trial(
        markdown_path=markdown_path,
        output_dir=tmp_path / "trial",
        query="公司主营业务是什么？",
    )

    assert report.decision == "blocked"
    assert report.reason_code == "trial_answer_citation_blocked"
    assert report.summary["invalid_citation_count"] == 1
