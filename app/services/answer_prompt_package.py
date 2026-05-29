from dataclasses import dataclass

from app.models.contracts import EvidenceDocument


PROMPT_PACKAGE_ID = "cited-answer-prompt-v1"
CITATION_POLICY = "use_only_allowed_citations"


@dataclass(frozen=True)
class AnswerPromptPackage:
    id: str
    query: str
    citation_policy: str
    allowed_citations: list[str]
    evidence: list[dict[str, str]]

    def metadata(self) -> dict[str, object]:
        return {
            "id": self.id,
            "citation_policy": self.citation_policy,
            "allowed_citations": self.allowed_citations,
            "evidence_count": len(self.evidence),
        }


def build_cited_answer_prompt_package(
    query: str,
    documents: list[EvidenceDocument],
) -> AnswerPromptPackage:
    return AnswerPromptPackage(
        id=PROMPT_PACKAGE_ID,
        query=query,
        citation_policy=CITATION_POLICY,
        allowed_citations=[document.citation for document in documents],
        evidence=[
            {
                "citation": document.citation,
                "title": document.title,
                "snippet": document.snippet,
            }
            for document in documents
        ],
    )
