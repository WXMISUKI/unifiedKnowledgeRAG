import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase11_source_binding_preview_smoke import (
    export_phase11_source_binding_preview_smoke_report,
)


def main() -> None:
    args = _parse_args()
    report = export_phase11_source_binding_preview_smoke_report(
        output_dir=args.output_dir,
        base_dir=args.artifact_base_dir,
    )
    print(f"Phase 11 source-binding preview smoke JSON ready: {report.json_path}")
    print(f"Phase 11 source-binding preview smoke Markdown ready: {report.markdown_path}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Phase 11 source-binding preview smoke."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/smoke/myprivateagent-local-provider-integration"),
    )
    parser.add_argument("--artifact-base-dir", type=Path, default=Path("."))
    return parser.parse_args()


if __name__ == "__main__":
    main()
