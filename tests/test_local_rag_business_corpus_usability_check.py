from pathlib import Path
from types import SimpleNamespace

from app.services.local_rag_business_corpus_usability_check import (
    export_local_rag_business_corpus_usability_check,
    run_local_rag_business_corpus_usability_check,
)
from scripts import export_local_rag_business_corpus_usability_check as cli


def test_usability_check_go_for_default_local_corpus(tmp_path):
    report = export_local_rag_business_corpus_usability_check(
        output_dir=tmp_path / "usability",
    )

    assert report.decision == "go"
    assert report.reason_code == "local_rag_business_corpus_usable"
    assert report.summary["required_check_count"] == 2
    assert report.summary["skipped_check_count"] == 1
    assert report.checks[-1].decision == "skipped"
    assert report.json_path.exists()
    assert report.markdown_path.exists()


def test_usability_check_reviews_when_required_check_reviews(tmp_path):
    report = run_local_rag_business_corpus_usability_check(
        output_dir=tmp_path / "usability",
        local_trial_runner=_runner("go", "local_ok"),
        acceptance_runner=_runner("review", "acceptance_needs_review"),
    )

    assert report.decision == "review"
    assert report.reason_code == "approved_local_corpus_acceptance_acceptance_needs_review"
    assert report.summary["review_check_count"] == 1


def test_usability_check_blocks_when_required_check_blocks(tmp_path):
    report = run_local_rag_business_corpus_usability_check(
        output_dir=tmp_path / "usability",
        local_trial_runner=_runner("blocked", "markdown_file_missing"),
        acceptance_runner=_runner("go", "acceptance_ok"),
    )

    assert report.decision == "blocked"
    assert report.reason_code == "local_business_corpus_trial_markdown_file_missing"
    assert report.summary["blocked_check_count"] == 1


def test_usability_check_includes_live_http_only_when_requested(tmp_path):
    calls = []

    def live_runner(**kwargs):
        calls.append(kwargs)
        return _report("blocked", "local_provider_unreachable")

    local_only = run_local_rag_business_corpus_usability_check(
        output_dir=tmp_path / "local-only",
        local_trial_runner=_runner("go", "local_ok"),
        acceptance_runner=_runner("go", "acceptance_ok"),
        live_http_runner=live_runner,
    )
    live = run_local_rag_business_corpus_usability_check(
        output_dir=tmp_path / "live",
        include_live_http=True,
        local_trial_runner=_runner("go", "local_ok"),
        acceptance_runner=_runner("go", "acceptance_ok"),
        live_http_runner=live_runner,
    )

    assert calls
    assert local_only.decision == "go"
    assert local_only.checks[-1].reason_code == "live_http_not_requested"
    assert live.decision == "blocked"
    assert live.reason_code == "approved_local_corpus_live_http_local_provider_unreachable"


def test_cli_exit_codes_follow_decision(monkeypatch, tmp_path):
    monkeypatch.setattr(
        cli,
        "export_local_rag_business_corpus_usability_check",
        lambda **kwargs: _report("go", "ok", json_path=tmp_path / "go.json", markdown_path=tmp_path / "go.md"),
    )
    assert cli.main([]) == 0

    monkeypatch.setattr(
        cli,
        "export_local_rag_business_corpus_usability_check",
        lambda **kwargs: _report("review", "needs_review", json_path=tmp_path / "review.json", markdown_path=tmp_path / "review.md"),
    )
    assert cli.main([]) == 2

    monkeypatch.setattr(
        cli,
        "export_local_rag_business_corpus_usability_check",
        lambda **kwargs: _report("blocked", "blocked", json_path=tmp_path / "blocked.json", markdown_path=tmp_path / "blocked.md"),
    )
    assert cli.main([]) == 1


def _runner(decision: str, reason_code: str):
    def run(**kwargs):
        return _report(decision, reason_code)

    return run


def _report(
    decision: str,
    reason_code: str,
    *,
    json_path: Path | None = None,
    markdown_path: Path | None = None,
):
    return SimpleNamespace(
        decision=decision,
        reason_code=reason_code,
        summary={"decision": decision},
        json_path=json_path,
        markdown_path=markdown_path,
    )
