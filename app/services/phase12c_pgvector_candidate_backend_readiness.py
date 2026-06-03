import json
import os
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable


PHASE12C_PGVECTOR_CANDIDATE_BACKEND_READINESS_ID = (
    "phase12c-pgvector-candidate-backend-readiness-v1"
)
OUTPUT_JSON_FILENAME = "phase12c-pgvector-candidate-backend-readiness.json"
OUTPUT_MARKDOWN_FILENAME = "phase12c-pgvector-candidate-backend-readiness.md"
STRATEGY_VERDICT = "continue_provider_first_with_candidate_backends"
PGVECTOR_DATABASE_URL_ENV = "PGVECTOR_DATABASE_URL"
PGVECTOR_SCHEMA_ENV = "PGVECTOR_SCHEMA"
PGVECTOR_TABLE_ENV = "PGVECTOR_TABLE"
PGVECTOR_INDEX_NAME_ENV = "PGVECTOR_INDEX_NAME"
PGVECTOR_VECTOR_SIZE_ENV = "PGVECTOR_VECTOR_SIZE"
PGVECTOR_DEFAULT_SCHEMA = "public"
PGVECTOR_DEFAULT_TABLE = "knowledge_chunks"
PGVECTOR_DEFAULT_INDEX_NAME = "knowledge_chunks_embedding_idx"
PGVECTOR_DEFAULT_VECTOR_SIZE = 1024


@dataclass(frozen=True)
class CandidateBackendSignalSpec:
    id: str
    required: bool
    path: Path | None = None
    missing_action: str = "review_evidence_notes"
    summary_builder: Callable[[dict[str, Any] | None], str] | None = None


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
class Phase12cPgvectorCandidateBackendReadinessReport:
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
        id="pgvector_connection_posture",
        required=True,
        summary_builder=lambda payload: _pgvector_connection_summary(),
    ),
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
        id="phase11_source_binding_preview_smoke",
        required=False,
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
        required=False,
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
        id="phase3_retrieval_promotion_readiness",
        required=False,
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
        required=False,
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
        required=False,
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
        id="phase6_bge_m3_artifact_readiness",
        required=False,
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
        required=False,
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
        required=False,
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
        required=False,
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
        id="phase12b_candidate_backend_evaluation_readiness",
        required=False,
        path=Path(
            "docs/operations/candidate-backend-evaluation-readiness/"
            "phase12b-candidate-backend-evaluation-readiness.json"
        ),
        missing_action="regenerate_phase12b_candidate_backend_evaluation_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"strategy_verdict={_dict_value(payload, 'summary', {}).get('strategy_verdict', 'continue_provider_first_with_candidate_backends')}"
        ),
    ),
]


FAMILY_SPECS: list[CandidateBackendFamilySpec] = [
    CandidateBackendFamilySpec(
        id="pgvector_configuration_gate",
        label="PGVector Configuration Gate",
        required_signal_ids=["pgvector_connection_posture"],
        notes=[
            "This family keeps pgvector evaluation explicit without adding a live PostgreSQL driver probe.",
        ],
    ),
    CandidateBackendFamilySpec(
        id="provider_integration_gate",
        label="Provider Integration Gate",
        required_signal_ids=[
            "phase12_local_rag_integration_hardening_profile",
            "phase11_local_provider_integration_profile",
            "provider_contract_smoke",
            "provider_handoff_bundle",
            "deployment_readiness",
            "reindex_readiness",
        ],
        optional_signal_ids=[
            "phase11_source_binding_preview_smoke",
            "phase11_rag_retrieve_consumption_smoke",
        ],
        notes=[
            "This family keeps the local provider path reviewable while pgvector stays candidate-only.",
        ],
    ),
    CandidateBackendFamilySpec(
        id="candidate_evidence_gate",
        label="Candidate Evidence Gate",
        required_signal_ids=[],
        optional_signal_ids=[
            "phase3_retrieval_promotion_readiness",
            "phase3_candidate_runtime_diagnostics",
            "phase3_candidate_latency_resource_diagnostics",
            "phase3_fp_fn_review",
            "phase6_bge_m3_artifact_readiness",
            "phase6_qdrant_vector_store_readiness",
            "phase6_qdrant_bge_private_network_promotion_readiness",
            "phase6_deployed_field_validation_readiness",
            "phase12b_candidate_backend_evaluation_readiness",
        ],
        notes=[
            "This family keeps the existing benchmark and operations evidence visible for pgvector comparison.",
        ],
    ),
]


