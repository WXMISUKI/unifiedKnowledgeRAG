from pathlib import Path
from types import SimpleNamespace

from app.services.local_document_source_onboarding import (
    export_local_document_source_onboarding_report,
    run_local_document_source_onboarding,
)


def test_onboarding_go_writes_summary(tmp_path):
    markdown_path = tmp_path / "company.md"
    markdown_path.write_text("公司主营业务包括交通工程咨询监理和试验检测服务。", encoding="utf-8")

    report = export_local_document_source_onboarding_report(
        markdown_path=markdown_path,
        source_id="company_profile_trial",
        title="公司简介 trial",
        query="公司主营业务是什么？",
        output_dir=tmp_path / "onboarding",
        business_trial_exporter=_trial_exporter("go"),
        handoff_exporter=_handoff_exporter("ready_for_caller_review"),
        registration_exporter=_registration_exporter("registered"),
        acceptance_exporter=_acceptance_exporter("go"),
    )

    assert report.decision == "go"
    assert report.reason_code == "local_document_source_onboarded"
    assert [step.id for step in report.steps] == [
        "business_corpus_trial",
        "caller_handoff",
        "approved_source_registration",
        "acceptance_smoke",
    ]
    assert report.summary["source_binding_status"] == "not_created"
    assert report.json_path.exists()
    assert report.markdown_path_out.exists()
    assert "- Decision: `go`" in report.markdown_path_out.read_text(encoding="utf-8")


def test_onboarding_blocks_when_markdown_trial_blocks(tmp_path):
    report = run_local_document_source_onboarding(
        markdown_path=tmp_path / "missing.md",
        output_dir=tmp_path / "onboarding",
        business_trial_exporter=_trial_exporter("blocked", reason_code="markdown_file_missing"),
        handoff_exporter=_should_not_run,
        registration_exporter=_should_not_run,
        acceptance_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "business_corpus_trial_blocked"
    assert [step.id for step in report.steps] == ["business_corpus_trial"]
    assert report.steps[0].reason_code == "markdown_file_missing"


def test_onboarding_reviews_when_markdown_trial_reviews(tmp_path):
    report = run_local_document_source_onboarding(
        markdown_path=tmp_path / "company.md",
        output_dir=tmp_path / "onboarding",
        business_trial_exporter=_trial_exporter("review", reason_code="business_corpus_evidence_needs_review"),
        handoff_exporter=_should_not_run,
        registration_exporter=_should_not_run,
        acceptance_exporter=_should_not_run,
    )

    assert report.decision == "review"
    assert report.reason_code == "business_corpus_trial_review"
    assert report.steps[0].status == "review"


def test_onboarding_blocks_when_registration_blocks(tmp_path):
    report = run_local_document_source_onboarding(
        markdown_path=tmp_path / "company.md",
        output_dir=tmp_path / "onboarding",
        business_trial_exporter=_trial_exporter("go"),
        handoff_exporter=_handoff_exporter("ready_for_caller_review"),
        registration_exporter=_registration_exporter("blocked", reason_code="handoff_markdown_missing"),
        acceptance_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "approved_source_registration_blocked"
    assert [step.id for step in report.steps] == [
        "business_corpus_trial",
        "caller_handoff",
        "approved_source_registration",
    ]
    assert report.steps[-1].reason_code == "handoff_markdown_missing"


def test_onboarding_reviews_when_acceptance_reviews(tmp_path):
    report = run_local_document_source_onboarding(
        markdown_path=tmp_path / "company.md",
        output_dir=tmp_path / "onboarding",
        business_trial_exporter=_trial_exporter("go"),
        handoff_exporter=_handoff_exporter("ready_for_caller_review"),
        registration_exporter=_registration_exporter("registered"),
        acceptance_exporter=_acceptance_exporter("review", reason_code="acceptance_needs_review"),
    )

    assert report.decision == "review"
    assert report.reason_code == "acceptance_smoke_review"
    assert report.steps[-1].id == "acceptance_smoke"
    assert report.steps[-1].status == "review"


def _trial_exporter(decision, *, reason_code=None):
    def exporter(*, output_dir, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "local-business-corpus-trial.json"
        markdown_path = output_dir / "local-business-corpus-trial.md"
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# trial\n", encoding="utf-8")
        return SimpleNamespace(
            decision=decision,
            reason_code=reason_code or f"trial_{decision}",
            json_path=json_path,
            report_markdown_path=markdown_path,
            overlay_path=output_dir / "overlay.json" if decision == "go" else None,
            chunks_path=output_dir / "chunks.json" if decision == "go" else None,
            summary={"decision": decision},
        )

    return exporter


def _handoff_exporter(status, *, reason_code=None):
    def exporter(*, output_dir, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "local-corpus-caller-handoff.json"
        markdown_path = output_dir / "local-corpus-caller-handoff.md"
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# handoff\n", encoding="utf-8")
        return SimpleNamespace(
            status=status,
            reason_code=reason_code or f"handoff_{status}",
            json_path=json_path,
            markdown_path=markdown_path,
            summary={"status": status},
        )

    return exporter


def _registration_exporter(status, *, reason_code=None):
    def exporter(*, output_dir, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "approved-local-source-registration.json"
        markdown_path = output_dir / "approved-local-source-registration.md"
        materialized = output_dir / "company_profile_trial.md" if status == "registered" else None
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# registration\n", encoding="utf-8")
        return SimpleNamespace(
            status=status,
            reason_code=reason_code or f"registration_{status}",
            json_path=json_path,
            markdown_path=markdown_path,
            materialized_source_path=materialized,
            summary={"status": status},
        )

    return exporter


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
