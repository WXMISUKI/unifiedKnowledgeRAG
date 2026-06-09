from pathlib import Path

from app.services.local_business_rag_golden_cases import export_local_business_rag_golden_cases
from app.services.source_evaluation_pack_onboarding import (
    export_source_evaluation_pack_onboarding,
)


def test_invoice_policy_real_source_can_pass_minimal_baseline(tmp_path):
    output_root = tmp_path / "onboarding"
    onboarding_report = export_source_evaluation_pack_onboarding(
        source_id="invoice_policy_faq",
        output_root=output_root,
    )
    case_file = output_root / "invoice_policy_faq" / "baseline-pack.fixture.json"
    case_file.write_text(
        Path(
            "docs/local-run/business-rag-golden-cases/onboarding/"
            "invoice_policy_faq/baseline-pack.fixture.json"
        ).read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    report = export_local_business_rag_golden_cases(
        source_id="invoice_policy_faq",
        case_file=case_file,
        output_dir=onboarding_report.output_dir,
    )

    assert report.decision == "go"
    assert report.reason_code == "local_business_rag_baseline_go"
    assert report.summary["case_count"] == 3
    assert report.summary["hit_rate"] == 1.0
    assert report.summary["empty_handling_rate"] == 1.0
    assert report.chunk_quality.status == "ready"


def test_invoice_policy_source_is_provider_visible():
    from app.services.source_catalog import list_knowledge_bases
    from app.services.source_document_manifest import get_source_document_manifest

    ids = {source.id for source in list_knowledge_bases()}
    assert "invoice_policy_faq" in ids

    manifest = get_source_document_manifest("invoice_policy_faq")
    assert manifest.ok is True
    assert manifest.result is not None
    assert manifest.result.documents[0].document_id == "invoice_policy_faq_2026"
