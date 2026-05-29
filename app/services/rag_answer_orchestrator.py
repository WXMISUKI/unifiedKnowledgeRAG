from abc import ABC, abstractmethod

from app.config import Settings
from app.models.contracts import EvidenceDocument, ProviderError, RagAnswerResult
from app.services.answer_output_validator import validate_cited_answer_output
from app.services.answer_prompt_package import (
    build_cited_answer_prompt_package,
    render_cited_answer_prompt,
)


DETERMINISTIC_COMPOSER_ID = "deterministic-extractive-v1"


class AnswerComposer(ABC):
    provider: str
    model: str

    @abstractmethod
    def compose(
        self,
        query: str,
        documents: list[EvidenceDocument],
        retrieval_backend: str,
        min_evidence_count: int,
        min_top_score: float,
    ) -> RagAnswerResult:
        raise NotImplementedError


class DeterministicAnswerComposer(AnswerComposer):
    provider = "deterministic"

    def __init__(self, model: str = DETERMINISTIC_COMPOSER_ID):
        self.model = model or DETERMINISTIC_COMPOSER_ID

    def compose(
        self,
        query: str,
        documents: list[EvidenceDocument],
        retrieval_backend: str,
        min_evidence_count: int,
        min_top_score: float,
    ) -> RagAnswerResult:
        gate = _evaluate_evidence_gate(
            documents=documents,
            min_evidence_count=min_evidence_count,
            min_top_score=min_top_score,
        )
        metadata = {
            "composer": DETERMINISTIC_COMPOSER_ID,
            "composer_provider": self.provider,
            "composer_model": self.model,
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
        prompt_package = build_cited_answer_prompt_package(query, cited_documents)
        rendered_prompt = render_cited_answer_prompt(prompt_package)
        validation = validate_cited_answer_output(
            citations=citations,
            allowed_citations=prompt_package.allowed_citations,
        )
        metadata["prompt_package"] = prompt_package.metadata()
        metadata["prompt_render"] = rendered_prompt.metadata()
        metadata["output_validation"] = validation.metadata()
        if not validation.passed:
            return RagAnswerResult(
                answer_status="insufficient_evidence",
                answer="",
                citations=[],
                documents=documents,
                metadata=metadata,
            )
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


def create_answer_composer(settings: Settings) -> tuple[AnswerComposer | None, ProviderError | None]:
    provider = settings.rag_answer_composer.lower()
    if provider == "deterministic":
        return DeterministicAnswerComposer(settings.rag_answer_composer_model), None
    if provider in {"hosted", "local"}:
        return None, ProviderError(
            code="ANSWER_COMPOSER_NOT_IMPLEMENTED",
            message=(
                f"Answer composer '{provider}' is not implemented yet. "
                "Use deterministic until a model provider change is approved."
            ),
        )
    return None, ProviderError(
        code="UNSUPPORTED_ANSWER_COMPOSER",
        message=f"Unsupported RAG_ANSWER_COMPOSER: {settings.rag_answer_composer}",
    )


def answer_composer_readiness(settings: Settings) -> tuple[str, str | None, str, str]:
    provider = settings.rag_answer_composer.lower()
    _, error = create_answer_composer(settings)
    if error is None:
        return "ready", None, provider, settings.rag_answer_composer_model
    return "degraded", error.message, provider, settings.rag_answer_composer_model


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
