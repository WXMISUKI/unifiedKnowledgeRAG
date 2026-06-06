import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase25_myprivateagent_live_trial_outcome_feedback import (
    export_phase25_live_trial_outcome_feedback_report,
)


def main() -> None:
    args = _parse_args()
    report = export_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=args.trial_outcome_path,
        output_dir=args.output_dir,
    )
    print(f"Phase 25 live trial outcome feedback JSON ready: {report.json_path}")
    print(f"Phase 25 live trial outcome feedback Markdown ready: {report.markdown_path}")
    print(f"Status: {report.status}")
    print(f"Provider action: {report.provider_action}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Phase 25 MyPrivateAgent live trial outcome feedback."
    )
    parser.add_argument(
        "--trial-outcome-path",
        type=Path,
        required=True,
        help="Explicit path to a MyPrivateAgent live trial outcome JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/integration/myprivateagent-live-trial-outcome-feedback"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
