import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase14_myprivateagent_provider_integration_acceptance_checkpoint import (
    export_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report,
)


def main() -> None:
    args = _parse_args()
    report = export_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report(
        output_dir=args.output_dir,
        base_dir=args.artifact_base_dir,
    )
    print(
        "Phase 14 MyPrivateAgent provider integration acceptance checkpoint JSON ready: "
        f"{report.json_path}"
    )
    print(
        "Phase 14 MyPrivateAgent provider integration acceptance checkpoint Markdown ready: "
        f"{report.markdown_path}"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Phase 14 MyPrivateAgent provider integration acceptance checkpoint."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/myprivateagent-provider-integration-acceptance"),
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
