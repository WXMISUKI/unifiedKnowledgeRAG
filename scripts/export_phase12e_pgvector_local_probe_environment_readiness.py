import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase12e_pgvector_local_probe_environment_readiness import (
    export_phase12e_pgvector_local_probe_environment_readiness_report,
)


def main() -> None:
    args = _parse_args()
    report = export_phase12e_pgvector_local_probe_environment_readiness_report(
        output_dir=args.output_dir,
        base_dir=args.artifact_base_dir,
    )
    print(
        "Phase 12e pgvector local probe environment readiness JSON ready: "
        f"{report.json_path}"
    )
    print(
        "Phase 12e pgvector local probe environment readiness Markdown ready: "
        f"{report.markdown_path}"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the local Phase 12e pgvector probe environment readiness report."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/operations/pgvector-local-probe-environment"),
    )
    parser.add_argument(
        "--artifact-base-dir",
        type=Path,
        default=Path("."),
        help="Base directory where benchmark and evidence artifacts are read from.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
