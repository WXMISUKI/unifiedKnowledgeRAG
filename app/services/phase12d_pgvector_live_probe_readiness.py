import json
import os
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from importlib import import_module
from pathlib import Path
from typing import Any, Callable


PHASE12D_PGVECTOR_LIVE_PROBE_READINESS_ID = "phase12d-pgvector-live-probe-readiness-v1"
OUTPUT_JSON_FILENAME = "phase12d-pgvector-live-probe-readiness.json"
OUTPUT_MARKDOWN_FILENAME = "phase12d-pgvector-live-probe-readiness.md"
STRATEGY_VERDICT = "continue_provider_first_with_candidate_backends"
PGVECTOR_DATABASE_URL_ENV = "PGVECTOR_DATABASE_URL"
PGVECTOR_SCHEMA_ENV = "PGVECTOR_SCHEMA"
PGVECTOR_TABLE_ENV = "PGVECTOR_TABLE"
PGVECTOR_INDEX_NAME_ENV = "PGVECTOR_INDEX_NAME"
PGVECTOR_VECTOR_SIZE_ENV = "PGVECTOR_VECTOR_SIZE"
PGVECTOR_PROBE_TIMEOUT_SECONDS_ENV = "PGVECTOR_PROBE_TIMEOUT_SECONDS"
PGVECTOR_DEFAULT_SCHEMA = "public"
PGVECTOR_DEFAULT_TABLE = "knowledge_chunks"
PGVECTOR_DEFAULT_INDEX_NAME = "knowledge_chunks_embedding_idx"
PGVECTOR_DEFAULT_VECTOR_SIZE = 1024
PGVECTOR_DEFAULT_PROBE_TIMEOUT_SECONDS = 5
PGVECTOR_DRIVER_MODULE = "psycopg"


@dataclass(frozen=True)
class LiveProbeSignalSpec:
    id: str
    required: bool
    path: Path | None = None
    missing_action: str = "review_evidence_notes"
    summary_builder: Callable[[dict[str, Any] | None], str] | None = None


@dataclass(frozen=True)
class LiveProbeSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class LiveProbeFamilySpec:
    id: str
    label: str
    required_signal_ids: list[str]
    optional_signal_ids: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LiveProbeFamilyReadout:
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
class Phase12dPgvectorLiveProbeReadinessReport:
    id: str
    generated_at: str
    status: str
    evaluation_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[LiveProbeSignal]
    candidate_families: list[LiveProbeFamilyReadout]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


