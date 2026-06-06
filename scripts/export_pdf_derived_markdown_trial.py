import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.pdf_derived_markdown_corpus_trial import (
    DEFAULT_MAX_PAGES,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_QUERY,
    DEFAULT_SOURCE_ID,
    export_pdf_derived_markdown_trial_report,
)


def main() -> None:
    args = _parse_args()
    report = export_pdf_derived_markdown_trial_report(
        pdf_path=args.pdf_path,
        output_dir=args.output_dir,
        source_id=args.source_id,
        query=args.query,
        max_pages=args.max_pages,
    )
    print(f"PDF-derived markdown ready: {report.markdown_path}")
    print(f"PDF-derived trial JSON ready: {report.json_path}")
    print(f"PDF-derived trial Markdown ready: {report.report_markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    if report.decision == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export a local PDF-derived markdown corpus trial report. "
            "Raw PDF remains unsupported by provider ingestion."
        )
    )
    parser.add_argument("--pdf-path", type=Path, required=True)
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    main()
