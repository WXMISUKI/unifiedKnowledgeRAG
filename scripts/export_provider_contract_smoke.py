import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.provider_contract_smoke import export_provider_contract_smoke_report


def main() -> None:
    args = _parse_args()
    report = export_provider_contract_smoke_report(output_dir=args.output_dir)
    print(f"Provider contract smoke JSON ready: {report.json_path}")
    print(f"Provider contract smoke Markdown ready: {report.markdown_path}")
    if not report.passed:
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export provider contract smoke evidence for local integration checks."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/smoke/provider-contract"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
