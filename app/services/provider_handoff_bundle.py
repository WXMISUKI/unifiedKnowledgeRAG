import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.services.provider_manifest import build_provider_integration_manifest


PROVIDER_HANDOFF_BUNDLE_ID = "provider-handoff-bundle-v1"


@dataclass(frozen=True)
class HandoffEvidenceSpec:
    id: str
    category: str
    path: Path
    required: bool = True


@dataclass(frozen=True)
class ProviderHandoffBundleReport:
    id: str
    generated_at: str
    status: str
    provider: dict[str, Any]
    evidence_artifacts: list[dict[str, Any]]
    operation_notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


DEFAULT_EVIDENCE_SPECS = [
    HandoffEvidenceSpec(
        id="provider_integration_probe",
        category="integration",
        path=Path("docs/integration/provider-binding/provider-integration-probe.json"),
    ),
    HandoffEvidenceSpec(
        id="provider_contract_smoke",
        category="contract",
        path=Path("docs/smoke/provider-contract/provider-contract-smoke.json"),
    ),
    HandoffEvidenceSpec(
        id="deployment_readiness",
        category="operations",
        path=Path("docs/operations/deployment-readiness/deployment-readiness.json"),
    ),
    HandoffEvidenceSpec(
        id="reindex_readiness",
        category="operations",
        path=Path("docs/operations/reindex-readiness/reindex-readiness.json"),
    ),
    HandoffEvidenceSpec(
        id="source_binding_summary",
        category="source-binding",
        path=Path("docs/integration/source-bindings/provider-source-bindings.json"),
    ),
    HandoffEvidenceSpec(
        id="phase2_source_format_demand_readiness",
        category="ingestion-evidence",
        path=Path(
            "docs/operations/source-format-demand/"
            "phase2-source-format-demand-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase2_unsupported_format_negative_control_smoke",
        category="ingestion-smoke",
        path=Path(
            "docs/smoke/source-format-demand/"
            "phase2-unsupported-format-negative-control-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="deployed_provider_smoke",
        category="deployed-integration",
        path=Path(
            "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_deployed_field_validation_readiness",
        category="operations",
        path=Path(
            "docs/operations/deployed-field-validation/"
            "phase6-deployed-field-validation-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_deployed_handoff_consistency_smoke",
        category="operations-smoke",
        path=Path(
            "docs/smoke/deployed-field-validation/"
            "phase6-deployed-handoff-consistency-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_seed_retrieval_baseline",
        category="retrieval-evidence",
        path=Path(
            "docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_fp_fn_review",
        category="retrieval-evidence",
        path=Path("docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json"),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_retrieval_promotion_readiness",
        category="retrieval-evidence",
        path=Path(
            "docs/benchmark/chinese-seed/retrieval-promotion-readiness/"
            "phase3-retrieval-promotion-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_candidate_runtime_diagnostics",
        category="retrieval-evidence",
        path=Path(
            "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/"
            "phase3-candidate-runtime-diagnostics.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_candidate_latency_resource_diagnostics",
        category="retrieval-evidence",
        path=Path(
            "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/"
            "phase3-candidate-latency-resource-diagnostics.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_hybrid_fusion_threshold_calibration",
        category="retrieval-evidence",
        path=Path(
            "docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/"
            "phase3-hybrid-fusion-threshold-calibration.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_bge_m3_artifact_readiness",
        category="operations",
        path=Path(
            "docs/operations/bge-m3-artifact-readiness/"
            "phase6-bge-m3-artifact-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_bge_m3_vs_mock_fixture_diagnostics",
        category="operations",
        path=Path(
            "docs/operations/bge-m3-comparison-readiness/"
            "phase6-bge-m3-vs-mock-fixture-diagnostics.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_bge_m3_comparison_smoke",
        category="operations-smoke",
        path=Path(
            "docs/smoke/bge-m3-comparison/"
            "phase6-bge-m3-comparison-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_qdrant_vector_store_readiness",
        category="operations",
        path=Path(
            "docs/operations/qdrant-vector-store-readiness/"
            "phase6-qdrant-vector-store-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_qdrant_backup_restore_smoke",
        category="operations-smoke",
        path=Path(
            "docs/smoke/qdrant-backup-restore/"
            "phase6-qdrant-backup-restore-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_qdrant_bge_private_network_promotion_readiness",
        category="operations",
        path=Path(
            "docs/operations/private-network-promotion/"
            "phase6-qdrant-bge-private-network-promotion-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase6_qdrant_bge_private_network_promotion_smoke",
        category="operations-smoke",
        path=Path(
            "docs/smoke/private-network-promotion/"
            "phase6-qdrant-bge-private-network-promotion-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase7_provider_release_readiness",
        category="release-readiness",
        path=Path(
            "docs/operations/provider-release-readiness/"
            "phase7-provider-release-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase7_cross_phase_handoff_consistency_smoke",
        category="release-smoke",
        path=Path(
            "docs/smoke/cross-phase-handoff/"
            "phase7-cross-phase-handoff-consistency-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase8_live_url_validation_readiness",
        category="live-url-validation",
        path=Path(
            "docs/operations/live-url-validation/"
            "phase8-live-url-validation-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase8_live_url_smoke_consistency_check",
        category="live-url-validation-smoke",
        path=Path(
            "docs/smoke/live-url-validation/"
            "phase8-live-url-smoke-consistency-check.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase9_myprivateagent_local_consumption_readiness",
        category="local-consumption",
        path=Path(
            "docs/integration/myprivateagent-local-consumption/"
            "phase9-myprivateagent-local-consumption-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase9_myprivateagent_local_consumption_smoke",
        category="local-consumption-smoke",
        path=Path(
            "docs/smoke/myprivateagent-local-consumption/"
            "phase9-myprivateagent-local-consumption-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase10_myprivateagent_local_consumer_readiness",
        category="local-consumer-verification",
        path=Path(
            "docs/integration/myprivateagent-local-consumer-verification/"
            "phase10-myprivateagent-local-consumer-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase10_myprivateagent_local_consumer_probe",
        category="local-consumer-verification-smoke",
        path=Path(
            "docs/smoke/myprivateagent-local-consumer-verification/"
            "phase10-myprivateagent-local-consumer-probe.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase11_local_provider_integration_profile",
        category="local-provider-integration",
        path=Path(
            "docs/integration/myprivateagent-local-provider-integration/"
            "phase11-local-provider-integration-profile.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase11_provider_discovery_smoke",
        category="local-provider-integration-smoke",
        path=Path(
            "docs/smoke/myprivateagent-local-provider-integration/"
            "phase11-provider-discovery-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase11_rag_retrieve_consumption_smoke",
        category="local-provider-integration-smoke",
        path=Path(
            "docs/smoke/myprivateagent-local-provider-integration/"
            "phase11-rag-retrieve-consumption-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase11_source_binding_preview_smoke",
        category="local-provider-integration-smoke",
        path=Path(
            "docs/smoke/myprivateagent-local-provider-integration/"
            "phase11-source-binding-preview-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase12_local_rag_integration_hardening_profile",
        category="local-rag-hardening",
        path=Path(
            "docs/integration/myprivateagent-local-rag-integration-hardening/"
            "phase12-local-rag-integration-hardening-profile.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase12b_candidate_backend_evaluation_readiness",
        category="candidate-backend-evaluation",
        path=Path(
            "docs/operations/candidate-backend-evaluation-readiness/"
            "phase12b-candidate-backend-evaluation-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase12c_pgvector_candidate_backend_readiness",
        category="candidate-backend-evaluation",
        path=Path(
            "docs/operations/pgvector-candidate-backend-readiness/"
            "phase12c-pgvector-candidate-backend-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase12d_pgvector_live_probe_readiness",
        category="candidate-backend-evaluation",
        path=Path(
            "docs/operations/pgvector-live-probe-readiness/"
            "phase12d-pgvector-live-probe-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_hybrid_cross_case_fp_fn_smoke",
        category="retrieval-evidence",
        path=Path(
            "docs/smoke/hybrid-cross-case-fp-fn/"
            "phase3-hybrid-cross-case-fp-fn-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_aggregation_relation_negative_control_smoke",
        category="retrieval-evidence",
        path=Path(
            "docs/smoke/aggregation-relation-negative-control/"
            "phase3-aggregation-relation-negative-control-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_hybrid_runtime_promotion_decision_readiness",
        category="retrieval-evidence",
        path=Path(
            "docs/benchmark/chinese-seed/hybrid-runtime-promotion/"
            "phase3-hybrid-runtime-promotion-decision-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase3_hybrid_runtime_promotion_decision_smoke",
        category="retrieval-evidence",
        path=Path(
            "docs/smoke/hybrid-runtime-promotion/"
            "phase3-hybrid-runtime-promotion-decision-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase4_evidence_pack_readiness",
        category="evidence-packaging",
        path=Path(
            "docs/benchmark/chinese-seed/evidence-pack-readiness/"
            "phase4-evidence-pack-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase4_caller_consumption_smoke",
        category="caller-consumption",
        path=Path(
            "docs/smoke/evidence-pack-consumption/"
            "phase4-caller-consumption-smoke.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase5_graph_use_case_readiness",
        category="graph-readiness",
        path=Path(
            "docs/benchmark/chinese-seed/graph-use-case-readiness/"
            "phase5-graph-use-case-readiness.json"
        ),
        required=False,
    ),
    HandoffEvidenceSpec(
        id="phase5_graph_boundary_smoke_summary",
        category="graph-boundary-smoke",
        path=Path(
            "docs/smoke/graph-boundary-summary/"
            "phase5-graph-boundary-smoke-summary.json"
        ),
        required=False,
    ),
]


def build_provider_handoff_bundle_report(
    *,
    base_dir: Path = Path("."),
    evidence_specs: list[HandoffEvidenceSpec] | None = None,
) -> ProviderHandoffBundleReport:
    manifest = build_provider_integration_manifest()
    specs = evidence_specs or DEFAULT_EVIDENCE_SPECS
    artifact_rows = [
        _artifact_row(base_dir=base_dir, spec=spec)
        for spec in specs
    ]
    return ProviderHandoffBundleReport(
        id=PROVIDER_HANDOFF_BUNDLE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(artifact_rows),
        provider={
            "provider_id": manifest.provider_id,
            "provider_name": manifest.provider_name,
            "provider_version": manifest.provider_version,
            "contract_version": manifest.contract_version,
            "manifest_version": manifest.manifest_version,
            "component_role": manifest.component_role,
            "compatible_control_planes": manifest.compatible_control_planes,
        },
        evidence_artifacts=artifact_rows,
        operation_notes=_operation_notes(artifact_rows),
    )


def provider_handoff_bundle_report_to_dict(
    report: ProviderHandoffBundleReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_provider_handoff_bundle_markdown(
    report: ProviderHandoffBundleReport,
) -> str:
    lines = [
        "# Provider Handoff Bundle",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Provider: `{report.provider['provider_id']}`",
        f"- Contract: `{report.provider['contract_version']}`",
        f"- Manifest: `{report.provider['manifest_version']}`",
        "",
        "## Evidence Artifacts",
        "",
        "| Artifact | Category | Present | Status | Summary | Recommended Action |",
        "|---|---|---|---|---|---|",
    ]
    for artifact in report.evidence_artifacts:
        lines.append(
            f"| `{artifact['id']}` | `{artifact['category']}` | "
            f"`{artifact['present']}` | `{artifact['status']}` | "
            f"{artifact['summary']} | `{artifact['recommended_action']}` |"
        )
    lines.extend(
        [
            "",
            "## Operation Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in report.operation_notes)
    lines.append("")
    return "\n".join(lines)


def export_provider_handoff_bundle_report(
    output_dir: Path = Path("docs/integration/provider-handoff"),
    *,
    base_dir: Path = Path("."),
    evidence_specs: list[HandoffEvidenceSpec] | None = None,
) -> ProviderHandoffBundleReport:
    report = build_provider_handoff_bundle_report(
        base_dir=base_dir,
        evidence_specs=evidence_specs,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "provider-handoff-bundle.json"
    markdown_path = output_dir / "provider-handoff-bundle.md"
    exported_report = ProviderHandoffBundleReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        provider=report.provider,
        evidence_artifacts=report.evidence_artifacts,
        operation_notes=report.operation_notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            provider_handoff_bundle_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_provider_handoff_bundle_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _artifact_row(
    *,
    base_dir: Path,
    spec: HandoffEvidenceSpec,
) -> dict[str, Any]:
    path = base_dir / spec.path
    if not path.exists():
        status = "missing" if spec.required else "review"
        return {
            "id": spec.id,
            "category": spec.category,
            "path": str(spec.path),
            "present": False,
            "required": spec.required,
            "status": status,
            "summary": (
                "Required evidence artifact is missing."
                if spec.required
                else _optional_missing_summary(spec.id)
            ),
            "recommended_action": (
                f"regenerate_{spec.id}"
                if spec.required
                else _optional_missing_action(spec.id)
            ),
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    status, summary = _artifact_status_and_summary(spec.id, payload)
    return {
        "id": spec.id,
        "category": spec.category,
        "path": str(spec.path),
        "present": True,
        "required": spec.required,
        "status": status,
        "summary": summary,
        "recommended_action": _recommended_action(status),
    }


def _artifact_status_and_summary(
    artifact_id: str,
    payload: dict[str, Any],
) -> tuple[str, str]:
    if artifact_id == "provider_integration_probe":
        bindable = payload.get("bindable") is True
        check_count = len(payload.get("checks", []))
        capability_count = len(payload.get("capability_bindings", []))
        return (
            "ready" if bindable else "blocked",
            f"bindable={bindable}; checks={check_count}; capabilities={capability_count}",
        )
    if artifact_id == "provider_contract_smoke":
        passed = payload.get("passed") is True
        summary = payload.get("summary", {})
        return (
            "ready" if passed else "blocked",
            (
                f"passed={passed}; "
                f"checks={summary.get('passed', 0)}/{summary.get('total', 0)}"
            ),
        )
    if artifact_id in {"deployment_readiness", "reindex_readiness"}:
        status = payload.get("status", "review")
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            f"status={status}",
        )
    if artifact_id == "source_binding_summary":
        status = payload.get("status", "review")
        sources = payload.get("sources", [])
        source_count = _int_value(
            payload.get("total_source_count"),
            fallback=len(sources),
        )
        bindable_count = _int_value(
            payload.get("bindable_source_count"),
            fallback=sum(
                1
                for source in sources
                if isinstance(source, dict) and source.get("bindable") is True
            ),
        )
        source_status_counts = _dict_counts(
            payload.get("status_counts"),
            fallback=_count_source_values(sources, "status"),
        )
        action_counts = _dict_counts(
            payload.get("recommended_action_counts"),
            fallback=_count_source_values(sources, "recommended_action"),
        )
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; bindable_sources={bindable_count}/{source_count}; "
                f"source_statuses={_format_counts(source_status_counts)}; "
                f"recommended_actions={_format_counts(action_counts)}"
            ),
        )
    if artifact_id == "phase2_source_format_demand_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        if not isinstance(summary, dict):
            summary = {}
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_markdown_baseline')}; "
                f"demand_signal={_bool_value(summary.get('format_expansion_demand_signal'))}; "
                f"unsupported_documents={_int_value(summary.get('unsupported_documents'), fallback=0)}; "
                f"non_markdown_sources={_int_value(summary.get('non_markdown_sources'), fallback=0)}; "
                f"open_gate_count={_int_value(summary.get('open_gate_count'), fallback=0)}"
            ),
        )
    if artifact_id == "phase2_unsupported_format_negative_control_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        if not isinstance(summary, dict):
            summary = {}
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_markdown_baseline')}; "
                f"passed_checks={_int_value(summary.get('passed_checks'), fallback=0)}/"
                f"{_int_value(summary.get('total_checks'), fallback=0)}; "
                f"failed_checks={_int_value(summary.get('failed_checks'), fallback=0)}; "
                f"unsupported_documents={_int_value(summary.get('unsupported_documents'), fallback=0)}; "
                f"non_markdown_sources={_int_value(summary.get('non_markdown_sources'), fallback=0)}"
            ),
        )
    if artifact_id == "deployed_provider_smoke":
        status = payload.get("status", "review")
        normalized_status = (
            status if status in {"ready", "review", "blocked"} else "review"
        )
        return (
            normalized_status,
            (
                f"status={status}; "
                f"base_url={payload.get('base_url', 'unknown')}; "
                f"handoff_status={(payload.get('handoff') or {}).get('status', 'unknown')}"
            ),
        )
    if artifact_id == "phase6_deployed_field_validation_readiness":
        status = payload.get("status", "review")
        normalized_status = (
            "review"
            if status == "blocked"
            else (status if status in {"ready", "review", "blocked"} else "review")
        )
        summary = payload.get("summary", {})
        if not isinstance(summary, dict):
            summary = {}
        decision = payload.get("decision", "keep_local_review_until_deployed_smoke")
        if decision == "blocked":
            decision = "keep_local_review_until_deployed_smoke"
        open_gate_ids = summary.get("open_gate_ids", [])
        return (
            normalized_status,
            (
                f"status={status}; field_validation_state={payload.get('field_validation_state', 'review')}; "
                f"decision={decision}; "
                f"live_url_present={_bool_value(summary.get('live_url_present'))}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id == "phase6_deployed_handoff_consistency_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"passed_checks={_int_value(summary.get('passed_checks'), fallback=0)}/"
                f"{_int_value(summary.get('total_checks'), fallback=0)}; "
                f"failed_checks={_int_value(summary.get('failed_checks'), fallback=0)}; "
                f"readiness_status={summary.get('readiness_status', 'unknown')}; "
                f"bundle_status={summary.get('bundle_status', 'unknown')}; "
                f"bundle_row_status={summary.get('bundle_row_status', 'unknown')}"
            ),
        )
    if artifact_id == "phase3_seed_retrieval_baseline":
        report = payload.get("report")
        summary = report.get("summary") if isinstance(report, dict) else {}
        if not isinstance(summary, dict):
            return "review", "phase3_summary=unavailable"
        total_cases = _int_value(summary.get("total_cases"), fallback=0)
        hit_rate = _float_value(summary.get("hit_rate"), fallback=0.0)
        citation_match_rate = _float_value(
            summary.get("citation_match_rate"),
            fallback=0.0,
        )
        empty_handling_rate = _float_value(
            summary.get("empty_handling_rate"),
            fallback=0.0,
        )
        return (
            "ready",
            (
                f"total_cases={total_cases}; "
                f"hit_rate={hit_rate:.4f}; "
                f"citation_match_rate={citation_match_rate:.4f}; "
                f"empty_handling_rate={empty_handling_rate:.4f}"
            ),
        )
    if artifact_id == "phase3_fp_fn_review":
        fp_count = _int_value(payload.get("false_positive_count"), fallback=0)
        fn_count = _int_value(payload.get("false_negative_count"), fallback=0)
        fp_rate = _float_value(payload.get("false_positive_rate"), fallback=0.0)
        fn_rate = _float_value(payload.get("false_negative_rate"), fallback=0.0)
        return (
            "ready",
            (
                f"false_positive_count={fp_count}; "
                f"false_negative_count={fn_count}; "
                f"false_positive_rate={fp_rate:.4f}; "
                f"false_negative_rate={fn_rate:.4f}"
            ),
        )
    if artifact_id == "phase3_retrieval_promotion_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gates = payload.get("open_gates", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"open_gates={_int_value(summary.get('open_gates'), fallback=len(open_gates))}; "
                f"ready_gates={_int_value(summary.get('ready_gates'), fallback=0)}; "
                f"review_gates={_int_value(summary.get('review_gates'), fallback=0)}; "
                f"candidate_gates={_int_value(summary.get('candidate_gates'), fallback=0)}"
            ),
        )
    if artifact_id == "phase3_candidate_runtime_diagnostics":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"ready_checks={_int_value(summary.get('ready_checks'), fallback=0)}/"
                f"{_int_value(summary.get('total_checks'), fallback=0)}; "
                f"review_checks={_int_value(summary.get('review_checks'), fallback=0)}; "
                f"blocked_checks={_int_value(summary.get('blocked_checks'), fallback=0)}"
            ),
        )
    if artifact_id == "phase3_candidate_latency_resource_diagnostics":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        latency_profile = payload.get("latency_profile", {})
        resource_posture = payload.get("resource_posture", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"total_signals={_int_value(summary.get('total_signals'), fallback=0)}; "
                f"ready_signals={_int_value(summary.get('ready_signals'), fallback=0)}; "
                f"review_signals={_int_value(summary.get('review_signals'), fallback=0)}; "
                f"backend={_dict_value(latency_profile, 'backend', 'unknown')}; "
                f"avg_latency_ms={_float_value(latency_profile.get('average_latency_ms'), fallback=0.0):.4f}; "
                f"deployment_status={_dict_value(resource_posture, 'deployment_readiness_status', 'unknown')}; "
                f"runtime_status={_dict_value(resource_posture, 'runtime_diagnostics_status', 'unknown')}"
            ),
        )
    if artifact_id == "phase3_hybrid_fusion_threshold_calibration":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        calibration = payload.get("calibration", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"ready_signals={_int_value(summary.get('ready_signals'), fallback=0)}/"
                f"{_int_value(summary.get('total_signals'), fallback=0)}; "
                f"review_signals={_int_value(summary.get('review_signals'), fallback=0)}; "
                f"fusion={_dict_value(calibration, 'fusion_mode', 'unknown')}; "
                f"score_filter={_dict_value(calibration, 'score_filter_mode', 'unknown')}; "
                f"selected_dense_threshold={_float_value(calibration.get('selected_dense_threshold'), fallback=0.0):.4f}; "
                f"runtime_threshold={_float_value(calibration.get('runtime_threshold'), fallback=0.0):.4f}"
            ),
        )
    if artifact_id == "phase6_bge_m3_artifact_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        artifact = payload.get("artifact", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"ready_signals={_int_value(summary.get('ready_signals'), fallback=0)}/"
                f"{_int_value(summary.get('total_signals'), fallback=0)}; "
                f"review_signals={_int_value(summary.get('review_signals'), fallback=0)}; "
                f"path_exists={bool(_dict_value(artifact, 'path_exists', False))}; "
                f"manifest_exists={bool(_dict_value(artifact, 'manifest_exists', False))}; "
                f"checksum_coverage={_int_value(artifact.get('checksum_coverage_count'), fallback=0)}/"
                f"{_int_value(artifact.get('checksum_target_count'), fallback=0)}"
            ),
        )
    if artifact_id == "phase6_bge_m3_vs_mock_fixture_diagnostics":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        quality_delta = payload.get("quality_delta", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"ready_signals={_int_value(summary.get('ready_signals'), fallback=0)}/"
                f"{_int_value(summary.get('total_signals'), fallback=0)}; "
                f"review_signals={_int_value(summary.get('review_signals'), fallback=0)}; "
                f"hit_rate_delta={_float_value(quality_delta.get('hit_rate_delta'), fallback=0.0):.4f}; "
                f"citation_match_rate_delta={_float_value(quality_delta.get('citation_match_rate_delta'), fallback=0.0):.4f}; "
                f"empty_handling_rate_delta={_float_value(quality_delta.get('empty_handling_rate_delta'), fallback=0.0):.4f}"
            ),
        )
    if artifact_id == "phase6_bge_m3_comparison_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"passed_checks={_int_value(summary.get('passed_checks'), fallback=0)}/"
                f"{_int_value(summary.get('total_checks'), fallback=0)}; "
                f"failed_checks={_int_value(summary.get('failed_checks'), fallback=0)}"
            ),
        )
    if artifact_id == "phase6_qdrant_vector_store_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        deployment = payload.get("deployment_readiness", {})
        candidate = payload.get("qdrant_candidate_evidence", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"ready_signals={_int_value(summary.get('ready_signals'), fallback=0)}/"
                f"{_int_value(summary.get('total_signals'), fallback=0)}; "
                f"review_signals={_int_value(summary.get('review_signals'), fallback=0)}; "
                f"backend={_dict_value(deployment, 'retrieval_backend', 'unknown')}; "
                f"candidate_present={bool(_dict_value(candidate, 'present', False))}; "
                f"empty_handling_rate={_float_value(candidate.get('empty_handling_rate'), fallback=0.0):.4f}"
            ),
        )
    if artifact_id == "phase6_qdrant_backup_restore_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"passed_checks={_int_value(summary.get('passed_checks'), fallback=0)}/"
                f"{_int_value(summary.get('total_checks'), fallback=0)}; "
                f"failed_checks={_int_value(summary.get('failed_checks'), fallback=0)}"
            ),
        )
    if artifact_id == "phase6_qdrant_bge_private_network_promotion_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; state={payload.get('promotion_review_state', 'review')}; "
                f"decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"ready_signals={_int_value(summary.get('ready_signals'), fallback=0)}/"
                f"{_int_value(summary.get('total_signals'), fallback=0)}; "
                f"review_signals={_int_value(summary.get('review_signals'), fallback=0)}; "
                f"blocked_signals={_int_value(summary.get('blocked_signals'), fallback=0)}"
            ),
        )
    if artifact_id == "phase6_qdrant_bge_private_network_promotion_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"passed_checks={_int_value(summary.get('passed_checks'), fallback=0)}/"
                f"{_int_value(summary.get('total_checks'), fallback=0)}; "
                f"failed_checks={_int_value(summary.get('failed_checks'), fallback=0)}"
            ),
        )
    if artifact_id == "phase7_provider_release_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; release_state={payload.get('release_state', 'review')}; "
                f"decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"local_handoff_ready={bool(_dict_value(summary, 'ready_for_local_provider_handoff', False))}; "
                f"runtime_promotion_ready={bool(_dict_value(summary, 'ready_for_runtime_default_promotion', False))}; "
                f"open_gate_count={_int_value(len(_dict_value(summary, 'open_gate_ids', [])), fallback=0)}"
            ),
        )
    if artifact_id == "phase7_cross_phase_handoff_consistency_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults_until_live_validation')}; "
                f"passed_checks={_int_value(_dict_value(summary, 'passed_checks', 0), fallback=0)}/"
                f"{_int_value(_dict_value(summary, 'total_checks', 0), fallback=0)}; "
                f"failed_checks={_int_value(_dict_value(summary, 'failed_checks', 0), fallback=0)}"
            ),
        )
    if artifact_id == "phase8_live_url_validation_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; "
                f"live_validation_state={payload.get('live_validation_state', 'review')}; "
                f"decision={payload.get('decision', 'keep_runtime_defaults_until_live_url_validation')}; "
                f"deployed_smoke_present={bool(_dict_value(summary, 'deployed_smoke_present', False))}; "
                f"deployed_smoke_status={_dict_value(summary, 'deployed_smoke_status', 'review')}; "
                f"live_url_present={bool(_dict_value(summary, 'live_url_present', False))}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id == "phase8_live_url_smoke_consistency_check":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults_until_live_url_validation')}; "
                f"passed_checks={_int_value(_dict_value(summary, 'passed_checks', 0), fallback=0)}/"
                f"{_int_value(_dict_value(summary, 'total_checks', 0), fallback=0)}; "
                f"failed_checks={_int_value(_dict_value(summary, 'failed_checks', 0), fallback=0)}; "
                f"readiness_status={_dict_value(summary, 'readiness_status', 'unknown')}; "
                f"bundle_status={_dict_value(summary, 'bundle_status', 'unknown')}; "
                f"bundle_row_status={_dict_value(summary, 'bundle_row_status', 'unknown')}"
            ),
        )
    if artifact_id == "phase9_myprivateagent_local_consumption_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; "
                f"local_consumption_state={payload.get('local_consumption_state', 'review')}; "
                f"decision={payload.get('decision', 'keep_local_consumption_review')}; "
                f"local_provider_url={_dict_value(summary, 'local_provider_url', 'http://127.0.0.1:8020')}; "
                f"local_handoff_ready={bool(_dict_value(summary, 'local_handoff_ready', False))}; "
                f"runtime_promotion_ready={bool(_dict_value(summary, 'runtime_promotion_ready', False))}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id == "phase9_myprivateagent_local_consumption_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"passed_checks={_int_value(_dict_value(summary, 'passed_checks', 0), fallback=0)}/"
                f"{_int_value(_dict_value(summary, 'total_checks', 0), fallback=0)}; "
                f"failed_checks={_int_value(_dict_value(summary, 'failed_checks', 0), fallback=0)}; "
                f"readiness_status={_dict_value(summary, 'readiness_status', 'unknown')}; "
                f"local_consumption_state={_dict_value(summary, 'local_consumption_state', 'unknown')}"
            ),
        )
    if artifact_id == "phase10_myprivateagent_local_consumer_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; "
                f"local_consumer_state={payload.get('local_consumer_state', 'review')}; "
                f"decision={payload.get('decision', 'run_local_consumer_probe_before_myprivateagent_integration')}; "
                f"local_provider_url={_dict_value(summary, 'local_provider_url', 'http://127.0.0.1:8020')}; "
                f"api_key_mode={_dict_value(summary, 'api_key_mode', 'not_configured_local_dev')}; "
                f"graph_boundary_ready={bool(_dict_value(summary, 'graph_boundary_ready', False))}; "
                f"runtime_promotion_status={_dict_value(summary, 'runtime_promotion_status', 'keep_runtime_defaults')}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id == "phase10_myprivateagent_local_consumer_probe":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_provider_side_consumer_probe_review')}; "
                f"passed_checks={_int_value(_dict_value(summary, 'passed_checks', 0), fallback=0)}/"
                f"{_int_value(_dict_value(summary, 'total_checks', 0), fallback=0)}; "
                f"failed_checks={_int_value(_dict_value(summary, 'failed_checks', 0), fallback=0)}; "
                f"local_consumer_state={_dict_value(summary, 'local_consumer_state', 'unknown')}; "
                f"api_key_mode={_dict_value(summary, 'api_key_mode', 'not_configured_local_dev')}; "
                f"runtime_promotion_status={_dict_value(summary, 'runtime_promotion_status', 'keep_runtime_defaults')}"
            ),
        )
    if artifact_id == "phase11_local_provider_integration_profile":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; integration_state={payload.get('integration_state', 'review')}; "
                f"decision={payload.get('decision', 'run_phase11_local_integration_smokes')}; "
                f"local_provider_url={_dict_value(summary, 'local_provider_url', 'http://127.0.0.1:8020')}; "
                f"api_key_mode={_dict_value(summary, 'api_key_mode', 'not_configured_local_dev')}; "
                f"runtime_promotion_status={_dict_value(summary, 'runtime_promotion_status', 'keep_runtime_defaults')}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id in {
        "phase11_provider_discovery_smoke",
        "phase11_rag_retrieve_consumption_smoke",
        "phase11_source_binding_preview_smoke",
    }:
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'review_evidence_notes')}; "
                f"passed_checks={_int_value(_dict_value(summary, 'passed_checks', 0), fallback=0)}/"
                f"{_int_value(_dict_value(summary, 'total_checks', 0), fallback=0)}; "
                f"failed_checks={_int_value(_dict_value(summary, 'failed_checks', 0), fallback=0)}"
            ),
        )
    if artifact_id == "phase3_hybrid_cross_case_fp_fn_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; "
                f"passed_checks={_int_value(summary.get('passed'), fallback=0)}/"
                f"{_int_value(summary.get('total'), fallback=0)}; "
                f"false_positive_count={_int_value(summary.get('false_positive_count'), fallback=0)}; "
                f"false_negative_count={_int_value(summary.get('false_negative_count'), fallback=0)}"
            ),
        )
    if artifact_id == "phase12_local_rag_integration_hardening_profile":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; hardening_state={payload.get('hardening_state', 'review')}; "
                f"decision={payload.get('decision', 'resolve_phase12_hardening_blockers')}; "
                f"local_provider_url={_dict_value(summary, 'local_provider_url', 'http://127.0.0.1:8020')}; "
                f"api_key_mode={_dict_value(summary, 'api_key_mode', 'not_configured_local_dev')}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id == "phase12b_candidate_backend_evaluation_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        reference_only_family_ids = summary.get("reference_only_family_ids", [])
        review_ready_family_ids = summary.get("review_ready_family_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; evaluation_state={payload.get('evaluation_state', 'review')}; "
                f"decision={payload.get('decision', 'continue_spike')}; "
                f"strategy_verdict={_dict_value(summary, 'strategy_verdict', 'continue_provider_first_with_candidate_backends')}; "
                f"review_ready_families={_jsonish_list(review_ready_family_ids if isinstance(review_ready_family_ids, list) else [])}; "
                f"reference_only_families={_jsonish_list(reference_only_family_ids if isinstance(reference_only_family_ids, list) else [])}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id == "phase12c_pgvector_candidate_backend_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        review_ready_family_ids = summary.get("review_ready_family_ids", [])
        ready_family_ids = summary.get("ready_family_ids", [])
        blocked_family_ids = summary.get("blocked_family_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; evaluation_state={payload.get('evaluation_state', 'review')}; "
                f"decision={payload.get('decision', 'continue_spike')}; "
                f"strategy_verdict={_dict_value(summary, 'strategy_verdict', 'continue_provider_first_with_candidate_backends')}; "
                f"pgvector_database_url_present={_bool_value(summary.get('pgvector_database_url_present', False))}; "
                f"review_ready_families={_jsonish_list(review_ready_family_ids if isinstance(review_ready_family_ids, list) else [])}; "
                f"ready_families={_jsonish_list(ready_family_ids if isinstance(ready_family_ids, list) else [])}; "
                f"blocked_families={_jsonish_list(blocked_family_ids if isinstance(blocked_family_ids, list) else [])}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id == "phase12d_pgvector_live_probe_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        review_ready_family_ids = summary.get("review_ready_family_ids", [])
        ready_family_ids = summary.get("ready_family_ids", [])
        blocked_family_ids = summary.get("blocked_family_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; evaluation_state={payload.get('evaluation_state', 'review')}; "
                f"decision={payload.get('decision', 'continue_spike')}; "
                f"strategy_verdict={_dict_value(summary, 'strategy_verdict', 'continue_provider_first_with_candidate_backends')}; "
                f"pgvector_database_url_present={_bool_value(summary.get('pgvector_database_url_present', False))}; "
                f"pgvector_driver_available={_bool_value(summary.get('pgvector_driver_available', False))}; "
                f"review_ready_families={_jsonish_list(review_ready_family_ids if isinstance(review_ready_family_ids, list) else [])}; "
                f"ready_families={_jsonish_list(ready_family_ids if isinstance(ready_family_ids, list) else [])}; "
                f"blocked_families={_jsonish_list(blocked_family_ids if isinstance(blocked_family_ids, list) else [])}; "
                f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
            ),
        )
    if artifact_id == "phase3_aggregation_relation_negative_control_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"total_checks={_int_value(summary.get('total_checks'), fallback=0)}; "
                f"passed_checks={_int_value(summary.get('passed_checks'), fallback=0)}; "
                f"failed_checks={_int_value(summary.get('failed_checks'), fallback=0)}; "
                f"relation_unsupported_count={_int_value(summary.get('relation_unsupported_count'), fallback=0)}; "
                f"expected_empty_pass_rate={_float_value(summary.get('expected_empty_pass_rate'), fallback=0.0):.4f}"
            ),
        )
    if artifact_id == "phase3_hybrid_runtime_promotion_decision_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        open_gate_ids = summary.get("open_gate_ids", [])
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"review_state={payload.get('review_state', 'review')}; "
                f"required_signals={_int_value(summary.get('required_signals'), fallback=0)}; "
                f"ready_signals={_int_value(summary.get('ready_signals'), fallback=0)}; "
                f"open_gates={_int_value(summary.get('review_signals'), fallback=0) + _int_value(summary.get('blocked_signals'), fallback=0)}; "
                f"open_gate_count={len(open_gate_ids) if isinstance(open_gate_ids, list) else 0}"
            ),
        )
    if artifact_id == "phase3_hybrid_runtime_promotion_decision_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_runtime_defaults')}; "
                f"passed_checks={_int_value(summary.get('passed_checks'), fallback=0)}/"
                f"{_int_value(summary.get('total_checks'), fallback=0)}; "
                f"failed_checks={_int_value(summary.get('failed_checks'), fallback=0)}"
            ),
        )
    if artifact_id == "phase4_evidence_pack_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_caller_ownership')}; "
                f"smoke_passed={bool(summary.get('smoke_passed', False))}; "
                f"ready_artifacts={_int_value(summary.get('ready_artifacts'), fallback=0)}/"
                f"{_int_value(summary.get('total_artifacts'), fallback=0)}; "
                f"required_ready={_int_value(summary.get('required_ready_artifacts'), fallback=0)}/"
                f"{_int_value(summary.get('required_artifacts'), fallback=0)}"
            ),
        )
    if artifact_id == "phase4_caller_consumption_smoke":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; passed_checks={_int_value(summary.get('passed'), fallback=0)}/"
                f"{_int_value(summary.get('total'), fallback=0)}; "
                f"answerable_checks={_int_value(summary.get('answerable_checks'), fallback=0)}; "
                f"insufficient_checks={_int_value(summary.get('insufficient_checks'), fallback=0)}; "
                f"contract_doc_present={bool(summary.get('contract_doc_present', False))}"
            ),
        )
    if artifact_id == "phase5_graph_use_case_readiness":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_graph_query_planned')}; "
                f"graph_schema_count={_int_value(summary.get('graph_schema_count'), fallback=0)}; "
                f"graph_query_status={summary.get('graph_query_status', 'unknown')}; "
                f"graph_query_planned={bool(summary.get('graph_query_planned', False))}; "
                f"preflight_graph_boundary_ready={bool(summary.get('preflight_graph_boundary_ready', False))}; "
                f"smoke_graph_check_passed={bool(summary.get('smoke_graph_check_passed', False))}; "
                f"smoke_checks_passed={bool(summary.get('smoke_checks_passed', False))}"
            ),
        )
    if artifact_id == "phase5_graph_boundary_smoke_summary":
        status = payload.get("status", "review")
        summary = payload.get("summary", {})
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            (
                f"status={status}; decision={payload.get('decision', 'keep_graph_query_planned')}; "
                f"source_smoke_passed={bool(summary.get('source_smoke_passed', False))}; "
                f"graph_checks_passed={_int_value(summary.get('graph_checks_passed'), fallback=0)}; "
                f"graph_schema_count={_int_value(summary.get('graph_schema_count'), fallback=0)}; "
                f"graph_query_status={summary.get('graph_query_status', 'unknown')}; "
                f"graph_query_planned={bool(summary.get('graph_query_planned', False))}; "
                f"graph_error_code={summary.get('graph_error_code', 'unknown')}"
            ),
        )
    return "review", "Unknown evidence artifact shape."


