import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase3_fp_fn_review import export_phase3_fp_fn_review_report


def main() -> None:
    args = _parse_args()
    report = export_phase3_fp_fn_review_report(
        benchmark_report_path=args.benchmark_report_path,
        output_dir=args.output_dir,
    )
    print(f"Phase 3 FP/FN review JSON ready: {report.json_path}")
    print(f"Phase 3 FP/FN review Markdown ready: {report.markdown_path}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a local read-only Phase 3 FP/FN review report."
    )
    parser.add_argument(
        "--benchmark-report-path",
        type=Path,
        default=Path(
            "docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/benchmark/chinese-seed/fp-fn-review"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
