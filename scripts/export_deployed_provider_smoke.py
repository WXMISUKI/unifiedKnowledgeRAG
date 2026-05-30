import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.deployed_provider_smoke import export_deployed_provider_smoke_report


def main() -> None:
    args = _parse_args()
    provider_api_key = args.provider_api_key or os.getenv("PROVIDER_API_KEY")
    report = export_deployed_provider_smoke_report(
        output_dir=args.output_dir,
        base_url=args.base_url,
        provider_api_key=provider_api_key,
        timeout_seconds=args.timeout_seconds,
    )
    print(f"Deployed provider smoke JSON ready: {report.json_path}")
    print(f"Deployed provider smoke Markdown ready: {report.markdown_path}")
    if report.status == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export deployed provider smoke evidence from a running HTTP provider."
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8020",
        help="Running provider base URL.",
    )
    parser.add_argument(
        "--provider-api-key",
        default=None,
        help="Optional provider API key. If omitted, PROVIDER_API_KEY is used.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=5.0,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/deployed-provider-smoke"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
