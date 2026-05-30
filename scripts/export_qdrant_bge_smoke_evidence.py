import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import get_settings
from app.services.retrieval_benchmark import (
    export_qdrant_bge_chunking_comparison_evidence,
    export_qdrant_bge_exact_term_smoke_evidence,
    export_qdrant_bge_hybrid_empty_stress_evidence,
    export_qdrant_bge_hybrid_alias_gating_candidate_evidence,
    export_qdrant_bge_hybrid_exact_term_smoke_evidence,
    export_qdrant_bge_hybrid_gating_candidate_evidence,
    export_qdrant_bge_hybrid_multi_chunk_aggregation_evidence,
    export_qdrant_bge_smoke_evidence,
    export_qdrant_bge_threshold_sweep_evidence,
    export_qdrant_threshold_recommendation,
    export_identifier_alias_governance_evidence,
    ThresholdRecommendationGates,
)


def main() -> None:
    args = _parse_args()
    update = {
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
    if args.rag_score_threshold is not None:
        update["rag_score_threshold"] = args.rag_score_threshold
    settings = get_settings().model_copy(update=update)
    if args.alias_governance:
        report = export_identifier_alias_governance_evidence(
            output_dir=args.output_dir,
            catalog_path=args.alias_catalog_path,
        )
        print(f"Identifier alias governance evidence ready: {report.json_path}")
        print(f"Identifier alias governance evidence ready: {report.markdown_path}")
        return

    if args.chunking_comparison:
        report = export_qdrant_bge_chunking_comparison_evidence(
            output_dir=args.output_dir,
            strategies=args.chunking_strategy,
            cases_path=args.cases_path,
            source_ids=args.source_id,
            case_ids=args.case_id,
            settings=settings,
        )
        print(f"Qdrant BGE-M3 chunking comparison evidence ready: {report.json_path}")
        print(f"Qdrant BGE-M3 chunking comparison evidence ready: {report.markdown_path}")
        return

    if args.threshold_sweep:
        report = export_qdrant_bge_threshold_sweep_evidence(
            output_dir=args.output_dir,
            thresholds=args.threshold_sweep,
            cases_path=args.cases_path,
            source_ids=args.source_id,
            case_ids=args.case_id,
            settings=settings,
        )
        print(f"Qdrant BGE-M3 threshold sweep evidence ready: {report.json_path}")
        print(f"Qdrant BGE-M3 threshold sweep evidence ready: {report.markdown_path}")
        return

    if args.recommend_threshold_from_sweep is not None:
        report = export_qdrant_threshold_recommendation(
            sweep_path=args.recommend_threshold_from_sweep,
            output_dir=args.output_dir,
            gates=ThresholdRecommendationGates(
                min_hit_rate=args.min_hit_rate,
                min_citation_match_rate=args.min_citation_match_rate,
                min_empty_handling_rate=args.min_empty_handling_rate,
            ),
        )
        print(f"Qdrant BGE-M3 threshold recommendation ready: {report.json_path}")
        print(f"Qdrant BGE-M3 threshold recommendation ready: {report.markdown_path}")
        return

    if args.exact_term_smoke:
        report = export_qdrant_bge_exact_term_smoke_evidence(
            output_dir=args.output_dir,
            cases_path=args.cases_path,
            source_ids=args.source_id,
            case_ids=args.case_id,
            settings=settings,
        )
        print(f"Qdrant BGE-M3 exact-term smoke evidence ready: {report.json_path}")
        print(f"Qdrant BGE-M3 exact-term smoke evidence ready: {report.markdown_path}")
        return

    if args.hybrid_exact_term_smoke:
        report = export_qdrant_bge_hybrid_exact_term_smoke_evidence(
            output_dir=args.output_dir,
            cases_path=args.cases_path,
            source_ids=args.source_id,
            case_ids=args.case_id,
            settings=settings,
        )
        print(f"Qdrant BGE-M3 hybrid exact-term smoke evidence ready: {report.json_path}")
        print(f"Qdrant BGE-M3 hybrid exact-term smoke evidence ready: {report.markdown_path}")
        return

    if args.hybrid_empty_stress:
        report = export_qdrant_bge_hybrid_empty_stress_evidence(
            output_dir=args.output_dir,
            cases_path=args.cases_path,
            source_ids=args.source_id,
            case_ids=args.case_id,
            settings=settings,
        )
        print(f"Qdrant BGE-M3 hybrid empty-stress evidence ready: {report.json_path}")
        print(f"Qdrant BGE-M3 hybrid empty-stress evidence ready: {report.markdown_path}")
        return

    if args.hybrid_gating_candidate:
        report = export_qdrant_bge_hybrid_gating_candidate_evidence(
            output_dir=args.output_dir,
            exact_cases_path=args.cases_path,
            empty_cases_path=args.empty_cases_path,
            source_ids=args.source_id,
            case_ids=args.case_id,
            settings=settings,
        )
        print(f"Qdrant BGE-M3 hybrid gating evidence ready: {report.json_path}")
        print(f"Qdrant BGE-M3 hybrid gating evidence ready: {report.markdown_path}")
        return

    if args.hybrid_alias_gating_candidate:
        report = export_qdrant_bge_hybrid_alias_gating_candidate_evidence(
            output_dir=args.output_dir,
            positive_cases_path=args.cases_path,
            empty_cases_path=args.empty_cases_path,
            source_ids=args.source_id,
            case_ids=args.case_id,
            settings=settings,
        )
        print(f"Qdrant BGE-M3 hybrid alias gating evidence ready: {report.json_path}")
        print(f"Qdrant BGE-M3 hybrid alias gating evidence ready: {report.markdown_path}")
        return

    if args.hybrid_multi_chunk_aggregation:
        report = export_qdrant_bge_hybrid_multi_chunk_aggregation_evidence(
            output_dir=args.output_dir,
            cases_path=args.cases_path,
            empty_cases_path=args.empty_cases_path,
            source_ids=args.source_id,
            case_ids=args.case_id,
            settings=settings,
        )
        print(
            "Qdrant BGE-M3 hybrid multi-chunk aggregation evidence ready: "
            f"{report.json_path}"
        )
        print(
            "Qdrant BGE-M3 hybrid multi-chunk aggregation evidence ready: "
            f"{report.markdown_path}"
        )
        return

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
        "--empty-cases-path",
        type=Path,
        default=Path("tests/fixtures/hybrid_empty_stress_cases.json"),
    )
    parser.add_argument(
        "--alias-governance",
        action="store_true",
        help="Export local identifier alias governance evidence without running Qdrant.",
    )
    parser.add_argument(
        "--alias-catalog-path",
        type=Path,
        default=Path("app/data/identifier_alias_catalog.json"),
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
    parser.add_argument("--rag-score-threshold", type=float, default=None)
    parser.add_argument(
        "--threshold-sweep",
        action="append",
        type=float,
        default=None,
        help=(
            "Run threshold sweep evidence for this threshold. "
            "Can be supplied multiple times."
        ),
    )
    parser.add_argument(
        "--chunking-comparison",
        action="store_true",
        help=(
            "Compare Qdrant+BGE smoke retrieval evidence across chunking strategies."
        ),
    )
    parser.add_argument(
        "--chunking-strategy",
        action="append",
        default=None,
        help=(
            "Chunking strategy to include in --chunking-comparison. "
            "Can be supplied multiple times."
        ),
    )
    parser.add_argument(
        "--recommend-threshold-from-sweep",
        type=Path,
        default=None,
        help="Read an existing threshold sweep JSON report and export a recommendation.",
    )
    parser.add_argument(
        "--exact-term-smoke",
        action="store_true",
        help="Export Qdrant+BGE smoke evidence using exact-term filenames.",
    )
    parser.add_argument(
        "--hybrid-exact-term-smoke",
        action="store_true",
        help="Export evaluation-only Qdrant+BGE dense+sparse exact-term evidence.",
    )
    parser.add_argument(
        "--hybrid-empty-stress",
        action="store_true",
        help="Export evaluation-only Qdrant+BGE dense+sparse expected-empty stress evidence.",
    )
    parser.add_argument(
        "--hybrid-gating-candidate",
        action="store_true",
        help=(
            "Export evaluation-only Qdrant+BGE hybrid gating evidence across "
            "exact-term and empty-stress fixtures."
        ),
    )
    parser.add_argument(
        "--hybrid-alias-gating-candidate",
        action="store_true",
        help=(
            "Export evaluation-only Qdrant+BGE hybrid alias-aware gating "
            "evidence across noisy positive and expected-empty fixtures."
        ),
    )
    parser.add_argument(
        "--hybrid-multi-chunk-aggregation",
        action="store_true",
        help=(
            "Export evaluation-only Qdrant+BGE hybrid source-document "
            "multi-chunk aggregation evidence."
        ),
    )
    parser.add_argument("--min-hit-rate", type=float, default=1.0)
    parser.add_argument("--min-citation-match-rate", type=float, default=1.0)
    parser.add_argument("--min-empty-handling-rate", type=float, default=1.0)
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
