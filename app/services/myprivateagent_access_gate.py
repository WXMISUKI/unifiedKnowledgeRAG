from dataclasses import dataclass
from typing import Any


MYPRIVATEAGENT_ACCESS_PRIMITIVE_IDS = {
    "provider_contract_smoke",
    "phase10_myprivateagent_local_consumer_probe",
    "phase11_provider_discovery_smoke",
    "phase11_rag_retrieve_consumption_smoke",
    "phase11_source_binding_preview_smoke",
}

MYPRIVATEAGENT_ACCESS_REVIEW_CONTEXT_IDS = {
    "phase10_myprivateagent_local_consumer_readiness",
    "phase11_local_provider_integration_profile",
    "phase13_provider_roadmap_decision_checkpoint",
    "phase14_myprivateagent_provider_integration_acceptance_checkpoint",
    "phase15_myprivateagent_repo_side_trial_dispatch_package",
    "phase16_myprivateagent_minimal_access_loop",
    "provider_handoff_bundle",
    "provider_handoff_refresh",
}


@dataclass(frozen=True)
class MyPrivateAgentAccessGate:
    status: str
    primitive_ids: list[str]
    ready_primitive_ids: list[str]
    review_primitive_ids: list[str]
    blocked_primitive_ids: list[str]
    missing_primitive_ids: list[str]
    review_context_ids: list[str]
    ready_context_ids: list[str]
    review_context_open_ids: list[str]
    blocked_context_ids: list[str]


def build_myprivateagent_access_gate(
    rows: list[dict[str, Any]],
) -> MyPrivateAgentAccessGate:
    by_id = {str(row.get("id")): row for row in rows if row.get("id")}
    primitive_ids = sorted(MYPRIVATEAGENT_ACCESS_PRIMITIVE_IDS)
    context_ids = sorted(
        artifact_id
        for artifact_id in MYPRIVATEAGENT_ACCESS_REVIEW_CONTEXT_IDS
        if artifact_id in by_id
    )

    ready_primitive_ids = _ids_with_status(by_id, primitive_ids, "ready")
    review_primitive_ids = _ids_with_status(by_id, primitive_ids, "review")
    blocked_primitive_ids = _ids_with_status(by_id, primitive_ids, "blocked")
    missing_primitive_ids = [
        artifact_id for artifact_id in primitive_ids if artifact_id not in by_id
    ]

    ready_context_ids = _ids_with_status(by_id, context_ids, "ready")
    review_context_open_ids = [
        artifact_id
        for artifact_id in context_ids
        if _normalize_status(by_id[artifact_id].get("status")) == "review"
    ]
    blocked_context_ids = _ids_with_status(by_id, context_ids, "blocked")

    if blocked_primitive_ids or missing_primitive_ids:
        status = "blocked"
    elif review_primitive_ids:
        status = "review"
    else:
        status = "ready"

    return MyPrivateAgentAccessGate(
        status=status,
        primitive_ids=primitive_ids,
        ready_primitive_ids=ready_primitive_ids,
        review_primitive_ids=review_primitive_ids,
        blocked_primitive_ids=blocked_primitive_ids,
        missing_primitive_ids=missing_primitive_ids,
        review_context_ids=context_ids,
        ready_context_ids=ready_context_ids,
        review_context_open_ids=review_context_open_ids,
        blocked_context_ids=blocked_context_ids,
    )


def myprivateagent_access_gate_to_dict(
    gate: MyPrivateAgentAccessGate,
    *,
    id_key: str = "artifact",
) -> dict[str, Any]:
    primitive_key = f"primitive_{id_key}_ids"
    context_key = f"review_context_{id_key}_ids"
    return {
        "status": gate.status,
        primitive_key: gate.primitive_ids,
        f"ready_primitive_{id_key}_ids": gate.ready_primitive_ids,
        f"review_primitive_{id_key}_ids": gate.review_primitive_ids,
        f"blocked_primitive_{id_key}_ids": gate.blocked_primitive_ids,
        f"missing_primitive_{id_key}_ids": gate.missing_primitive_ids,
        context_key: gate.review_context_ids,
        f"ready_review_context_{id_key}_ids": gate.ready_context_ids,
        f"open_review_context_{id_key}_ids": gate.review_context_open_ids,
        f"blocked_review_context_{id_key}_ids": gate.blocked_context_ids,
        "primitive_count": len(gate.primitive_ids),
        "ready_primitive_count": len(gate.ready_primitive_ids),
        "review_primitive_count": len(gate.review_primitive_ids),
        "blocked_primitive_count": len(gate.blocked_primitive_ids),
        "missing_primitive_count": len(gate.missing_primitive_ids),
        "review_context_count": len(gate.review_context_ids),
        "open_review_context_count": len(gate.review_context_open_ids),
        "blocked_review_context_count": len(gate.blocked_context_ids),
    }


def _ids_with_status(
    by_id: dict[str, dict[str, Any]],
    ids: list[str],
    status: str,
) -> list[str]:
    return [
        artifact_id
        for artifact_id in ids
        if artifact_id in by_id
        and _normalize_status(by_id[artifact_id].get("status")) == status
    ]


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    if value in {"missing", "skipped"}:
        return "blocked"
    return "review"
