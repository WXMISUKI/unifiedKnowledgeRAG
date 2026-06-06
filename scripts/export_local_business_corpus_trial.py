import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_business_corpus_trial import (
    DEFAULT_DOMAIN,
    DEFAULT_LANGUAGE,
    DEFAULT_MARKDOWN_PATH,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_OWNER,
    DEFAULT_QUERY,
    DEFAULT_SENSITIVITY,
    DEFAULT_SOURCE_ID,
    DEFAULT_TITLE,
    DEFAULT_TOP_K,
    export_local_business_corpus_trial_report,
)


def main() -> None:
    args = _parse_args()
    report = export_local_business_corpus_trial_report(
        markdown_path=args.markdown_path,
        output_dir=args.output_dir,
        source_id=args.source_id,
        title=args.title,
        query=args.query,
        owner=args.owner,
        domain=args.domain,
        language=args.language,
        sensitivity=args.sensitivity,
        top_k=args.top_k,
    )
    print(f"Local business corpus overlay ready: {report.overlay_path}")
    print(f"Local business corpus chunks ready: {report.chunks_path}")
    print(f"Local business corpus trial JSON ready: {report.json_path}")
    print(f"Local business corpus trial Markdown ready: {report.report_markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    if report.decision == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export a local business corpus trial report for a markdown file. "
            "This does not register a formal provider source."
        )
    )
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--domain", default=DEFAULT_DOMAIN)
    parser.add_argument("--language", default=DEFAULT_LANGUAGE)
    parser.add_argument("--sensitivity", default=DEFAULT_SENSITIVITY)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    main()
