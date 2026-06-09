import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_business_rag_golden_cases import DEFAULT_OUTPUT_DIR
from app.services.source_evaluation_pack_catalog import (
    export_source_evaluation_pack_catalog,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export unified source evaluation pack catalog.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_source_evaluation_pack_catalog(output_dir=args.output_dir)
    print(f"Source evaluation pack catalog JSON ready: {report.json_path}")
    print(f"Source evaluation pack catalog Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    print(f"Pack count: {report.summary['pack_count']}")
    print(f"Available pack count: {report.summary['available_pack_count']}")
    print(f"Missing pack count: {report.summary['missing_pack_count']}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
