from dataclasses import dataclass, field


VALIDATOR_ID = "cited-answer-output-validator-v1"


@dataclass(frozen=True)
class AnswerOutputValidation:
    passed: bool
    reason: str
    citations: list[str]
    allowed_citations: list[str]
    invalid_citations: list[str] = field(default_factory=list)

    def metadata(self) -> dict[str, object]:
        metadata: dict[str, object] = {
            "validator": VALIDATOR_ID,
            "passed": self.passed,
            "reason": self.reason,
            "citation_count": len(self.citations),
            "allowed_citation_count": len(self.allowed_citations),
        }
        if self.invalid_citations:
            metadata["invalid_citations"] = self.invalid_citations
        return metadata


def validate_cited_answer_output(
    citations: list[str],
    allowed_citations: list[str],
) -> AnswerOutputValidation:
    if not citations:
        return AnswerOutputValidation(
            passed=False,
            reason="missing_citations",
            citations=citations,
            allowed_citations=allowed_citations,
        )

    allowed = set(allowed_citations)
    invalid_citations = [
        citation for citation in citations if citation not in allowed
    ]
    if invalid_citations:
        return AnswerOutputValidation(
            passed=False,
            reason="citation_not_allowed",
            citations=citations,
            allowed_citations=allowed_citations,
            invalid_citations=invalid_citations,
        )

    return AnswerOutputValidation(
        passed=True,
        reason="passed",
        citations=citations,
        allowed_citations=allowed_citations,
    )
