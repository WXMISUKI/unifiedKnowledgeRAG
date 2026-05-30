import json
from dataclasses import dataclass
from pathlib import Path

from app.services.provider_handoff_refresh import (
    HandoffRefreshStepSpec,
    refresh_provider_handoff_evidence,
    render_provider_handoff_refresh_markdown,
)


@dataclass(frozen=True)
class FakeRefreshReport:
    status: str
    json_path: Path
    markdown_path: Path


def test_handoff_refresh_reports_ready_when_all_steps_ready(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[
            _step(tmp_path, "integration", "ready"),
            _step(tmp_path, "smoke", "ready"),
        ],
    )

    assert report.status == "ready"
    assert [step["status"] for step in report.steps] == ["ready", "ready"]
    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")
    assert payload["id"] == "provider-handoff-refresh-v1"
    assert "# Provider Handoff Evidence Refresh" in markdown


def test_handoff_refresh_preserves_review_state(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[
            _step(tmp_path, "integration", "ready"),
            _step(tmp_path, "deployment", "review"),
            _step(tmp_path, "handoff", "ready"),
        ],
    )

    assert report.status == "review"
    assert [step["status"] for step in report.steps] == [
        "ready",
        "review",
        "ready",
    ]
    assert any("human review" in note for note in report.operation_notes)


def test_handoff_refresh_blocks_and_skips_after_failure(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[
            _step(tmp_path, "integration", "ready"),
            _failing_step("smoke"),
            _step(tmp_path, "deployment", "ready"),
        ],
    )

    assert report.status == "blocked"
    assert [step["status"] for step in report.steps] == [
        "ready",
        "blocked",
        "skipped",
    ]
    assert report.steps[1]["recommended_action"] == "resolve_step_failure"
    assert report.steps[2]["recommended_action"] == "not_run_due_to_previous_failure"


def test_handoff_refresh_blocks_on_blocked_step_status(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[
            _step(tmp_path, "integration", "blocked"),
            _step(tmp_path, "smoke", "ready"),
        ],
    )

    assert report.status == "blocked"
    assert [step["status"] for step in report.steps] == ["blocked", "skipped"]
    assert "Refresh stopped" in "\n".join(report.operation_notes)


def test_handoff_refresh_markdown_lists_outputs(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[_step(tmp_path, "integration", "ready")],
    )

    markdown = render_provider_handoff_refresh_markdown(report)

    assert "| Step | Category | Status | Output Paths | Recommended Action | Summary |" in markdown
    assert "integration.json" in markdown
    assert "integration.md" in markdown


def _step(tmp_path: Path, step_id: str, status: str) -> HandoffRefreshStepSpec:
    def exporter(output_dir: Path) -> FakeRefreshReport:
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / f"{step_id}.json"
        markdown_path = output_dir / f"{step_id}.md"
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# report\n", encoding="utf-8")
        return FakeRefreshReport(
            status=status,
            json_path=json_path,
            markdown_path=markdown_path,
        )

    return HandoffRefreshStepSpec(
        id=step_id,
        category="test",
        output_dir=tmp_path / step_id,
        exporter=exporter,
        status_reader=lambda report: report.status,
    )


def _failing_step(step_id: str) -> HandoffRefreshStepSpec:
    def exporter(output_dir: Path) -> FakeRefreshReport:
        raise RuntimeError("boom")

    return HandoffRefreshStepSpec(
        id=step_id,
        category="test",
        output_dir=Path(step_id),
        exporter=exporter,
        status_reader=lambda report: report.status,
    )
