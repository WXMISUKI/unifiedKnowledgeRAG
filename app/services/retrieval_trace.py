from hashlib import sha256
from typing import Any

from app.models.contracts import EvidenceDocument


RETRIEVAL_TRACE_VERSION = "retrieval-trace-v1"


def build_retrieval_trace(
    backend: str,
    requested_source_ids: list[str],
    top_k: int,
    documents: list[EvidenceDocument],
    filter_context: dict[str, Any],
) -> dict[str, Any]:
    citations = [document.citation for document in documents]
    score_summary = _score_summary(documents)
    trace_core = {
        "version": RETRIEVAL_TRACE_VERSION,
        "backend": backend,
        "requested_source_ids": requested_source_ids,
        "top_k": top_k,
        "document_count": len(documents),
        "citations": citations,
        "score_summary": score_summary,
        "filter_context": filter_context,
    }
    return {
        "trace_id": _trace_id(trace_core),
        **trace_core,
    }


def _score_summary(documents: list[EvidenceDocument]) -> dict[str, float | None]:
    if not documents:
        return {
            "max_score": None,
            "min_score": None,
        }
    scores = [document.score for document in documents]
    return {
        "max_score": max(scores),
        "min_score": min(scores),
    }


def _trace_id(trace_core: dict[str, Any]) -> str:
    citations = "|".join(trace_core["citations"])
    sources = "|".join(trace_core["requested_source_ids"])
    filter_context = trace_core["filter_context"]
    fingerprint = (
        f"{trace_core['backend']}|{sources}|{trace_core['top_k']}|"
        f"{trace_core['document_count']}|{citations}|{filter_context}"
    )
    digest = sha256(fingerprint.encode("utf-8")).hexdigest()
    return f"retrieval-trace-{digest[:16]}"
