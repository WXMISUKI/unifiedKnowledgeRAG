import json

from app.services.phase11_local_provider_integration_profile import (
    build_phase11_local_provider_integration_profile_report,
    export_phase11_local_provider_integration_profile_report,
)


def test_build_phase11_profile_blocks_without_inputs(tmp_path):
    report = build_phase11_local_provider_integration_profile_report(base_dir=tmp_path)

    assert report.status == "blocked"
    assert report.summary["total_signals"] == 4


def test_export_phase11_profile_ready(tmp_path):
    _write_phase10_readiness(tmp_path, status="ready")
    _write_phase10_probe(tmp_path, status="ready")
    _write_integration_probe(tmp_path, bindable=True)
    _write_handoff(tmp_path, status="ready")

    report = export_phase11_local_provider_integration_profile_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "ready"
    assert payload["summary"]["runtime_promotion_status"] == "keep_runtime_defaults"


def _write_phase10_readiness(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "local_consumer_state": "ready_for_local_consumer_probe_review",
                "summary": {
                    "local_provider_url": "http://127.0.0.1:8020",
                    "api_key_mode": "not_configured_local_dev",
                    "runtime_promotion_status": "keep_runtime_defaults",
                    "source_binding_policy_owner": "caller",
                },
            }
        ),
        encoding="utf-8",
    )


def _write_phase10_probe(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/smoke/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-probe.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "summary": {"passed_checks": 7, "total_checks": 7},
            }
        ),
        encoding="utf-8",
    )


def _write_integration_probe(base_dir, *, bindable: bool) -> None:
    path = base_dir / "docs/integration/provider-binding/provider-integration-probe.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"bindable": bindable}), encoding="utf-8")


def _write_handoff(base_dir, *, status: str) -> None:
    path = base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": status}), encoding="utf-8")
