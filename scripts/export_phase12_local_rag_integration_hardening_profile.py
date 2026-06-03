import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase12_local_rag_integration_hardening_profile import (
    export_phase12_local_rag_integration_hardening_profile_report,
)


def main() -> None:
    args = _parse_args()
    report = export_phase12_local_rag_integration_hardening_profile_report(
        output_dir=args.output_dir,
        base_dir=args.artifact_base_dir,
    )
    print(f"Phase 12 local hardening profile JSON ready: {report.json_path}")
    print(f"Phase 12 local hardening profile Markdown ready: {report.markdown_path}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Phase 12 local RAG integration hardening profile."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/myprivateagent-local-rag-integration-hardening"),
    )
    parser.add_argument(
        "--artifact-base-dir",
        type=Path,
        default=Path("."),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
