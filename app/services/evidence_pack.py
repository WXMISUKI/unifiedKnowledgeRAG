import json
from hashlib import sha256
from typing import Any

from app.models.contracts import EvidenceDocument


EVIDENCE_PACK_VERSION = "evidence-pack-v1"
EVIDENCE_PACK_CITATION_POLICY = "use_only_returned_citations"


def build_evidence_pack(
    *,
    query: str,
    requested_source_ids: list[str],
    retrieval_backend: str,
    documents: list[EvidenceDocument],
    filter_context: dict[str, Any],
) -> dict[str, Any]:
    allowed_citations = [document.citation for document in documents]
    score_summary = _score_summary(documents)
    pack_core: dict[str, Any] = {
        "version": EVIDENCE_PACK_VERSION,
        "status": "answerable" if documents else "insufficient_evidence",
        "reason": "documents_returned" if documents else "no_documents",
        "query": query,
        "requested_source_ids": requested_source_ids,
        "retrieval_backend": retrieval_backend,
        "citation_policy": EVIDENCE_PACK_CITATION_POLICY,
        "allowed_citations": allowed_citations,
        "evidence_count": len(documents),
        "score_summary": score_summary,
        "filter_context": filter_context,
        "evidence": [_document_to_pack_entry(document) for document in documents],
    }
    return {
        "pack_id": _pack_id(pack_core),
        **pack_core,
    }


def _document_to_pack_entry(document: EvidenceDocument) -> dict[str, Any]:
    return {
        "source_id": document.source_id,
        "document_id": document.document_id,
        "title": document.title,
        "citation": document.citation,
        "score": document.score,
        "snippet": document.snippet,
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


def _pack_id(pack_core: dict[str, Any]) -> str:
    fingerprint = json.dumps(pack_core, ensure_ascii=False, sort_keys=True)
    digest = sha256(fingerprint.encode("utf-8")).hexdigest()
    return f"evidence-pack-{digest[:16]}"
