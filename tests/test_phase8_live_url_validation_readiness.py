import json

from app.services.phase8_live_url_validation_readiness import (
    build_phase8_live_url_validation_readiness_report,
    export_phase8_live_url_validation_readiness_report,
)


def test_build_phase8_live_url_validation_readiness_report_defaults():
    report = build_phase8_live_url_validation_readiness_report()

    assert report.id == "phase8-live-url-validation-readiness-v1"
    assert report.status in {"ready", "review", "blocked"}
    assert report.live_validation_state in {
        "await_live_url_validation",
        "review",
        "ready_for_live_url_validation",
        "blocked",
    }
    assert report.decision in {
        "keep_runtime_defaults_until_live_url_validation",
        "confirm_live_url_validation_evidence",
        "resolve_live_url_validation_blockers",
    }
    assert report.summary["total_signals"] == 4


def test_export_phase8_live_url_validation_readiness_report(tmp_path):
    contract_path = (
        tmp_path
        / "docs/operations/live-url-validation/phase8-live-url-validation-execution-contract.md"
    )
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text("# contract\n", encoding="utf-8")

    phase6_path = (
        tmp_path
        / "docs/operations/deployed-field-validation/phase6-deployed-field-validation-readiness.json"
    )
    phase6_path.parent.mkdir(parents=True, exist_ok=True)
    phase6_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "field_validation_state": "ready_for_live_validation",
                "decision": "confirm_deployed_field_validation",
                "summary": {
                    "live_url_present": True,
                    "open_gate_ids": [],
                },
            }
        ),
        encoding="utf-8",
    )

    phase7_path = (
        tmp_path
        / "docs/operations/provider-release-readiness/phase7-provider-release-readiness.json"
    )
    phase7_path.parent.mkdir(parents=True, exist_ok=True)
    phase7_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "release_state": "ready_for_local_handoff",
                "decision": "keep_runtime_defaults",
                "summary": {
                    "ready_for_local_provider_handoff": True,
                    "ready_for_runtime_default_promotion": False,
                    "open_gate_ids": [],
                },
            }
        ),
        encoding="utf-8",
    )

    deployed_smoke_path = (
        tmp_path / "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
    )
    deployed_smoke_path.parent.mkdir(parents=True, exist_ok=True)
    deployed_smoke_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "base_url": "https://provider.example.com",
                "handoff": {"status": "ready"},
                "checks": [{"name": "health_readiness"}],
            }
        ),
        encoding="utf-8",
    )

    report = export_phase8_live_url_validation_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "ready"
    assert report.live_validation_state == "ready_for_live_url_validation"
    assert report.decision == "confirm_live_url_validation_evidence"
    assert payload["summary"]["live_url_present"] is True
    assert payload["summary"]["deployed_smoke_status"] == "ready"


def test_phase8_live_url_validation_readiness_marks_missing_deployed_smoke_review(
    tmp_path,
):
    contract_path = (
        tmp_path
        / "docs/operations/live-url-validation/phase8-live-url-validation-execution-contract.md"
    )
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text("# contract\n", encoding="utf-8")

    phase6_path = (
        tmp_path
        / "docs/operations/deployed-field-validation/phase6-deployed-field-validation-readiness.json"
    )
    phase6_path.parent.mkdir(parents=True, exist_ok=True)
    phase6_path.write_text(
        json.dumps({"status": "review", "summary": {"open_gate_ids": []}}),
        encoding="utf-8",
    )

    phase7_path = (
        tmp_path
        / "docs/operations/provider-release-readiness/phase7-provider-release-readiness.json"
    )
    phase7_path.parent.mkdir(parents=True, exist_ok=True)
    phase7_path.write_text(
        json.dumps({"status": "review", "summary": {"open_gate_ids": []}}),
        encoding="utf-8",
    )

    report = build_phase8_live_url_validation_readiness_report(base_dir=tmp_path)

    assert report.status == "review"
    assert report.live_validation_state == "await_live_url_validation"
    assert report.summary["deployed_smoke_present"] is False
    assert "deployed_provider_smoke" in report.summary["open_gate_ids"]
