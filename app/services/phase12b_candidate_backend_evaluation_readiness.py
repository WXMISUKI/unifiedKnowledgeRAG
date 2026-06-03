import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable


PHASE12B_CANDIDATE_BACKEND_EVALUATION_READINESS_ID = (
    "phase12b-candidate-backend-evaluation-readiness-v1"
)
OUTPUT_JSON_FILENAME = "phase12b-candidate-backend-evaluation-readiness.json"
OUTPUT_MARKDOWN_FILENAME = "phase12b-candidate-backend-evaluation-readiness.md"
LOCAL_PROVIDER_URL_DEFAULT = "http://127.0.0.1:8020"
STRATEGY_VERDICT = "continue_provider_first_with_candidate_backends"
REFERENCE_ONLY_CANDIDATES = ["Haystack", "RAGFlow", "LightRAG", "pgvector"]


@dataclass(frozen=True)
class CandidateBackendSignalSpec:
    id: str
    required: bool
    path: Path
    missing_action: str
    summary_builder: Callable[[dict[str, Any]], str]


@dataclass(frozen=True)
class CandidateBackendSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class CandidateBackendFamilySpec:
    id: str
    label: str
    required_signal_ids: list[str]
    optional_signal_ids: list[str] = field(default_factory=list)
    reference_only: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CandidateBackendFamilyReadout:
    id: str
    label: str
    status: str
    decision: str
    summary: str
    required_signal_ids: list[str]
    optional_signal_ids: list[str]
    evidence_paths: list[str]
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Phase12bCandidateBackendEvaluationReadinessReport:
    id: str
    generated_at: str
    status: str
    evaluation_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[CandidateBackendSignal]
    candidate_families: list[CandidateBackendFamilyReadout]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


