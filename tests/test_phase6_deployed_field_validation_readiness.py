import json

from app.services.phase6_deployed_field_validation_readiness import (
    build_phase6_deployed_field_validation_readiness_report,
    export_phase6_deployed_field_validation_readiness_report,
)


def test_build_phase6_deployed_field_validation_readiness_report_defaults():
    report = build_phase6_deployed_field_validation_readiness_report()

    assert report.id == "phase6-deployed-field-validation-readiness-v1"
    assert report.status in {"review", "blocked", "ready"}
    assert report.field_validation_state in {
        "await_live_url",
        "review",
        "ready_for_live_validation",
        "blocked",
    }
    assert report.decision in {
        "keep_local_review_until_deployed_smoke",
        "confirm_deployed_field_validation",
        "blocked",
    }
    assert report.summary["total_signals"] == 4


def test_export_phase6_deployed_field_validation_readiness_report(tmp_path):
    (tmp_path / "docs/operations/deployed-field-validation").mkdir(
        parents=True,
        exist_ok=True,
    )
    (
        tmp_path
        / "docs/operations/deployed-field-validation/phase6-deployed-field-validation-contract.md"
    ).write_text("# contract\n", encoding="utf-8")

    deployment_dir = tmp_path / "docs/operations/deployment-readiness"
    handoff_dir = tmp_path / "docs/integration/provider-handoff"
    smoke_dir = tmp_path / "docs/integration/deployed-provider-smoke"
    deployment_dir.mkdir(parents=True, exist_ok=True)
    handoff_dir.mkdir(parents=True, exist_ok=True)
    smoke_dir.mkdir(parents=True, exist_ok=True)

    deployment_dir.joinpath("deployment-readiness.json").write_text(
        json.dumps(
            {
                "status": "ready",
                "runtime_config": {"rag_retrieval_backend": "qdrant"},
            }
        ),
        encoding="utf-8",
    )
    handoff_dir.joinpath("provider-handoff-bundle.json").write_text(
        json.dumps(
            {
                "status": "ready",
                "evidence_artifacts": [{"id": "deployment_readiness"}],
            }
        ),
        encoding="utf-8",
    )
    smoke_dir.joinpath("deployed-provider-smoke.json").write_text(
        json.dumps(
            {
                "status": "ready",
                "base_url": "https://provider.example.com",
                "handoff": {"status": "ready"},
            }
        ),
        encoding="utf-8",
    )

    report = export_phase6_deployed_field_validation_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "ready"
    assert report.field_validation_state == "ready_for_live_validation"
    assert report.decision == "confirm_deployed_field_validation"
    assert payload["summary"]["live_url_present"] is True


def test_deployed_field_validation_readiness_marks_missing_smoke_as_review(tmp_path):
    (tmp_path / "docs/operations/deployed-field-validation").mkdir(
        parents=True,
        exist_ok=True,
    )
    (
        tmp_path
        / "docs/operations/deployed-field-validation/phase6-deployed-field-validation-contract.md"
    ).write_text("# contract\n", encoding="utf-8")

    (tmp_path / "docs/operations/deployment-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/integration/provider-handoff").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/operations/deployment-readiness/deployment-readiness.json").write_text(
        json.dumps({"status": "review", "runtime_config": {"rag_retrieval_backend": "fixture"}}),
        encoding="utf-8",
    )
    (tmp_path / "docs/integration/provider-handoff/provider-handoff-bundle.json").write_text(
        json.dumps({"status": "review", "evidence_artifacts": []}),
        encoding="utf-8",
    )

    report = build_phase6_deployed_field_validation_readiness_report(base_dir=tmp_path)

    assert report.status == "review"
    assert report.field_validation_state == "await_live_url"
    assert "deployed_provider_smoke" in report.summary["open_gate_ids"]
