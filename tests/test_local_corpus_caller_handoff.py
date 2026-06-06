import json

from app.services.local_corpus_caller_handoff import (
    build_local_corpus_caller_handoff,
    export_local_corpus_caller_handoff,
)


def test_local_corpus_caller_handoff_ready_for_go_trial(tmp_path):
    trial_report = tmp_path / "trial.json"
    _write_trial_report(trial_report, decision="go")

    handoff = export_local_corpus_caller_handoff(
        trial_report_path=trial_report,
        output_dir=tmp_path / "handoff",
    )

    assert handoff.status == "ready_for_caller_review"
    assert handoff.reason_code == "trial_go_ready_for_caller_review"
    assert handoff.source_id == "company_profile_2025_trial"
    assert handoff.registration_status == "not_registered"
    assert handoff.caller_next_action == "review_trial_artifacts_before_formal_binding"
    assert handoff.artifacts["markdown"] == "docs/local-run/company.md"
    assert handoff.json_path is not None
    assert handoff.markdown_path is not None
    payload = json.loads(handoff.json_path.read_text(encoding="utf-8"))
    markdown = handoff.markdown_path.read_text(encoding="utf-8")
    assert payload["status"] == "ready_for_caller_review"
    assert "does_not_modify_default_source_catalog" in payload["non_goals"]
    assert "- Status: `ready_for_caller_review`" in markdown


def test_local_corpus_caller_handoff_preserves_review_trial(tmp_path):
    trial_report = tmp_path / "trial.json"
    _write_trial_report(trial_report, decision="review")

    handoff = build_local_corpus_caller_handoff(trial_report_path=trial_report)

    assert handoff.status == "review"
    assert handoff.reason_code == "trial_needs_review_before_caller_handoff"
    assert handoff.caller_next_action == (
        "review_trial_query_markdown_and_evidence_before_integration"
    )


def test_local_corpus_caller_handoff_preserves_blocked_trial(tmp_path):
    trial_report = tmp_path / "trial.json"
    _write_trial_report(trial_report, decision="blocked")

    handoff = build_local_corpus_caller_handoff(trial_report_path=trial_report)

    assert handoff.status == "blocked"
    assert handoff.reason_code == "trial_blocked_before_caller_handoff"
    assert handoff.caller_next_action == "fix_blocked_trial_before_caller_review"


def test_local_corpus_caller_handoff_blocks_when_report_missing(tmp_path):
    handoff = build_local_corpus_caller_handoff(
        trial_report_path=tmp_path / "missing.json",
    )

    assert handoff.status == "blocked"
    assert handoff.reason_code == "trial_report_missing"
    assert handoff.caller_next_action == "export_local_business_corpus_trial_first"


def test_local_corpus_caller_handoff_blocks_when_artifact_pointers_missing(tmp_path):
    trial_report = tmp_path / "trial.json"
    _write_trial_report(trial_report, decision="go", overlay_path=None)

    handoff = build_local_corpus_caller_handoff(trial_report_path=trial_report)

    assert handoff.status == "blocked"
    assert handoff.reason_code == "trial_artifact_pointers_missing"
    assert handoff.summary["missing_artifact_fields"] == ["overlay_path"]
    assert handoff.caller_next_action == (
        "rerun_local_business_corpus_trial_before_caller_review"
    )


def _write_trial_report(
    path,
    *,
    decision: str,
    overlay_path: str | None = "docs/local-run/source.json",
) -> None:
    payload = {
        "decision": decision,
        "source_id": "company_profile_2025_trial",
        "title": "公司简介 2025 trial",
        "query": "公司主营业务是什么？",
        "markdown_path": "docs/local-run/company.md",
        "overlay_path": overlay_path,
        "chunks_path": "docs/local-run/chunks.json",
        "summary": {
            "formal_registration_status": "not_registered",
            "retrieved_evidence_count": 3,
            "answer_citation_count": 3,
            "invalid_citation_count": 0,
            "default_source_catalog_status": "unchanged",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
