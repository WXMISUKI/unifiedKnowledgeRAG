import json
from pathlib import Path

from app.services.phase3_fp_fn_review import (
    build_phase3_fp_fn_review_report,
    export_phase3_fp_fn_review_report,
    phase3_fp_fn_review_report_to_dict,
    render_phase3_fp_fn_review_markdown,
)


def test_build_phase3_fp_fn_review_report_classifies_fp_and_fn(tmp_path):
    benchmark_path = tmp_path / "baseline.json"
    benchmark_path.write_text(
        json.dumps(
            {
                "report": {
                    "cases": [
                        {
                            "id": "ok-non-empty",
                            "category": "policy",
                            "expect_empty": False,
                            "hit_at_k": True,
                            "citation_match": True,
                            "empty_query_handling": None,
                            "returned_citations": ["c1"],
                        },
                        {
                            "id": "fp-empty-case",
                            "category": "empty",
                            "hit_at_k": False,
                            "citation_match": False,
                            "empty_query_handling": False,
                            "returned_citations": ["c-fp"],
                        },
                        {
                            "id": "fn-non-empty-case",
                            "category": "policy-nuance",
                            "expect_empty": False,
                            "hit_at_k": False,
                            "citation_match": False,
                            "empty_query_handling": None,
                            "returned_citations": [],
                        },
                    ]
                }
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = build_phase3_fp_fn_review_report(benchmark_path)

    assert report.total_cases == 3
    assert report.false_positive_count == 1
    assert report.false_negative_count == 1
    assert report.false_positive_rate == 0.3333
    assert report.false_negative_rate == 0.3333
    assert [item.id for item in report.false_positive_cases] == ["fp-empty-case"]
    assert [item.id for item in report.false_negative_cases] == ["fn-non-empty-case"]


def test_export_phase3_fp_fn_review_report_writes_json_and_markdown(tmp_path):
    benchmark_path = tmp_path / "baseline.json"
    benchmark_path.write_text(
        json.dumps(
            {
                "report": {
                    "cases": [
                        {
                            "id": "fp-empty-case",
                            "category": "empty",
                            "expect_empty": True,
                            "hit_at_k": False,
                            "citation_match": False,
                            "empty_query_handling": False,
                            "returned_citations": ["c-fp"],
                        }
                    ]
                }
            }
        ),
        encoding="utf-8",
    )

    report = export_phase3_fp_fn_review_report(
        benchmark_report_path=benchmark_path,
        output_dir=tmp_path / "review",
    )

    assert report.json_path == tmp_path / "review" / "phase3-fp-fn-review.json"
    assert report.markdown_path == tmp_path / "review" / "phase3-fp-fn-review.md"
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")
    assert payload == phase3_fp_fn_review_report_to_dict(report)
    assert "# Phase 3 FP/FN Review Report" in markdown
    assert "| False Positive Count | `1` |" in markdown
    assert render_phase3_fp_fn_review_markdown(report) == markdown


def test_build_phase3_fp_fn_review_report_rejects_invalid_payload(tmp_path):
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text(json.dumps({"summary": {}}), encoding="utf-8")

    try:
        build_phase3_fp_fn_review_report(invalid_path)
    except ValueError as error:
        assert "missing report" in str(error)
    else:
        raise AssertionError("Expected invalid benchmark report to be rejected")
