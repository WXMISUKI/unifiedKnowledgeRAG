from dataclasses import dataclass

from app.models.contracts import EvidenceDocument


PROMPT_PACKAGE_ID = "cited-answer-prompt-v1"
CITATION_POLICY = "use_only_allowed_citations"
PROMPT_RENDERER_ID = "cited-chat-messages-v1"


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


@dataclass(frozen=True)
class PromptMessage:
    role: str
    content: str


@dataclass(frozen=True)
class RenderedPrompt:
    renderer: str
    prompt_package_id: str
    messages: list[PromptMessage]
    citation_policy: str

    def metadata(self) -> dict[str, object]:
        return {
            "renderer": self.renderer,
            "prompt_package_id": self.prompt_package_id,
            "message_count": len(self.messages),
            "citation_policy": self.citation_policy,
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


def render_cited_answer_prompt(package: AnswerPromptPackage) -> RenderedPrompt:
    evidence_lines = [
        f"[{item['citation']}] {item['title']}: {item['snippet']}"
        for item in package.evidence
    ]
    system_message = (
        "Answer only from the provided evidence. "
        "Use only allowed citations and do not invent facts."
    )
    user_message = "\n".join(
        [
            f"Question: {package.query}",
            f"Citation policy: {package.citation_policy}",
            "Evidence:",
            *evidence_lines,
        ]
    )
    return RenderedPrompt(
        renderer=PROMPT_RENDERER_ID,
        prompt_package_id=package.id,
        messages=[
            PromptMessage(role="system", content=system_message),
            PromptMessage(role="user", content=user_message),
        ],
        citation_policy=package.citation_policy,
    )
