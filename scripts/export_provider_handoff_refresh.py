import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.provider_handoff_refresh import refresh_provider_handoff_evidence


def main() -> None:
    args = _parse_args()
    report = refresh_provider_handoff_evidence(
        output_dir=args.output_dir,
        artifact_base_dir=args.artifact_base_dir,
    )
    print(f"Provider handoff refresh JSON ready: {report.json_path}")
    print(f"Provider handoff refresh Markdown ready: {report.markdown_path}")
    if report.status == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh provider handoff prerequisite evidence and bundle."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/provider-handoff-refresh"),
    )
    parser.add_argument(
        "--artifact-base-dir",
        type=Path,
        default=Path("."),
        help="Base directory where refreshed evidence artifacts are written.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
