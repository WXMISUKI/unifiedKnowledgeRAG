import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.reindex_readiness import export_reindex_readiness_report


def main() -> None:
    args = _parse_args()
    report = export_reindex_readiness_report(output_dir=args.output_dir)
    print(f"Reindex readiness JSON ready: {report.json_path}")
    print(f"Reindex readiness Markdown ready: {report.markdown_path}")
    if report.status == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a read-only reindex readiness plan."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/operations/reindex-readiness"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
