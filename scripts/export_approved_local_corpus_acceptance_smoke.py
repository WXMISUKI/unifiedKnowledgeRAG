import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.approved_local_corpus_acceptance_smoke import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SOURCE_ID,
    DEFAULT_TOP_K,
    export_approved_local_corpus_acceptance_smoke,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export an acceptance smoke for a registered approved local corpus.",
    )
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--case-file", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    report = export_approved_local_corpus_acceptance_smoke(
        source_id=args.source_id,
        top_k=args.top_k,
        case_file=args.case_file,
        output_dir=args.output_dir,
    )
    print(f"Approved local corpus acceptance JSON ready: {report.json_path}")
    print(f"Approved local corpus acceptance Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
