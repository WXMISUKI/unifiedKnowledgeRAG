import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_business_rag_golden_cases import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_REFUND_ORGANIZATION_CONFIRMATION_CASE_FILE,
    DEFAULT_TOP_K,
    export_refund_organization_negative_control_confirmation,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export refund organization negative-control confirmation baseline.",
    )
    parser.add_argument(
        "--case-file",
        type=Path,
        default=DEFAULT_REFUND_ORGANIZATION_CONFIRMATION_CASE_FILE,
    )
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_refund_organization_negative_control_confirmation(
        case_file=args.case_file,
        top_k=args.top_k,
        output_dir=args.output_dir,
    )
    print(f"Refund confirmation JSON ready: {report.json_path}")
    print(f"Refund confirmation Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    print(f"Likely failure class: {report.summary['likely_failure_class']}")
    print(f"Recommended next gate: {report.summary['recommended_next_gate']}")
    print(f"Variant count: {report.summary['variant_count']}")
    print(
        "Expected-empty review count: "
        f"{report.summary['expected_empty_review_count']}"
    )
    print(f"Answerable pass count: {report.summary['answerable_pass_count']}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
