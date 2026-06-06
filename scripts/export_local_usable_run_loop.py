import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_usable_run_loop import (
    DEFAULT_BASE_URL,
    DEFAULT_QUERY,
    DEFAULT_SOURCE_ID,
    DEFAULT_TOP_K,
    export_local_usable_run_loop_report,
)


def main() -> None:
    args = _parse_args()
    report = export_local_usable_run_loop_report(
        output_dir=args.output_dir,
        base_url=args.base_url,
        query=args.query,
        source_id=args.source_id,
        top_k=args.top_k,
        provider_api_key=args.provider_api_key,
        timeout_seconds=args.timeout_seconds,
    )
    print(f"Local usable run-loop JSON ready: {report.json_path}")
    print(f"Local usable run-loop Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    if report.decision == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a local usability run-loop report for an already-running provider."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--source-id", default=DEFAULT_SOURCE_ID)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--timeout-seconds", type=float, default=5.0)
    parser.add_argument(
        "--provider-api-key",
        default=os.getenv("PROVIDER_API_KEY"),
        help="Optional provider API key. Defaults to PROVIDER_API_KEY.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/local-run"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
