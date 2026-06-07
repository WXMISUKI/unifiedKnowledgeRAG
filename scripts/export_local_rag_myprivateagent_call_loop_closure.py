import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.local_rag_myprivateagent_call_loop_closure import (
    DEFAULT_MYPRIVATEAGENT_REPORT_PATH,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PROVIDER_REPORT_PATH,
    export_local_rag_myprivateagent_call_loop_closure,
)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    report = export_local_rag_myprivateagent_call_loop_closure(
        provider_report_path=args.provider_report,
        myprivateagent_report_path=args.myprivateagent_report,
        output_dir=args.output_dir,
    )
    print(f"Local RAG MyPrivateAgent closure JSON ready: {report.json_path}")
    print(f"Local RAG MyPrivateAgent closure Markdown ready: {report.markdown_path}")
    print(f"Decision: {report.decision}")
    print(f"Reason: {report.reason_code}")
    if report.decision == "go":
        return 0
    if report.decision == "review":
        return 2
    return 1


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a read-only closure report over provider live HTTP and MyPrivateAgent local corpus trials.",
    )
    parser.add_argument("--provider-report", type=Path, default=DEFAULT_PROVIDER_REPORT_PATH)
    parser.add_argument("--myprivateagent-report", type=Path, default=DEFAULT_MYPRIVATEAGENT_REPORT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