SIGNAL_SPECS: list[CandidateBackendSignalSpec] = [
    CandidateBackendSignalSpec(
        id="phase12_local_rag_integration_hardening_profile",
        required=True,
        path=Path(
            "docs/integration/myprivateagent-local-rag-integration-hardening/"
            "phase12-local-rag-integration-hardening-profile.json"
        ),
        missing_action="regenerate_phase12_local_rag_integration_hardening_profile",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"hardening_state={payload.get('hardening_state', 'review')}; "
            f"open_gates={_jsonish_list(_dict_value(payload, 'summary', {}).get('open_gate_ids', []))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase11_local_provider_integration_profile",
        required=True,
        path=Path(
            "docs/integration/myprivateagent-local-provider-integration/"
            "phase11-local-provider-integration-profile.json"
        ),
        missing_action="regenerate_phase11_local_provider_integration_profile",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"integration_state={payload.get('integration_state', 'review')}; "
            f"open_gates={_jsonish_list(_dict_value(payload, 'summary', {}).get('open_gate_ids', []))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="provider_contract_smoke",
        required=True,
        path=Path("docs/smoke/provider-contract/provider-contract-smoke.json"),
        missing_action="regenerate_provider_contract_smoke",
        summary_builder=lambda payload: (
            f"passed={_boolish(payload.get('passed', _dict_value(payload, 'summary', {}).get('passed', False)))}; "
            f"checks={_int_value(_dict_value(payload, 'summary', {}).get('passed', 0), 0)}/"
            f"{_int_value(_dict_value(payload, 'summary', {}).get('total', 0), 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="provider_handoff_bundle",
        required=True,
        path=Path("docs/integration/provider-handoff/provider-handoff-bundle.json"),
        missing_action="regenerate_provider_handoff_bundle",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"evidence_artifacts={_int_value(payload.get('evidence_artifacts', 0), 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase11_source_binding_preview_smoke",
        required=True,
        path=Path(
            "docs/smoke/myprivateagent-local-provider-integration/"
            "phase11-source-binding-preview-smoke.json"
        ),
        missing_action="regenerate_phase11_source_binding_preview_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"passed_checks={_int_value(_dict_value(payload, 'summary', {}).get('passed_checks', 0), 0)}/"
            f"{_int_value(_dict_value(payload, 'summary', {}).get('total_checks', 0), 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase11_rag_retrieve_consumption_smoke",
        required=True,
        path=Path(
            "docs/smoke/myprivateagent-local-provider-integration/"
            "phase11-rag-retrieve-consumption-smoke.json"
        ),
        missing_action="regenerate_phase11_rag_retrieve_consumption_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"passed_checks={_int_value(_dict_value(payload, 'summary', {}).get('passed_checks', 0), 0)}/"
            f"{_int_value(_dict_value(payload, 'summary', {}).get('total_checks', 0), 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="deployment_readiness",
        required=True,
        path=Path("docs/operations/deployment-readiness/deployment-readiness.json"),
        missing_action="regenerate_deployment_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"backend={_dict_value(payload, 'runtime_config', {}).get('rag_retrieval_backend', 'unknown')}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="reindex_readiness",
        required=True,
        path=Path("docs/operations/reindex-readiness/reindex-readiness.json"),
        missing_action="regenerate_reindex_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"backend={payload.get('retrieval_backend', 'unknown')}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase3_retrieval_promotion_readiness",
        required=True,
        path=Path(
            "docs/benchmark/chinese-seed/retrieval-promotion-readiness/"
            "phase3-retrieval-promotion-readiness.json"
        ),
        missing_action="regenerate_phase3_retrieval_promotion_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"decision={_dict_value(payload, 'summary', {}).get('decision', payload.get('decision', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase3_candidate_runtime_diagnostics",
        required=True,
        path=Path(
            "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/"
            "phase3-candidate-runtime-diagnostics.json"
        ),
        missing_action="regenerate_phase3_candidate_runtime_diagnostics",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"decision={_dict_value(payload, 'summary', {}).get('decision', payload.get('decision', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase3_candidate_latency_resource_diagnostics",
        required=True,
        path=Path(
            "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/"
            "phase3-candidate-latency-resource-diagnostics.json"
        ),
        missing_action="regenerate_phase3_candidate_latency_resource_diagnostics",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"avg_latency_ms={_dict_value(payload, 'summary', {}).get('avg_latency_ms', 'unknown')}; "
            f"decision={_dict_value(payload, 'summary', {}).get('decision', payload.get('decision', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_bge_m3_artifact_readiness",
        required=True,
        path=Path(
            "docs/operations/bge-m3-artifact-readiness/"
            "phase6-bge-m3-artifact-readiness.json"
        ),
        missing_action="regenerate_phase6_bge_m3_artifact_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"artifact_state={_dict_value(payload, 'summary', {}).get('artifact_state', payload.get('artifact_state', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_qdrant_vector_store_readiness",
        required=True,
        path=Path(
            "docs/operations/qdrant-vector-store-readiness/"
            "phase6-qdrant-vector-store-readiness.json"
        ),
        missing_action="regenerate_phase6_qdrant_vector_store_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"decision={_dict_value(payload, 'summary', {}).get('decision', payload.get('decision', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_qdrant_bge_private_network_promotion_readiness",
        required=True,
        path=Path(
            "docs/operations/private-network-promotion/"
            "phase6-qdrant-bge-private-network-promotion-readiness.json"
        ),
        missing_action="regenerate_phase6_qdrant_bge_private_network_promotion_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"decision={_dict_value(payload, 'summary', {}).get('decision', payload.get('decision', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_deployed_field_validation_readiness",
        required=True,
        path=Path(
            "docs/operations/deployed-field-validation/"
            "phase6-deployed-field-validation-readiness.json"
        ),
        missing_action="regenerate_phase6_deployed_field_validation_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"decision={_dict_value(payload, 'summary', {}).get('decision', payload.get('decision', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase3_fp_fn_review",
        required=False,
        path=Path("docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json"),
        missing_action="regenerate_phase3_fp_fn_review",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"false_positive_count={_dict_value(payload, 'summary', {}).get('false_positive_count', 0)}; "
            f"false_negative_count={_dict_value(payload, 'summary', {}).get('false_negative_count', 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase3_hybrid_cross_case_fp_fn_smoke",
        required=False,
        path=Path("docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.json"),
        missing_action="regenerate_phase3_hybrid_cross_case_fp_fn_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"false_positive_count={_dict_value(payload, 'summary', {}).get('false_positive_count', 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase3_aggregation_relation_negative_control_smoke",
        required=False,
        path=Path(
            "docs/smoke/aggregation-relation-negative-control/"
            "phase3-aggregation-relation-negative-control-smoke.json"
        ),
        missing_action="regenerate_phase3_aggregation_relation_negative_control_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"relation_unsupported_count={_dict_value(payload, 'summary', {}).get('relation_unsupported_count', 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase3_hybrid_runtime_promotion_decision_readiness",
        required=False,
        path=Path(
            "docs/benchmark/chinese-seed/hybrid-runtime-promotion/"
            "phase3-hybrid-runtime-promotion-decision-readiness.json"
        ),
        missing_action="regenerate_phase3_hybrid_runtime_promotion_decision_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"decision={_dict_value(payload, 'summary', {}).get('decision', payload.get('decision', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase3_hybrid_runtime_promotion_decision_smoke",
        required=False,
        path=Path(
            "docs/smoke/hybrid-runtime-promotion/"
            "phase3-hybrid-runtime-promotion-decision-smoke.json"
        ),
        missing_action="regenerate_phase3_hybrid_runtime_promotion_decision_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"passed_checks={_dict_value(payload, 'summary', {}).get('passed_checks', 0)}/"
            f"{_dict_value(payload, 'summary', {}).get('total_checks', 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_bge_m3_vs_mock_fixture_diagnostics",
        required=False,
        path=Path(
            "docs/operations/bge-m3-comparison-readiness/"
            "phase6-bge-m3-vs-mock-fixture-diagnostics.json"
        ),
        missing_action="regenerate_phase6_bge_m3_vs_mock_fixture_diagnostics",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"decision={_dict_value(payload, 'summary', {}).get('decision', payload.get('decision', 'review'))}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_bge_m3_comparison_smoke",
        required=False,
        path=Path("docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json"),
        missing_action="regenerate_phase6_bge_m3_comparison_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"passed_checks={_dict_value(payload, 'summary', {}).get('passed_checks', 0)}/"
            f"{_dict_value(payload, 'summary', {}).get('total_checks', 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_qdrant_backup_restore_smoke",
        required=False,
        path=Path("docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json"),
        missing_action="regenerate_phase6_qdrant_backup_restore_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"passed_checks={_dict_value(payload, 'summary', {}).get('passed_checks', 0)}/"
            f"{_dict_value(payload, 'summary', {}).get('total_checks', 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_qdrant_bge_private_network_promotion_smoke",
        required=False,
        path=Path(
            "docs/smoke/private-network-promotion/"
            "phase6-qdrant-bge-private-network-promotion-smoke.json"
        ),
        missing_action="regenerate_phase6_qdrant_bge_private_network_promotion_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"passed_checks={_dict_value(payload, 'summary', {}).get('passed_checks', 0)}/"
            f"{_dict_value(payload, 'summary', {}).get('total_checks', 0)}"
        ),
    ),
    CandidateBackendSignalSpec(
        id="phase6_deployed_handoff_consistency_smoke",
        required=False,
        path=Path(
            "docs/smoke/deployed-field-validation/"
            "phase6-deployed-handoff-consistency-smoke.json"
        ),
        missing_action="regenerate_phase6_deployed_handoff_consistency_smoke",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"passed_checks={_dict_value(payload, 'summary', {}).get('passed_checks', 0)}/"
            f"{_dict_value(payload, 'summary', {}).get('total_checks', 0)}"
        ),
    ),
]


FAMILY_SPECS: list[CandidateBackendFamilySpec] = [
    CandidateBackendFamilySpec(
        id="local_provider_integration_gate",
        label="Local Provider Integration Gate",
        required_signal_ids=[
            "phase12_local_rag_integration_hardening_profile",
            "phase11_local_provider_integration_profile",
            "provider_contract_smoke",
            "provider_handoff_bundle",
            "phase11_source_binding_preview_smoke",
            "phase11_rag_retrieve_consumption_smoke",
        ],
        optional_signal_ids=["deployment_readiness", "reindex_readiness"],
        notes=[
            "This family keeps the current provider contract and local integration path reviewable.",
        ],
    ),
    CandidateBackendFamilySpec(
        id="retrieval_quality_candidates",
        label="Retrieval Quality Candidates",
        required_signal_ids=[
            "phase3_retrieval_promotion_readiness",
            "phase3_candidate_runtime_diagnostics",
            "phase3_candidate_latency_resource_diagnostics",
            "phase3_hybrid_runtime_promotion_decision_readiness",
        ],
        optional_signal_ids=[
            "phase3_fp_fn_review",
            "phase3_hybrid_cross_case_fp_fn_smoke",
            "phase3_aggregation_relation_negative_control_smoke",
            "phase3_hybrid_runtime_promotion_decision_smoke",
        ],
        notes=[
            "These are the current evidence-backed quality gates for hybrid and retrieval promotion review.",
        ],
    ),
    CandidateBackendFamilySpec(
        id="storage_and_private_network_candidates",
        label="Storage and Private-Network Candidates",
        required_signal_ids=[
            "phase6_bge_m3_artifact_readiness",
            "phase6_qdrant_vector_store_readiness",
            "phase6_qdrant_bge_private_network_promotion_readiness",
            "phase6_deployed_field_validation_readiness",
        ],
        optional_signal_ids=[
            "phase6_bge_m3_vs_mock_fixture_diagnostics",
            "phase6_bge_m3_comparison_smoke",
            "phase6_qdrant_backup_restore_smoke",
            "phase6_qdrant_bge_private_network_promotion_smoke",
            "phase6_deployed_handoff_consistency_smoke",
        ],
        notes=[
            "These gates keep Qdrant/BGE-M3 and private-network promotion review evidence explicit.",
        ],
    ),
    CandidateBackendFamilySpec(
        id="deployment_and_ops_candidates",
        label="Deployment and Operations",
        required_signal_ids=["deployment_readiness", "reindex_readiness"],
        optional_signal_ids=["phase6_deployed_field_validation_readiness", "phase6_deployed_handoff_consistency_smoke"],
        notes=[
            "This family keeps deployment and reindex posture visible without changing runtime defaults.",
        ],
    ),
    CandidateBackendFamilySpec(
        id="reference_only_candidates",
        label="Reference-Only Open-Source Engines",
        required_signal_ids=[],
        optional_signal_ids=[],
        reference_only=True,
        notes=[
            "Haystack, RAGFlow, LightRAG, and pgvector remain comparison references until a separate spike adds local candidate evidence.",
        ],
    ),
]


def build_phase12b_candidate_backend_evaluation_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase12bCandidateBackendEvaluationReadinessReport:
    signals = [_build_signal(spec, base_dir=base_dir) for spec in SIGNAL_SPECS]
    signal_map = {signal.id: signal for signal in signals}
    families = [_build_family_readout(spec, signal_map) for spec in FAMILY_SPECS]
    reference_only_family_ids = [spec.id for spec in FAMILY_SPECS if spec.reference_only]

    required_blocked = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    required_review = any(
        signal.required and signal.status == "review" for signal in signals
    )
    open_gate_ids = [signal.id for signal in signals if signal.status in {"review", "blocked"}]
    review_ready_family_ids = [
        family.id for family in families if family.status == "review" and family.id not in reference_only_family_ids
    ]
    ready_family_ids = [family.id for family in families if family.status == "ready"]
    blocked_family_ids = [family.id for family in families if family.status == "blocked"]
    reference_only_family_ids = [
        family.id for family in families if family.id in reference_only_family_ids
    ]

    local_provider_url = _read_local_provider_url(base_dir)
    api_key_mode = _read_api_key_mode(base_dir)

    if required_blocked:
        status = "blocked"
        evaluation_state = "candidate_backend_evaluation_blocked"
        decision = "keep_current_default"
    elif required_review:
        status = "review"
        evaluation_state = "ready_for_candidate_backend_evaluation_review"
        decision = "continue_spike"
    else:
        status = "ready"
        evaluation_state = "ready_for_candidate_backend_evaluation_review"
        decision = "eligible_for_promotion_review"

    return Phase12bCandidateBackendEvaluationReadinessReport(
        id=PHASE12B_CANDIDATE_BACKEND_EVALUATION_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        evaluation_state=evaluation_state,
        decision=decision,
        summary={
            "strategy_verdict": STRATEGY_VERDICT,
            "total_signals": len(signals),
            "required_signals": sum(1 for signal in signals if signal.required),
            "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
            "review_signals": sum(1 for signal in signals if signal.status == "review"),
            "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
            "local_provider_url": local_provider_url,
            "api_key_mode": api_key_mode,
            "open_gate_ids": open_gate_ids,
            "review_ready_family_ids": review_ready_family_ids,
            "ready_family_ids": ready_family_ids,
            "blocked_family_ids": blocked_family_ids,
            "reference_only_family_ids": reference_only_family_ids,
            "reference_only_candidates": REFERENCE_ONLY_CANDIDATES,
        },
        signals=signals,
        candidate_families=families,
        notes=[
            "Phase 12b is read-only and keeps runtime defaults unchanged.",
            "Candidate backend families are review artifacts, not automatic promotion approval.",
            "Haystack, RAGFlow, LightRAG, and pgvector remain reference-only until separate evidence-backed spikes are approved.",
        ],
    )


def phase12b_candidate_backend_evaluation_readiness_report_to_dict(
    report: Phase12bCandidateBackendEvaluationReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase12b_candidate_backend_evaluation_readiness_markdown(
    report: Phase12bCandidateBackendEvaluationReadinessReport,
) -> str:
    lines = [
        "# Phase 12b Candidate Backend Evaluation Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Evaluation State: `{report.evaluation_state}`",
        f"- Decision: `{report.decision}`",
        f"- Strategy Verdict: `{STRATEGY_VERDICT}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        lines.append(f"| {key} | `{rendered}` |")

    lines.extend(
        [
            "",
            "## Candidate Families",
            "",
            "| Family | Status | Decision | Evidence Paths | Notes |",
            "|---|---|---|---|---|",
        ]
    )
    for family in report.candidate_families:
        evidence_paths = _jsonish_list(family.evidence_paths)
        notes = _jsonish_list(family.notes)
        lines.append(
            f"| `{family.label}` | `{family.status}` | `{family.decision}` | {evidence_paths} | {notes} |"
        )

    lines.extend(
        [
            "",
            "## Signals",
            "",
            "| Signal | Required | Status | Summary | Recommended Action |",
            "|---|---|---|---|---|",
        ]
    )
    for signal in report.signals:
        lines.append(
            f"| `{signal.id}` | `{signal.required}` | `{signal.status}` | "
            f"{signal.summary} | `{signal.recommended_action}` |"
        )

    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase12b_candidate_backend_evaluation_readiness_report(
    output_dir: Path = Path("docs/operations/candidate-backend-evaluation-readiness"),
    *,
    base_dir: Path = Path("."),
) -> Phase12bCandidateBackendEvaluationReadinessReport:
    report = build_phase12b_candidate_backend_evaluation_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = Phase12bCandidateBackendEvaluationReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        evaluation_state=report.evaluation_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        candidate_families=report.candidate_families,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase12b_candidate_backend_evaluation_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase12b_candidate_backend_evaluation_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_signal(
    spec: CandidateBackendSignalSpec,
    *,
    base_dir: Path,
) -> CandidateBackendSignal:
    payload = _read_json_if_present(base_dir / spec.path)
    if payload is None:
        return _missing_signal(
            id=spec.id,
            path=spec.path,
            action=spec.missing_action,
            required=spec.required,
        )
    status = _normalize_status(payload.get("status"))
    return CandidateBackendSignal(
        id=spec.id,
        required=spec.required,
        status=status,
        summary=spec.summary_builder(payload),
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(spec.path),
    )


def _build_family_readout(
    spec: CandidateBackendFamilySpec,
    signal_map: dict[str, CandidateBackendSignal],
) -> CandidateBackendFamilyReadout:
    if spec.reference_only:
        return CandidateBackendFamilyReadout(
            id=spec.id,
            label=spec.label,
            status="reference_only",
            decision="reference_only",
            summary="reference-only candidate engines remain comparison references only",
            required_signal_ids=[],
            optional_signal_ids=[],
            evidence_paths=[],
            notes=spec.notes,
        )

    required_signals = [signal_map[signal_id] for signal_id in spec.required_signal_ids]
    optional_signals = [signal_map[signal_id] for signal_id in spec.optional_signal_ids]
    signal_statuses = [signal.status for signal in required_signals]
    optional_statuses = [signal.status for signal in optional_signals]

    if any(status == "blocked" for status in signal_statuses):
        status = "blocked"
        decision = "keep_current_default"
    elif any(status == "review" for status in signal_statuses):
        status = "review"
        decision = "continue_spike"
    else:
        status = "ready"
        decision = "eligible_for_promotion_review"

    evidence_paths = [
        signal.evidence_path for signal in required_signals + optional_signals
    ]
    summary = (
        f"required_ready={signal_statuses.count('ready')}/{len(required_signals)}; "
        f"required_review={signal_statuses.count('review')}; "
        f"required_blocked={signal_statuses.count('blocked')}; "
        f"optional_review={optional_statuses.count('review')}; "
        f"optional_blocked={optional_statuses.count('blocked')}"
    )
    return CandidateBackendFamilyReadout(
        id=spec.id,
        label=spec.label,
        status=status,
        decision=decision,
        summary=summary,
        required_signal_ids=spec.required_signal_ids,
        optional_signal_ids=spec.optional_signal_ids,
        evidence_paths=evidence_paths,
        notes=spec.notes,
    )


def _read_local_provider_url(base_dir: Path) -> str:
    payload = _read_json_if_present(
        base_dir
        / Path(
            "docs/integration/myprivateagent-local-consumer-verification/"
            "phase10-myprivateagent-local-consumer-readiness.json"
        )
    )
    if payload is None:
        return LOCAL_PROVIDER_URL_DEFAULT
    summary = _dict_value(payload, "summary", {})
    return str(summary.get("local_provider_url", LOCAL_PROVIDER_URL_DEFAULT))


def _read_api_key_mode(base_dir: Path) -> str:
    payload = _read_json_if_present(
        base_dir
        / Path(
            "docs/integration/myprivateagent-local-consumer-verification/"
            "phase10-myprivateagent-local-consumer-readiness.json"
        )
    )
    if payload is None:
        return "not_configured_local_dev"
    summary = _dict_value(payload, "summary", {})
    return str(summary.get("api_key_mode", "not_configured_local_dev"))


def _missing_signal(
    *,
    id: str,
    path: Path,
    action: str,
    required: bool,
) -> CandidateBackendSignal:
    return CandidateBackendSignal(
        id=id,
        required=required,
        status="blocked" if required else "review",
        summary=f"missing={path.as_posix()}",
        recommended_action=action,
        evidence_path=str(path),
    )


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _dict_value(payload: Any, key: str, default: Any) -> Any:
    if isinstance(payload, dict):
        return payload.get(key, default)
    return default


def _normalize_status(value: Any) -> str:
    if value == "ready":
        return "ready"
    if value == "blocked":
        return "blocked"
    if value == "review":
        return "review"
    return "review"


def _boolish(value: Any) -> str:
    return "true" if bool(value) else "false"


def _int_value(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _jsonish_list(values: list[Any]) -> str:
    return json.dumps(values, ensure_ascii=False)