def _count_source_values(
    sources: list[Any],
    field_name: str,
) -> dict[str, int]:
    counts = Counter(
        source.get(field_name)
        for source in sources
        if isinstance(source, dict) and source.get(field_name)
    )
    return dict(sorted(counts.items()))


def _dict_counts(value: Any, *, fallback: dict[str, int]) -> dict[str, int]:
    if not isinstance(value, dict):
        return fallback
    counts: dict[str, int] = {}
    for key, count in value.items():
        if not isinstance(key, str):
            continue
        normalized_count = _int_value(count, fallback=0)
        if normalized_count > 0:
            counts[key] = normalized_count
    return dict(sorted(counts.items()))


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return False


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)


def _jsonish_list(values: list[Any]) -> str:
    return json.dumps(values, ensure_ascii=False)


def _float_value(value: Any, *, fallback: float) -> float:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int | float):
        return float(value)
    return fallback


def _format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return ", ".join(
        f"{value}:{count}"
        for value, count in counts.items()
    )


def _recommended_action(status: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "review":
        return "review_evidence_notes"
    if status == "missing":
        return "regenerate_evidence"
    return "resolve_failed_evidence"


def _optional_missing_summary(artifact_id: str) -> str:
    if artifact_id == "deployed_provider_smoke":
        return "Optional deployed evidence is missing."
    if artifact_id == "phase6_deployed_field_validation_readiness":
        return "Optional Phase 6 deployed field-validation readiness evidence is missing."
    if artifact_id == "phase6_deployed_handoff_consistency_smoke":
        return "Optional Phase 6 deployed handoff consistency smoke evidence is missing."
    if artifact_id == "phase2_source_format_demand_readiness":
        return "Optional Phase 2 source-format demand readiness evidence is missing."
    if artifact_id == "phase2_unsupported_format_negative_control_smoke":
        return "Optional Phase 2 unsupported-format negative-control smoke evidence is missing."
    if artifact_id == "phase3_seed_retrieval_baseline":
        return "Optional Phase 3 retrieval baseline evidence is missing."
    if artifact_id == "phase3_fp_fn_review":
        return "Optional Phase 3 FP/FN review evidence is missing."
    if artifact_id == "phase3_retrieval_promotion_readiness":
        return "Optional Phase 3 readiness export is missing."
    if artifact_id == "phase3_candidate_runtime_diagnostics":
        return "Optional Phase 3 runtime diagnostics export is missing."
    if artifact_id == "phase3_candidate_latency_resource_diagnostics":
        return "Optional Phase 3 latency/resource diagnostics export is missing."
    if artifact_id == "phase3_hybrid_cross_case_fp_fn_smoke":
        return "Optional Phase 3 hybrid cross-case FP/FN smoke evidence is missing."
    if artifact_id == "phase3_hybrid_fusion_threshold_calibration":
        return "Optional Phase 3 hybrid fusion/threshold calibration evidence is missing."
    if artifact_id == "phase6_bge_m3_artifact_readiness":
        return "Optional Phase 6 BGE-M3 artifact readiness evidence is missing."
    if artifact_id == "phase6_bge_m3_vs_mock_fixture_diagnostics":
        return "Optional Phase 6 BGE-M3 comparison diagnostics evidence is missing."
    if artifact_id == "phase6_bge_m3_comparison_smoke":
        return "Optional Phase 6 BGE-M3 comparison smoke evidence is missing."
    if artifact_id == "phase6_qdrant_vector_store_readiness":
        return "Optional Phase 6 Qdrant vector-store readiness evidence is missing."
    if artifact_id == "phase6_qdrant_backup_restore_smoke":
        return "Optional Phase 6 Qdrant backup/restore smoke evidence is missing."
    if artifact_id == "phase6_qdrant_bge_private_network_promotion_readiness":
        return "Optional Phase 6 private-network promotion readiness evidence is missing."
    if artifact_id == "phase6_qdrant_bge_private_network_promotion_smoke":
        return "Optional Phase 6 private-network promotion smoke evidence is missing."
    if artifact_id == "phase7_provider_release_readiness":
        return "Optional Phase 7 provider release readiness evidence is missing."
    if artifact_id == "phase7_cross_phase_handoff_consistency_smoke":
        return "Optional Phase 7 cross-phase handoff consistency smoke evidence is missing."
    if artifact_id == "phase8_live_url_validation_readiness":
        return "Optional Phase 8 live URL validation readiness evidence is missing."
    if artifact_id == "phase8_live_url_smoke_consistency_check":
        return "Optional Phase 8 live URL smoke consistency evidence is missing."
    if artifact_id == "phase9_myprivateagent_local_consumption_readiness":
        return "Optional Phase 9 MyPrivateAgent local-consumption readiness evidence is missing."
    if artifact_id == "phase9_myprivateagent_local_consumption_smoke":
        return "Optional Phase 9 MyPrivateAgent local-consumption smoke evidence is missing."
    if artifact_id == "phase10_myprivateagent_local_consumer_readiness":
        return "Optional Phase 10 MyPrivateAgent local consumer readiness evidence is missing."
    if artifact_id == "phase10_myprivateagent_local_consumer_probe":
        return "Optional Phase 10 MyPrivateAgent local consumer probe evidence is missing."
    if artifact_id == "phase11_local_provider_integration_profile":
        return "Optional Phase 11 local provider integration profile evidence is missing."
    if artifact_id == "phase11_provider_discovery_smoke":
        return "Optional Phase 11 provider discovery smoke evidence is missing."
    if artifact_id == "phase11_rag_retrieve_consumption_smoke":
        return "Optional Phase 11 retrieve-consumption smoke evidence is missing."
    if artifact_id == "phase11_source_binding_preview_smoke":
        return "Optional Phase 11 source-binding preview smoke evidence is missing."
    if artifact_id == "phase12_local_rag_integration_hardening_profile":
        return "Optional Phase 12 local RAG integration hardening profile evidence is missing."
    if artifact_id == "phase12b_candidate_backend_evaluation_readiness":
        return "Optional Phase 12b candidate backend evaluation readiness evidence is missing."
    if artifact_id == "phase12c_pgvector_candidate_backend_readiness":
        return "Optional Phase 12c pgvector candidate backend readiness evidence is missing."
    if artifact_id == "phase12d_pgvector_live_probe_readiness":
        return "Optional Phase 12d pgvector live probe readiness evidence is missing."
    if artifact_id == "phase3_aggregation_relation_negative_control_smoke":
        return "Optional Phase 3 aggregation/relation negative-control smoke evidence is missing."
    if artifact_id == "phase3_hybrid_runtime_promotion_decision_readiness":
        return (
            "Optional Phase 3 hybrid runtime promotion decision readiness "
            "export is missing."
        )
    if artifact_id == "phase3_hybrid_runtime_promotion_decision_smoke":
        return (
            "Optional Phase 3 hybrid runtime promotion decision smoke "
            "evidence is missing."
        )
    if artifact_id == "phase4_evidence_pack_readiness":
        return "Optional Phase 4 evidence pack readiness export is missing."
    if artifact_id == "phase4_caller_consumption_smoke":
        return "Optional Phase 4 caller-consumption smoke evidence is missing."
    if artifact_id == "phase5_graph_use_case_readiness":
        return "Optional Phase 5 graph readiness export is missing."
    if artifact_id == "phase5_graph_boundary_smoke_summary":
        return "Optional Phase 5 graph boundary smoke summary is missing."
    return "Optional evidence artifact is missing."


def _optional_missing_action(artifact_id: str) -> str:
    if artifact_id == "deployed_provider_smoke":
        return "run_deployed_provider_smoke_after_deployment"
    if artifact_id == "phase6_deployed_field_validation_readiness":
        return "regenerate_phase6_deployed_field_validation_readiness"
    if artifact_id == "phase6_deployed_handoff_consistency_smoke":
        return "regenerate_phase6_deployed_handoff_consistency_smoke"
    if artifact_id == "phase2_source_format_demand_readiness":
        return "regenerate_phase2_source_format_demand_readiness"
    if artifact_id == "phase2_unsupported_format_negative_control_smoke":
        return "regenerate_phase2_unsupported_format_negative_control_smoke"
    if artifact_id == "phase3_seed_retrieval_baseline":
        return "regenerate_phase3_seed_retrieval_baseline"
    if artifact_id == "phase3_fp_fn_review":
        return "regenerate_phase3_fp_fn_review"
    if artifact_id == "phase3_retrieval_promotion_readiness":
        return "regenerate_phase3_retrieval_promotion_readiness"
    if artifact_id == "phase3_candidate_runtime_diagnostics":
        return "regenerate_phase3_candidate_runtime_diagnostics"
    if artifact_id == "phase3_candidate_latency_resource_diagnostics":
        return "regenerate_phase3_candidate_latency_resource_diagnostics"
    if artifact_id == "phase3_hybrid_cross_case_fp_fn_smoke":
        return "regenerate_phase3_hybrid_cross_case_fp_fn_smoke"
    if artifact_id == "phase3_hybrid_fusion_threshold_calibration":
        return "regenerate_phase3_hybrid_fusion_threshold_calibration"
    if artifact_id == "phase6_bge_m3_artifact_readiness":
        return "regenerate_phase6_bge_m3_artifact_readiness"
    if artifact_id == "phase6_bge_m3_vs_mock_fixture_diagnostics":
        return "regenerate_phase6_bge_m3_vs_mock_fixture_diagnostics"
    if artifact_id == "phase6_bge_m3_comparison_smoke":
        return "regenerate_phase6_bge_m3_comparison_smoke"
    if artifact_id == "phase6_qdrant_vector_store_readiness":
        return "regenerate_phase6_qdrant_vector_store_readiness"
    if artifact_id == "phase6_qdrant_backup_restore_smoke":
        return "regenerate_phase6_qdrant_backup_restore_smoke"
    if artifact_id == "phase6_qdrant_bge_private_network_promotion_readiness":
        return "regenerate_phase6_qdrant_bge_private_network_promotion_readiness"
    if artifact_id == "phase6_qdrant_bge_private_network_promotion_smoke":
        return "regenerate_phase6_qdrant_bge_private_network_promotion_smoke"
    if artifact_id == "phase7_provider_release_readiness":
        return "regenerate_phase7_provider_release_readiness"
    if artifact_id == "phase7_cross_phase_handoff_consistency_smoke":
        return "regenerate_phase7_cross_phase_handoff_consistency_smoke"
    if artifact_id == "phase8_live_url_validation_readiness":
        return "regenerate_phase8_live_url_validation_readiness"
    if artifact_id == "phase8_live_url_smoke_consistency_check":
        return "regenerate_phase8_live_url_smoke_consistency_check"
    if artifact_id == "phase9_myprivateagent_local_consumption_readiness":
        return "regenerate_phase9_myprivateagent_local_consumption_readiness"
    if artifact_id == "phase9_myprivateagent_local_consumption_smoke":
        return "regenerate_phase9_myprivateagent_local_consumption_smoke"
    if artifact_id == "phase10_myprivateagent_local_consumer_readiness":
        return "regenerate_phase10_myprivateagent_local_consumer_readiness"
    if artifact_id == "phase10_myprivateagent_local_consumer_probe":
        return "regenerate_phase10_myprivateagent_local_consumer_probe"
    if artifact_id == "phase11_local_provider_integration_profile":
        return "regenerate_phase11_local_provider_integration_profile"
    if artifact_id == "phase11_provider_discovery_smoke":
        return "regenerate_phase11_provider_discovery_smoke"
    if artifact_id == "phase11_rag_retrieve_consumption_smoke":
        return "regenerate_phase11_rag_retrieve_consumption_smoke"
    if artifact_id == "phase11_source_binding_preview_smoke":
        return "regenerate_phase11_source_binding_preview_smoke"
    if artifact_id == "phase12_local_rag_integration_hardening_profile":
        return "regenerate_phase12_local_rag_integration_hardening_profile"
    if artifact_id == "phase12b_candidate_backend_evaluation_readiness":
        return "regenerate_phase12b_candidate_backend_evaluation_readiness"
    if artifact_id == "phase12c_pgvector_candidate_backend_readiness":
        return "regenerate_phase12c_pgvector_candidate_backend_readiness"
    if artifact_id == "phase12d_pgvector_live_probe_readiness":
        return "regenerate_phase12d_pgvector_live_probe_readiness"
    if artifact_id == "phase3_aggregation_relation_negative_control_smoke":
        return "regenerate_phase3_aggregation_relation_negative_control_smoke"
    if artifact_id == "phase3_hybrid_runtime_promotion_decision_readiness":
        return "regenerate_phase3_hybrid_runtime_promotion_decision_readiness"
    if artifact_id == "phase3_hybrid_runtime_promotion_decision_smoke":
        return "regenerate_phase3_hybrid_runtime_promotion_decision_smoke"
    if artifact_id == "phase4_evidence_pack_readiness":
        return "regenerate_phase4_evidence_pack_readiness"
    if artifact_id == "phase4_caller_consumption_smoke":
        return "regenerate_phase4_caller_consumption_smoke"
    if artifact_id == "phase5_graph_use_case_readiness":
        return "regenerate_phase5_graph_use_case_readiness"
    if artifact_id == "phase5_graph_boundary_smoke_summary":
        return "regenerate_phase5_graph_boundary_smoke_summary"
    return "review_evidence_notes"


def _overall_status(artifact_rows: list[dict[str, Any]]) -> str:
    if any(
        artifact.get("id") == "deployed_provider_smoke"
        and artifact.get("status") == "blocked"
        for artifact in artifact_rows
    ):
        return "blocked"
    if any(
        artifact.get("required", False)
        and artifact.get("status") in {"missing", "blocked"}
        for artifact in artifact_rows
    ):
        return "blocked"
    if any(artifact.get("status") != "ready" for artifact in artifact_rows):
        return "review"
    return "ready"


def _operation_notes(artifact_rows: list[dict[str, Any]]) -> list[str]:
    notes = [
        "This bundle is a read-only handoff index over existing local evidence files.",
        "Regenerate prerequisite evidence reports after configuration, dependency, source, or index lifecycle changes.",
        "External control planes still own provider registration, heartbeat governance, audit policy, and source-to-agent binding decisions.",
    ]
    if any(artifact["status"] == "missing" for artifact in artifact_rows):
        notes.append("At least one required evidence artifact is missing.")
    if any(artifact["status"] == "review" for artifact in artifact_rows):
        notes.append("At least one evidence artifact requires human review before promotion.")
    if any(
        artifact["id"] == "deployed_provider_smoke" and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Deployed provider smoke evidence is optional before deployment; run it against the deployed base URL before external binding."
        )
    if any(
        artifact["id"] == "phase2_source_format_demand_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 2 source-format demand readiness export is optional before parser-expansion review; regenerate it after source-binding evidence changes."
        )
    if any(
        artifact["id"] == "phase2_unsupported_format_negative_control_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 2 unsupported-format negative-control smoke is optional before parser-expansion review; regenerate it after Phase 2 source-format demand readiness changes."
        )
    if any(
        artifact["id"] == "phase6_deployed_field_validation_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 deployed field-validation readiness evidence is optional before live-url review; regenerate it after deployed smoke or handoff evidence changes."
        )
    if any(
        artifact["id"] == "phase6_deployed_handoff_consistency_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 deployed handoff consistency smoke is optional before live-url review; regenerate it after deployed field-validation readiness or handoff bundle changes."
        )
    if any(
        artifact["id"] == "phase3_candidate_runtime_diagnostics"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 3 candidate runtime diagnostics export is optional before promotion review; regenerate it after runtime configuration or readiness evidence changes."
        )
    if any(
        artifact["id"] == "phase3_candidate_latency_resource_diagnostics"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 3 latency/resource diagnostics export is optional before promotion review; regenerate it after benchmark latency or deployment posture changes."
        )
    if any(
        artifact["id"] == "phase3_hybrid_fusion_threshold_calibration"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 3 hybrid fusion/threshold calibration export is optional before promotion review; regenerate it after hybrid evidence or threshold recommendation updates."
        )
    if any(
        artifact["id"] == "phase6_bge_m3_artifact_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 BGE-M3 artifact readiness export is optional before deployment promotion review; regenerate it after model artifact or deployment readiness changes."
        )
    if any(
        artifact["id"] == "phase6_bge_m3_vs_mock_fixture_diagnostics"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 BGE-M3 comparison diagnostics export is optional before promotion review; regenerate it after baseline/candidate evidence or deployment linkage changes."
        )
    if any(
        artifact["id"] == "phase6_bge_m3_comparison_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 BGE-M3 comparison smoke is optional before promotion review; regenerate it after comparison diagnostics or artifact readiness changes."
        )
    if any(
        artifact["id"] == "phase6_qdrant_vector_store_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 Qdrant vector-store readiness export is optional before deployment promotion review; regenerate it after deployment/reindex evidence or qdrant candidate evidence changes."
        )
    if any(
        artifact["id"] == "phase6_qdrant_backup_restore_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 Qdrant backup/restore smoke is optional before deployment promotion review; regenerate it after qdrant readiness evidence changes."
        )
    if any(
        artifact["id"] == "phase6_qdrant_bge_private_network_promotion_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 private-network promotion readiness export is optional before promotion review; regenerate it after qdrant/bge comparison evidence changes."
        )
    if any(
        artifact["id"] == "phase6_qdrant_bge_private_network_promotion_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 6 private-network promotion smoke is optional before promotion review; regenerate it after private-network readiness evidence changes."
        )
    if any(
        artifact["id"] == "phase7_provider_release_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 7 provider release readiness is optional before final handoff review; regenerate it after cross-phase evidence updates."
        )
    if any(
        artifact["id"] == "phase7_cross_phase_handoff_consistency_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 7 cross-phase handoff consistency smoke is optional before final handoff review; regenerate it after Phase 7 release-readiness or phase decision evidence changes."
        )
    if any(
        artifact["id"] == "phase8_live_url_validation_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 8 live URL validation readiness is optional before deployed live validation review; regenerate it after Phase 6/7 evidence or deployed smoke changes."
        )
    if any(
        artifact["id"] == "phase8_live_url_smoke_consistency_check"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 8 live URL smoke consistency check is optional before deployed live validation review; regenerate it after Phase 8 readiness or handoff bundle changes."
        )
    if any(
        artifact["id"] == "phase9_myprivateagent_local_consumption_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 9 MyPrivateAgent local-consumption readiness is optional before caller local-consumption review; regenerate it after Phase 7/8/handoff evidence updates."
        )
    if any(
        artifact["id"] == "phase9_myprivateagent_local_consumption_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 9 MyPrivateAgent local-consumption smoke is optional before caller local-consumption review; regenerate it after Phase 9 readiness or provider contract evidence changes."
        )
    if any(
        artifact["id"] == "phase10_myprivateagent_local_consumer_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 10 MyPrivateAgent local consumer readiness is optional before caller-shaped local verification; regenerate it after Phase 9, Phase 4, handoff, or provider contract evidence changes."
        )
    if any(
        artifact["id"] == "phase10_myprivateagent_local_consumer_probe"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 10 MyPrivateAgent local consumer probe is optional before MyPrivateAgent repository integration; regenerate it after Phase 10 readiness or handoff bundle evidence changes."
        )
    if any(
        artifact["id"] == "phase11_local_provider_integration_profile"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 11 local provider integration profile is optional before caller-side integration dry-run review; regenerate it after Phase 10 or handoff evidence updates."
        )
    if any(
        artifact["id"] == "phase11_provider_discovery_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 11 provider discovery smoke is optional before caller-side integration dry-run review; regenerate it after profile or provider discovery evidence updates."
        )
    if any(
        artifact["id"] == "phase11_rag_retrieve_consumption_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 11 retrieve-consumption smoke is optional before caller-side integration dry-run review; regenerate it after Phase 4 or provider contract smoke evidence updates."
        )
    if any(
        artifact["id"] == "phase11_source_binding_preview_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 11 source-binding preview smoke is optional before caller-side integration dry-run review; regenerate it after source-binding or Phase 10 readiness evidence updates."
        )
    if any(
        artifact["id"] == "phase12_local_rag_integration_hardening_profile"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 12 local RAG integration hardening profile is optional for local hardening review; regenerate it after provider contract or readiness evidence updates."
        )
    if any(
        artifact["id"] == "phase12b_candidate_backend_evaluation_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 12b candidate backend evaluation readiness is optional before backend candidate review; regenerate it after Phase 3, Phase 6, or local integration evidence changes."
        )
    if any(
        artifact["id"] == "phase12c_pgvector_candidate_backend_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 12c pgvector candidate backend readiness is optional before pgvector spike review; regenerate it after pgvector configuration or candidate evidence changes."
        )
    if any(
        artifact["id"] == "phase12d_pgvector_live_probe_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 12d pgvector live probe readiness is optional before pgvector probe review; regenerate it after PostgreSQL or pgvector runtime posture changes."
        )
    if any(
        artifact["id"] == "phase3_hybrid_cross_case_fp_fn_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 3 hybrid cross-case FP/FN smoke is optional before promotion review; regenerate it after baseline or FP/FN evidence changes."
        )
    if any(
        artifact["id"] == "phase3_aggregation_relation_negative_control_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 3 aggregation/relation negative-control smoke is optional before promotion review; regenerate it after aggregation or relation-aware grading evidence changes."
        )
    if any(
        artifact["id"] == "phase3_hybrid_runtime_promotion_decision_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 3 hybrid runtime promotion decision readiness export is optional before final promotion review; regenerate it after Phase 3 or Phase 6 bridge evidence updates."
        )
    if any(
        artifact["id"] == "phase3_hybrid_runtime_promotion_decision_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 3 hybrid runtime promotion decision smoke is optional before final promotion review; regenerate it after readiness or prerequisite evidence changes."
        )
    if any(
        artifact["id"] == "phase4_evidence_pack_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 4 evidence pack readiness export is optional before caller review; regenerate it after the contract or contract-smoke evidence changes."
        )
    if any(
        artifact["id"] == "phase4_caller_consumption_smoke"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 4 caller-consumption smoke is optional before caller review; regenerate it after the evidence-pack contract or readiness export changes."
        )
    if any(
        artifact["id"] == "phase5_graph_use_case_readiness"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 5 graph use-case readiness export is optional before graph review; regenerate it after the graph contract or graph boundary evidence changes."
        )
    if any(
        artifact["id"] == "phase5_graph_boundary_smoke_summary"
        and not artifact["present"]
        for artifact in artifact_rows
    ):
        notes.append(
            "Phase 5 graph boundary smoke summary is optional before graph review; regenerate it after provider contract smoke changes."
        )
    return notes
