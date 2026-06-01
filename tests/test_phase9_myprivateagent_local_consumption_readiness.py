import json

from app.services.phase9_myprivateagent_local_consumption_readiness import (
    build_phase9_myprivateagent_local_consumption_readiness_report,
    export_phase9_myprivateagent_local_consumption_readiness_report,
)


def test_build_phase9_local_consumption_readiness_defaults():
    report = build_phase9_myprivateagent_local_consumption_readiness_report()

    assert report.id == "phase9-myprivateagent-local-consumption-readiness-v1"
    assert report.status in {"ready", "review", "blocked"}
    assert report.local_consumption_state in {
        "ready_for_local_consumption",
        "review",
        "blocked",
    }
    assert report.summary["total_signals"] == 8


def test_export_phase9_local_consumption_readiness_report(tmp_path):
    _write_contract(tmp_path)
    _write_phase7(tmp_path, status="ready")
    _write_phase8(tmp_path, status="ready")
    _write_integration_probe(tmp_path, bindable=True, compatible=True)
    _write_deployed_smoke(tmp_path, status="ready")
    _write_source_bindings(tmp_path, status="ready")
    _write_phase4_pack(tmp_path, status="ready")
    _write_phase4_smoke(tmp_path, status="ready")

    report = export_phase9_myprivateagent_local_consumption_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "ready"
    assert report.local_consumption_state == "ready_for_local_consumption"
    assert payload["summary"]["local_handoff_ready"] is True
    assert payload["summary"]["runtime_promotion_ready"] is False


def test_phase9_local_consumption_readiness_blocks_without_probe(tmp_path):
    _write_contract(tmp_path)
    _write_phase7(tmp_path, status="review")
    _write_phase8(tmp_path, status="review")

    report = build_phase9_myprivateagent_local_consumption_readiness_report(
        base_dir=tmp_path
    )

    assert report.status == "blocked"
    assert "provider_integration_probe" in report.summary["open_gate_ids"]


def _write_contract(base_dir) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumption/"
        / "phase9-myprivateagent-local-consumption-contract.md"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# contract\n", encoding="utf-8")


def _write_phase7(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/operations/provider-release-readiness/"
        / "phase7-provider-release-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "release_state": "ready_for_local_handoff",
                "summary": {
                    "ready_for_local_provider_handoff": status == "ready",
                    "ready_for_runtime_default_promotion": False,
                },
            }
        ),
        encoding="utf-8",
    )


def _write_phase8(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/operations/live-url-validation/"
        / "phase8-live-url-validation-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "live_validation_state": "review",
                "summary": {
                    "deployed_smoke_status": "review",
                    "live_url_present": True,
                },
            }
        ),
        encoding="utf-8",
    )


def _write_integration_probe(base_dir, *, bindable: bool, compatible: bool) -> None:
    path = base_dir / "docs/integration/provider-binding/provider-integration-probe.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    planes = ["MyPrivateAgent"] if compatible else ["OtherControlPlane"]
    path.write_text(
        json.dumps(
            {
                "bindable": bindable,
                "checks": [
                    {
                        "name": "manifest_identity",
                        "details": {"compatible_control_planes": planes},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def _write_deployed_smoke(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "base_url": "http://127.0.0.1:8020",
                "handoff": {"status": "review"},
                "operation_notes": [
                    "No provider API credentials were supplied; this is only expected for local or intentionally open deployments."
                ],
            }
        ),
        encoding="utf-8",
    )


def _write_source_bindings(base_dir, *, status: str) -> None:
    path = base_dir / "docs/integration/source-bindings/provider-source-bindings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "bindable_source_count": 2,
                "total_source_count": 2,
            }
        ),
        encoding="utf-8",
    )


def _write_phase4_pack(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/benchmark/chinese-seed/evidence-pack-readiness/"
        / "phase4-evidence-pack-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"status": status, "decision": "keep_caller_ownership"}),
        encoding="utf-8",
    )


def _write_phase4_smoke(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/smoke/evidence-pack-consumption/"
        / "phase4-caller-consumption-smoke.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"status": status, "summary": {"passed": 3, "total": 3}}),
        encoding="utf-8",
    )
