import json

from app.services.local_rag_myprivateagent_call_loop_closure import (
    build_local_rag_myprivateagent_call_loop_closure,
    export_local_rag_myprivateagent_call_loop_closure,
)
from scripts import export_local_rag_myprivateagent_call_loop_closure as cli


def test_call_loop_closure_go(tmp_path):
    provider = _write_report(
        tmp_path / "provider.json",
        decision="go",
        reason_code="local_rag_business_corpus_usable",
        source_id="company_profile_2025_trial",
        summary={"live_http_required": True},
    )
    caller = _write_report(
        tmp_path / "caller.json",
        decision="go",
        reason_code="local_corpus_trial_accepted",
        source_id="company_profile_2025_trial",
    )

    report = export_local_rag_myprivateagent_call_loop_closure(
        provider_report_path=provider,
        myprivateagent_report_path=caller,
        output_dir=tmp_path / "closure",
    )

    assert report.decision == "go"
    assert report.reason_code == "local_rag_http_myprivateagent_call_loop_closed"
    assert report.summary["source_ids_match"] is True
    assert report.json_path.exists()
    assert report.markdown_path.exists()


def test_call_loop_closure_reviews_when_live_http_not_included(tmp_path):
    provider = _write_report(
        tmp_path / "provider.json",
        decision="go",
        reason_code="local_rag_business_corpus_usable",
        source_id="company_profile_2025_trial",
        summary={"live_http_required": False},
    )
    caller = _write_report(
        tmp_path / "caller.json",
        decision="go",
        reason_code="local_corpus_trial_accepted",
        source_id="company_profile_2025_trial",
    )

    report = build_local_rag_myprivateagent_call_loop_closure(
        provider_report_path=provider,
        myprivateagent_report_path=caller,
    )

    assert report.decision == "review"
    assert report.reason_code == "provider_live_http_not_included"


def test_call_loop_closure_blocks_missing_report(tmp_path):
    provider = _write_report(
        tmp_path / "provider.json",
        decision="go",
        reason_code="local_rag_business_corpus_usable",
        source_id="company_profile_2025_trial",
        summary={"live_http_required": True},
    )

    report = build_local_rag_myprivateagent_call_loop_closure(
        provider_report_path=provider,
        myprivateagent_report_path=tmp_path / "missing.json",
    )

    assert report.decision == "blocked"
    assert report.reason_code == "myprivateagent_caller_trial_report_missing"


def test_call_loop_closure_blocks_source_mismatch(tmp_path):
    provider = _write_report(
        tmp_path / "provider.json",
        decision="go",
        reason_code="local_rag_business_corpus_usable",
        source_id="company_profile_2025_trial",
        summary={"live_http_required": True},
    )
    caller = _write_report(
        tmp_path / "caller.json",
        decision="go",
        reason_code="local_corpus_trial_accepted",
        source_id="other_source",
    )

    report = build_local_rag_myprivateagent_call_loop_closure(
        provider_report_path=provider,
        myprivateagent_report_path=caller,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "source_id_mismatch"


def test_cli_exit_codes_follow_decision(monkeypatch, tmp_path):
    monkeypatch.setattr(
        cli,
        "export_local_rag_myprivateagent_call_loop_closure",
        lambda **kwargs: _fake_report("go", "ok", tmp_path),
    )
    assert cli.main([]) == 0

    monkeypatch.setattr(
        cli,
        "export_local_rag_myprivateagent_call_loop_closure",
        lambda **kwargs: _fake_report("review", "review", tmp_path),
    )
    assert cli.main([]) == 2

    monkeypatch.setattr(
        cli,
        "export_local_rag_myprivateagent_call_loop_closure",
        lambda **kwargs: _fake_report("blocked", "blocked", tmp_path),
    )
    assert cli.main([]) == 1


def _write_report(
    path,
    *,
    decision: str,
    reason_code: str,
    source_id: str,
    summary: dict | None = None,
):
    payload = {
        "decision": decision,
        "reason_code": reason_code,
        "source_id": source_id,
        "summary": summary or {},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


class _fake_report:
    def __init__(self, decision: str, reason_code: str, tmp_path):
        self.decision = decision
        self.reason_code = reason_code
        self.json_path = tmp_path / f"{decision}.json"
        self.markdown_path = tmp_path / f"{decision}.md"
