import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.approved_local_corpus_acceptance_smoke import DEFAULT_TOP_K
from app.services.local_business_corpus_trial import DEFAULT_QUERY
from app.services.normalized_parser_artifact_ingestion_boundary import DEFAULT_ARTIFACT_PATH
from app.services.parser_artifact_local_ingestion_loop import (
    DEFAULT_OUTPUT_DIR,
    export_parser_artifact_local_ingestion_loop_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the parser artifact local ingestion loop.",
    )
    parser.add_argument("--artifact-path", type=Path, default=DEFAULT_ARTIFACT_PATH)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_parser_artifact_local_ingestion_loop_report(
        artifact_path=args.artifact_path,
        query=args.query,
        top_k=args.top_k,
        output_dir=args.output_dir,
    )
    print(f"Parser artifact local ingestion loop JSON ready: {report.json_path}")
    print(f"Parser artifact local ingestion loop Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
