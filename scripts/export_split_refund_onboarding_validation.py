import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_business_rag_golden_cases import export_local_business_rag_golden_cases
from app.services.source_evaluation_pack_onboarding import (
    DEFAULT_ONBOARDING_ROOT,
    export_source_evaluation_pack_onboarding,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate onboarding template path with split_refund_policy_docs.",
    )
    parser.add_argument("--source-id", default="split_refund_policy_docs")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_ONBOARDING_ROOT,
    )
    args = parser.parse_args()

    onboarding_report = export_source_evaluation_pack_onboarding(
        source_id=args.source_id,
        output_root=args.output_root,
    )
    output_dir = onboarding_report.output_dir
    case_file = output_dir / "baseline-pack.fixture.json"
    report = export_local_business_rag_golden_cases(
        source_id=args.source_id,
        case_file=case_file,
        output_dir=output_dir,
    )

    split_json = output_dir / "split-refund-local-business-rag-golden-cases.json"
    split_md = output_dir / "split-refund-local-business-rag-golden-cases.md"
    report.json_path.rename(split_json)
    report.markdown_path.rename(split_md)

    print(f"Onboarding JSON ready: {onboarding_report.json_path}")
    print(f"Baseline fixture: {case_file}")
    print(f"Validation JSON ready: {split_json}")
    print(f"Validation Markdown ready: {split_md}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    print(f"Hit rate: {report.summary['hit_rate']}")
    print(f"Empty handling rate: {report.summary['empty_handling_rate']}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
