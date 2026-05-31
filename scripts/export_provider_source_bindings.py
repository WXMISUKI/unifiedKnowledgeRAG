import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.provider_source_binding import export_provider_source_binding_summary


def main() -> None:
    args = _parse_args()
    report = export_provider_source_binding_summary(output_dir=args.output_dir)
    print(
        "Provider source binding summary JSON ready: "
        f"{args.output_dir / 'provider-source-bindings.json'}"
    )
    print(
        "Provider source binding summary Markdown ready: "
        f"{args.output_dir / 'provider-source-bindings.md'}"
    )
    if report.status == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export provider source binding summary evidence."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/source-bindings"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
