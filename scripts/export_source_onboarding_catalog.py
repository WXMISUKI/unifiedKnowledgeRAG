import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_business_rag_golden_cases import DEFAULT_OUTPUT_DIR
from app.services.source_evaluation_pack_onboarding import DEFAULT_ONBOARDING_ROOT
from app.services.source_onboarding_catalog import export_source_onboarding_catalog


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export source onboarding catalog discovery bridge.",
    )
    parser.add_argument("--onboarding-root", type=Path, default=DEFAULT_ONBOARDING_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_source_onboarding_catalog(
        onboarding_root=args.onboarding_root,
        output_dir=args.output_dir,
    )
    print(f"Source onboarding catalog JSON ready: {report.json_path}")
    print(f"Source onboarding catalog Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    print(f"Source count: {report.summary['source_count']}")
    print(f"Ready source count: {report.summary['ready_source_count']}")
    print(f"Template-only source count: {report.summary['template_only_source_count']}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
