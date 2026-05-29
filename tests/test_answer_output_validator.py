from app.services.answer_output_validator import validate_cited_answer_output


def test_output_validator_rejects_citations_outside_allowed_set():
    result = validate_cited_answer_output(
        citations=["refund_policy_2026#section-3", "made_up#citation"],
        allowed_citations=["refund_policy_2026#section-3"],
    )

    assert result.passed is False
    assert result.reason == "citation_not_allowed"
    assert result.invalid_citations == ["made_up#citation"]
    assert result.metadata() == {
        "validator": "cited-answer-output-validator-v1",
        "passed": False,
        "reason": "citation_not_allowed",
        "citation_count": 2,
        "allowed_citation_count": 1,
        "invalid_citations": ["made_up#citation"],
    }


def test_output_validator_requires_non_empty_citations():
    result = validate_cited_answer_output(
        citations=[],
        allowed_citations=["refund_policy_2026#section-3"],
    )

    assert result.passed is False
    assert result.reason == "missing_citations"
