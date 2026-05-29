from hashlib import sha256
from typing import Any

from app.models.contracts import EvidenceDocument


ANSWER_TRACE_VERSION = "answer-trace-v1"


def build_answer_trace(
    final_status: str,
    metadata: dict[str, Any],
    documents: list[EvidenceDocument],
) -> dict[str, Any]:
    stages: list[dict[str, Any]] = [
        _retrieval_stage(metadata, documents),
        _evidence_gate_stage(metadata),
        _composer_stage(metadata),
    ]

    output_parser = metadata.get("output_parser")
    if isinstance(output_parser, dict):
        stages.append(_output_parser_stage(output_parser))

    output_validation = metadata.get("output_validation")
    if isinstance(output_validation, dict):
        stages.append(_output_validator_stage(output_validation))

    stages.append(
        {
            "name": "final_decision",
            "status": final_status,
            "reason": _final_reason(final_status, stages),
        }
    )
    return {
        "trace_id": _trace_id(final_status, stages, documents),
        "version": ANSWER_TRACE_VERSION,
        "final_status": final_status,
        "stages": stages,
    }


def attach_answer_trace(
    final_status: str,
    metadata: dict[str, Any],
    documents: list[EvidenceDocument],
) -> dict[str, Any]:
    return {
        **metadata,
        "answer_trace": build_answer_trace(
            final_status=final_status,
            metadata=metadata,
            documents=documents,
        ),
    }


def _retrieval_stage(
    metadata: dict[str, Any],
    documents: list[EvidenceDocument],
) -> dict[str, Any]:
    return {
        "name": "retrieval",
        "status": "completed",
        "reason": "documents_retrieved" if documents else "no_documents",
        "backend": metadata.get("retrieval_backend"),
        "document_count": len(documents),
    }


def _evidence_gate_stage(metadata: dict[str, Any]) -> dict[str, Any]:
    gate = metadata.get("evidence_gate")
    if not isinstance(gate, dict):
        return {
            "name": "evidence_gate",
            "status": "not_available",
            "reason": "metadata_missing",
        }
    passed = bool(gate.get("passed"))
    return {
        "name": "evidence_gate",
        "status": "passed" if passed else "failed",
        "reason": gate.get("reason"),
        "min_evidence_count": gate.get("min_evidence_count"),
        "min_top_score": gate.get("min_top_score"),
        "top_score": gate.get("top_score"),
    }


def _composer_stage(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": "composer",
        "status": "completed",
        "reason": "candidate_created",
        "provider": metadata.get("composer_provider"),
        "model": metadata.get("composer_model"),
    }


def _output_parser_stage(output_parser: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": "output_parser",
        "status": "completed",
        "reason": "citations_extracted",
        "parser": output_parser.get("parser"),
        "citation_count": output_parser.get("citation_count"),
    }


def _output_validator_stage(output_validation: dict[str, Any]) -> dict[str, Any]:
    passed = bool(output_validation.get("passed"))
    return {
        "name": "output_validator",
        "status": "passed" if passed else "failed",
        "reason": output_validation.get("reason"),
        "validator": output_validation.get("validator"),
        "citation_count": output_validation.get("citation_count"),
        "allowed_citation_count": output_validation.get("allowed_citation_count"),
    }


def _final_reason(final_status: str, stages: list[dict[str, Any]]) -> str:
    if final_status == "answered":
        return "validated_answer"
    failed_stages = [stage["name"] for stage in stages if stage.get("status") == "failed"]
    if failed_stages:
        return f"{failed_stages[-1]}_failed"
    return "insufficient_evidence"


def _trace_id(
    final_status: str,
    stages: list[dict[str, Any]],
    documents: list[EvidenceDocument],
) -> str:
    citations = "|".join(document.citation for document in documents)
    stage_fingerprint = "|".join(
        f"{stage.get('name')}:{stage.get('status')}:{stage.get('reason')}"
        for stage in stages
    )
    digest = sha256(f"{final_status}|{citations}|{stage_fingerprint}".encode("utf-8")).hexdigest()
    return f"answer-trace-{digest[:16]}"
