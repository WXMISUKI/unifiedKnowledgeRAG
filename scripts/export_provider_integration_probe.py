import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.provider_integration_client import (
    export_provider_integration_probe_report,
)


def main() -> None:
    args = _parse_args()
    report = export_provider_integration_probe_report(
        output_dir=args.output_dir,
        required_contract_version=args.required_contract_version,
        required_capability_ids=args.required_capability_ids,
    )
    print(f"Provider integration probe JSON ready: {report.json_path}")
    print(f"Provider integration probe Markdown ready: {report.markdown_path}")
    if not report.bindable:
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export provider integration probe evidence for control-plane binding."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/provider-binding"),
    )
    parser.add_argument(
        "--required-contract-version",
        default="knowledge-provider-contract-v1",
    )
    parser.add_argument(
        "--required-capability-ids",
        action="append",
        default=None,
        help="Required capability id. Repeat to pass multiple ids.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
