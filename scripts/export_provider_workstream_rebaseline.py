import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.provider_workstream_rebaseline import (
    export_provider_workstream_rebaseline_report,
)


def main() -> None:
    args = _parse_args()
    report = export_provider_workstream_rebaseline_report(output_dir=args.output_dir)
    print(f"Provider workstream rebaseline JSON ready: {report.json_path}")
    print(f"Provider workstream rebaseline Markdown ready: {report.markdown_path}")
    print(f"Status: {report.status}")
    print(f"Decision: {report.decision}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export provider workstream rebaseline after access closure."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/roadmap/provider-workstream-rebaseline"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
