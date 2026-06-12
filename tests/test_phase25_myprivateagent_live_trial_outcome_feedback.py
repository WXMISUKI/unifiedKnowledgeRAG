import json

from app.services.phase25_myprivateagent_live_trial_outcome_feedback import (
    build_phase25_live_trial_outcome_feedback_report,
    export_phase25_live_trial_outcome_feedback_report,
)


def test_phase25_feedback_ready_when_live_trial_goes(tmp_path):
    outcome_path = tmp_path / "outcome.json"
    _write_json(outcome_path, _trial_outcome(live_status="go", retrieve_status="ready"))

    report = build_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=outcome_path
    )

    assert report.status == "ready"
    assert report.provider_action == "no_provider_action_required"
    assert report.reason_code == "caller_live_trial_passed"
    assert report.trial_outcome_evidence.document_count == 2
    assert report.trial_outcome_evidence.allowed_citation_count == 2


def test_phase25_feedback_reads_nested_provider_feedback_input(tmp_path):
    outcome_path = tmp_path / "myprivateagent-trial-outcome.json"
    _write_json(
        outcome_path,
        {
            "id": "unified-knowledge-provider-repo-side-trial-v1",
            "status": "trial_passed",
            "provider_feedback_input": _trial_outcome(
                live_status="go",
                retrieve_status="ready",
            ),
        },
    )

    report = build_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=outcome_path
    )

    assert report.status == "ready"
    assert report.provider_action == "no_provider_action_required"
    assert report.reason_code == "caller_live_trial_passed"
    assert report.trial_outcome_evidence.live_trial_status == "go"
    assert report.trial_outcome_evidence.allowed_citation_count == 2


def test_phase25_feedback_review_when_evidence_is_insufficient(tmp_path):
    outcome_path = tmp_path / "outcome.json"
    _write_json(
        outcome_path,
        _trial_outcome(
            live_status="review",
            retrieve_status="ready",
            evidence_pack_status="insufficient_evidence",
            document_count=0,
            allowed_citations=[],
        ),
    )

    report = build_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=outcome_path
    )

    assert report.status == "review"
    assert report.provider_action == "provider_review_required"
    assert report.reason_code == "caller_live_trial_needs_review"


def test_phase25_feedback_blocks_provider_retrieve_failure(tmp_path):
    outcome_path = tmp_path / "outcome.json"
    _write_json(
        outcome_path,
        _trial_outcome(
            live_status="blocked",
            retrieve_status="blocked",
            retrieve_reason="RAG_DOWN",
            blockers=["provider_http_error"],
        ),
    )

    report = build_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=outcome_path
    )

    assert report.status == "blocked"
    assert report.provider_action == "provider_blocked"
    assert report.reason_code == "provider_retrieve_failed"
    assert "provider_http_error" in report.trial_outcome_evidence.blockers


def test_phase25_feedback_blocks_invalid_input(tmp_path):
    outcome_path = tmp_path / "missing.json"

    report = build_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=outcome_path
    )

    assert report.status == "blocked"
    assert report.provider_action == "provider_blocked"
    assert report.reason_code == "invalid_trial_outcome_input"
    assert report.trial_outcome_evidence.input_status == "missing"
    assert "trial_outcome_file_missing" in report.trial_outcome_evidence.blockers


def test_phase25_feedback_reviews_incomplete_input_when_critical_fields_missing(tmp_path):
    outcome_path = tmp_path / "outcome.json"
    payload = _trial_outcome(live_status="go", retrieve_status="ready")
    payload.pop("live_trial_status")
    payload["provider_retrieve"].pop("status")
    _write_json(outcome_path, payload)

    report = build_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=outcome_path
    )

    assert report.status == "review"
    assert report.provider_action == "provider_review_required"
    assert report.reason_code == "incomplete_trial_outcome_input"
    assert "live_trial_status" in report.trial_outcome_evidence.missing_critical_fields
    assert (
        "provider_retrieve.status"
        in report.trial_outcome_evidence.missing_critical_fields
    )


def test_phase25_feedback_exports_json_and_markdown(tmp_path):
    outcome_path = tmp_path / "outcome.json"
    _write_json(outcome_path, _trial_outcome(live_status="go", retrieve_status="ready"))

    report = export_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=outcome_path,
        output_dir=tmp_path / "out",
    )

    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["status"] == "ready"
    assert payload["provider_action"] == "no_provider_action_required"
    assert "# Phase 25 MyPrivateAgent Live Trial Outcome Feedback" in markdown
    assert "`provider_retrieve_status`" in markdown
    assert "`missing_critical_fields`" in markdown


def _trial_outcome(
    *,
    live_status,
    retrieve_status,
    retrieve_reason="provider_retrieve_ready",
    evidence_pack_status="answerable",
    document_count=2,
    allowed_citations=None,
    blockers=None,
):
    allowed_citations = (
        ["refund_policy_2026#section-3", "refund_policy_2026#section-5"]
        if allowed_citations is None
        else allowed_citations
    )
    blockers = [] if blockers is None else blockers
    return {
        "live_trial_status": live_status,
        "reason_code": "live_grounded_answer_trial_ready",
        "provider_base_url": "http://127.0.0.1:8020",
        "agent_id": "ecommerce_support",
        "domain": "refund.policy",
        "query": "退款政策是什么？",
        "provider_retrieve": {
            "status": retrieve_status,
            "reason_code": retrieve_reason,
            "document_count": document_count,
            "evidence_pack_status": evidence_pack_status,
            "citation_policy": "use_only_returned_citations",
            "allowed_citations": allowed_citations,
            "blockers": blockers,
            "warnings": [],
            "evidence_pack": {
                "status": evidence_pack_status,
                "allowed_citations": allowed_citations,
            },
        },
        "blockers": [],
        "warnings": [],
    }


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
