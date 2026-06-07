import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.approved_local_corpus_acceptance_smoke import DEFAULT_TOP_K
from app.services.local_business_corpus_trial import DEFAULT_QUERY, DEFAULT_SOURCE_ID, DEFAULT_TITLE
from app.services.local_enterprise_corpus_ingestion_qa_loop import (
    DEFAULT_INPUT_PATH,
    DEFAULT_OUTPUT_DIR,
    export_local_enterprise_corpus_ingestion_qa_loop_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run local enterprise corpus file ingestion and QA loop.",
    )
    parser.add_argument("--input-path", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_local_enterprise_corpus_ingestion_qa_loop_report(
        input_path=args.input_path,
        source_id=args.source_id,
        title=args.title,
        query=args.query,
        top_k=args.top_k,
        output_dir=args.output_dir,
    )
    print(f"Local enterprise corpus QA loop JSON ready: {report.json_path}")
    print(f"Local enterprise corpus QA loop Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
