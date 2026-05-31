import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.models.contracts import EvidenceDocument
from app.services.evidence_pack import build_evidence_pack


PHASE4_CALLER_CONSUMPTION_SMOKE_ID = "phase4-caller-consumption-smoke-v1"
PHASE4_CALLER_CONSUMPTION_CONTRACT_PATH = Path(
    "docs/benchmark/chinese-seed/evidence-pack-consumption-contract/"
    "phase4-evidence-pack-consumption-contract.md"
)
PHASE4_CALLER_CONSUMPTION_SMOKE_JSON = (
    "phase4-caller-consumption-smoke.json"
)
PHASE4_CALLER_CONSUMPTION_SMOKE_MARKDOWN = (
    "phase4-caller-consumption-smoke.md"
)


@dataclass(frozen=True)
class Phase4CallerConsumptionSmokeCheck:
    name: str
    passed: bool
    scenario: str
    details: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(frozen=True)
class Phase4CallerConsumptionSmokeReport:
    id: str
    generated_at: str
    status: str
    checks: list[Phase4CallerConsumptionSmokeCheck]
    summary: dict[str, int | bool]
    contract_path: str
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def run_phase4_caller_consumption_smoke(
    *,
    base_dir: Path = Path("."),
) -> Phase4CallerConsumptionSmokeReport:
    checks = [
        _run_check(
            "caller_allowlist_rule",
            "build_evidence_pack(answerable)",
            lambda: _check_answerable_allowlist(),
        ),
        _run_check(
            "caller_fail_closed_rule",
            "build_evidence_pack(insufficient_evidence)",
            lambda: _check_fail_closed(),
        ),
        _run_check(
            "caller_contract_artifact",
            "docs/benchmark/chinese-seed/evidence-pack-consumption-contract",
            lambda: _check_contract_artifact(base_dir),
        ),
    ]
    passed_count = sum(1 for check in checks if check.passed)
    summary = {
        "total": len(checks),
        "passed": passed_count,
        "failed": len(checks) - passed_count,
        "answerable_checks": sum(
            1 for check in checks if check.name == "caller_allowlist_rule" and check.passed
        ),
        "insufficient_checks": sum(
            1 for check in checks if check.name == "caller_fail_closed_rule" and check.passed
        ),
        "contract_doc_present": sum(
            1 for check in checks if check.name == "caller_contract_artifact" and check.passed
        ),
    }
    return Phase4CallerConsumptionSmokeReport(
        id=PHASE4_CALLER_CONSUMPTION_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status="ready" if summary["failed"] == 0 else "blocked",
        checks=checks,
        summary=summary,
        contract_path=str(PHASE4_CALLER_CONSUMPTION_CONTRACT_PATH),
        notes=[
            "This smoke is local, read-only caller-consumption evidence.",
            "It exercises build_evidence_pack directly instead of re-running provider HTTP flow.",
            "It complements the provider contract smoke and the Phase 4 readiness export.",
        ],
    )


