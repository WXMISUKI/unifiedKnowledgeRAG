import json

from app.services.phase11_source_binding_preview_smoke import (
    build_phase11_source_binding_preview_smoke_report,
)


def test_phase11_source_binding_preview_smoke_ready(tmp_path):
    _write_source_binding(tmp_path, status="ready", bindable=2, total=2)
    _write_phase10_readiness(tmp_path, owner="caller")

    report = build_phase11_source_binding_preview_smoke_report(base_dir=tmp_path)

    assert report.status == "ready"


def test_phase11_source_binding_preview_smoke_blocks_on_owner(tmp_path):
    _write_source_binding(tmp_path, status="ready", bindable=2, total=2)
    _write_phase10_readiness(tmp_path, owner="provider")

    report = build_phase11_source_binding_preview_smoke_report(base_dir=tmp_path)

    assert report.status == "blocked"


def _write_source_binding(base_dir, *, status: str, bindable: int, total: int) -> None:
    path = base_dir / "docs/integration/source-bindings/provider-source-bindings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "bindable_source_count": bindable,
                "total_source_count": total,
            }
        ),
        encoding="utf-8",
    )


def _write_phase10_readiness(base_dir, *, owner: str) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"summary": {"source_binding_policy_owner": owner}}),
        encoding="utf-8",
    )
