from app.models.contracts import EvidenceDocument, RagAnswerResult
from app.services.answer_output_parser import parse_cited_answer_output
from app.services.answer_output_validator import validate_cited_answer_output
from app.services.answer_prompt_package import (
    build_cited_answer_prompt_package,
    render_cited_answer_prompt,
)


def finalize_cited_answer(
    query: str,
    documents: list[EvidenceDocument],
    candidate_answer: str,
    base_metadata: dict[str, object],
) -> RagAnswerResult:
    prompt_package = build_cited_answer_prompt_package(query, documents)
    rendered_prompt = render_cited_answer_prompt(prompt_package)
    parsed_output = parse_cited_answer_output(candidate_answer)
    validation = validate_cited_answer_output(
        citations=parsed_output.citations,
        allowed_citations=prompt_package.allowed_citations,
    )
    metadata = {
        **base_metadata,
        "prompt_package": prompt_package.metadata(),
        "prompt_render": rendered_prompt.metadata(),
        "output_parser": parsed_output.metadata(),
        "output_validation": validation.metadata(),
    }
    if not validation.passed:
        return RagAnswerResult(
            answer_status="insufficient_evidence",
            answer="",
            citations=[],
            documents=documents,
            metadata=metadata,
        )

    return RagAnswerResult(
        answer_status="answered",
        answer=parsed_output.answer_text,
        citations=parsed_output.citations,
        documents=documents,
        metadata=metadata,
    )