def phase4_caller_consumption_smoke_report_to_dict(
    report: Phase4CallerConsumptionSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase4_caller_consumption_smoke_markdown(
    report: Phase4CallerConsumptionSmokeReport,
) -> str:
    status = "passed" if report.status == "ready" else report.status
    lines = [
        "# Phase 4 Caller Consumption Smoke Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{status}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Contract Doc: `{report.contract_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Checks | `{report.summary['total']}` |",
        f"| Passed Checks | `{report.summary['passed']}` |",
        f"| Failed Checks | `{report.summary['failed']}` |",
        f"| Answerable Checks | `{report.summary['answerable_checks']}` |",
        f"| Insufficient Checks | `{report.summary['insufficient_checks']}` |",
        f"| Contract Doc Present | `{report.summary['contract_doc_present']}` |",
        "",
        "## Checks",
        "",
        "| Check | Scenario | Status | Details |",
        "|---|---|---|---|",
    ]
    for check in report.checks:
        check_status = "passed" if check.passed else "failed"
        details = _compact_markdown_details(check)
        lines.append(
            f"| `{check.name}` | `{check.scenario}` | `{check_status}` | {details} |"
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


def export_phase4_caller_consumption_smoke_report(
    output_dir: Path = Path("docs/smoke/evidence-pack-consumption"),
    *,
    base_dir: Path = Path("."),
) -> Phase4CallerConsumptionSmokeReport:
    report = run_phase4_caller_consumption_smoke(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE4_CALLER_CONSUMPTION_SMOKE_JSON
    markdown_path = output_dir / PHASE4_CALLER_CONSUMPTION_SMOKE_MARKDOWN
    exported_report = Phase4CallerConsumptionSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        checks=report.checks,
        summary=report.summary,
        contract_path=report.contract_path,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase4_caller_consumption_smoke_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase4_caller_consumption_smoke_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _check_answerable_allowlist() -> dict[str, Any]:
    documents = [
        _document(
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            title="售后退款规则",
            snippet="客户三天未发货可以申请退款。",
            score=0.91,
            citation="refund_policy_2026#section-3",
            metadata={
                "source_path": "app/data/sources/refund_policy_docs.md",
                "chunk_id": "section-3",
                "chunking_strategy": "fixture-evidence-v1",
                "citation_anchor": "refund_policy_2026#section-3",
            },
        ),
        _document(
            source_id="logistics_faq",
            document_id="logistics_2026",
            title="物流时效 FAQ",
            snippet="默认 2-3 天送达，异常件需要人工跟进。",
            score=0.87,
            citation="logistics_2026#section-2",
            metadata={
                "source_path": "app/data/sources/logistics_faq.md",
                "chunk_id": "section-2",
                "chunking_strategy": "fixture-evidence-v1",
                "citation_anchor": "logistics_2026#section-2",
            },
        ),
    ]
    pack = build_evidence_pack(
        query="客户三天未发货能否退款？",
        requested_source_ids=["refund_policy_docs", "logistics_faq"],
        retrieval_backend="fixture",
        documents=documents,
        filter_context={"backend": "fixture", "enforced": False},
    )
    assert pack["version"] == "evidence-pack-v1"
    assert pack["status"] == "answerable"
    assert pack["reason"] == "documents_returned"
    assert pack["citation_policy"] == "use_only_returned_citations"
    assert pack["allowed_citations"] == [document.citation for document in documents]
    assert pack["evidence_count"] == len(documents)
    assert pack["evidence"][0]["provenance"] == {
        "source_path": "app/data/sources/refund_policy_docs.md",
        "chunk_id": "section-3",
        "chunking_strategy": "fixture-evidence-v1",
        "citation_anchor": "refund_policy_2026#section-3",
    }
    return {
        "version": pack["version"],
        "status": pack["status"],
        "reason": pack["reason"],
        "citation_policy": pack["citation_policy"],
        "allowed_citations": pack["allowed_citations"],
        "evidence_count": pack["evidence_count"],
    }


def _check_fail_closed() -> dict[str, Any]:
    pack = build_evidence_pack(
        query="完全不存在的月球仓库规则",
        requested_source_ids=["refund_policy_docs"],
        retrieval_backend="fixture",
        documents=[],
        filter_context={"backend": "fixture", "enforced": False},
    )
    assert pack["version"] == "evidence-pack-v1"
    assert pack["status"] == "insufficient_evidence"
    assert pack["reason"] == "no_documents"
    assert pack["allowed_citations"] == []
    assert pack["evidence_count"] == 0
    assert pack["score_summary"] == {"max_score": None, "min_score": None}
    assert pack["evidence"] == []
    return {
        "version": pack["version"],
        "status": pack["status"],
        "reason": pack["reason"],
        "allowed_citations": len(pack["allowed_citations"]),
        "evidence_count": pack["evidence_count"],
    }


def _check_contract_artifact(base_dir: Path) -> dict[str, Any]:
    path = base_dir / PHASE4_CALLER_CONSUMPTION_CONTRACT_PATH
    assert path.exists(), "caller-consumption contract doc is missing"
    return {"present": True, "contract_path": str(PHASE4_CALLER_CONSUMPTION_CONTRACT_PATH)}


def _document(
    *,
    source_id: str,
    document_id: str,
    title: str,
    snippet: str,
    score: float,
    citation: str,
    metadata: dict[str, Any],
) -> EvidenceDocument:
    return EvidenceDocument(
        source_id=source_id,
        document_id=document_id,
        title=title,
        snippet=snippet,
        score=score,
        citation=citation,
        metadata=metadata,
    )


def _run_check(name: str, scenario: str, check_fn: Any) -> Phase4CallerConsumptionSmokeCheck:
    try:
        details = check_fn()
    except AssertionError as error:
        return Phase4CallerConsumptionSmokeCheck(
            name=name,
            passed=False,
            scenario=scenario,
            error=str(error) or error.__class__.__name__,
        )
    except Exception as error:
        return Phase4CallerConsumptionSmokeCheck(
            name=name,
            passed=False,
            scenario=scenario,
            error=f"{error.__class__.__name__}: {error}",
        )
    return Phase4CallerConsumptionSmokeCheck(
        name=name,
        passed=True,
        scenario=scenario,
        details=details,
    )


def _compact_markdown_details(check: Phase4CallerConsumptionSmokeCheck) -> str:
    if not check.passed:
        return check.error or "failed"
    return json.dumps(check.details, ensure_ascii=False, sort_keys=True)
