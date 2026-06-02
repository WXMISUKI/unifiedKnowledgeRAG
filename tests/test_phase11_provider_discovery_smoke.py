import json

from app.services.phase11_provider_discovery_smoke import (
    build_phase11_provider_discovery_smoke_report,
    export_phase11_provider_discovery_smoke_report,
)


def test_phase11_discovery_smoke_ready(tmp_path):
    _write_profile(tmp_path)
    _write_probe(tmp_path)
    _write_contract_smoke(tmp_path, passed=True)
    _write_handoff(tmp_path, include_phase11=True)

    report = build_phase11_provider_discovery_smoke_report(base_dir=tmp_path)

    assert report.status == "ready"
    assert report.summary["passed_checks"] == 4


def test_phase11_discovery_smoke_blocks_missing_handoff_row(tmp_path):
    _write_profile(tmp_path)
    _write_probe(tmp_path)
    _write_contract_smoke(tmp_path, passed=True)
    _write_handoff(tmp_path, include_phase11=False)

    report = build_phase11_provider_discovery_smoke_report(base_dir=tmp_path)

    assert report.status == "blocked"


def test_export_phase11_discovery_smoke(tmp_path):
    _write_profile(tmp_path)
    _write_probe(tmp_path)
    _write_contract_smoke(tmp_path, passed=True)
    _write_handoff(tmp_path, include_phase11=True)
    report = export_phase11_provider_discovery_smoke_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    assert payload["status"] == "ready"


def _write_profile(base_dir) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-provider-integration/"
        / "phase11-local-provider-integration-profile.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")


def _write_probe(base_dir) -> None:
    path = base_dir / "docs/integration/provider-binding/provider-integration-probe.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"bindable": True}), encoding="utf-8")


def _write_contract_smoke(base_dir, *, passed: bool) -> None:
    path = base_dir / "docs/smoke/provider-contract/provider-contract-smoke.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"passed": passed}), encoding="utf-8")


def _write_handoff(base_dir, *, include_phase11: bool) -> None:
    path = base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    artifacts = [{"id": "phase11_local_provider_integration_profile"}] if include_phase11 else []
    path.write_text(json.dumps({"evidence_artifacts": artifacts}), encoding="utf-8")
