import json

from app.services.source_evaluation_pack_catalog import (
    build_source_evaluation_pack_catalog,
    export_source_evaluation_pack_catalog,
)


def test_source_evaluation_pack_catalog_summarizes_existing_packs(tmp_path):
    _write_pack(
        tmp_path / "local-business-rag-golden-cases.json",
        report_id="local-business-rag-golden-cases-v1",
        decision="go",
        reason_code="local_business_rag_baseline_go",
        case_count=6,
    )
    _write_pack(
        tmp_path / "real-business-corpus-golden-cases.json",
        report_id="real-business-corpus-golden-cases-v1",
        decision="go",
        reason_code="real_business_corpus_baseline_go",
        case_count=12,
    )
    _write_pack(
        tmp_path / "real-failed-question-pack.json",
        report_id="real-failed-question-pack-baseline-v1",
        decision="review",
        reason_code="real_business_corpus_baseline_needs_review",
        case_count=6,
    )
    _write_pack(
        tmp_path / "refund-organization-negative-control-confirmation.json",
        report_id="refund-organization-negative-control-confirmation-v1",
        decision="review",
        reason_code="real_business_corpus_baseline_needs_review",
        case_count=8,
        extra_summary={
            "recommended_next_gate": "open_refund_negative_control_hardening_scope_review"
        },
    )

    report = build_source_evaluation_pack_catalog(output_dir=tmp_path)

    assert report.decision == "review"
    assert report.summary["pack_count"] == 4
    assert report.summary["available_pack_count"] == 4
    assert report.summary["baseline_pack_count"] == 2
    assert report.summary["failed_question_pack_count"] == 1
    assert report.summary["confirmation_pack_count"] == 1
    failed_pack = next(
        pack for pack in report.packs if pack.pack_type == "failed_question_pack"
    )
    assert failed_pack.recommended_next_gate == "confirm_failure_class_before_strategy_changes"
    confirmation_pack = next(
        pack for pack in report.packs if pack.pack_type == "confirmation_pack"
    )
    assert (
        confirmation_pack.recommended_next_gate
        == "open_refund_negative_control_hardening_scope_review"
    )


def test_source_evaluation_pack_catalog_marks_missing_artifacts(tmp_path):
    _write_pack(
        tmp_path / "local-business-rag-golden-cases.json",
        report_id="local-business-rag-golden-cases-v1",
        decision="go",
        reason_code="local_business_rag_baseline_go",
        case_count=6,
    )

    report = export_source_evaluation_pack_catalog(output_dir=tmp_path)

    assert report.decision == "review"
    assert report.summary["missing_pack_count"] == 3
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    assert payload["summary"]["missing_pack_count"] == 3


def _write_pack(
    path,
    *,
    report_id: str,
    decision: str,
    reason_code: str,
    case_count: int,
    extra_summary: dict | None = None,
):
    path.write_text(
        json.dumps(
            {
                "id": report_id,
                "decision": decision,
                "reason_code": reason_code,
                "summary": {
                    "case_count": case_count,
                    **(extra_summary or {}),
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
