import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase16_myprivateagent_minimal_access_loop import (
    export_phase16_myprivateagent_minimal_access_loop_report,
)


def main() -> None:
    args = _parse_args()
    report = export_phase16_myprivateagent_minimal_access_loop_report(
        output_dir=args.output_dir,
        base_dir=args.artifact_base_dir,
    )
    print(
        "Phase 16 MyPrivateAgent minimal access loop JSON ready: "
        f"{report.json_path}"
    )
    print(
        "Phase 16 MyPrivateAgent minimal access loop Markdown ready: "
        f"{report.markdown_path}"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Phase 16 MyPrivateAgent minimal access loop."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/myprivateagent-minimal-access-loop"),
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