def build_phase12c_pgvector_candidate_backend_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase12cPgvectorCandidateBackendReadinessReport:
    signals = [_build_signal(spec, base_dir=base_dir) for spec in SIGNAL_SPECS]
    signal_map = {signal.id: signal for signal in signals}
    families = [_build_family_readout(spec, signal_map) for spec in FAMILY_SPECS]

    required_blocked = any(signal.required and signal.status == "blocked" for signal in signals)
    required_review = any(signal.required and signal.status == "review" for signal in signals)
    open_gate_ids = [signal.id for signal in signals if signal.status in {"review", "blocked"}]
    pgvector_config_state = signal_map["pgvector_connection_posture"].status

    if pgvector_config_state == "blocked":
        status = "blocked"
        evaluation_state = "pgvector_candidate_configuration_blocked"
        decision = "keep_current_default"
    elif required_blocked:
        status = "blocked"
        evaluation_state = "pgvector_candidate_evaluation_blocked"
        decision = "keep_current_default"
    elif required_review:
        status = "review"
        evaluation_state = "ready_for_pgvector_candidate_review"
        decision = "continue_spike"
    else:
        status = "ready"
        evaluation_state = "ready_for_pgvector_candidate_promotion_review"
        decision = "eligible_for_promotion_review"

    review_ready_family_ids = [family.id for family in families if family.status == "review"]
    ready_family_ids = [family.id for family in families if family.status == "ready"]
    blocked_family_ids = [family.id for family in families if family.status == "blocked"]

    return Phase12cPgvectorCandidateBackendReadinessReport(
        id=PHASE12C_PGVECTOR_CANDIDATE_BACKEND_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        evaluation_state=evaluation_state,
        decision=decision,
        summary={
            "strategy_verdict": STRATEGY_VERDICT,
            "candidate_backend_id": "pgvector",
            "candidate_backend_kind": "postgresql_native_vector_search",
            "total_signals": len(signals),
            "required_signals": sum(1 for signal in signals if signal.required),
            "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
            "review_signals": sum(1 for signal in signals if signal.status == "review"),
            "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
            "pgvector_database_url_present": bool(_env_value(PGVECTOR_DATABASE_URL_ENV)),
            "pgvector_schema": _env_value(PGVECTOR_SCHEMA_ENV, PGVECTOR_DEFAULT_SCHEMA),
            "pgvector_table": _env_value(PGVECTOR_TABLE_ENV, PGVECTOR_DEFAULT_TABLE),
            "pgvector_index_name": _env_value(
                PGVECTOR_INDEX_NAME_ENV,
                PGVECTOR_DEFAULT_INDEX_NAME,
            ),
            "pgvector_vector_size": _int_value(
                _env_value(PGVECTOR_VECTOR_SIZE_ENV),
                PGVECTOR_DEFAULT_VECTOR_SIZE,
            ),
            "open_gate_ids": open_gate_ids,
            "review_ready_family_ids": review_ready_family_ids,
            "ready_family_ids": ready_family_ids,
            "blocked_family_ids": blocked_family_ids,
        },
        signals=signals,
        candidate_families=families,
        notes=[
            "Phase 12c is read-only and keeps runtime defaults unchanged.",
            "The pgvector candidate is configuration-driven and intentionally does not add a PostgreSQL driver dependency.",
            "pgvector remains candidate-only until a separate promotion change closes the required gates.",
        ],
    )


