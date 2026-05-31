import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE4_EVIDENCE_PACK_READINESS_ID = "phase4-evidence-pack-readiness-v1"
PHASE4_EVIDENCE_PACK_CONTRACT_PATH = Path(
    "docs/benchmark/chinese-seed/evidence-pack-consumption-contract/"
    "phase4-evidence-pack-consumption-contract.md"
)
PHASE4_PROVIDER_CONTRACT_SMOKE_JSON = Path(
    "docs/smoke/provider-contract/provider-contract-smoke.json"
)
PHASE4_PROVIDER_CONTRACT_SMOKE_MARKDOWN = Path(
    "docs/smoke/provider-contract/provider-contract-smoke.md"
)
PHASE4_EVIDENCE_PACK_READINESS_JSON = "phase4-evidence-pack-readiness.json"
PHASE4_EVIDENCE_PACK_READINESS_MARKDOWN = "phase4-evidence-pack-readiness.md"
PHASE4_SUPPORTING_TEST_PATHS = [
    Path("tests/test_evidence_pack.py"),
    Path("tests/test_provider_contract.py"),
    Path("tests/test_provider_contract_smoke.py"),
]


@dataclass(frozen=True)
class Phase4EvidencePackReadinessArtifact:
    id: str
    category: str
    path: str
    status: str
    summary: str
    present: bool
    required: bool
    recommended_action: str


@dataclass(frozen=True)
class Phase4EvidencePackReadinessReport:
    id: str
    generated_at: str
    status: str
    decision: str
    contract_path: str
    smoke_report_path: str
    summary: dict[str, int | bool]
    supporting_evidence: list[Phase4EvidencePackReadinessArtifact]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase4_evidence_pack_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase4EvidencePackReadinessReport:
    supporting_evidence = [
        _build_contract_doc_artifact(base_dir),
        _build_smoke_artifact(base_dir),
        *[
            _build_supporting_test_artifact(base_dir, path)
            for path in PHASE4_SUPPORTING_TEST_PATHS
        ],
    ]
    summary = _readiness_summary(supporting_evidence)
    return Phase4EvidencePackReadinessReport(
        id=PHASE4_EVIDENCE_PACK_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(supporting_evidence),
        decision="keep_caller_ownership",
        contract_path=str(PHASE4_EVIDENCE_PACK_CONTRACT_PATH),
        smoke_report_path=str(PHASE4_PROVIDER_CONTRACT_SMOKE_JSON),
        summary=summary,
        supporting_evidence=supporting_evidence,
        notes=[
            "This report is local, read-only evidence for Phase 4 caller-consumption review.",
            "It complements the evidence pack consumption contract and provider contract smoke report.",
            "It does not change runtime defaults, caller ownership, or provider HTTP contracts.",
        ],
    )


