import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase9_myprivateagent_local_consumption_readiness import (
    export_phase9_myprivateagent_local_consumption_readiness_report,
)


def main() -> None:
    args = _parse_args()
    report = export_phase9_myprivateagent_local_consumption_readiness_report(
        output_dir=args.output_dir,
        base_dir=args.artifact_base_dir,
    )
    print(f"Phase 9 local consumption readiness JSON ready: {report.json_path}")
    print(
        "Phase 9 local consumption readiness Markdown ready: "
        f"{report.markdown_path}"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the local Phase 9 MyPrivateAgent consumption readiness report."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/myprivateagent-local-consumption"),
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
