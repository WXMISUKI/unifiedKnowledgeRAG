import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import get_settings
from app.services.retrieval_benchmark import export_qdrant_bge_smoke_evidence


def main() -> None:
    args = _parse_args()
    settings = get_settings().model_copy(
        update={
            "rag_retrieval_backend": "qdrant",
            "qdrant_url": args.qdrant_url,
            "qdrant_collection": args.qdrant_collection,
            "qdrant_vector_name": args.qdrant_vector_name,
            "qdrant_vector_size": args.qdrant_vector_size,
            "embedding_provider": args.embedding_provider,
            "embedding_model": args.embedding_model,
            "embedding_model_path": args.embedding_model_path,
            "embedding_vector_size": args.embedding_vector_size,
            "embedding_local_files_only": args.embedding_local_files_only,
            "rag_source_dir": args.source_dir,
            "rag_index_dir": args.index_dir,
        }
    )
    report = export_qdrant_bge_smoke_evidence(
        output_dir=args.output_dir,
        cases_path=args.cases_path,
        source_ids=args.source_id,
        case_ids=args.case_id,
        settings=settings,
    )
    print(f"Qdrant BGE-M3 smoke evidence ready: {report.json_path}")
    print(f"Qdrant BGE-M3 smoke evidence ready: {report.markdown_path}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export local Qdrant + BGE-M3 smoke retrieval evidence."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/benchmark/chinese-seed/retrieval-candidates"),
    )
    parser.add_argument(
        "--cases-path",
        type=Path,
        default=Path("tests/fixtures/retrieval_benchmark_cases.json"),
    )
    parser.add_argument(
        "--source-id",
        action="append",
        default=None,
        help="Source id to index. Can be supplied multiple times.",
    )
    parser.add_argument(
        "--case-id",
        action="append",
        default=None,
        help="Benchmark case id to query. Can be supplied multiple times.",
    )
    parser.add_argument("--source-dir", type=Path, default=Path("app/data/sources"))
    parser.add_argument("--index-dir", type=Path, default=Path("app/data/indexes/qdrant-smoke"))
    parser.add_argument("--qdrant-url", default=":memory:")
    parser.add_argument("--qdrant-collection", default="knowledge_chunks")
    parser.add_argument("--qdrant-vector-name", default="text-dense")
    parser.add_argument("--qdrant-vector-size", type=int, default=1024)
    parser.add_argument("--embedding-provider", default="bge_m3_local")
    parser.add_argument("--embedding-model", default="BAAI/bge-m3")
    parser.add_argument("--embedding-model-path", type=Path, default=Path("models/bge-m3"))
    parser.add_argument("--embedding-vector-size", type=int, default=1024)
    parser.add_argument("--embedding-local-files-only", action="store_true", default=True)
    parser.add_argument(
        "--allow-model-download",
        action="store_false",
        dest="embedding_local_files_only",
        help="Allow the embedding adapter to download model files if needed.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
