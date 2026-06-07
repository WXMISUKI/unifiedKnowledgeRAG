import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.approved_local_corpus_acceptance_smoke import DEFAULT_TOP_K
from app.services.local_business_corpus_trial import DEFAULT_QUERY, DEFAULT_SOURCE_ID, DEFAULT_TITLE
from app.services.local_pdf_parser_provider_bridge import (
    DEFAULT_MAX_PAGES,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PDF_PATH,
    DEFAULT_PROVIDER_PATH,
    DEFAULT_PROVIDER_URL,
    export_local_pdf_parser_provider_bridge_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run local PDF parser provider bridge into the RAG ingestion loop.",
    )
    parser.add_argument("--pdf-path", type=Path, default=DEFAULT_PDF_PATH)
    parser.add_argument("--provider-url", default=DEFAULT_PROVIDER_URL)
    parser.add_argument("--provider-path", default=DEFAULT_PROVIDER_PATH)
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_local_pdf_parser_provider_bridge_report(
        pdf_path=args.pdf_path,
        provider_url=args.provider_url,
        provider_path=args.provider_path,
        source_id=args.source_id,
        title=args.title,
        query=args.query,
        top_k=args.top_k,
        max_pages=args.max_pages,
        output_dir=args.output_dir,
    )
    print(f"Local PDF parser provider bridge JSON ready: {report.json_path}")
    print(f"Local PDF parser provider bridge Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