def phase4_evidence_pack_readiness_report_to_dict(
    report: Phase4EvidencePackReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase4_evidence_pack_readiness_markdown(
    report: Phase4EvidencePackReadinessReport,
) -> str:
    status = "passed" if report.status == "ready" else report.status
    lines = [
        "# Phase 4 Evidence Pack Readiness Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Contract Doc: `{report.contract_path}`",
        f"- Smoke Report: `{report.smoke_report_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Artifacts | `{report.summary['total_artifacts']}` |",
        f"| Ready Artifacts | `{report.summary['ready_artifacts']}` |",
        f"| Review Artifacts | `{report.summary['review_artifacts']}` |",
        f"| Blocked Artifacts | `{report.summary['blocked_artifacts']}` |",
        f"| Required Artifacts | `{report.summary['required_artifacts']}` |",
        f"| Required Ready Artifacts | `{report.summary['required_ready_artifacts']}` |",
        f"| Smoke Passed | `{report.summary['smoke_passed']}` |",
        f"| Evidence Pack Checks Passed | `{report.summary['evidence_pack_checks_passed']}` |",
        "",
        "## Supporting Evidence",
        "",
        "| Evidence | Category | Status | Summary |",
        "|---|---|---|---|",
    ]
    for item in report.supporting_evidence:
        lines.append(
            f"| `{item.id}` | `{item.category}` | `{item.status}` | {item.summary} |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase4_evidence_pack_readiness_report(
    output_dir: Path = Path("docs/benchmark/chinese-seed/evidence-pack-readiness"),
    *,
    base_dir: Path = Path("."),
) -> Phase4EvidencePackReadinessReport:
    report = build_phase4_evidence_pack_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE4_EVIDENCE_PACK_READINESS_JSON
    markdown_path = output_dir / PHASE4_EVIDENCE_PACK_READINESS_MARKDOWN
    exported_report = Phase4EvidencePackReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        contract_path=report.contract_path,
        smoke_report_path=report.smoke_report_path,
        summary=report.summary,
        supporting_evidence=report.supporting_evidence,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase4_evidence_pack_readiness_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase4_evidence_pack_readiness_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _build_contract_doc_artifact(base_dir: Path) -> Phase4EvidencePackReadinessArtifact:
    path = base_dir / PHASE4_EVIDENCE_PACK_CONTRACT_PATH
    present = path.exists()
    if not present:
        return Phase4EvidencePackReadinessArtifact(
            id="evidence_pack_contract_doc",
            category="contract",
            path=str(PHASE4_EVIDENCE_PACK_CONTRACT_PATH),
            status="blocked",
            summary="Evidence pack consumption contract document is missing.",
            present=False,
            required=True,
            recommended_action="regenerate_evidence_pack_contract_doc",
        )
    return Phase4EvidencePackReadinessArtifact(
        id="evidence_pack_contract_doc",
        category="contract",
        path=str(PHASE4_EVIDENCE_PACK_CONTRACT_PATH),
        status="ready",
        summary="contract_doc_present=True",
        present=True,
        required=True,
        recommended_action="no_action_required",
    )


def _build_smoke_artifact(base_dir: Path) -> Phase4EvidencePackReadinessArtifact:
    path = base_dir / PHASE4_PROVIDER_CONTRACT_SMOKE_JSON
    if not path.exists():
        return Phase4EvidencePackReadinessArtifact(
            id="provider_contract_smoke",
            category="smoke",
            path=str(PHASE4_PROVIDER_CONTRACT_SMOKE_JSON),
            status="blocked",
            summary="Provider contract smoke report is missing.",
            present=False,
            required=True,
            recommended_action="regenerate_provider_contract_smoke",
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    passed = payload.get("passed") is True
    summary = payload.get("summary", {})
    total = _int_value(summary.get("total"), fallback=0)
    passed_count = _int_value(summary.get("passed"), fallback=0)
    failed_count = _int_value(summary.get("failed"), fallback=0)
    evidence_pack_checks_passed = _evidence_pack_checks_passed(payload)
    status = "ready" if passed else "blocked"
    return Phase4EvidencePackReadinessArtifact(
        id="provider_contract_smoke",
        category="smoke",
        path=str(PHASE4_PROVIDER_CONTRACT_SMOKE_JSON),
        status=status,
        summary=(
            f"passed={passed}; checks={passed_count}/{total}; "
            f"failed_checks={failed_count}; evidence_pack_checks={evidence_pack_checks_passed}"
        ),
        present=True,
        required=True,
        recommended_action=_recommended_action(status),
    )


def _build_supporting_test_artifact(
    base_dir: Path,
    relative_path: Path,
) -> Phase4EvidencePackReadinessArtifact:
    path = base_dir / relative_path
    present = path.exists()
    artifact_id = relative_path.stem.replace("_", "-")
    if not present:
        return Phase4EvidencePackReadinessArtifact(
            id=artifact_id,
            category="test",
            path=str(relative_path),
            status="review",
            summary="Supporting test file is missing.",
            present=False,
            required=False,
            recommended_action="review_evidence_notes",
        )
    return Phase4EvidencePackReadinessArtifact(
        id=artifact_id,
        category="test",
        path=str(relative_path),
        status="ready",
        summary="present=True",
        present=True,
        required=False,
        recommended_action="no_action_required",
    )


def _readiness_summary(
    supporting_evidence: list[Phase4EvidencePackReadinessArtifact],
) -> dict[str, int | bool]:
    total = len(supporting_evidence)
    ready = sum(1 for item in supporting_evidence if item.status == "ready")
    review = sum(1 for item in supporting_evidence if item.status == "review")
    blocked = sum(1 for item in supporting_evidence if item.status == "blocked")
    required = sum(1 for item in supporting_evidence if item.required)
    required_ready = sum(
        1 for item in supporting_evidence if item.required and item.status == "ready"
    )
    smoke_item = next(
        (item for item in supporting_evidence if item.id == "provider_contract_smoke"),
        None,
    )
    smoke_passed = smoke_item is not None and smoke_item.status == "ready"
    evidence_pack_checks_passed = smoke_passed and required_ready >= 2
    return {
        "total_artifacts": total,
        "ready_artifacts": ready,
        "review_artifacts": review,
        "blocked_artifacts": blocked,
        "required_artifacts": required,
        "required_ready_artifacts": required_ready,
        "smoke_passed": smoke_passed,
        "evidence_pack_checks_passed": evidence_pack_checks_passed,
    }


def _overall_status(
    supporting_evidence: list[Phase4EvidencePackReadinessArtifact],
) -> str:
    if any(item.status == "blocked" and item.required for item in supporting_evidence):
        return "blocked"
    if any(item.status == "blocked" for item in supporting_evidence):
        return "blocked"
    if any(item.status == "review" for item in supporting_evidence):
        return "review"
    return "ready"


def _evidence_pack_checks_passed(payload: dict[str, Any]) -> int:
    checks = payload.get("checks", [])
    required_checks = {
        "rag_retrieve_contract",
        "rag_answer_contract",
        "rag_insufficient_evidence_pack_contract",
    }
    passed = 0
    for check in checks:
        if not isinstance(check, dict):
            continue
        if check.get("name") in required_checks and check.get("passed") is True:
            passed += 1
    return passed


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback


def _recommended_action(status: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "review":
        return "review_evidence_notes"
    return "regenerate_evidence"
