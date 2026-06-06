import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_corpus_caller_handoff import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TRIAL_REPORT_PATH,
    export_local_corpus_caller_handoff,
)


def main() -> None:
    args = _parse_args()
    handoff = export_local_corpus_caller_handoff(
        trial_report_path=args.trial_report,
        output_dir=args.output_dir,
    )
    print(f"Local corpus caller handoff JSON ready: {handoff.json_path}")
    print(f"Local corpus caller handoff Markdown ready: {handoff.markdown_path}")
    print(f"Status: {handoff.status}")
    print(f"Reason: {handoff.reason_code}")
    if handoff.status == "blocked":
        raise SystemExit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export a caller-facing handoff from a local business corpus trial report. "
            "This does not register a formal provider source."
        )
    )
    parser.add_argument("--trial-report", type=Path, default=DEFAULT_TRIAL_REPORT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


if __name__ == "__main__":
    main()
