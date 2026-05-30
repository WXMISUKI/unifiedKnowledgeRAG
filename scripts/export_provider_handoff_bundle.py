import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.provider_handoff_bundle import export_provider_handoff_bundle_report


def main() -> None:
    args = _parse_args()
    report = export_provider_handoff_bundle_report(
        output_dir=args.output_dir,
        base_dir=args.base_dir,
    )
    print(f"Provider handoff bundle JSON ready: {report.json_path}")
    print(f"Provider handoff bundle Markdown ready: {report.markdown_path}")
    if report.status == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a read-only provider handoff evidence bundle."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/provider-handoff"),
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("."),
        help="Base directory for reading prerequisite evidence artifacts.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