SIGNAL_SPECS: list[LiveProbeSignalSpec] = [
    LiveProbeSignalSpec(
        id="pgvector_configuration",
        required=True,
        summary_builder=lambda payload: _configuration_summary(payload),
    ),
    LiveProbeSignalSpec(
        id="pgvector_driver",
        required=True,
        summary_builder=lambda payload: _driver_summary(payload),
    ),
    LiveProbeSignalSpec(
        id="pgvector_connection",
        required=True,
        summary_builder=lambda payload: _connection_summary(payload),
    ),
    LiveProbeSignalSpec(
        id="pgvector_extension",
        required=True,
        summary_builder=lambda payload: _extension_summary(payload),
    ),
    LiveProbeSignalSpec(
        id="pgvector_schema",
        required=True,
        summary_builder=lambda payload: _schema_summary(payload),
    ),
    LiveProbeSignalSpec(
        id="pgvector_table",
        required=True,
        summary_builder=lambda payload: _table_summary(payload),
    ),
    LiveProbeSignalSpec(
        id="pgvector_index",
        required=True,
        summary_builder=lambda payload: _index_summary(payload),
    ),
    LiveProbeSignalSpec(
        id="phase12c_pgvector_candidate_backend_readiness",
        required=False,
        path=Path(
            "docs/operations/pgvector-candidate-backend-readiness/"
            "phase12c-pgvector-candidate-backend-readiness.json"
        ),
        missing_action="regenerate_phase12c_pgvector_candidate_backend_readiness",
        summary_builder=lambda payload: (
            f"status={_normalize_status(payload.get('status'))}; "
            f"evaluation_state={payload.get('evaluation_state', 'review')}; "
            f"decision={payload.get('decision', 'continue_spike')}"
        ),
    ),
    LiveProbeSignalSpec(
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


FAMILY_SPECS: list[LiveProbeFamilySpec] = [
    LiveProbeFamilySpec(
        id="pgvector_probe_gate",
        label="PGVector Probe Gate",
        required_signal_ids=[
            "pgvector_configuration",
            "pgvector_driver",
            "pgvector_connection",
        ],
        notes=[
            "This family keeps the live pgvector probe explicit while avoiding runtime promotion.",
        ],
    ),
    LiveProbeFamilySpec(
        id="pgvector_runtime_gate",
        label="PGVector Runtime Gate",
        required_signal_ids=[
            "pgvector_extension",
            "pgvector_schema",
            "pgvector_table",
            "pgvector_index",
        ],
        notes=[
            "This family checks the minimum runtime posture needed for a realistic pgvector candidate review.",
        ],
    ),
    LiveProbeFamilySpec(
        id="candidate_evidence_bridge_gate",
        label="Candidate Evidence Bridge Gate",
        required_signal_ids=[],
        optional_signal_ids=[
            "phase12c_pgvector_candidate_backend_readiness",
            "phase12b_candidate_backend_evaluation_readiness",
        ],
        notes=[
            "This family keeps the earlier candidate evidence visible next to the live probe.",
        ],
    ),
]


def build_phase12d_pgvector_live_probe_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase12dPgvectorLiveProbeReadinessReport:
    probe_result = _run_pgvector_live_probe()
    signals = [_build_signal(spec, probe_result, base_dir=base_dir) for spec in SIGNAL_SPECS]
    signal_map = {signal.id: signal for signal in signals}
    families = [_build_family_readout(spec, signal_map) for spec in FAMILY_SPECS]

    required_blocked = any(signal.required and signal.status == "blocked" for signal in signals)
    required_review = any(signal.required and signal.status == "review" for signal in signals)
    open_gate_ids = [signal.id for signal in signals if signal.status in {"review", "blocked"}]
    review_ready_family_ids = [family.id for family in families if family.status == "review"]
    ready_family_ids = [family.id for family in families if family.status == "ready"]
    blocked_family_ids = [family.id for family in families if family.status == "blocked"]

    if required_blocked:
        status = "blocked"
        evaluation_state = probe_result.get("evaluation_state", "pgvector_probe_blocked")
        decision = "keep_current_default"
    elif required_review:
        status = "review"
        evaluation_state = "ready_for_pgvector_probe_follow_up"
        decision = "continue_spike"
    else:
        status = "ready" if not review_ready_family_ids else "review"
        evaluation_state = "ready_for_pgvector_candidate_promotion_review"
        decision = "eligible_for_promotion_review" if status == "ready" else "continue_spike"

    return Phase12dPgvectorLiveProbeReadinessReport(
        id=PHASE12D_PGVECTOR_LIVE_PROBE_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        evaluation_state=evaluation_state,
        decision=decision,
        summary={
            "strategy_verdict": STRATEGY_VERDICT,
            "candidate_backend_id": "pgvector",
            "candidate_backend_kind": "postgresql_native_vector_search_live_probe",
            "probe_mode": probe_result.get("probe_mode", "optional_psycopg_live_probe"),
            "pgvector_database_url_present": probe_result.get("database_url_present", False),
            "pgvector_driver_available": probe_result.get("driver_available", False),
            "pgvector_connection_attempted": probe_result.get("connection_attempted", False),
            "pgvector_connection_status": probe_result.get("connection_status", "blocked"),
            "pgvector_extension_installed": probe_result.get("extension_installed", False),
            "pgvector_schema_exists": probe_result.get("schema_exists", False),
            "pgvector_table_exists": probe_result.get("table_exists", False),
            "pgvector_index_exists": probe_result.get("index_exists", False),
            "pgvector_server_version": probe_result.get("server_version", "unknown"),
            "pgvector_schema": probe_result.get("schema", PGVECTOR_DEFAULT_SCHEMA),
            "pgvector_table": probe_result.get("table", PGVECTOR_DEFAULT_TABLE),
            "pgvector_index_name": probe_result.get("index_name", PGVECTOR_DEFAULT_INDEX_NAME),
            "pgvector_vector_size": probe_result.get("vector_size", PGVECTOR_DEFAULT_VECTOR_SIZE),
            "probe_timeout_seconds": probe_result.get(
                "probe_timeout_seconds",
                PGVECTOR_DEFAULT_PROBE_TIMEOUT_SECONDS,
            ),
            "open_gate_ids": open_gate_ids,
            "review_ready_family_ids": review_ready_family_ids,
            "ready_family_ids": ready_family_ids,
            "blocked_family_ids": blocked_family_ids,
        },
        signals=signals,
        candidate_families=families,
        notes=[
            "Phase 12d is read-only and keeps runtime defaults unchanged.",
            "The live probe is optional and intentionally does not write to PostgreSQL or rebuild indexes.",
            "pgvector remains candidate-only until a separate promotion change closes the required gates.",
        ],
    )


def phase12d_pgvector_live_probe_readiness_report_to_dict(
    report: Phase12dPgvectorLiveProbeReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase12d_pgvector_live_probe_readiness_markdown(
    report: Phase12dPgvectorLiveProbeReadinessReport,
) -> str:
    lines = [
        "# Phase 12d PGVector Live Probe Readiness",
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


def export_phase12d_pgvector_live_probe_readiness_report(
    output_dir: Path = Path("docs/operations/pgvector-live-probe-readiness"),
    *,
    base_dir: Path = Path("."),
) -> Phase12dPgvectorLiveProbeReadinessReport:
    report = build_phase12d_pgvector_live_probe_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = Phase12dPgvectorLiveProbeReadinessReport(
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
            phase12d_pgvector_live_probe_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
            sort_keys=False,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase12d_pgvector_live_probe_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_signal(
    spec: LiveProbeSignalSpec,
    probe_result: dict[str, Any],
    *,
    base_dir: Path,
) -> LiveProbeSignal:
    if spec.path is None:
        summary_builder = spec.summary_builder
        summary = summary_builder(probe_result) if summary_builder is not None else "status=review"
        status = "ready" if summary.startswith("status=ready") else "review"
        if summary.startswith("status=blocked"):
            status = "blocked"
        return LiveProbeSignal(
            id=spec.id,
            required=spec.required,
            status=status,
            summary=summary,
            recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
            evidence_path=_configuration_evidence_path(),
        )

    payload = _read_json_if_present(base_dir / spec.path)
    if payload is None:
        return LiveProbeSignal(
            id=spec.id,
            required=spec.required,
            status="review",
            summary=f"status=review; missing_local_evidence={spec.path.as_posix()}",
            recommended_action=spec.missing_action,
            evidence_path=str(spec.path.as_posix()),
        )

    summary_builder = spec.summary_builder
    summary = summary_builder(payload) if summary_builder is not None else "status=ready"
    status = _normalize_status(payload.get("status"))
    return LiveProbeSignal(
        id=spec.id,
        required=spec.required,
        status=status,
        summary=summary,
        recommended_action="no_action_required" if status == "ready" else spec.missing_action,
        evidence_path=str(spec.path.as_posix()),
    )


def _build_family_readout(
    spec: LiveProbeFamilySpec,
    signal_map: dict[str, LiveProbeSignal],
) -> LiveProbeFamilyReadout:
    required_signals = [signal_map[signal_id] for signal_id in spec.required_signal_ids]
    optional_signals = [
        signal_map[signal_id] for signal_id in spec.optional_signal_ids if signal_id in signal_map
    ]
    if not required_signals:
        status = "ready"
        decision = (
            "continue_spike"
            if any(signal.status in {"review", "blocked"} for signal in optional_signals)
            else "eligible_for_promotion_review"
        )
    elif any(signal.status == "blocked" for signal in required_signals):
        status = "blocked"
        decision = "keep_current_default"
    elif any(signal.status == "review" for signal in required_signals):
        status = "review"
        decision = "continue_spike"
    elif any(signal.status in {"review", "blocked"} for signal in optional_signals):
        status = "review"
        decision = "continue_spike"
    else:
        status = "ready"
        decision = "eligible_for_promotion_review"
    evidence_paths = [signal.evidence_path for signal in required_signals + optional_signals]
    return LiveProbeFamilyReadout(
        id=spec.id,
        label=spec.label,
        status=status,
        decision=decision,
        summary=_family_summary(required_signals, optional_signals),
        required_signal_ids=spec.required_signal_ids,
        optional_signal_ids=spec.optional_signal_ids,
        evidence_paths=evidence_paths,
        notes=spec.notes,
    )


def _family_summary(
    required_signals: list[LiveProbeSignal],
    optional_signals: list[LiveProbeSignal],
) -> str:
    required_ready = sum(1 for signal in required_signals if signal.status == "ready")
    required_total = len(required_signals)
    optional_open = sum(1 for signal in optional_signals if signal.status in {"review", "blocked"})
    return (
        f"required_ready={required_ready}/{required_total}; "
        f"optional_open={optional_open}; "
        f"required_ids={_jsonish_list([signal.id for signal in required_signals])}"
    )


def _configuration_summary(probe_result: dict[str, Any]) -> str:
    database_url_present = bool(probe_result.get("database_url_present", False))
    schema = probe_result.get("schema", PGVECTOR_DEFAULT_SCHEMA)
    table = probe_result.get("table", PGVECTOR_DEFAULT_TABLE)
    index_name = probe_result.get("index_name", PGVECTOR_DEFAULT_INDEX_NAME)
    vector_size = probe_result.get("vector_size", PGVECTOR_DEFAULT_VECTOR_SIZE)
    timeout_seconds = probe_result.get("probe_timeout_seconds", PGVECTOR_DEFAULT_PROBE_TIMEOUT_SECONDS)
    if not database_url_present:
        return (
            "status=blocked; connection_mode=not_configured_local_dev; "
            f"database_url_present={False}; schema={schema}; table={table}; "
            f"index_name={index_name}; vector_size={vector_size}; "
            f"probe_timeout_seconds={timeout_seconds}; next_step=configure_pgvector_database_url"
        )
    return (
        "status=ready; connection_mode=configured_for_optional_live_probe; "
        f"database_url_present={True}; schema={schema}; table={table}; "
        f"index_name={index_name}; vector_size={vector_size}; "
        f"probe_timeout_seconds={timeout_seconds}; next_step=run_optional_live_probe"
        )


def _driver_summary(probe_result: dict[str, Any]) -> str:
    if not probe_result.get("database_url_present", False):
        return (
            "status=blocked; driver_available=False; "
            f"driver_module={PGVECTOR_DRIVER_MODULE}; next_step=configure_pgvector_database_url"
        )
    if not probe_result.get("driver_available", False):
        return (
            "status=blocked; driver_available=False; "
            f"driver_module={PGVECTOR_DRIVER_MODULE}; next_step=install_optional_driver"
        )
    return (
        "status=ready; driver_available=True; "
        f"driver_module={PGVECTOR_DRIVER_MODULE}; next_step=run_optional_live_probe"
        )


def _connection_summary(payload: dict[str, Any]) -> str:
    probe_result = payload
    if not probe_result.get("database_url_present", False):
        return "status=blocked; connection_attempted=False; connection_mode=not_configured_local_dev"
    if not probe_result.get("driver_available", False):
        return "status=blocked; connection_attempted=False; connection_mode=driver_missing"
    if probe_result.get("connection_status") != "ready":
        return (
            f"status=blocked; connection_attempted={probe_result.get('connection_attempted', False)}; "
            f"connection_mode={probe_result.get('connection_status', 'blocked')}; "
            f"message={probe_result.get('connection_message', 'unknown')}"
        )
    return (
        "status=ready; connection_attempted=True; connection_mode=live_probe_success; "
        f"server_version={probe_result.get('server_version', 'unknown')}"
        )


def _extension_summary(payload: dict[str, Any]) -> str:
    probe_result = payload
    if probe_result.get("connection_status") != "ready":
        return "status=blocked; vector_extension_installed=False; next_step=restore_connection"
    if probe_result.get("extension_installed", False):
        return "status=ready; vector_extension_installed=True; next_step=no_action_required"
    return (
        "status=blocked; vector_extension_installed=False; "
        "next_step=create_or_enable_vector_extension"
        )


def _schema_summary(payload: dict[str, Any]) -> str:
    probe_result = payload
    if probe_result.get("connection_status") != "ready":
        return "status=blocked; schema_exists=False; next_step=restore_connection"
    if probe_result.get("schema_exists", False):
        return f"status=ready; schema_exists=True; schema={probe_result.get('schema', PGVECTOR_DEFAULT_SCHEMA)}"
    return (
        "status=blocked; schema_exists=False; "
        f"schema={probe_result.get('schema', PGVECTOR_DEFAULT_SCHEMA)}; next_step=create_schema"
        )


def _table_summary(payload: dict[str, Any]) -> str:
    probe_result = payload
    if probe_result.get("connection_status") != "ready":
        return "status=blocked; table_exists=False; next_step=restore_connection"
    if probe_result.get("table_exists", False):
        return f"status=ready; table_exists=True; table={probe_result.get('table', PGVECTOR_DEFAULT_TABLE)}"
    return (
        "status=blocked; table_exists=False; "
        f"table={probe_result.get('table', PGVECTOR_DEFAULT_TABLE)}; next_step=create_table"
        )


def _index_summary(payload: dict[str, Any]) -> str:
    probe_result = payload
    if probe_result.get("connection_status") != "ready":
        return "status=blocked; index_exists=False; next_step=restore_connection"
    if probe_result.get("index_exists", False):
        return (
            "status=ready; index_exists=True; "
            f"index_name={probe_result.get('index_name', PGVECTOR_DEFAULT_INDEX_NAME)}"
        )
    return (
        "status=blocked; index_exists=False; "
        f"index_name={probe_result.get('index_name', PGVECTOR_DEFAULT_INDEX_NAME)}; "
        "next_step=create_index"
    )


def _run_pgvector_live_probe() -> dict[str, Any]:
    database_url = _env_value(PGVECTOR_DATABASE_URL_ENV)
    schema = _env_value(PGVECTOR_SCHEMA_ENV, PGVECTOR_DEFAULT_SCHEMA)
    table = _env_value(PGVECTOR_TABLE_ENV, PGVECTOR_DEFAULT_TABLE)
    index_name = _env_value(PGVECTOR_INDEX_NAME_ENV, PGVECTOR_DEFAULT_INDEX_NAME)
    vector_size = _int_value(_env_value(PGVECTOR_VECTOR_SIZE_ENV), PGVECTOR_DEFAULT_VECTOR_SIZE)
    timeout_seconds = _int_value(
        _env_value(PGVECTOR_PROBE_TIMEOUT_SECONDS_ENV),
        PGVECTOR_DEFAULT_PROBE_TIMEOUT_SECONDS,
    )
    probe_result: dict[str, Any] = {
        "probe_mode": "optional_psycopg_live_probe",
        "database_url_present": bool(database_url),
        "driver_available": False,
        "connection_attempted": False,
        "connection_status": "blocked",
        "connection_message": "database_url_missing" if not database_url else "driver_unavailable",
        "server_version": "unknown",
        "extension_installed": False,
        "schema_exists": False,
        "table_exists": False,
        "index_exists": False,
        "schema": schema,
        "table": table,
        "index_name": index_name,
        "vector_size": vector_size,
        "probe_timeout_seconds": timeout_seconds,
    }
    if not database_url:
        probe_result["evaluation_state"] = "pgvector_probe_configuration_blocked"
        return probe_result

    driver = _load_psycopg_driver()
    if driver is None:
        probe_result["evaluation_state"] = "pgvector_probe_driver_missing"
        return probe_result

    connect = getattr(driver, "connect", None)
    if not callable(connect):
        probe_result["evaluation_state"] = "pgvector_probe_driver_missing"
        return probe_result

    probe_result["driver_available"] = True
    try:
        connection = connect(database_url, connect_timeout=timeout_seconds)
    except Exception as error:  # pragma: no cover - exercised via fake driver failure path
        probe_result["evaluation_state"] = "pgvector_probe_connection_failed"
        probe_result["connection_message"] = str(error)
        return probe_result

    probe_result["connection_attempted"] = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            probe_result["server_version"] = _row_scalar(cursor.fetchone(), fallback="unknown")

            cursor.execute("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = %s)", ("vector",))
            probe_result["extension_installed"] = bool(_row_scalar(cursor.fetchone(), fallback=False))

            cursor.execute("SELECT to_regclass(%s)", (f"{schema}.{table}",))
            probe_result["table_exists"] = _row_scalar(cursor.fetchone()) is not None

            cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = %s)",
                (schema,),
            )
            probe_result["schema_exists"] = bool(_row_scalar(cursor.fetchone(), fallback=False))

            cursor.execute(
                "SELECT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = %s AND tablename = %s AND indexname = %s)",
                (schema, table, index_name),
            )
            probe_result["index_exists"] = bool(_row_scalar(cursor.fetchone(), fallback=False))
    except Exception as error:  # pragma: no cover - defensive for unexpected driver issues
        probe_result["evaluation_state"] = "pgvector_probe_runtime_error"
        probe_result["connection_message"] = str(error)
        try:
            connection.close()
        except Exception:  # pragma: no cover - defensive cleanup
            pass
        return probe_result

    try:
        connection.close()
    except Exception:  # pragma: no cover - defensive cleanup
        pass

    probe_result["connection_status"] = "ready"
    if probe_result["extension_installed"] and probe_result["schema_exists"] and probe_result["table_exists"] and probe_result["index_exists"]:
        probe_result["evaluation_state"] = "ready_for_pgvector_candidate_promotion_review"
    else:
        probe_result["evaluation_state"] = "ready_for_pgvector_probe_follow_up"
    probe_result["connection_message"] = "live_probe_success"
    return probe_result


def _load_psycopg_driver():
    try:
        return import_module(PGVECTOR_DRIVER_MODULE)
    except ModuleNotFoundError:
        return None


def _row_scalar(row: Any, *, fallback: Any = None) -> Any:
    if isinstance(row, (list, tuple)) and row:
        return row[0]
    return fallback


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


def _env_value(name: str, fallback: str = "") -> str:
    value = os.environ.get(name, "")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def _configuration_evidence_path() -> str:
    return (
        "environment:"
        f"{PGVECTOR_DATABASE_URL_ENV},"
        f"{PGVECTOR_SCHEMA_ENV},"
        f"{PGVECTOR_TABLE_ENV},"
        f"{PGVECTOR_INDEX_NAME_ENV},"
        f"{PGVECTOR_VECTOR_SIZE_ENV},"
        f"{PGVECTOR_PROBE_TIMEOUT_SECONDS_ENV}"
    )
