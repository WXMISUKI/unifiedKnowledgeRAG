import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE6_QDRANT_VECTOR_STORE_READINESS_ID = "phase6-qdrant-vector-store-readiness-v1"


@dataclass(frozen=True)
class Phase6QdrantVectorStoreReadinessReport:
    id: str
    generated_at: str
    status: str
    decision: str
    deployment_readiness: dict[str, Any]
    reindex_readiness: dict[str, Any]
    backup_recovery_contract: dict[str, Any]
    qdrant_candidate_evidence: dict[str, Any]
    summary: dict[str, int]
    open_signal_ids: list[str]
    operation_notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase6_qdrant_vector_store_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase6QdrantVectorStoreReadinessReport:
    deployment_payload = _load_json(
        base_dir / "docs/operations/deployment-readiness/deployment-readiness.json"
    )
    reindex_payload = _load_json(
        base_dir / "docs/operations/reindex-readiness/reindex-readiness.json"
    )
    contract_path = (
        base_dir
        / "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-deployment-backup-recovery-contract.md"
    )
    candidate_payload = _load_json_optional(
        base_dir / "docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json"
    )

    deployment = _deployment_summary(deployment_payload)
    reindex = _reindex_summary(reindex_payload)
    contract = {
        "path": str(contract_path.relative_to(base_dir)),
        "present": contract_path.exists(),
    }
    candidate = _candidate_summary(candidate_payload)

    signal_pairs = [
        (
            "deployment_readiness_status",
            deployment["status"] == "ready",
        ),
        (
            "deployment_uses_qdrant_backend",
            deployment["retrieval_backend"] == "qdrant",
        ),
        (
            "reindex_readiness_status",
            reindex["status"] == "ready",
        ),
        (
            "backup_recovery_contract_present",
            contract["present"] is True,
        ),
        (
            "qdrant_candidate_evidence_present",
            candidate["present"] is True,
        ),
        (
            "qdrant_candidate_empty_handling_review",
            candidate["empty_handling_rate"] >= 0.8 if candidate["present"] else False,
        ),
    ]
    ready_signals = sum(1 for _, passed in signal_pairs if passed)
    total_signals = len(signal_pairs)
    review_signals = total_signals - ready_signals
    open_signal_ids = [signal_id for signal_id, passed in signal_pairs if not passed]

    status = "ready" if review_signals == 0 else "review"
    if not contract["present"] or deployment["status"] == "blocked":
        status = "blocked"

    return Phase6QdrantVectorStoreReadinessReport(
        id=PHASE6_QDRANT_VECTOR_STORE_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_runtime_defaults",
        deployment_readiness=deployment,
        reindex_readiness=reindex,
        backup_recovery_contract=contract,
        qdrant_candidate_evidence=candidate,
        summary={
            "total_signals": total_signals,
            "ready_signals": ready_signals,
            "review_signals": review_signals,
        },
        open_signal_ids=open_signal_ids,
        operation_notes=_operation_notes(
            deployment=deployment,
            candidate=candidate,
            contract_present=contract["present"],
        ),
    )


def phase6_qdrant_vector_store_readiness_report_to_dict(
    report: Phase6QdrantVectorStoreReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase6_qdrant_vector_store_readiness_markdown(
    report: Phase6QdrantVectorStoreReadinessReport,
) -> str:
    lines = [
        "# Phase 6 Qdrant Vector Store Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Signals",
        "",
        "| Group | Value |",
        "|---|---|",
        f"| Deployment status | `{report.deployment_readiness['status']}` |",
        f"| Retrieval backend | `{report.deployment_readiness['retrieval_backend']}` |",
        f"| Reindex status | `{report.reindex_readiness['status']}` |",
        f"| Contract present | `{report.backup_recovery_contract['present']}` |",
        f"| Candidate evidence present | `{report.qdrant_candidate_evidence['present']}` |",
        f"| Candidate empty handling rate | `{report.qdrant_candidate_evidence['empty_handling_rate']:.4f}` |",
        "",
        "## Summary",
        "",
        f"- Total signals: `{report.summary['total_signals']}`",
        f"- Ready signals: `{report.summary['ready_signals']}`",
        f"- Review signals: `{report.summary['review_signals']}`",
        f"- Open signals: `{', '.join(report.open_signal_ids) if report.open_signal_ids else 'none'}`",
        "",
        "## Operation Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in report.operation_notes)
    lines.append("")
    return "\n".join(lines)


def export_phase6_qdrant_vector_store_readiness_report(
    output_dir: Path = Path("docs/operations/qdrant-vector-store-readiness"),
    *,
    base_dir: Path = Path("."),
) -> Phase6QdrantVectorStoreReadinessReport:
    report = build_phase6_qdrant_vector_store_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase6-qdrant-vector-store-readiness.json"
    markdown_path = output_dir / "phase6-qdrant-vector-store-readiness.md"
    exported_report = Phase6QdrantVectorStoreReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        deployment_readiness=report.deployment_readiness,
        reindex_readiness=report.reindex_readiness,
        backup_recovery_contract=report.backup_recovery_contract,
        qdrant_candidate_evidence=report.qdrant_candidate_evidence,
        summary=report.summary,
        open_signal_ids=report.open_signal_ids,
        operation_notes=report.operation_notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase6_qdrant_vector_store_readiness_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase6_qdrant_vector_store_readiness_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_json_optional(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _deployment_summary(payload: dict[str, Any]) -> dict[str, Any]:
    runtime = payload.get("runtime_config", {})
    return {
        "status": payload.get("status", "review"),
        "retrieval_backend": runtime.get("rag_retrieval_backend", "unknown"),
        "embedding_provider": runtime.get("embedding_provider", "unknown"),
        "qdrant_url": runtime.get("qdrant_url"),
        "qdrant_collection": runtime.get("qdrant_collection"),
    }


def _reindex_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": payload.get("status", "review"),
        "retrieval_backend": payload.get("retrieval_backend", "unknown"),
        "source_count": len(payload.get("sources", [])),
    }


def _candidate_summary(payload: dict[str, Any] | None) -> dict[str, Any]:
    if payload is None:
        return {
            "present": False,
            "path": "docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json",
            "hit_rate": 0.0,
            "citation_match_rate": 0.0,
            "empty_handling_rate": 0.0,
            "total_cases": 0,
        }
    summary = ((payload.get("report") or {}).get("summary") or {})
    return {
        "present": True,
        "path": "docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json",
        "hit_rate": float(summary.get("hit_rate", 0.0)),
        "citation_match_rate": float(summary.get("citation_match_rate", 0.0)),
        "empty_handling_rate": float(summary.get("empty_handling_rate", 0.0)),
        "total_cases": int(summary.get("total_cases", 0)),
    }


def _operation_notes(
    *,
    deployment: dict[str, Any],
    candidate: dict[str, Any],
    contract_present: bool,
) -> list[str]:
    notes = [
        "This report is local, read-only, and does not run backup or restore operations.",
        "Runtime promotion remains gated; this export is prerequisite evidence only.",
    ]
    if deployment["retrieval_backend"] != "qdrant":
        notes.append(
            "Runtime retrieval backend is not qdrant; keep runtime defaults and treat this as candidate readiness."
        )
    if deployment["embedding_provider"] == "mock":
        notes.append(
            "Embedding provider is mock; complete non-mock embedding validation before any promotion review."
        )
    if not contract_present:
        notes.append(
            "Qdrant deployment/backup/recovery contract is missing and should be restored before review."
        )
    if not candidate["present"]:
        notes.append(
            "Qdrant candidate benchmark evidence is missing; regenerate qdrant-bge smoke evidence."
        )
    return notes
