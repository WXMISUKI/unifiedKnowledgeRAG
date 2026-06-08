import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_business_rag_golden_cases import (
    DEFAULT_CASE_FILE,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SOURCE_ID,
    DEFAULT_TOP_K,
    export_local_business_rag_golden_cases,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export local business RAG golden cases and chunk-quality baseline.",
    )
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--case-file", type=Path, default=DEFAULT_CASE_FILE)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_local_business_rag_golden_cases(
        source_id=args.source_id,
        case_file=args.case_file,
        top_k=args.top_k,
        output_dir=args.output_dir,
    )
    print(f"Local business RAG golden cases JSON ready: {report.json_path}")
    print(f"Local business RAG golden cases Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    print(f"Hit rate: {report.summary['hit_rate']}")
    print(f"Citation match rate: {report.summary['citation_match_rate']}")
    print(f"Empty handling rate: {report.summary['empty_handling_rate']}")
    print(f"Chunk quality: {report.chunk_quality.status}")
    print(f"Chunk quality reason: {report.chunk_quality.reason_code}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
