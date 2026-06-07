import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.approved_local_corpus_acceptance_smoke import (
    DEFAULT_SOURCE_ID,
    DEFAULT_TOP_K,
)
from app.services.approved_local_corpus_live_http_smoke import (
    DEFAULT_BASE_URL,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TIMEOUT_SECONDS,
    export_approved_local_corpus_live_http_smoke,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Export a live HTTP smoke for a registered approved local corpus source."
        ),
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--case-file", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument(
        "--provider-api-key",
        default=os.getenv("PROVIDER_API_KEY"),
        help="Optional provider API key. Defaults to PROVIDER_API_KEY.",
    )
    args = parser.parse_args()

    report = export_approved_local_corpus_live_http_smoke(
        base_url=args.base_url,
        source_id=args.source_id,
        top_k=args.top_k,
        case_file=args.case_file,
        output_dir=args.output_dir,
        provider_api_key=args.provider_api_key,
        timeout_seconds=args.timeout_seconds,
    )
    print(f"Approved local corpus live HTTP JSON ready: {report.json_path}")
    print(f"Approved local corpus live HTTP Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    return 0 if report.decision != "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
