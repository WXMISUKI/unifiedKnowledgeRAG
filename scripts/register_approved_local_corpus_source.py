import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.approved_local_corpus_source_registration import (
    DEFAULT_HANDOFF_PATH,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_REGISTRY_PATH,
    DEFAULT_SOURCE_DIR,
    register_approved_local_corpus_source,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Register a ready local corpus handoff as an approved local provider source.",
    )
    parser.add_argument("--handoff", type=Path, default=DEFAULT_HANDOFF_PATH)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    result = register_approved_local_corpus_source(
        handoff_path=args.handoff,
        registry_path=args.registry,
        source_dir=args.source_dir,
        output_dir=args.output_dir,
    )
    print(f"Approved local source registration JSON ready: {result.json_path}")
    print(f"Approved local source registration Markdown ready: {result.markdown_path}")
    print(f"Status: {result.status}")
    print(f"Reason: {result.reason_code}")
    print(f"Registration Status: {result.registration_status}")
    return 0 if result.status == "registered" else 1


if __name__ == "__main__":
    raise SystemExit(main())
