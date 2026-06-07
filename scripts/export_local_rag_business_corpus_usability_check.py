import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.approved_local_corpus_acceptance_smoke import DEFAULT_SOURCE_ID, DEFAULT_TOP_K
from app.services.approved_local_corpus_live_http_smoke import DEFAULT_BASE_URL, DEFAULT_TIMEOUT_SECONDS
from app.services.local_business_corpus_trial import DEFAULT_MARKDOWN_PATH, DEFAULT_QUERY, DEFAULT_TITLE
from app.services.local_rag_business_corpus_usability_check import (
    DEFAULT_OUTPUT_DIR,
    export_local_rag_business_corpus_usability_check,
)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    report = export_local_rag_business_corpus_usability_check(
        markdown_path=args.markdown_path,
        source_id=args.source_id,
        title=args.title,
        query=args.query,
        top_k=args.top_k,
        output_dir=args.output_dir,
        base_url=args.base_url,
        include_live_http=args.include_live_http,
        provider_api_key=args.provider_api_key,
        timeout_seconds=args.timeout_seconds,
    )
    print(f"Local RAG business corpus usability JSON ready: {report.json_path}")
    print(f"Local RAG business corpus usability Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    if report.decision == "go":
        return 0
    if report.decision == "review":
        return 2
    return 1


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a lightweight local RAG business corpus usability check.",
    )
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--include-live-http", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument(
        "--provider-api-key",
        default=os.getenv("PROVIDER_API_KEY"),
        help="Optional provider API key. Defaults to PROVIDER_API_KEY.",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
