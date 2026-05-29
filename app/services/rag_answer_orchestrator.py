from app.models.contracts import EvidenceDocument, RagAnswerResult


COMPOSER_ID = "deterministic-extractive-v1"


def compose_cited_answer(
    documents: list[EvidenceDocument],
    retrieval_backend: str,
) -> RagAnswerResult:
    metadata = {
        "composer": COMPOSER_ID,
        "evidence_count": len(documents),
        "retrieval_backend": retrieval_backend,
    }
    if not documents:
        return RagAnswerResult(
            answer_status="insufficient_evidence",
            answer="",
            citations=[],
            documents=[],
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
