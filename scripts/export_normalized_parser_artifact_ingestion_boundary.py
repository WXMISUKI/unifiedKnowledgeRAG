import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.normalized_parser_artifact_ingestion_boundary import (
    DEFAULT_ARTIFACT_PATH,
    DEFAULT_OUTPUT_DIR,
    export_normalized_parser_artifact_ingestion_boundary_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and materialize a normalized external parser artifact.",
    )
    parser.add_argument("--artifact-path", type=Path, default=DEFAULT_ARTIFACT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_normalized_parser_artifact_ingestion_boundary_report(
        artifact_path=args.artifact_path,
        output_dir=args.output_dir,
    )
    print(f"Normalized parser artifact boundary JSON ready: {report.json_path}")
    print(f"Normalized parser artifact boundary Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    if report.markdown_artifact_path is not None:
        print(f"Materialized Markdown: {report.markdown_artifact_path}")
    if report.source_overlay_path is not None:
        print(f"Source Overlay: {report.source_overlay_path}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
