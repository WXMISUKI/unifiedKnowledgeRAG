from app.services.approved_local_corpus_acceptance_smoke import (
    AcceptanceCase,
    export_approved_local_corpus_acceptance_smoke,
    run_approved_local_corpus_acceptance_smoke,
)


def test_acceptance_smoke_go_for_registered_company_source(tmp_path):
    report = export_approved_local_corpus_acceptance_smoke(
        output_dir=tmp_path / "acceptance",
    )

    assert report.decision == "go"
    assert report.reason_code == "approved_local_corpus_accepted"
    assert report.summary["case_count"] == 5
    assert report.summary["invalid_citation_count"] == 0
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert all(case.status == "ready" for case in report.cases)


def test_acceptance_smoke_blocks_when_source_missing():
    report = run_approved_local_corpus_acceptance_smoke(source_id="missing_source")

    assert report.decision == "blocked"
    assert report.reason_code == "approved_source_not_ready_for_acceptance"
    assert report.cases[0].id == "catalog_visibility"
    assert report.cases[0].reason_code == "source_not_registered"


def test_acceptance_smoke_reviews_when_answerable_case_has_no_evidence():
    report = run_approved_local_corpus_acceptance_smoke(
        cases=[
            AcceptanceCase(
                id="weak_case",
                query="完全不存在的专有术语 ABCXYZ",
                expected_mode="answerable",
                description="Expected answerable case with no matching evidence.",
            )
        ]
    )

    assert report.decision == "review"
    assert report.reason_code == "acceptance_needs_review"
    assert report.cases[0].status == "review"
    assert report.cases[0].reason_code == "expected_answerable_evidence_missing"


def test_acceptance_smoke_negative_control_passes_without_evidence():
    report = run_approved_local_corpus_acceptance_smoke(
        cases=[
            AcceptanceCase(
                id="negative",
                query="售后退款凭证规则",
                expected_mode="insufficient_evidence",
                description="Unrelated negative control.",
            )
        ]
    )

    assert report.decision == "go"
    assert report.cases[0].status == "ready"
    assert report.cases[0].reason_code == "negative_control_passed"


def test_acceptance_smoke_blocks_invalid_answer_citation():
    report = run_approved_local_corpus_acceptance_smoke(
        cases=[
            AcceptanceCase(
                id="invalid_citation",
                query="公司主营业务是什么？",
                expected_mode="answerable",
                description="Answer returns a citation outside retrieved evidence.",
            )
        ],
        client=_FakeInvalidCitationClient(),
    )

    assert report.decision == "blocked"
    assert report.cases[0].status == "blocked"
    assert report.cases[0].reason_code == "answer_citation_outside_retrieval_allowlist"
    assert report.cases[0].invalid_citations == ["company_profile_2025_trial#bad"]


class _FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


class _FakeInvalidCitationClient:
    def get(self, path):
        if path == "/api/rag/sources":
            return _FakeResponse(
                {
                    "knowledge_bases": [
                        {
                            "id": "company_profile_2025_trial",
                            "status": "ready",
                        }
                    ],
                    "graphs": [],
                }
            )
        return _FakeResponse(
            {
                "ok": True,
                "result": {
                    "documents": [
                        {
                            "document_id": "company_profile_2025_trial",
                            "title": "公司简介 2025 trial",
                        }
                    ]
                },
            }
        )

    def post(self, path, json):
        if path == "/api/rag/retrieve":
            return _FakeResponse(
                {
                    "ok": True,
                    "result": {
                        "documents": [
                            {
                                "source_id": "company_profile_2025_trial",
                                "citation": "company_profile_2025_trial#chunk-1",
                            }
                        ]
                    },
                }
            )
        return _FakeResponse(
            {
                "ok": True,
                "result": {
                    "answer_status": "answered",
                    "citations": ["company_profile_2025_trial#bad"],
                },
            }
        )
