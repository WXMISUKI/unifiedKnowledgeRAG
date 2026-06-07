from pathlib import Path
from types import SimpleNamespace

import httpx

from app.services.local_pdf_parser_provider_bridge import (
    export_local_pdf_parser_provider_bridge_report,
    run_local_pdf_parser_provider_bridge,
)


def test_local_pdf_parser_provider_bridge_go_writes_artifact_and_runs_downstream(tmp_path):
    pdf_path = _write_pdf(tmp_path)
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=_ocr_response(["公司主营业务包括工程咨询。", "公司服务对象覆盖能源行业。"]))

    report = export_local_pdf_parser_provider_bridge_report(
        pdf_path=pdf_path,
        source_id="company_profile_2025_trial",
        title="公司简介 2025 trial",
        output_dir=tmp_path / "out",
        client=httpx.Client(base_url="http://provider.test", transport=httpx.MockTransport(handler)),
        downstream_exporter=_downstream_exporter("go"),
    )

    assert report.decision == "go"
    assert report.reason_code == "local_pdf_parser_provider_bridge_ready"
    assert requests[0].url.path == "/ocr"
    assert report.artifact_path.exists()
    artifact = report.artifact_path.read_text(encoding="utf-8")
    assert '"parser_id": "paddleocr-http-ocr-provider-v1"' in artifact
    assert '"citation": "company_profile_2025_trial#page-1"' in artifact
    assert [step.id for step in report.steps] == [
        "parser_provider_call",
        "normalized_parser_artifact",
        "parser_artifact_local_ingestion_loop",
    ]
    assert report.summary["myprivateagent_call_status"] == "not_called"
    assert report.summary["ocr_service_start_status"] == "not_started"
    assert report.json_path.exists()
    assert report.markdown_path.exists()


def test_local_pdf_parser_provider_bridge_blocks_when_provider_unreachable(tmp_path):
    pdf_path = _write_pdf(tmp_path)

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    report = run_local_pdf_parser_provider_bridge(
        pdf_path=pdf_path,
        output_dir=tmp_path / "out",
        client=httpx.Client(base_url="http://provider.test", transport=httpx.MockTransport(handler)),
        downstream_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "parser_provider_unreachable"
    assert [step.id for step in report.steps] == ["parser_provider_call"]
    assert report.artifact_path is None


def test_local_pdf_parser_provider_bridge_blocks_when_provider_returns_no_text(tmp_path):
    pdf_path = _write_pdf(tmp_path)

    report = run_local_pdf_parser_provider_bridge(
        pdf_path=pdf_path,
        output_dir=tmp_path / "out",
        client=httpx.Client(
            base_url="http://provider.test",
            transport=httpx.MockTransport(lambda request: httpx.Response(200, json=_ocr_response([]))),
        ),
        downstream_exporter=_should_not_run,
    )

    assert report.decision == "blocked"
    assert report.reason_code == "parser_provider_returned_no_text"
    assert report.steps[0].summary["text_block_count"] == 0


def test_local_pdf_parser_provider_bridge_reviews_when_downstream_reviews(tmp_path):
    pdf_path = _write_pdf(tmp_path)

    report = run_local_pdf_parser_provider_bridge(
        pdf_path=pdf_path,
        output_dir=tmp_path / "out",
        client=httpx.Client(
            base_url="http://provider.test",
            transport=httpx.MockTransport(lambda request: httpx.Response(200, json=_ocr_response(["公司简介"]))),
        ),
        downstream_exporter=_downstream_exporter("review", reason_code="artifact_missing_citation_anchors"),
    )

    assert report.decision == "review"
    assert report.reason_code == "downstream_artifact_missing_citation_anchors"
    assert report.downstream["decision"] == "review"


def test_local_pdf_parser_provider_bridge_blocks_when_downstream_blocks(tmp_path):
    pdf_path = _write_pdf(tmp_path)

    report = run_local_pdf_parser_provider_bridge(
        pdf_path=pdf_path,
        output_dir=tmp_path / "out",
        client=httpx.Client(
            base_url="http://provider.test",
            transport=httpx.MockTransport(lambda request: httpx.Response(200, json=_ocr_response(["公司简介"]))),
        ),
        downstream_exporter=_downstream_exporter("blocked", reason_code="ingestion_preflight_blocked"),
    )

    assert report.decision == "blocked"
    assert report.reason_code == "downstream_ingestion_preflight_blocked"


def _write_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "company.pdf"
    path.write_bytes(b"%PDF-1.7 local test")
    return path


def _ocr_response(texts: list[str]) -> dict:
    return {
        "errorCode": 0,
        "result": {
            "ocrResults": [
                {
                    "prunedResult": {
                        "rec_texts": texts,
                        "rec_scores": [0.99 for _ in texts],
                    }
                }
            ]
        },
    }


def _downstream_exporter(decision: str, *, reason_code: str | None = None):
    def exporter(*, output_dir, artifact_path, **kwargs):
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "parser-artifact-local-ingestion-loop.json"
        markdown_path = output_dir / "parser-artifact-local-ingestion-loop.md"
        materialized_path = output_dir / "parser-derived-source.md"
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# report\n", encoding="utf-8")
        materialized_path.write_text("# source\n", encoding="utf-8")
        return SimpleNamespace(
            decision=decision,
            reason_code=reason_code or f"downstream_{decision}",
            artifact_id="company_profile_2025_trial_paddleocr_pdf_pages_1_5",
            source_id="company_profile_2025_trial",
            materialized_markdown_path=materialized_path if decision != "blocked" else None,
            source_overlay_path=output_dir / "source-overlay.json" if decision != "blocked" else None,
            json_path=json_path,
            markdown_path=markdown_path,
            summary={"final_decision": decision},
        )

    return exporter


def _should_not_run(**kwargs):
    raise AssertionError("downstream should not run")
