from pathlib import Path

from app.services.local_business_rag_golden_cases import export_local_business_rag_golden_cases
from app.services.source_evaluation_pack_onboarding import (
    export_source_evaluation_pack_onboarding,
)
from app.services.source_onboarding_catalog import build_source_onboarding_catalog


def test_source_template_example_can_pass_minimal_baseline(tmp_path):
    output_root = tmp_path / "onboarding"
    onboarding_report = export_source_evaluation_pack_onboarding(
        source_id="source_template_example",
        output_root=output_root,
    )
    case_file = output_root / "source_template_example" / "baseline-pack.fixture.json"
    case_file.write_text(
        Path(
            "docs/local-run/business-rag-golden-cases/onboarding/"
            "source_template_example/baseline-pack.fixture.json"
        ).read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    report = export_local_business_rag_golden_cases(
        source_id="source_template_example",
        case_file=case_file,
        output_dir=onboarding_report.output_dir,
    )

    assert report.decision == "go"
    assert report.reason_code == "local_business_rag_baseline_go"
    assert report.summary["case_count"] == 3
    assert report.summary["hit_rate"] == 1.0
    assert report.summary["empty_handling_rate"] == 1.0
    assert report.chunk_quality.status == "ready"


def test_source_template_example_is_provider_visible():
    from app.services.source_catalog import list_knowledge_bases
    from app.services.source_document_manifest import get_source_document_manifest

    ids = {source.id for source in list_knowledge_bases()}
    assert "source_template_example" in ids

    manifest = get_source_document_manifest("source_template_example")
    assert manifest.ok is True
    assert manifest.result is not None
    assert manifest.result.documents[0].document_id == "source_template_example_2026"


def test_source_template_example_no_longer_looks_template_only(tmp_path):
    onboarding_root = tmp_path / "onboarding"
    source_dir = onboarding_root / "source_template_example"
    source_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        "baseline-pack.fixture.template.json",
        "failed-question-pack.fixture.template.json",
        "confirmation-pack.fixture.template.json",
        "baseline-pack.fixture.json",
    ):
        source_dir.joinpath(name).write_text("[]\n", encoding="utf-8")
    source_dir.joinpath("source-evaluation-pack-onboarding.json").write_text(
        '{"summary":{"template_count":3}}\n',
        encoding="utf-8",
    )
    source_dir.joinpath("source-template-local-business-rag-golden-cases.json").write_text(
        '{"decision":"go","reason_code":"local_business_rag_baseline_go"}\n',
        encoding="utf-8",
    )

    report = build_source_onboarding_catalog(
        onboarding_root=onboarding_root,
        output_dir=tmp_path,
    )

    entry = report.entries[0]
    assert entry.source_id == "source_template_example"
    assert entry.onboarding_status == "ready"