def phase12c_pgvector_candidate_backend_readiness_report_to_dict(
    report: Phase12cPgvectorCandidateBackendReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase12c_pgvector_candidate_backend_readiness_markdown(
    report: Phase12cPgvectorCandidateBackendReadinessReport,
) -> str:
    lines = [
        "# Phase 12c PGVector Candidate Backend Readiness",
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


def export_phase12c_pgvector_candidate_backend_readiness_report(
    output_dir: Path = Path("docs/operations/pgvector-candidate-backend-readiness"),
    *,
    base_dir: Path = Path("."),
) -> Phase12cPgvectorCandidateBackendReadinessReport:
    report = build_phase12c_pgvector_candidate_backend_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = Phase12cPgvectorCandidateBackendReadinessReport(
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
            phase12c_pgvector_candidate_backend_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase12c_pgvector_candidate_backend_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_signal(
    spec: CandidateBackendSignalSpec,
    *,
    base_dir: Path,
) -> CandidateBackendSignal:
    payload = _read_json_if_present(base_dir / spec.path) if spec.path is not None else None
    if payload is None and spec.path is not None:
        return _missing_signal(
            id=spec.id,
            path=spec.path,
            action=spec.missing_action,
            required=spec.required,
        )
    if spec.path is None:
        return _pgvector_connection_signal()
    assert spec.summary_builder is not None
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
    required_signals = [signal_map[signal_id] for signal_id in spec.required_signal_ids if signal_id in signal_map]
    optional_signals = [signal_map[signal_id] for signal_id in spec.optional_signal_ids if signal_id in signal_map]
    evidence_paths = [signal.evidence_path for signal in required_signals + optional_signals if signal.evidence_path]

    if any(signal.status == "blocked" for signal in required_signals):
        status = "blocked"
    elif any(signal.status in {"review", "blocked"} for signal in required_signals + optional_signals):
        status = "review"
    else:
        status = "ready"

    decision = _decision_for_status(status)
    summary = (
        f"required={_jsonish_list(spec.required_signal_ids)}; "
        f"optional={_jsonish_list(spec.optional_signal_ids)}; "
        f"ready={_int_value(sum(1 for signal in required_signals + optional_signals if signal.status == 'ready'), 0)}; "
        f"review={_int_value(sum(1 for signal in required_signals + optional_signals if signal.status == 'review'), 0)}; "
        f"blocked={_int_value(sum(1 for signal in required_signals + optional_signals if signal.status == 'blocked'), 0)}"
    )
    return CandidateBackendFamilyReadout(
        id=spec.id,
        label=spec.label,
        status=status,
        decision=decision,
        summary=summary,
        required_signal_ids=list(spec.required_signal_ids),
        optional_signal_ids=list(spec.optional_signal_ids),
        evidence_paths=evidence_paths,
        notes=list(spec.notes),
    )


def _missing_signal(*, id: str, path: Path, action: str, required: bool) -> CandidateBackendSignal:
    summary = f"status=missing; path={path.as_posix()}; missing"
    return CandidateBackendSignal(
        id=id,
        required=required,
        status="blocked" if required else "review",
        summary=summary,
        recommended_action=action,
        evidence_path=str(path),
    )


def _decision_for_status(status: str) -> str:
    if status == "blocked":
        return "keep_current_default"
    if status == "review":
        return "continue_spike"
    return "eligible_for_promotion_review"


def _pgvector_connection_signal() -> CandidateBackendSignal:
    summary = _pgvector_connection_summary()
    status = "ready" if summary.startswith("status=ready") else "blocked"
    return CandidateBackendSignal(
        id="pgvector_connection_posture",
        required=True,
        status=status,
        summary=summary,
        recommended_action="no_action_required" if status == "ready" else "configure_pgvector_database_url",
        evidence_path=_pgvector_connection_evidence_path(),
    )


def _pgvector_connection_summary() -> str:
    database_url = _env_value(PGVECTOR_DATABASE_URL_ENV)
    schema = _env_value(PGVECTOR_SCHEMA_ENV, PGVECTOR_DEFAULT_SCHEMA)
    table = _env_value(PGVECTOR_TABLE_ENV, PGVECTOR_DEFAULT_TABLE)
    index_name = _env_value(PGVECTOR_INDEX_NAME_ENV, PGVECTOR_DEFAULT_INDEX_NAME)
    vector_size = _int_value(_env_value(PGVECTOR_VECTOR_SIZE_ENV), PGVECTOR_DEFAULT_VECTOR_SIZE)
    if not database_url:
        return (
            "status=blocked; connection_mode=not_configured_local_dev; "
            f"database_url_present={False}; schema={schema}; table={table}; "
            f"index_name={index_name}; vector_size={vector_size}; "
            "driver_dependency=absent; next_step=configure_pgvector_database_url"
        )
    return (
        "status=ready; connection_mode=configured_without_live_probe; "
        f"database_url_present={True}; schema={schema}; table={table}; "
        f"index_name={index_name}; vector_size={vector_size}; "
        "driver_dependency=absent; next_step=review_candidate_evidence"
    )


def _pgvector_connection_evidence_path() -> str:
    return (
        "environment:"
        f"{PGVECTOR_DATABASE_URL_ENV},"
        f"{PGVECTOR_SCHEMA_ENV},"
        f"{PGVECTOR_TABLE_ENV},"
        f"{PGVECTOR_INDEX_NAME_ENV},"
        f"{PGVECTOR_VECTOR_SIZE_ENV}"
    )


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_status(value: Any) -> str:
    if isinstance(value, str) and value in {"ready", "review", "blocked"}:
        return value
    return "review"


def _jsonish_list(values: list[Any]) -> str:
    return json.dumps(values, ensure_ascii=False)


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)


def _int_value(value: Any, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    if isinstance(value, str):
        try:
            parsed = int(value)
        except ValueError:
            return fallback
        return parsed if parsed >= 0 else fallback
    return fallback


def _boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return False


def _env_value(name: str, fallback: str = "") -> str:
    value = os.environ.get(name, "")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback
