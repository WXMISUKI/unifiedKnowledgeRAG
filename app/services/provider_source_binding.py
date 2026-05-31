from datetime import UTC, datetime
from app.config import Settings, get_settings
from app.models.contracts import (
    KnowledgeBaseSource,
    ProviderSourceBindingSummaryResponse,
    SourceBindingSummaryRow,
)
from app.services.ingestion_preflight import get_ingestion_source_preflight
from app.services.provider_manifest import build_provider_integration_manifest
from app.services.source_catalog import list_knowledge_bases
from app.services.source_document_manifest import get_source_document_manifest


SOURCE_BINDING_SUMMARY_ID = "provider-source-binding-summary-v1"


def build_provider_source_binding_summary(
    settings: Settings | None = None,
) -> ProviderSourceBindingSummaryResponse:
    settings = settings or get_settings()
    manifest = build_provider_integration_manifest()
    sources = [
        _source_binding_row(source, settings)
        for source in list_knowledge_bases(settings)
    ]
    return ProviderSourceBindingSummaryResponse(
        id=SOURCE_BINDING_SUMMARY_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(sources),
        provider={
            "provider_id": manifest.provider_id,
            "provider_name": manifest.provider_name,
            "provider_version": manifest.provider_version,
            "contract_version": manifest.contract_version,
            "manifest_version": manifest.manifest_version,
            "component_role": manifest.component_role,
        },
        sources=sources,
        operation_notes=_operation_notes(sources),
    )


def _source_binding_row(
    source: KnowledgeBaseSource,
    settings: Settings,
) -> SourceBindingSummaryRow:
    manifest_response = get_source_document_manifest(source.id, settings)
    preflight_response = get_ingestion_source_preflight(source.id, settings)
    if not manifest_response.ok or manifest_response.result is None:
        return _blocked_row(
            source,
            recommended_action="review_source_manifest_before_binding",
            reason="Source document manifest is unavailable.",
        )
    if not preflight_response.ok or preflight_response.result is None:
        return _blocked_row(
            source,
            recommended_action="review_ingestion_preflight_before_binding",
            reason="Source ingestion preflight is unavailable.",
        )

    manifest = manifest_response.result
    preflight = preflight_response.result
    drift_statuses = sorted(
        {
            document.drift_status or "unchecked"
            for document in manifest.documents
        }
    )
    parser_statuses = sorted(
        {
            document.parser_status
            for document in preflight.documents
        }
    )
    status, bindable, recommended_action, reasons = _binding_decision(
        source=source,
        drift_statuses=drift_statuses,
        preflight_status=preflight.status,
    )
    return SourceBindingSummaryRow(
        source_id=source.id,
        owner=source.owner,
        source_status=source.status,
        status=status,
        bindable=bindable,
        retrieval_backend=source.retrieval_backend or settings.rag_retrieval_backend,
        backend_status=source.backend_status,
        backend_reason=source.backend_reason,
        index_status=source.index_status or "unknown",
        index_reason=source.index_reason,
        latest_index_job_id=source.latest_index_job_id,
        document_count=len(manifest.documents),
        drift_statuses=drift_statuses,
        parser_statuses=parser_statuses,
        ingestion_preflight_status=preflight.status,
        recommended_action=recommended_action,
        reasons=reasons,
    )


def _binding_decision(
    *,
    source: KnowledgeBaseSource,
    drift_statuses: list[str],
    preflight_status: str,
) -> tuple[str, bool, str, list[str]]:
    reasons: list[str] = []
    if source.status != "ready":
        reasons.append("Source catalog status is not ready.")
        return "blocked", False, "review_source_catalog_before_binding", reasons
    if source.backend_status != "ready":
        reasons.append("Retrieval backend is not ready.")
        return "blocked", False, "resolve_retrieval_backend_before_binding", reasons
    if source.index_status != "ready":
        reasons.append("Source index is not ready.")
        return "blocked", False, "run_ingestion_job_before_binding", reasons
    if "missing" in drift_statuses:
        reasons.append("At least one source document file is missing.")
        return "blocked", False, "restore_source_file_before_binding", reasons
    if "changed" in drift_statuses:
        reasons.append("At least one source document fingerprint changed.")
        return "blocked", False, "run_ingestion_job_before_binding", reasons
    if preflight_status != "ready":
        reasons.append("Ingestion preflight is not ready.")
        return "blocked", False, "review_ingestion_preflight_before_binding", reasons
    if "unchecked" in drift_statuses:
        reasons.append("At least one source document fingerprint is unchecked.")
        return "review", False, "review_source_fingerprint_before_binding", reasons
    return "ready", True, "bind_source_from_control_plane", reasons


def _blocked_row(
    source: KnowledgeBaseSource,
    *,
    recommended_action: str,
    reason: str,
) -> SourceBindingSummaryRow:
    return SourceBindingSummaryRow(
        source_id=source.id,
        owner=source.owner,
        source_status=source.status,
        status="blocked",
        bindable=False,
        retrieval_backend=source.retrieval_backend or "unknown",
        backend_status=source.backend_status,
        backend_reason=source.backend_reason,
        index_status=source.index_status or "unknown",
        index_reason=source.index_reason,
        latest_index_job_id=source.latest_index_job_id,
        recommended_action=recommended_action,
        reasons=[reason],
    )


def _overall_status(rows: list[SourceBindingSummaryRow]) -> str:
    statuses = {row.status for row in rows}
    if "blocked" in statuses:
        return "blocked"
    if statuses - {"ready"}:
        return "review"
    return "ready"


def _operation_notes(rows: list[SourceBindingSummaryRow]) -> list[str]:
    notes = [
        "This summary is read-only and does not create source-to-agent bindings.",
        "External control planes own binding policy, approvals, audit, and final answer workflow.",
        "Detailed document diagnostics remain available from source document manifests and ingestion preflight endpoints.",
    ]
    if any(row.status == "blocked" for row in rows):
        notes.append("At least one source must be repaired or reindexed before binding.")
    if any(row.status == "review" for row in rows):
        notes.append("At least one source requires review before binding.")
    return notes
