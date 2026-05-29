from app.models.contracts import EvidenceDocument, RagAnswerResult


COMPOSER_ID = "deterministic-extractive-v1"


def compose_cited_answer(
    documents: list[EvidenceDocument],
    retrieval_backend: str,
    min_evidence_count: int = 1,
    min_top_score: float = 0.0,
) -> RagAnswerResult:
    gate = _evaluate_evidence_gate(
        documents=documents,
        min_evidence_count=min_evidence_count,
        min_top_score=min_top_score,
    )
    metadata = {
        "composer": COMPOSER_ID,
        "evidence_count": len(documents),
        "evidence_gate": gate,
        "retrieval_backend": retrieval_backend,
    }
    if not gate["passed"]:
        return RagAnswerResult(
            answer_status="insufficient_evidence",
            answer="",
            citations=[],
            documents=documents,
            metadata=metadata,
        )

    cited_documents = documents[:3]
    citations = _unique_citations(cited_documents)
    answer_parts = [
        f"[{document.citation}] {document.snippet}" for document in cited_documents
    ]
    return RagAnswerResult(
        answer_status="answered",
        answer="\n".join(answer_parts),
        citations=citations,
        documents=documents,
        metadata=metadata,
    )


def _unique_citations(documents: list[EvidenceDocument]) -> list[str]:
    citations: list[str] = []
    seen: set[str] = set()
    for document in documents:
        if document.citation in seen:
            continue
        seen.add(document.citation)
        citations.append(document.citation)
    return citations


def _evaluate_evidence_gate(
    documents: list[EvidenceDocument],
    min_evidence_count: int,
    min_top_score: float,
) -> dict[str, object]:
    top_score = max((document.score for document in documents), default=None)
    base_gate = {
        "min_evidence_count": min_evidence_count,
        "min_top_score": min_top_score,
        "top_score": top_score,
    }
    if not documents:
        return {
            **base_gate,
            "passed": False,
            "reason": "no_documents",
        }
    if len(documents) < min_evidence_count:
        return {
            **base_gate,
            "passed": False,
            "reason": "evidence_count_below_minimum",
        }
    if top_score is None or top_score < min_top_score:
        return {
            **base_gate,
            "passed": False,
            "reason": "top_score_below_minimum",
        }
    return {
        **base_gate,
        "passed": True,
        "reason": "passed",
    }
