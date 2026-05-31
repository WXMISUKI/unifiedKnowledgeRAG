import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase5_graph_use_case_readiness import (
    export_phase5_graph_use_case_readiness_report,
)


def main() -> None:
    args = _parse_args()
    report = export_phase5_graph_use_case_readiness_report(
        output_dir=args.output_dir,
        base_dir=args.artifact_base_dir,
    )
    print(f"Phase 5 graph use-case readiness JSON ready: {report.json_path}")
    print(f"Phase 5 graph use-case readiness Markdown ready: {report.markdown_path}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the local Phase 5 graph use-case readiness report."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/benchmark/chinese-seed/graph-use-case-readiness"),
    )
    parser.add_argument(
        "--artifact-base-dir",
        type=Path,
        default=Path("."),
        help="Base directory where local evidence artifacts are read from.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
