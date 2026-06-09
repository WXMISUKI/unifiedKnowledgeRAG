import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.source_evaluation_pack_onboarding import (
    DEFAULT_ONBOARDING_ROOT,
    export_source_evaluation_pack_onboarding,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export source evaluation pack onboarding templates.",
    )
    parser.add_argument("--source-id", default="source_template_example")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_ONBOARDING_ROOT)
    args = parser.parse_args()

    report = export_source_evaluation_pack_onboarding(
        source_id=args.source_id,
        output_root=args.output_root,
    )
    print(f"Onboarding JSON ready: {report.json_path}")
    print(f"Onboarding Markdown ready: {report.markdown_path}")
    print(f"Source ID: {report.source_id}")
    print(f"Template count: {report.summary['template_count']}")
    print(f"Output dir: {report.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
