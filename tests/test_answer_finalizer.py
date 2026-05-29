from app.models.contracts import EvidenceDocument
from app.services.answer_finalizer import finalize_cited_answer


def _document(citation: str = "refund_policy_2026#section-3") -> EvidenceDocument:
    return EvidenceDocument(
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="售后退款规则",
        snippet="客户三天未发货可以申请退款。",
        score=0.91,
        citation=citation,
    )


def test_finalizer_returns_answered_result_for_valid_candidate():
    document = _document()

    result = finalize_cited_answer(
        query="客户三天未发货能否退款？",
        documents=[document],
        candidate_answer=f"[{document.citation}] 客户三天未发货可以申请退款。",
        base_metadata={
            "composer": "test-composer",
            "composer_provider": "test",
            "composer_model": "test-model",
            "evidence_count": 1,
            "evidence_gate": {"passed": True, "reason": "passed"},
            "retrieval_backend": "fixture",
        },
    )

    assert result.answer_status == "answered"
    assert result.citations == [document.citation]
    assert result.metadata["prompt_package"]["allowed_citations"] == [document.citation]
    assert result.metadata["output_validation"]["passed"] is True
    trace = result.metadata["answer_trace"]
    assert trace["version"] == "answer-trace-v1"
    assert trace["final_status"] == "answered"
    assert [stage["name"] for stage in trace["stages"]] == [
        "retrieval",
        "evidence_gate",
        "composer",
        "output_parser",
        "output_validator",
        "final_decision",
    ]
    assert trace["stages"][-1]["reason"] == "validated_answer"


def test_finalizer_fails_closed_for_candidate_without_citations():
    document = _document()

    result = finalize_cited_answer(
        query="客户三天未发货能否退款？",
        documents=[document],
        candidate_answer="客户三天未发货可以申请退款。",
        base_metadata={
            "composer": "test-composer",
            "composer_provider": "test",
            "composer_model": "test-model",
            "evidence_count": 1,
            "evidence_gate": {"passed": True, "reason": "passed"},
            "retrieval_backend": "fixture",
        },
    )

    assert result.answer_status == "insufficient_evidence"
    assert result.answer == ""
    assert result.citations == []
    assert result.metadata["output_parser"]["citation_count"] == 0
    assert result.metadata["output_validation"]["reason"] == "missing_citations"
    trace = result.metadata["answer_trace"]
    assert trace["final_status"] == "insufficient_evidence"
    assert trace["stages"][3]["name"] == "output_parser"
    assert trace["stages"][3]["citation_count"] == 0
    assert trace["stages"][4]["name"] == "output_validator"
    assert trace["stages"][4]["status"] == "failed"
    assert trace["stages"][-1]["reason"] == "output_validator_failed"
