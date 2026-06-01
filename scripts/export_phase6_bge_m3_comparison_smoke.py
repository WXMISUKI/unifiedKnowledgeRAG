from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.phase6_bge_m3_comparison_smoke import (
    export_phase6_bge_m3_comparison_smoke_report,
)


def main() -> None:
    report = export_phase6_bge_m3_comparison_smoke_report()
    print(f"Phase 6 BGE-M3 comparison smoke report ready: {report.json_path}")
    print(f"Phase 6 BGE-M3 comparison smoke report ready: {report.markdown_path}")


if __name__ == "__main__":
    main()
