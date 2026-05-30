import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from app.config import Settings, get_settings
from app.models.contracts import IndexStatusResponse
from app.models.contracts import EvidenceDocument
from app.services.embedding_adapters import create_embedding_adapter
from app.services.index_lifecycle_store import IndexLifecycleStore
from app.services.qdrant_vector_store import (
    QDRANT_CHUNKING_STRATEGY,
    QDRANT_HYBRID_FUSION_STRATEGY,
    QDRANT_LEXICAL_SPARSE_VECTORIZER_ID,
    QDRANT_SECTION_CHUNKING_STRATEGY,
    QDRANT_SPARSE_VECTOR_NAME,
    QDRANT_TOKEN_WINDOW_CHUNKING_STRATEGY,
    create_qdrant_client,
    embed_qdrant_chunks,
    ensure_qdrant_collection,
    ensure_qdrant_hybrid_collection,
    extract_lexical_identifiers,
    load_qdrant_source_chunks,
    markdown_source_to_section_chunks,
    markdown_source_to_token_window_chunks,
    query_qdrant_hybrid_documents_for_text,
    query_qdrant_documents_for_text,
    upsert_qdrant_hybrid_chunks,
    upsert_qdrant_chunks,
)
from app.services.retrieval_backends import create_document_retriever


@dataclass(frozen=True)
class RetrievalBenchmarkCase:
    id: str
    category: str
    difficulty: str
    query: str
    knowledge_base_ids: list[str]
    top_k: int
    expected_source_id: str | None
    expected_citation: str | None
    expect_empty: bool = False


@dataclass(frozen=True)
class RetrievalBenchmarkCaseResult:
    id: str
    category: str
    difficulty: str
    hit_at_k: bool
    citation_match: bool
    empty_query_handling: bool | None
    latency_ms: float
    returned_citations: list[str]
    returned_source_ids: list[str]


@dataclass(frozen=True)
class RetrievalBenchmarkSummary:
    backend: str
    total_cases: int
    hit_rate: float
    citation_match_rate: float
    empty_handling_rate: float
    category_summaries: dict[str, dict[str, float | int]]


@dataclass(frozen=True)
class RetrievalBenchmarkReport:
    summary: RetrievalBenchmarkSummary
    cases: list[RetrievalBenchmarkCaseResult]


@dataclass(frozen=True)
class RetrievalCandidate:
    id: str
    backend: str
    description: str
    metadata: dict[str, str] | None = None


@dataclass(frozen=True)
class RetrievalCandidateEvaluation:
    candidate: RetrievalCandidate
    report: RetrievalBenchmarkReport
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class EmbeddingCandidate:
    id: str
    provider_family: str
    model_name: str
    deployment_mode: str
    language_profile: str
    vector_dimension: int | None
    data_residency: str
    operational_complexity: str
    reranker_compatibility: str
    approval_status: str
    chinese_heavy_suitable: bool
    private_network_supported: bool
    notes: list[str]


@dataclass(frozen=True)
class EmbeddingCandidateResult:
    candidate: EmbeddingCandidate
    readiness_status: str
    criteria_coverage: dict[str, bool]
    decision_notes: list[str]


@dataclass(frozen=True)
class EmbeddingCandidateEvaluation:
    result: EmbeddingCandidateResult
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class ChineseSeedEvidenceBundle:
    retrieval_evaluations: list[RetrievalCandidateEvaluation]
    embedding_evaluations: list[EmbeddingCandidateEvaluation]
    output_dir: Path


@dataclass(frozen=True)
class QdrantSmokeEvidenceReport:
    candidate: RetrievalCandidate
    report: RetrievalBenchmarkReport
    metadata: dict[str, str | list[str] | dict[str, str]]
    indexed_sources: dict[str, dict[str, str | int]]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class HybridGatingCaseResult:
    id: str
    category: str
    difficulty: str
    expect_empty: bool
    query_identifiers: list[str]
    gate_applied: bool
    raw_returned_citations: list[str]
    raw_returned_source_ids: list[str]
    gated_result: RetrievalBenchmarkCaseResult


@dataclass(frozen=True)
class QdrantHybridGatingEvidenceReport:
    candidate: RetrievalCandidate
    report: RetrievalBenchmarkReport
    cases: list[HybridGatingCaseResult]
    metadata: dict[str, str | list[str] | dict[str, str]]
    indexed_sources: dict[str, dict[str, str | int]]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class IdentifierAliasRule:
    id: str
    canonical_prefix: str
    match_pattern: str
    segment_widths: list[int]
    owner: str
    status: str
    version: str
    risk_level: str
    notes: list[str]


@dataclass(frozen=True)
class IdentifierAliasGovernanceReport:
    aliases: list[IdentifierAliasRule]
    summary: dict[str, int | dict[str, int]]
    decision_notes: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class QdrantThresholdSweepEvidenceReport:
    candidate: RetrievalCandidate
    thresholds: list[float]
    reports: list[QdrantSmokeEvidenceReport]
    metadata: dict[str, str | list[str] | dict[str, str]]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class ThresholdRecommendationGates:
    min_hit_rate: float = 1.0
    min_citation_match_rate: float = 1.0
    min_empty_handling_rate: float = 1.0


@dataclass(frozen=True)
class QdrantThresholdRecommendation:
    selected_threshold: float
    gates: ThresholdRecommendationGates
    selected_metrics: dict[str, float | int]
    sweep_path: str
    approval_status: str
    caveats: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class QdrantChunkingComparisonReport:
    strategies: list[str]
    reports: list[QdrantSmokeEvidenceReport]
    metadata: dict[str, str | list[str]]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class ChunkingStrategyCandidate:
    id: str
    description: str
    implementation_status: str
    expected_fit: str
    tradeoffs: list[str]


@dataclass(frozen=True)
class ChunkingStrategyResult:
    candidate: ChunkingStrategyCandidate
    source_ids: list[str]
    total_chunks: int | None
    citation_stability: str
    long_section_support: str
    decision_notes: list[str]


@dataclass(frozen=True)
class ChunkingStrategyEvaluation:
    results: list[ChunkingStrategyResult]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class QueryRewriteCandidate:
    id: str
    description: str
    implementation_status: str
    rewrite_policy: str
    risk_notes: list[str]


@dataclass(frozen=True)
class QueryRewriteCaseResult:
    case_id: str
    category: str
    difficulty: str
    original_query: str
    rewritten_query: str
    rewritten: bool
    expect_empty: bool
    result: RetrievalBenchmarkCaseResult


@dataclass(frozen=True)
class QueryRewriteCandidateResult:
    candidate: QueryRewriteCandidate
    total_cases: int
    rewritten_cases: int
    rewrite_rate: float
    expected_empty_rewrites: int
    report: RetrievalBenchmarkReport
    cases: list[QueryRewriteCaseResult]
    decision_notes: list[str]


@dataclass(frozen=True)
class QueryRewriteCandidateEvaluation:
    results: list[QueryRewriteCandidateResult]
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class EvidenceGradingCandidate:
    id: str
    description: str
    implementation_status: str
    grading_policy: str
    risk_notes: list[str]


@dataclass(frozen=True)
class EvidenceGradingCaseResult:
    case_id: str
    category: str
    difficulty: str
    expected_source_id: str | None
    expected_citation: str | None
    returned_source_ids: list[str]
    returned_citations: list[str]
    grading_label: str
    grading_reason: str
    result: RetrievalBenchmarkCaseResult


@dataclass(frozen=True)
class EvidenceGradingCandidateResult:
    candidate: EvidenceGradingCandidate
    total_cases: int
    answer_bearing_rate: float
    related_insufficient_count: int
    missing_evidence_count: int
    unexpected_evidence_count: int
    expected_empty_pass_rate: float
    report: RetrievalBenchmarkReport
    cases: list[EvidenceGradingCaseResult]
    decision_notes: list[str]


@dataclass(frozen=True)
class EvidenceGradingCandidateEvaluation:
    results: list[EvidenceGradingCandidateResult]
    json_path: Path | None = None
    markdown_path: Path | None = None


CONTROLLED_SUPPORT_QUERY_REWRITES = {
    "refund-delivery-paraphrase": (
        "客户三天未发货可以申请退款，售后专员应核验订单状态和发货记录后处理。"
    ),
    "logistics-carrier-paraphrase": (
        "物流轨迹超过二十四小时未更新时，应先联系承运商确认揽收和中转状态。"
    ),
    "refund-address-change-before-shipping": (
        "用户同时反馈未发货和地址变更，售后专员应先暂停发货，再确认继续履约或退款。"
    ),
    "logistics-lost-package-cross-team": (
        "承运商确认包裹丢失后，客服应创建物流异常工单，并同步售后团队评估补发或退款。"
    ),
    "refund-appeal-second-review": (
        "退款申诉复核场景中，客服应补充原始订单、沟通记录和拒绝理由交由二线复核。"
    ),
    "logistics-batch-exception-escalation": (
        "批量物流异常需要创建批量异常工单，记录受影响订单范围并通知运营负责人。"
    ),
}


def load_benchmark_cases(path: Path) -> list[RetrievalBenchmarkCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [RetrievalBenchmarkCase(**item) for item in payload]


def run_retrieval_benchmark(
    cases: list[RetrievalBenchmarkCase],
    settings: Settings | None = None,
) -> RetrievalBenchmarkReport:
    settings = settings or get_settings()
    retriever = create_document_retriever(settings)
    results = [_run_case(retriever, case) for case in cases]
    return RetrievalBenchmarkReport(
        summary=_summarize(retriever.backend_name, results),
        cases=results,
    )


def evaluate_retrieval_candidates(
    cases: list[RetrievalBenchmarkCase],
    candidates: list[RetrievalCandidate],
    base_settings: Settings | None = None,
    output_dir: Path | None = None,
) -> list[RetrievalCandidateEvaluation]:
    _validate_candidates(candidates)
    base_settings = base_settings or get_settings()
    evaluations = []
    for candidate in candidates:
        report = run_retrieval_benchmark(
            cases,
            base_settings.model_copy(
                update={"rag_retrieval_backend": candidate.backend}
            ),
        )
        json_path = None
        markdown_path = None
        if output_dir is not None:
            json_path = export_candidate_evaluation_json(
                candidate,
                report,
                output_dir / f"{candidate.id}.json",
            )
            markdown_path = export_candidate_evaluation_markdown(
                candidate,
                report,
                output_dir / f"{candidate.id}.md",
            )
        evaluations.append(
            RetrievalCandidateEvaluation(
                candidate=candidate,
                report=report,
                json_path=json_path,
                markdown_path=markdown_path,
            )
        )
    return evaluations


def qdrant_retrieval_candidate(settings: Settings | None = None) -> RetrievalCandidate:
    settings = settings or get_settings()
    return RetrievalCandidate(
        id="qdrant-candidate",
        backend="qdrant",
        description="Qdrant vector-store candidate; embedding and reranker remain undecided.",
        metadata={
            "vector_store": "qdrant",
            "collection": settings.qdrant_collection,
            "vector_name": settings.qdrant_vector_name,
            "embedding": "undecided",
            "reranker": "undecided",
            "deployment_path": "local-public-test-or-private-network",
        },
    )


def qdrant_bge_smoke_candidate(settings: Settings | None = None) -> RetrievalCandidate:
    settings = settings or get_settings()
    return RetrievalCandidate(
        id="qdrant-bge-m3-smoke",
        backend="qdrant",
        description=(
            "Local Qdrant ingestion/retrieval smoke path using the configured "
            "embedding adapter, intended for BGE-M3 local evidence."
        ),
        metadata={
            "vector_store": "qdrant",
            "collection": settings.qdrant_collection,
            "vector_name": settings.qdrant_vector_name,
            "embedding_provider": settings.embedding_provider,
            "embedding_model": settings.embedding_model,
            "embedding_model_path": (
                str(settings.embedding_model_path)
                if settings.embedding_model_path is not None
                else ""
            ),
            "deployment_path": "local-smoke-or-private-network",
        },
    )


def qdrant_bge_exact_term_smoke_candidate(
    settings: Settings | None = None,
) -> RetrievalCandidate:
    settings = settings or get_settings()
    base_candidate = qdrant_bge_smoke_candidate(settings)
    metadata = dict(base_candidate.metadata or {})
    metadata["benchmark_fixture"] = "exact-term-identifier-v1"
    return RetrievalCandidate(
        id="qdrant-bge-m3-exact-term-smoke",
        backend=base_candidate.backend,
        description=(
            "Local Qdrant+BGE-M3 dense-only smoke path for exact terms, "
            "identifiers, acronyms, and order-like ids."
        ),
        metadata=metadata,
    )


def qdrant_bge_hybrid_exact_term_smoke_candidate(
    settings: Settings | None = None,
) -> RetrievalCandidate:
    settings = settings or get_settings()
    base_candidate = qdrant_bge_smoke_candidate(settings)
    metadata = dict(base_candidate.metadata or {})
    metadata.update({
        "benchmark_fixture": "exact-term-identifier-v1",
        "retrieval_mode": "dense+sparse-hybrid",
        "sparse_vector_name": QDRANT_SPARSE_VECTOR_NAME,
        "sparse_vectorizer": QDRANT_LEXICAL_SPARSE_VECTORIZER_ID,
        "fusion": QDRANT_HYBRID_FUSION_STRATEGY,
    })
    return RetrievalCandidate(
        id="qdrant-bge-m3-hybrid-exact-term-smoke",
        backend=base_candidate.backend,
        description=(
            "Evaluation-only Qdrant+BGE-M3 dense+sparse smoke path for exact "
            "terms, identifiers, acronyms, and order-like ids."
        ),
        metadata=metadata,
    )


def qdrant_bge_hybrid_empty_stress_candidate(
    settings: Settings | None = None,
) -> RetrievalCandidate:
    settings = settings or get_settings()
    base_candidate = qdrant_bge_hybrid_exact_term_smoke_candidate(settings)
    metadata = dict(base_candidate.metadata or {})
    metadata["benchmark_fixture"] = "hybrid-empty-stress-v1"
    return RetrievalCandidate(
        id="qdrant-bge-m3-hybrid-empty-stress",
        backend=base_candidate.backend,
        description=(
            "Evaluation-only Qdrant+BGE-M3 dense+sparse smoke path for "
            "expected-empty cases with exact-token overlap."
        ),
        metadata=metadata,
    )


def qdrant_bge_hybrid_gating_candidate(
    settings: Settings | None = None,
) -> RetrievalCandidate:
    settings = settings or get_settings()
    base_candidate = qdrant_bge_hybrid_exact_term_smoke_candidate(settings)
    metadata = dict(base_candidate.metadata or {})
    metadata.update({
        "benchmark_fixture": "hybrid-gating-combined-v1",
        "gating_policy": "exact-identifier-containment-gate-v1",
    })
    return RetrievalCandidate(
        id="qdrant-bge-m3-hybrid-exact-identifier-gate",
        backend=base_candidate.backend,
        description=(
            "Evaluation-only Qdrant+BGE-M3 dense+sparse candidate with an "
            "exact identifier containment gate for retrieved evidence."
        ),
        metadata=metadata,
    )


def qdrant_bge_hybrid_alias_gating_candidate(
    settings: Settings | None = None,
) -> RetrievalCandidate:
    settings = settings or get_settings()
    base_candidate = qdrant_bge_hybrid_exact_term_smoke_candidate(settings)
    metadata = dict(base_candidate.metadata or {})
    metadata.update({
        "benchmark_fixture": "noisy-identifier-gating-v1",
        "gating_policy": "alias-aware-identifier-gate-v1",
    })
    return RetrievalCandidate(
        id="qdrant-bge-m3-hybrid-alias-identifier-gate",
        backend=base_candidate.backend,
        description=(
            "Evaluation-only Qdrant+BGE-M3 dense+sparse candidate with "
            "OCR and local alias normalization before identifier gating."
        ),
        metadata=metadata,
    )


def qdrant_bge_hybrid_multi_chunk_aggregation_candidate(
    settings: Settings | None = None,
) -> RetrievalCandidate:
    settings = settings or get_settings()
    base_candidate = qdrant_bge_hybrid_exact_term_smoke_candidate(settings)
    metadata = dict(base_candidate.metadata or {})
    metadata.update({
        "benchmark_fixture": "split-chunk-identifier-v1",
        "aggregation_policy": "source-document-identifier-coverage-v1",
    })
    return RetrievalCandidate(
        id="qdrant-bge-m3-hybrid-multi-chunk-aggregation",
        backend=base_candidate.backend,
        description=(
            "Evaluation-only Qdrant+BGE-M3 dense+sparse candidate that groups "
            "retrieved chunks by source document before checking identifier coverage."
        ),
        metadata=metadata,
    )


def fixture_chinese_seed_retrieval_candidate() -> RetrievalCandidate:
    return RetrievalCandidate(
        id="fixture-chinese-seed-baseline",
        backend="fixture",
        description=(
            "Fixture baseline for the local Chinese benchmark seed; "
            "contract evidence only, not semantic retrieval quality."
        ),
        metadata={
            "benchmark_seed": "chinese-enterprise-support-v1",
            "embedding": "none",
            "vector_store": "none",
            "quality_claim": "contract-baseline-only",
        },
    )


def default_embedding_candidates() -> list[EmbeddingCandidate]:
    return [
        EmbeddingCandidate(
            id="mock-hash-v1",
            provider_family="mock",
            model_name="mock-hash-v1",
            deployment_mode="local-deterministic-test",
            language_profile="contract-only",
            vector_dimension=None,
            data_residency="local-only",
            operational_complexity="low",
            reranker_compatibility="not-applicable",
            approval_status="baseline",
            chinese_heavy_suitable=False,
            private_network_supported=True,
            notes=[
                "Deterministic contract baseline only.",
                "Not a semantic embedding model.",
            ],
        ),
        EmbeddingCandidate(
            id="qwen-embedding-candidate",
            provider_family="hosted",
            model_name="qwen-embedding",
            deployment_mode="public-hosted-or-private-compatible",
            language_profile="chinese-heavy",
            vector_dimension=None,
            data_residency="depends-on-provider-and-deployment",
            operational_complexity="medium",
            reranker_compatibility="candidate-specific",
            approval_status="candidate",
            chinese_heavy_suitable=True,
            private_network_supported=False,
            notes=[
                "Hosted/public route must be reviewed for data residency.",
                "Private-network feasibility remains a later implementation decision.",
            ],
        ),
        EmbeddingCandidate(
            id="bge-m3-local-candidate",
            provider_family="local",
            model_name="bge-m3",
            deployment_mode="local-or-private-network",
            language_profile="chinese-heavy-and-multilingual",
            vector_dimension=1024,
            data_residency="private-network-capable",
            operational_complexity="medium-high",
            reranker_compatibility="strong-local-reranker-ecosystem",
            approval_status="candidate",
            chinese_heavy_suitable=True,
            private_network_supported=True,
            notes=[
                "Local route is suitable for private data constraints.",
                "Dense embedding adapter is available as an opt-in local path.",
                "Runtime footprint and serving stack still need benchmark evidence.",
            ],
        ),
        EmbeddingCandidate(
            id="openai-embedding-candidate",
            provider_family="hosted",
            model_name="openai-embedding",
            deployment_mode="public-hosted",
            language_profile="multilingual",
            vector_dimension=None,
            data_residency="public-provider-dependent",
            operational_complexity="low-medium",
            reranker_compatibility="candidate-specific",
            approval_status="candidate",
            chinese_heavy_suitable=True,
            private_network_supported=False,
            notes=[
                "Useful as hosted multilingual quality baseline.",
                "Public data egress must be explicitly approved before use.",
            ],
        ),
    ]


def evaluate_embedding_candidates(
    candidates: list[EmbeddingCandidate] | None = None,
    output_dir: Path | None = None,
) -> list[EmbeddingCandidateEvaluation]:
    candidates = candidates or default_embedding_candidates()
    _validate_candidate_ids(candidates, "embedding candidate")
    evaluations = []
    for candidate in candidates:
        result = _evaluate_embedding_candidate(candidate)
        json_path = None
        markdown_path = None
        if output_dir is not None:
            json_path = export_embedding_candidate_json(
                result,
                output_dir / f"{candidate.id}.json",
            )
            markdown_path = export_embedding_candidate_markdown(
                result,
                output_dir / f"{candidate.id}.md",
            )
        evaluations.append(
            EmbeddingCandidateEvaluation(
                result=result,
                json_path=json_path,
                markdown_path=markdown_path,
            )
        )
    return evaluations


def export_chinese_seed_evidence_bundle(
    output_dir: Path,
    cases_path: Path = Path("tests/fixtures/retrieval_benchmark_cases.json"),
    base_settings: Settings | None = None,
) -> ChineseSeedEvidenceBundle:
    cases = load_benchmark_cases(cases_path)
    retrieval_evaluations = evaluate_retrieval_candidates(
        cases=cases,
        candidates=[fixture_chinese_seed_retrieval_candidate()],
        base_settings=base_settings or Settings(rag_retrieval_backend="fixture"),
        output_dir=output_dir / "retrieval-candidates",
    )
    embedding_evaluations = evaluate_embedding_candidates(
        output_dir=output_dir / "embedding-candidates",
    )
    return ChineseSeedEvidenceBundle(
        retrieval_evaluations=retrieval_evaluations,
        embedding_evaluations=embedding_evaluations,
        output_dir=output_dir,
    )


def export_qdrant_bge_smoke_evidence(
    output_dir: Path,
    cases_path: Path = Path("tests/fixtures/retrieval_benchmark_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
    write_files: bool = True,
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
) -> QdrantSmokeEvidenceReport:
    settings = settings or get_settings()
    source_ids = source_ids or ["refund_policy_docs", "logistics_faq"]
    cases = load_benchmark_cases(cases_path)
    if case_ids is not None:
        allowed = set(case_ids)
        cases = [case for case in cases if case.id in allowed]

    client = create_qdrant_client(settings)
    embedding_adapter = create_embedding_adapter(settings)
    indexed_sources = _index_qdrant_smoke_sources(
        client=client,
        settings=settings,
        source_ids=source_ids,
        embedding_adapter=embedding_adapter,
        chunking_strategy=chunking_strategy,
    )
    case_results = [
        _run_qdrant_smoke_case(
            client=client,
            settings=settings,
            embedding_adapter=embedding_adapter,
            case=case,
        )
        for case in cases
    ]
    report = RetrievalBenchmarkReport(
        summary=_summarize("qdrant", case_results),
        cases=case_results,
    )
    smoke_report = QdrantSmokeEvidenceReport(
        candidate=qdrant_bge_smoke_candidate(settings),
        report=report,
        metadata=_qdrant_smoke_metadata(settings, source_ids, chunking_strategy),
        indexed_sources=indexed_sources,
    )
    json_path = None
    markdown_path = None
    if write_files:
        json_path = export_qdrant_smoke_evidence_json(
            smoke_report,
            output_dir / "qdrant-bge-m3-smoke.json",
        )
        markdown_path = export_qdrant_smoke_evidence_markdown(
            smoke_report,
            output_dir / "qdrant-bge-m3-smoke.md",
        )
    return QdrantSmokeEvidenceReport(
        candidate=smoke_report.candidate,
        report=smoke_report.report,
        metadata=smoke_report.metadata,
        indexed_sources=smoke_report.indexed_sources,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_bge_exact_term_smoke_evidence(
    output_dir: Path,
    cases_path: Path = Path("tests/fixtures/exact_term_identifier_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
) -> QdrantSmokeEvidenceReport:
    settings = settings or get_settings()
    report = export_qdrant_bge_smoke_evidence(
        output_dir=output_dir,
        cases_path=cases_path,
        source_ids=source_ids,
        case_ids=case_ids,
        settings=settings,
        write_files=False,
        chunking_strategy=chunking_strategy,
    )
    metadata = dict(report.metadata)
    metadata["benchmark_fixture"] = "exact-term-identifier-v1"
    metadata["benchmark_cases_path"] = str(cases_path)
    exact_report = QdrantSmokeEvidenceReport(
        candidate=qdrant_bge_exact_term_smoke_candidate(settings),
        report=report.report,
        metadata=metadata,
        indexed_sources=report.indexed_sources,
    )
    json_path = export_qdrant_smoke_evidence_json(
        exact_report,
        output_dir / "qdrant-bge-m3-exact-term-smoke.json",
    )
    markdown_path = export_qdrant_smoke_evidence_markdown(
        exact_report,
        output_dir / "qdrant-bge-m3-exact-term-smoke.md",
    )
    return QdrantSmokeEvidenceReport(
        candidate=exact_report.candidate,
        report=exact_report.report,
        metadata=exact_report.metadata,
        indexed_sources=exact_report.indexed_sources,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_bge_hybrid_exact_term_smoke_evidence(
    output_dir: Path,
    cases_path: Path = Path("tests/fixtures/exact_term_identifier_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
    sparse_vector_name: str = QDRANT_SPARSE_VECTOR_NAME,
) -> QdrantSmokeEvidenceReport:
    settings = settings or get_settings()
    source_ids = source_ids or ["refund_policy_docs", "logistics_faq"]
    cases = load_benchmark_cases(cases_path)
    if case_ids is not None:
        allowed = set(case_ids)
        cases = [case for case in cases if case.id in allowed]

    client = create_qdrant_client(settings)
    embedding_adapter = create_embedding_adapter(settings)
    indexed_sources = _index_qdrant_hybrid_smoke_sources(
        client=client,
        settings=settings,
        source_ids=source_ids,
        embedding_adapter=embedding_adapter,
        chunking_strategy=chunking_strategy,
        sparse_vector_name=sparse_vector_name,
    )
    case_results = [
        _run_qdrant_hybrid_smoke_case(
            client=client,
            settings=settings,
            embedding_adapter=embedding_adapter,
            case=case,
            sparse_vector_name=sparse_vector_name,
        )
        for case in cases
    ]
    report = RetrievalBenchmarkReport(
        summary=_summarize("qdrant-hybrid", case_results),
        cases=case_results,
    )
    metadata = _qdrant_smoke_metadata(settings, source_ids, chunking_strategy)
    metadata.update({
        "benchmark_fixture": "exact-term-identifier-v1",
        "benchmark_cases_path": str(cases_path),
        "retrieval_mode": "dense+sparse-hybrid",
        "sparse_vector_name": sparse_vector_name,
        "sparse_vectorizer": QDRANT_LEXICAL_SPARSE_VECTORIZER_ID,
        "fusion": QDRANT_HYBRID_FUSION_STRATEGY,
        "score_filter": "disabled-for-rrf-fusion-score",
    })
    hybrid_report = QdrantSmokeEvidenceReport(
        candidate=qdrant_bge_hybrid_exact_term_smoke_candidate(settings),
        report=report,
        metadata=metadata,
        indexed_sources=indexed_sources,
    )
    json_path = export_qdrant_smoke_evidence_json(
        hybrid_report,
        output_dir / "qdrant-bge-m3-hybrid-exact-term-smoke.json",
    )
    markdown_path = export_qdrant_smoke_evidence_markdown(
        hybrid_report,
        output_dir / "qdrant-bge-m3-hybrid-exact-term-smoke.md",
    )
    return QdrantSmokeEvidenceReport(
        candidate=hybrid_report.candidate,
        report=hybrid_report.report,
        metadata=hybrid_report.metadata,
        indexed_sources=hybrid_report.indexed_sources,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_bge_hybrid_empty_stress_evidence(
    output_dir: Path,
    cases_path: Path = Path("tests/fixtures/hybrid_empty_stress_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
    sparse_vector_name: str = QDRANT_SPARSE_VECTOR_NAME,
) -> QdrantSmokeEvidenceReport:
    settings = settings or get_settings()
    source_ids = source_ids or ["refund_policy_docs", "logistics_faq"]
    cases = load_benchmark_cases(cases_path)
    if case_ids is not None:
        allowed = set(case_ids)
        cases = [case for case in cases if case.id in allowed]

    client = create_qdrant_client(settings)
    embedding_adapter = create_embedding_adapter(settings)
    indexed_sources = _index_qdrant_hybrid_smoke_sources(
        client=client,
        settings=settings,
        source_ids=source_ids,
        embedding_adapter=embedding_adapter,
        chunking_strategy=chunking_strategy,
        sparse_vector_name=sparse_vector_name,
    )
    case_results = [
        _run_qdrant_hybrid_smoke_case(
            client=client,
            settings=settings,
            embedding_adapter=embedding_adapter,
            case=case,
            sparse_vector_name=sparse_vector_name,
        )
        for case in cases
    ]
    report = RetrievalBenchmarkReport(
        summary=_summarize("qdrant-hybrid", case_results),
        cases=case_results,
    )
    metadata = _qdrant_smoke_metadata(settings, source_ids, chunking_strategy)
    metadata.update({
        "benchmark_fixture": "hybrid-empty-stress-v1",
        "benchmark_cases_path": str(cases_path),
        "retrieval_mode": "dense+sparse-hybrid",
        "sparse_vector_name": sparse_vector_name,
        "sparse_vectorizer": QDRANT_LEXICAL_SPARSE_VECTORIZER_ID,
        "fusion": QDRANT_HYBRID_FUSION_STRATEGY,
        "score_filter": "disabled-for-rrf-fusion-score",
    })
    stress_report = QdrantSmokeEvidenceReport(
        candidate=qdrant_bge_hybrid_empty_stress_candidate(settings),
        report=report,
        metadata=metadata,
        indexed_sources=indexed_sources,
    )
    json_path = export_qdrant_smoke_evidence_json(
        stress_report,
        output_dir / "qdrant-bge-m3-hybrid-empty-stress.json",
    )
    markdown_path = export_qdrant_smoke_evidence_markdown(
        stress_report,
        output_dir / "qdrant-bge-m3-hybrid-empty-stress.md",
    )
    return QdrantSmokeEvidenceReport(
        candidate=stress_report.candidate,
        report=stress_report.report,
        metadata=stress_report.metadata,
        indexed_sources=stress_report.indexed_sources,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_bge_hybrid_gating_candidate_evidence(
    output_dir: Path,
    exact_cases_path: Path = Path("tests/fixtures/exact_term_identifier_cases.json"),
    empty_cases_path: Path = Path("tests/fixtures/hybrid_empty_stress_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
    sparse_vector_name: str = QDRANT_SPARSE_VECTOR_NAME,
) -> QdrantHybridGatingEvidenceReport:
    settings = settings or get_settings()
    source_ids = source_ids or ["refund_policy_docs", "logistics_faq"]
    cases = [
        *load_benchmark_cases(exact_cases_path),
        *load_benchmark_cases(empty_cases_path),
    ]
    if case_ids is not None:
        allowed = set(case_ids)
        cases = [case for case in cases if case.id in allowed]

    client = create_qdrant_client(settings)
    embedding_adapter = create_embedding_adapter(settings)
    indexed_sources = _index_qdrant_hybrid_smoke_sources(
        client=client,
        settings=settings,
        source_ids=source_ids,
        embedding_adapter=embedding_adapter,
        chunking_strategy=chunking_strategy,
        sparse_vector_name=sparse_vector_name,
    )
    case_results = [
        _run_qdrant_hybrid_gated_smoke_case(
            client=client,
            settings=settings,
            embedding_adapter=embedding_adapter,
            case=case,
            sparse_vector_name=sparse_vector_name,
        )
        for case in cases
    ]
    report = RetrievalBenchmarkReport(
        summary=_summarize(
            "qdrant-hybrid:exact-identifier-containment-gate-v1",
            [case.gated_result for case in case_results],
        ),
        cases=[case.gated_result for case in case_results],
    )
    metadata = _qdrant_smoke_metadata(settings, source_ids, chunking_strategy)
    metadata.update({
        "benchmark_fixture": "hybrid-gating-combined-v1",
        "exact_cases_path": str(exact_cases_path),
        "empty_cases_path": str(empty_cases_path),
        "retrieval_mode": "dense+sparse-hybrid",
        "gating_policy": "exact-identifier-containment-gate-v1",
        "sparse_vector_name": sparse_vector_name,
        "sparse_vectorizer": QDRANT_LEXICAL_SPARSE_VECTORIZER_ID,
        "fusion": QDRANT_HYBRID_FUSION_STRATEGY,
        "score_filter": "disabled-for-rrf-fusion-score",
    })
    gating_report = QdrantHybridGatingEvidenceReport(
        candidate=qdrant_bge_hybrid_gating_candidate(settings),
        report=report,
        cases=case_results,
        metadata=metadata,
        indexed_sources=indexed_sources,
    )
    json_path = export_qdrant_hybrid_gating_evidence_json(
        gating_report,
        output_dir / "qdrant-bge-m3-hybrid-exact-identifier-gate.json",
    )
    markdown_path = export_qdrant_hybrid_gating_evidence_markdown(
        gating_report,
        output_dir / "qdrant-bge-m3-hybrid-exact-identifier-gate.md",
    )
    return QdrantHybridGatingEvidenceReport(
        candidate=gating_report.candidate,
        report=gating_report.report,
        cases=gating_report.cases,
        metadata=gating_report.metadata,
        indexed_sources=gating_report.indexed_sources,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_bge_hybrid_alias_gating_candidate_evidence(
    output_dir: Path,
    positive_cases_path: Path = Path(
        "tests/fixtures/noisy_identifier_positive_cases.json"
    ),
    empty_cases_path: Path = Path("tests/fixtures/noisy_identifier_empty_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
    sparse_vector_name: str = QDRANT_SPARSE_VECTOR_NAME,
) -> QdrantHybridGatingEvidenceReport:
    settings = settings or get_settings()
    source_ids = source_ids or ["refund_policy_docs", "logistics_faq"]
    cases = [
        *load_benchmark_cases(positive_cases_path),
        *load_benchmark_cases(empty_cases_path),
    ]
    if case_ids is not None:
        allowed = set(case_ids)
        cases = [case for case in cases if case.id in allowed]

    client = create_qdrant_client(settings)
    embedding_adapter = create_embedding_adapter(settings)
    indexed_sources = _index_qdrant_hybrid_smoke_sources(
        client=client,
        settings=settings,
        source_ids=source_ids,
        embedding_adapter=embedding_adapter,
        chunking_strategy=chunking_strategy,
        sparse_vector_name=sparse_vector_name,
    )
    case_results = [
        _run_qdrant_hybrid_gated_smoke_case(
            client=client,
            settings=settings,
            embedding_adapter=embedding_adapter,
            case=case,
            sparse_vector_name=sparse_vector_name,
            gate_fn=apply_alias_aware_identifier_gate,
        )
        for case in cases
    ]
    report = RetrievalBenchmarkReport(
        summary=_summarize(
            "qdrant-hybrid:alias-aware-identifier-gate-v1",
            [case.gated_result for case in case_results],
        ),
        cases=[case.gated_result for case in case_results],
    )
    metadata = _qdrant_smoke_metadata(settings, source_ids, chunking_strategy)
    metadata.update({
        "benchmark_fixture": "noisy-identifier-gating-v1",
        "positive_cases_path": str(positive_cases_path),
        "empty_cases_path": str(empty_cases_path),
        "retrieval_mode": "dense+sparse-hybrid",
        "gating_policy": "alias-aware-identifier-gate-v1",
        "sparse_vector_name": sparse_vector_name,
        "sparse_vectorizer": QDRANT_LEXICAL_SPARSE_VECTORIZER_ID,
        "fusion": QDRANT_HYBRID_FUSION_STRATEGY,
        "score_filter": "disabled-for-rrf-fusion-score",
    })
    gating_report = QdrantHybridGatingEvidenceReport(
        candidate=qdrant_bge_hybrid_alias_gating_candidate(settings),
        report=report,
        cases=case_results,
        metadata=metadata,
        indexed_sources=indexed_sources,
    )
    json_path = export_qdrant_hybrid_gating_evidence_json(
        gating_report,
        output_dir / "qdrant-bge-m3-hybrid-alias-identifier-gate.json",
    )
    markdown_path = export_qdrant_hybrid_gating_evidence_markdown(
        gating_report,
        output_dir / "qdrant-bge-m3-hybrid-alias-identifier-gate.md",
    )
    return QdrantHybridGatingEvidenceReport(
        candidate=gating_report.candidate,
        report=gating_report.report,
        cases=gating_report.cases,
        metadata=gating_report.metadata,
        indexed_sources=gating_report.indexed_sources,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_bge_hybrid_multi_chunk_aggregation_evidence(
    output_dir: Path,
    cases_path: Path = Path("tests/fixtures/split_chunk_identifier_cases.json"),
    empty_cases_path: Path = Path("tests/fixtures/no_benchmark_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
    sparse_vector_name: str = QDRANT_SPARSE_VECTOR_NAME,
) -> QdrantHybridGatingEvidenceReport:
    settings = settings or get_settings()
    source_ids = source_ids or ["split_refund_policy_docs"]
    cases = [
        *load_benchmark_cases(cases_path),
        *load_benchmark_cases(empty_cases_path),
    ]
    if case_ids is not None:
        allowed = set(case_ids)
        cases = [case for case in cases if case.id in allowed]

    client = create_qdrant_client(settings)
    embedding_adapter = create_embedding_adapter(settings)
    indexed_sources = _index_qdrant_hybrid_smoke_sources(
        client=client,
        settings=settings,
        source_ids=source_ids,
        embedding_adapter=embedding_adapter,
        chunking_strategy=chunking_strategy,
        sparse_vector_name=sparse_vector_name,
    )
    case_results = [
        _run_qdrant_hybrid_gated_smoke_case(
            client=client,
            settings=settings,
            embedding_adapter=embedding_adapter,
            case=case,
            sparse_vector_name=sparse_vector_name,
            gate_fn=apply_source_document_identifier_aggregation,
        )
        for case in cases
    ]
    report = RetrievalBenchmarkReport(
        summary=_summarize(
            "qdrant-hybrid:source-document-identifier-coverage-v1",
            [case.gated_result for case in case_results],
        ),
        cases=[case.gated_result for case in case_results],
    )
    metadata = _qdrant_smoke_metadata(settings, source_ids, chunking_strategy)
    metadata.update({
        "benchmark_fixture": "split-chunk-identifier-v1",
        "cases_path": str(cases_path),
        "empty_cases_path": str(empty_cases_path),
        "retrieval_mode": "dense+sparse-hybrid",
        "aggregation_policy": "source-document-identifier-coverage-v1",
        "sparse_vector_name": sparse_vector_name,
        "sparse_vectorizer": QDRANT_LEXICAL_SPARSE_VECTORIZER_ID,
        "fusion": QDRANT_HYBRID_FUSION_STRATEGY,
        "score_filter": "disabled-for-rrf-fusion-score",
    })
    aggregation_report = QdrantHybridGatingEvidenceReport(
        candidate=qdrant_bge_hybrid_multi_chunk_aggregation_candidate(settings),
        report=report,
        cases=case_results,
        metadata=metadata,
        indexed_sources=indexed_sources,
    )
    json_path = export_qdrant_hybrid_gating_evidence_json(
        aggregation_report,
        output_dir / "qdrant-bge-m3-hybrid-multi-chunk-aggregation.json",
    )
    markdown_path = export_qdrant_hybrid_gating_evidence_markdown(
        aggregation_report,
        output_dir / "qdrant-bge-m3-hybrid-multi-chunk-aggregation.md",
    )
    return QdrantHybridGatingEvidenceReport(
        candidate=aggregation_report.candidate,
        report=aggregation_report.report,
        cases=aggregation_report.cases,
        metadata=aggregation_report.metadata,
        indexed_sources=aggregation_report.indexed_sources,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_identifier_alias_governance_evidence(
    output_dir: Path,
    catalog_path: Path = Path("app/data/identifier_alias_catalog.json"),
) -> IdentifierAliasGovernanceReport:
    aliases = load_identifier_alias_catalog(catalog_path)
    report = IdentifierAliasGovernanceReport(
        aliases=aliases,
        summary=_alias_governance_summary(aliases),
        decision_notes=_alias_governance_decision_notes(aliases),
    )
    json_path = export_identifier_alias_governance_json(
        report,
        output_dir / "identifier-alias-governance.json",
    )
    markdown_path = export_identifier_alias_governance_markdown(
        report,
        output_dir / "identifier-alias-governance.md",
    )
    return IdentifierAliasGovernanceReport(
        aliases=report.aliases,
        summary=report.summary,
        decision_notes=report.decision_notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_bge_threshold_sweep_evidence(
    output_dir: Path,
    thresholds: list[float],
    cases_path: Path = Path("tests/fixtures/retrieval_benchmark_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
) -> QdrantThresholdSweepEvidenceReport:
    settings = settings or get_settings()
    validated_thresholds = _validate_thresholds(thresholds)
    reports = [
        export_qdrant_bge_smoke_evidence(
            output_dir=output_dir,
            cases_path=cases_path,
            source_ids=source_ids,
            case_ids=case_ids,
            settings=settings.model_copy(
                update={"rag_score_threshold": threshold}
            ),
            write_files=False,
            chunking_strategy=chunking_strategy,
        )
        for threshold in validated_thresholds
    ]
    sweep_report = QdrantThresholdSweepEvidenceReport(
        candidate=qdrant_bge_smoke_candidate(settings),
        thresholds=validated_thresholds,
        reports=reports,
        metadata=_qdrant_threshold_sweep_metadata(
            settings=settings,
            source_ids=source_ids or ["refund_policy_docs", "logistics_faq"],
            thresholds=validated_thresholds,
            chunking_strategy=chunking_strategy,
        ),
    )
    json_path = export_qdrant_threshold_sweep_evidence_json(
        sweep_report,
        output_dir / "qdrant-bge-m3-threshold-sweep.json",
    )
    markdown_path = export_qdrant_threshold_sweep_evidence_markdown(
        sweep_report,
        output_dir / "qdrant-bge-m3-threshold-sweep.md",
    )
    return QdrantThresholdSweepEvidenceReport(
        candidate=sweep_report.candidate,
        thresholds=sweep_report.thresholds,
        reports=sweep_report.reports,
        metadata=sweep_report.metadata,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_bge_chunking_comparison_evidence(
    output_dir: Path,
    strategies: list[str] | None = None,
    cases_path: Path = Path("tests/fixtures/retrieval_benchmark_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
) -> QdrantChunkingComparisonReport:
    settings = settings or get_settings()
    source_ids = source_ids or ["refund_policy_docs", "logistics_faq"]
    if strategies is None:
        strategies = [
            QDRANT_CHUNKING_STRATEGY,
            QDRANT_SECTION_CHUNKING_STRATEGY,
            QDRANT_TOKEN_WINDOW_CHUNKING_STRATEGY,
        ]
    _validate_chunking_strategies(strategies)
    reports = [
        export_qdrant_bge_smoke_evidence(
            output_dir=output_dir,
            cases_path=cases_path,
            source_ids=source_ids,
            case_ids=case_ids,
            settings=settings,
            write_files=False,
            chunking_strategy=strategy,
        )
        for strategy in strategies
    ]
    comparison = QdrantChunkingComparisonReport(
        strategies=strategies,
        reports=reports,
        metadata={
            "created_at": datetime.now(UTC).isoformat(),
            "embedding_provider": settings.embedding_provider,
            "embedding_model": settings.embedding_model,
            "embedding_model_path": (
                str(settings.embedding_model_path)
                if settings.embedding_model_path is not None
                else ""
            ),
            "rag_score_threshold": str(settings.rag_score_threshold),
            "source_ids": source_ids,
        },
    )
    json_path = export_qdrant_chunking_comparison_json(
        comparison,
        output_dir / "qdrant-bge-m3-chunking-comparison.json",
    )
    markdown_path = export_qdrant_chunking_comparison_markdown(
        comparison,
        output_dir / "qdrant-bge-m3-chunking-comparison.md",
    )
    return QdrantChunkingComparisonReport(
        strategies=comparison.strategies,
        reports=comparison.reports,
        metadata=comparison.metadata,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def export_qdrant_threshold_recommendation(
    sweep_path: Path,
    output_dir: Path | None = None,
    gates: ThresholdRecommendationGates | None = None,
) -> QdrantThresholdRecommendation:
    gates = gates or ThresholdRecommendationGates()
    recommendation = recommend_qdrant_threshold_from_sweep(sweep_path, gates)
    output_dir = output_dir or sweep_path.parent
    json_path = export_qdrant_threshold_recommendation_json(
        recommendation,
        output_dir / "qdrant-bge-m3-threshold-recommendation.json",
    )
    markdown_path = export_qdrant_threshold_recommendation_markdown(
        recommendation,
        output_dir / "qdrant-bge-m3-threshold-recommendation.md",
    )
    return QdrantThresholdRecommendation(
        selected_threshold=recommendation.selected_threshold,
        gates=recommendation.gates,
        selected_metrics=recommendation.selected_metrics,
        sweep_path=recommendation.sweep_path,
        approval_status=recommendation.approval_status,
        caveats=recommendation.caveats,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def recommend_qdrant_threshold_from_sweep(
    sweep_path: Path,
    gates: ThresholdRecommendationGates | None = None,
) -> QdrantThresholdRecommendation:
    gates = gates or ThresholdRecommendationGates()
    _validate_recommendation_gates(gates)
    payload = json.loads(sweep_path.read_text(encoding="utf-8"))
    rows = sorted(payload.get("summary", []), key=lambda row: row["threshold"])
    for row in rows:
        if _threshold_row_passes_gates(row, gates):
            return QdrantThresholdRecommendation(
                selected_threshold=float(row["threshold"]),
                gates=gates,
                selected_metrics={
                    "total_cases": int(row["total_cases"]),
                    "hit_rate": float(row["hit_rate"]),
                    "citation_match_rate": float(row["citation_match_rate"]),
                    "empty_handling_rate": float(row["empty_handling_rate"]),
                },
                sweep_path=str(sweep_path),
                approval_status="local_seed_recommendation",
                caveats=[
                    "This recommendation is based on local Chinese seed evidence only.",
                    "It does not change the runtime RAG_SCORE_THRESHOLD default.",
                    "Regenerate the recommendation after adding customer-specific cases or changing chunking.",
                ],
            )
    raise ValueError("No threshold satisfies the configured recommendation gates.")


def default_chunking_strategy_candidates() -> list[ChunkingStrategyCandidate]:
    return [
        ChunkingStrategyCandidate(
            id="markdown-paragraph-v1",
            description="Current local markdown paragraph baseline used by Qdrant ingestion.",
            implementation_status="implemented",
            expected_fit="simple markdown, short procedures, deterministic local evidence",
            tradeoffs=[
                "Stable and easy to audit.",
                "Can be too coarse when one paragraph contains several details.",
                "Does not model PDF/Word structure or token overlap.",
            ],
        ),
        ChunkingStrategyCandidate(
            id="markdown-section-v1",
            description="Planned section-aware markdown chunking using headings and paragraphs.",
            implementation_status="runnable",
            expected_fit="manuals, policy sections, documents with useful headings",
            tradeoffs=[
                "May improve citation context for long sections.",
                "Needs heading-aware citation and section boundary rules.",
                "Still does not solve scanned documents or tables.",
            ],
        ),
        ChunkingStrategyCandidate(
            id="token-window-v1",
            description="Runnable token-window chunking with overlap for long dense content.",
            implementation_status="runnable",
            expected_fit="long paragraphs, pasted policy text, PDF/Word extracted body text",
            tradeoffs=[
                "May improve recall inside long dense sections.",
                "Can duplicate evidence and complicate citation stability.",
                "Uses a deterministic lightweight tokenizer until production tokenizer evidence exists.",
            ],
        ),
    ]


def evaluate_chunking_strategy_candidates(
    source_ids: list[str] | None = None,
    settings: Settings | None = None,
    candidates: list[ChunkingStrategyCandidate] | None = None,
) -> ChunkingStrategyEvaluation:
    settings = settings or get_settings()
    source_ids = source_ids or ["refund_policy_docs", "logistics_faq"]
    candidates = candidates or default_chunking_strategy_candidates()
    _validate_candidate_ids(candidates, "chunking strategy candidate")
    results = [
        _evaluate_chunking_candidate(candidate, source_ids, settings)
        for candidate in candidates
    ]
    return ChunkingStrategyEvaluation(results=results)


def export_chunking_strategy_evaluation(
    output_dir: Path,
    source_ids: list[str] | None = None,
    settings: Settings | None = None,
    candidates: list[ChunkingStrategyCandidate] | None = None,
) -> ChunkingStrategyEvaluation:
    evaluation = evaluate_chunking_strategy_candidates(
        source_ids=source_ids,
        settings=settings,
        candidates=candidates,
    )
    json_path = export_chunking_strategy_evaluation_json(
        evaluation,
        output_dir / "chunking-strategy-candidates.json",
    )
    markdown_path = export_chunking_strategy_evaluation_markdown(
        evaluation,
        output_dir / "chunking-strategy-candidates.md",
    )
    return ChunkingStrategyEvaluation(
        results=evaluation.results,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def default_query_rewrite_candidates() -> list[QueryRewriteCandidate]:
    return [
        QueryRewriteCandidate(
            id="original-query-baseline",
            description="Original benchmark queries without rewrite.",
            implementation_status="baseline",
            rewrite_policy="none",
            risk_notes=[
                "Used as the regression control for any future rewrite strategy.",
                "Does not improve ambiguous or terse user wording.",
            ],
        ),
        QueryRewriteCandidate(
            id="controlled-support-rewrite-v1",
            description=(
                "Deterministic support-domain rewrite for selected non-empty "
                "benchmark cases."
            ),
            implementation_status="candidate",
            rewrite_policy="controlled_support_rules",
            risk_notes=[
                "Only rewrites known benchmark cases; not a general production policy.",
                "Expected-empty cases are never rewritten to avoid false positives.",
                "Runtime adoption still requires broader false-positive evidence.",
            ],
        ),
    ]


def evaluate_query_rewrite_candidates(
    cases: list[RetrievalBenchmarkCase],
    candidates: list[QueryRewriteCandidate] | None = None,
    settings: Settings | None = None,
) -> QueryRewriteCandidateEvaluation:
    candidates = candidates or default_query_rewrite_candidates()
    _validate_candidate_ids(candidates, "query rewrite candidate")
    settings = settings or Settings(rag_retrieval_backend="fixture")

    results = [
        _evaluate_query_rewrite_candidate(candidate, cases, settings)
        for candidate in candidates
    ]
    return QueryRewriteCandidateEvaluation(results=results)


def export_query_rewrite_candidate_evaluation(
    output_dir: Path,
    cases_path: Path = Path("tests/fixtures/retrieval_benchmark_cases.json"),
    candidates: list[QueryRewriteCandidate] | None = None,
    settings: Settings | None = None,
) -> QueryRewriteCandidateEvaluation:
    cases = load_benchmark_cases(cases_path)
    evaluation = evaluate_query_rewrite_candidates(
        cases=cases,
        candidates=candidates,
        settings=settings,
    )
    json_path = export_query_rewrite_candidate_evaluation_json(
        evaluation,
        output_dir / "query-rewrite-candidates.json",
    )
    markdown_path = export_query_rewrite_candidate_evaluation_markdown(
        evaluation,
        output_dir / "query-rewrite-candidates.md",
    )
    return QueryRewriteCandidateEvaluation(
        results=evaluation.results,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def default_evidence_grading_candidates() -> list[EvidenceGradingCandidate]:
    return [
        EvidenceGradingCandidate(
            id="citation-match-grader-v1",
            description="Strict local grader that requires the expected citation.",
            implementation_status="candidate",
            grading_policy="citation_match",
            risk_notes=[
                "Can mark source-level evidence as insufficient when citation granularity changes.",
                "Useful as a strict grounding gate baseline, not a runtime answer gate.",
            ],
        ),
        EvidenceGradingCandidate(
            id="source-match-grader-v1",
            description="Looser local grader that accepts the expected source.",
            implementation_status="candidate",
            grading_policy="source_match",
            risk_notes=[
                "Can over-credit evidence when the correct source contains multiple topics.",
                "Useful for diagnosing citation granularity problems before reranking.",
            ],
        ),
    ]


def evaluate_evidence_grading_candidates(
    cases: list[RetrievalBenchmarkCase],
    candidates: list[EvidenceGradingCandidate] | None = None,
    settings: Settings | None = None,
) -> EvidenceGradingCandidateEvaluation:
    candidates = candidates or default_evidence_grading_candidates()
    _validate_candidate_ids(candidates, "evidence grading candidate")
    settings = settings or Settings(rag_retrieval_backend="fixture")
    retriever = create_document_retriever(settings)
    benchmark_results = [_run_case(retriever, case) for case in cases]
    report = RetrievalBenchmarkReport(
        summary=_summarize(retriever.backend_name, benchmark_results),
        cases=benchmark_results,
    )
    results = [
        _evaluate_evidence_grading_candidate(candidate, cases, report)
        for candidate in candidates
    ]
    return EvidenceGradingCandidateEvaluation(results=results)


def export_evidence_grading_candidate_evaluation(
    output_dir: Path,
    cases_path: Path = Path("tests/fixtures/retrieval_benchmark_cases.json"),
    candidates: list[EvidenceGradingCandidate] | None = None,
    settings: Settings | None = None,
) -> EvidenceGradingCandidateEvaluation:
    cases = load_benchmark_cases(cases_path)
    evaluation = evaluate_evidence_grading_candidates(
        cases=cases,
        candidates=candidates,
        settings=settings,
    )
    json_path = export_evidence_grading_candidate_evaluation_json(
        evaluation,
        output_dir / "evidence-grading-candidates.json",
    )
    markdown_path = export_evidence_grading_candidate_evaluation_markdown(
        evaluation,
        output_dir / "evidence-grading-candidates.md",
    )
    return EvidenceGradingCandidateEvaluation(
        results=evaluation.results,
        json_path=json_path,
        markdown_path=markdown_path,
    )


def benchmark_report_to_dict(report: RetrievalBenchmarkReport) -> dict:
    return {
        "summary": asdict(report.summary),
        "cases": [asdict(case) for case in report.cases],
    }


def candidate_evaluation_to_dict(
    candidate: RetrievalCandidate,
    report: RetrievalBenchmarkReport,
) -> dict:
    return {
        "candidate": asdict(candidate),
        "report": benchmark_report_to_dict(report),
    }


def qdrant_smoke_evidence_to_dict(report: QdrantSmokeEvidenceReport) -> dict:
    return {
        "candidate": asdict(report.candidate),
        "metadata": report.metadata,
        "indexed_sources": report.indexed_sources,
        "report": benchmark_report_to_dict(report.report),
    }


def qdrant_hybrid_gating_evidence_to_dict(
    report: QdrantHybridGatingEvidenceReport,
) -> dict:
    return {
        "candidate": asdict(report.candidate),
        "metadata": report.metadata,
        "indexed_sources": report.indexed_sources,
        "report": benchmark_report_to_dict(report.report),
        "cases": [
            {
                "id": case.id,
                "category": case.category,
                "difficulty": case.difficulty,
                "expect_empty": case.expect_empty,
                "query_identifiers": case.query_identifiers,
                "gate_applied": case.gate_applied,
                "raw_returned_citations": case.raw_returned_citations,
                "raw_returned_source_ids": case.raw_returned_source_ids,
                "gated_result": asdict(case.gated_result),
            }
            for case in report.cases
        ],
    }


def identifier_alias_governance_to_dict(
    report: IdentifierAliasGovernanceReport,
) -> dict:
    return {
        "summary": report.summary,
        "aliases": [asdict(alias) for alias in report.aliases],
        "decision_notes": report.decision_notes,
    }


def qdrant_threshold_sweep_evidence_to_dict(
    report: QdrantThresholdSweepEvidenceReport,
) -> dict:
    return {
        "candidate": asdict(report.candidate),
        "metadata": report.metadata,
        "thresholds": report.thresholds,
        "reports": [
            qdrant_smoke_evidence_to_dict(smoke_report)
            for smoke_report in report.reports
        ],
        "summary": [
            {
                "threshold": threshold,
                "total_cases": smoke_report.report.summary.total_cases,
                "hit_rate": smoke_report.report.summary.hit_rate,
                "citation_match_rate": (
                    smoke_report.report.summary.citation_match_rate
                ),
                "empty_handling_rate": (
                    smoke_report.report.summary.empty_handling_rate
                ),
            }
            for threshold, smoke_report in zip(report.thresholds, report.reports)
        ],
    }


def qdrant_chunking_comparison_to_dict(
    report: QdrantChunkingComparisonReport,
) -> dict:
    return {
        "metadata": report.metadata,
        "strategies": report.strategies,
        "summary": [
            _chunking_comparison_summary(strategy, smoke_report)
            for strategy, smoke_report in zip(report.strategies, report.reports)
        ],
        "reports": [
            qdrant_smoke_evidence_to_dict(smoke_report)
            for smoke_report in report.reports
        ],
    }


def qdrant_threshold_recommendation_to_dict(
    recommendation: QdrantThresholdRecommendation,
) -> dict:
    return {
        "selected_threshold": recommendation.selected_threshold,
        "gates": asdict(recommendation.gates),
        "selected_metrics": recommendation.selected_metrics,
        "sweep_path": recommendation.sweep_path,
        "approval_status": recommendation.approval_status,
        "caveats": recommendation.caveats,
    }


def chunking_strategy_evaluation_to_dict(
    evaluation: ChunkingStrategyEvaluation,
) -> dict:
    return {
        "results": [
            {
                "candidate": asdict(result.candidate),
                "source_ids": result.source_ids,
                "total_chunks": result.total_chunks,
                "citation_stability": result.citation_stability,
                "long_section_support": result.long_section_support,
                "decision_notes": result.decision_notes,
            }
            for result in evaluation.results
        ]
    }


def query_rewrite_candidate_evaluation_to_dict(
    evaluation: QueryRewriteCandidateEvaluation,
) -> dict:
    return {
        "results": [
            {
                "candidate": asdict(result.candidate),
                "total_cases": result.total_cases,
                "rewritten_cases": result.rewritten_cases,
                "rewrite_rate": result.rewrite_rate,
                "expected_empty_rewrites": result.expected_empty_rewrites,
                "report": benchmark_report_to_dict(result.report),
                "cases": [
                    {
                        "case_id": case.case_id,
                        "category": case.category,
                        "difficulty": case.difficulty,
                        "original_query": case.original_query,
                        "rewritten_query": case.rewritten_query,
                        "rewritten": case.rewritten,
                        "expect_empty": case.expect_empty,
                        "result": asdict(case.result),
                    }
                    for case in result.cases
                ],
                "decision_notes": result.decision_notes,
            }
            for result in evaluation.results
        ]
    }


def evidence_grading_candidate_evaluation_to_dict(
    evaluation: EvidenceGradingCandidateEvaluation,
) -> dict:
    return {
        "results": [
            {
                "candidate": asdict(result.candidate),
                "total_cases": result.total_cases,
                "answer_bearing_rate": result.answer_bearing_rate,
                "related_insufficient_count": result.related_insufficient_count,
                "missing_evidence_count": result.missing_evidence_count,
                "unexpected_evidence_count": result.unexpected_evidence_count,
                "expected_empty_pass_rate": result.expected_empty_pass_rate,
                "report": benchmark_report_to_dict(result.report),
                "cases": [
                    {
                        "case_id": case.case_id,
                        "category": case.category,
                        "difficulty": case.difficulty,
                        "expected_source_id": case.expected_source_id,
                        "expected_citation": case.expected_citation,
                        "returned_source_ids": case.returned_source_ids,
                        "returned_citations": case.returned_citations,
                        "grading_label": case.grading_label,
                        "grading_reason": case.grading_reason,
                        "result": asdict(case.result),
                    }
                    for case in result.cases
                ],
                "decision_notes": result.decision_notes,
            }
            for result in evaluation.results
        ]
    }


def embedding_candidate_result_to_dict(result: EmbeddingCandidateResult) -> dict:
    return asdict(result)


def export_benchmark_report_json(
    report: RetrievalBenchmarkReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(benchmark_report_to_dict(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def export_candidate_evaluation_json(
    candidate: RetrievalCandidate,
    report: RetrievalBenchmarkReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            candidate_evaluation_to_dict(candidate, report),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_embedding_candidate_json(
    result: EmbeddingCandidateResult,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            embedding_candidate_result_to_dict(result),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_qdrant_smoke_evidence_json(
    report: QdrantSmokeEvidenceReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            qdrant_smoke_evidence_to_dict(report),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_qdrant_hybrid_gating_evidence_json(
    report: QdrantHybridGatingEvidenceReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            qdrant_hybrid_gating_evidence_to_dict(report),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_identifier_alias_governance_json(
    report: IdentifierAliasGovernanceReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            identifier_alias_governance_to_dict(report),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_qdrant_threshold_sweep_evidence_json(
    report: QdrantThresholdSweepEvidenceReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            qdrant_threshold_sweep_evidence_to_dict(report),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_qdrant_chunking_comparison_json(
    report: QdrantChunkingComparisonReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            qdrant_chunking_comparison_to_dict(report),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_qdrant_threshold_recommendation_json(
    recommendation: QdrantThresholdRecommendation,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            qdrant_threshold_recommendation_to_dict(recommendation),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_chunking_strategy_evaluation_json(
    evaluation: ChunkingStrategyEvaluation,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            chunking_strategy_evaluation_to_dict(evaluation),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_query_rewrite_candidate_evaluation_json(
    evaluation: QueryRewriteCandidateEvaluation,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            query_rewrite_candidate_evaluation_to_dict(evaluation),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def export_evidence_grading_candidate_evaluation_json(
    evaluation: EvidenceGradingCandidateEvaluation,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            evidence_grading_candidate_evaluation_to_dict(evaluation),
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return path


def render_benchmark_report_markdown(report: RetrievalBenchmarkReport) -> str:
    summary = report.summary
    lines = [
        "# Retrieval Benchmark Report",
        "",
        "## Summary",
        "",
        "| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |",
        "| --- | ---: | ---: | ---: | ---: |",
        (
            f"| {summary.backend} | {summary.total_cases} | {summary.hit_rate:.4f} | "
            f"{summary.citation_match_rate:.4f} | {summary.empty_handling_rate:.4f} |"
        ),
        "",
        "## Category Summary",
        "",
        "| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for category, metrics in summary.category_summaries.items():
        lines.append(
            f"| {category} | {metrics['total_cases']} | {metrics['hit_rate']:.4f} | "
            f"{metrics['citation_match_rate']:.4f} | {metrics['empty_handling_rate']:.4f} |"
        )

    lines.extend([
        "",
        "## Case Results",
        "",
        "| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- |",
    ])
    for case in report.cases:
        empty = "" if case.empty_query_handling is None else str(case.empty_query_handling).lower()
        lines.append(
            f"| {case.id} | {case.category} | {case.difficulty} | "
            f"{str(case.hit_at_k).lower()} | {str(case.citation_match).lower()} | "
            f"{empty} | {case.latency_ms:.3f} | {', '.join(case.returned_citations)} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_candidate_evaluation_markdown(
    candidate: RetrievalCandidate,
    report: RetrievalBenchmarkReport,
) -> str:
    metadata = candidate.metadata or {}
    lines = [
        "# Retrieval Candidate Evaluation",
        "",
        "## Candidate",
        "",
        "| ID | Backend | Description |",
        "| --- | --- | --- |",
        f"| {candidate.id} | {candidate.backend} | {candidate.description} |",
    ]
    if metadata:
        lines.extend([
            "",
            "## Metadata",
            "",
            "| Key | Value |",
            "| --- | --- |",
        ])
        for key, value in sorted(metadata.items()):
            lines.append(f"| {key} | {value} |")
    lines.extend(["", render_benchmark_report_markdown(report)])
    return "\n".join(lines)


def render_qdrant_smoke_evidence_markdown(report: QdrantSmokeEvidenceReport) -> str:
    lines = [
        "# Qdrant BGE-M3 Smoke Evidence",
        "",
        "## Candidate",
        "",
        "| ID | Backend | Description |",
        "| --- | --- | --- |",
        (
            f"| {report.candidate.id} | {report.candidate.backend} | "
            f"{report.candidate.description} |"
        ),
        "",
        "## Metadata",
        "",
        "| Key | Value |",
        "| --- | --- |",
    ]
    for key, value in sorted(report.metadata.items()):
        lines.append(f"| {key} | {_markdown_value(value)} |")

    lines.extend([
        "",
        "## Indexed Sources",
        "",
        "| Source | Job ID | Chunk Count | Status |",
        "| --- | --- | ---: | --- |",
    ])
    for source_id, source in sorted(report.indexed_sources.items()):
        lines.append(
            f"| {source_id} | {source['job_id']} | "
            f"{source['chunk_count']} | {source['status']} |"
        )

    lines.extend(["", render_benchmark_report_markdown(report.report)])
    return "\n".join(lines)


def render_qdrant_hybrid_gating_evidence_markdown(
    report: QdrantHybridGatingEvidenceReport,
) -> str:
    lines = [
        "# Qdrant BGE-M3 Hybrid Gating Evidence",
        "",
        "## Candidate",
        "",
        "| ID | Backend | Description |",
        "| --- | --- | --- |",
        (
            f"| {report.candidate.id} | {report.candidate.backend} | "
            f"{report.candidate.description} |"
        ),
        "",
        "## Metadata",
        "",
        "| Key | Value |",
        "| --- | --- |",
    ]
    for key, value in sorted(report.metadata.items()):
        lines.append(f"| {key} | {_markdown_value(value)} |")

    lines.extend([
        "",
        "## Indexed Sources",
        "",
        "| Source | Job ID | Chunk Count | Status |",
        "| --- | --- | ---: | --- |",
    ])
    for source_id, source in sorted(report.indexed_sources.items()):
        lines.append(
            f"| {source_id} | {source['job_id']} | "
            f"{source['chunk_count']} | {source['status']} |"
        )

    summary = report.report.summary
    lines.extend([
        "",
        "## Gated Summary",
        "",
        "| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |",
        "| --- | ---: | ---: | ---: | ---: |",
        (
            f"| {summary.backend} | {summary.total_cases} | "
            f"{summary.hit_rate:.4f} | {summary.citation_match_rate:.4f} | "
            f"{summary.empty_handling_rate:.4f} |"
        ),
        "",
        "## Raw And Gated Case Results",
        "",
        "| Case | Category | Identifiers | Gate Applied | Raw Citations | Gated Citations | Empty Handling |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for case in report.cases:
        empty = (
            ""
            if case.gated_result.empty_query_handling is None
            else str(case.gated_result.empty_query_handling).lower()
        )
        lines.append(
            f"| {case.id} | {case.category} | "
            f"{', '.join(case.query_identifiers)} | "
            f"{str(case.gate_applied).lower()} | "
            f"{', '.join(case.raw_returned_citations)} | "
            f"{', '.join(case.gated_result.returned_citations)} | {empty} |"
        )
    return "\n".join(lines)


def render_identifier_alias_governance_markdown(
    report: IdentifierAliasGovernanceReport,
) -> str:
    lines = [
        "# Identifier Alias Governance Evidence",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| total_aliases | {report.summary['total_aliases']} |",
    ]
    for status, count in sorted(report.summary["status_counts"].items()):
        lines.append(f"| status:{status} | {count} |")
    for risk_level, count in sorted(report.summary["risk_counts"].items()):
        lines.append(f"| risk:{risk_level} | {count} |")

    lines.extend([
        "",
        "## Alias Rules",
        "",
        "| ID | Canonical Prefix | Pattern | Owner | Status | Version | Risk |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for alias in report.aliases:
        lines.append(
            f"| {alias.id} | {alias.canonical_prefix} | `{alias.match_pattern}` | "
            f"{alias.owner} | {alias.status} | {alias.version} | {alias.risk_level} |"
        )

    lines.extend(["", "## Decision Notes", ""])
    lines.extend(f"- {note}" for note in report.decision_notes)
    return "\n".join(lines)


def render_qdrant_threshold_sweep_evidence_markdown(
    report: QdrantThresholdSweepEvidenceReport,
) -> str:
    lines = [
        "# Qdrant BGE-M3 Threshold Sweep Evidence",
        "",
        "## Candidate",
        "",
        "| ID | Backend | Description |",
        "| --- | --- | --- |",
        (
            f"| {report.candidate.id} | {report.candidate.backend} | "
            f"{report.candidate.description} |"
        ),
        "",
        "## Metadata",
        "",
        "| Key | Value |",
        "| --- | --- |",
    ]
    for key, value in sorted(report.metadata.items()):
        lines.append(f"| {key} | {_markdown_value(value)} |")

    lines.extend([
        "",
        "## Threshold Summary",
        "",
        "| Threshold | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ])
    for threshold, smoke_report in zip(report.thresholds, report.reports):
        summary = smoke_report.report.summary
        lines.append(
            f"| {threshold:.4f} | {summary.total_cases} | {summary.hit_rate:.4f} | "
            f"{summary.citation_match_rate:.4f} | {summary.empty_handling_rate:.4f} |"
        )

    lines.extend(["", "## Case Results By Threshold", ""])
    for threshold, smoke_report in zip(report.thresholds, report.reports):
        lines.extend([
            f"### Threshold {threshold:.4f}",
            "",
            "| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Returned Citations |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ])
        for case in smoke_report.report.cases:
            empty = (
                ""
                if case.empty_query_handling is None
                else str(case.empty_query_handling).lower()
            )
            lines.append(
                f"| {case.id} | {case.category} | {case.difficulty} | "
                f"{str(case.hit_at_k).lower()} | "
                f"{str(case.citation_match).lower()} | {empty} | "
                f"{', '.join(case.returned_citations)} |"
            )
        lines.append("")
    return "\n".join(lines)


def render_qdrant_chunking_comparison_markdown(
    report: QdrantChunkingComparisonReport,
) -> str:
    lines = [
        "# Qdrant BGE-M3 Chunking Comparison Evidence",
        "",
        "## Metadata",
        "",
        "| Key | Value |",
        "| --- | --- |",
    ]
    for key, value in sorted(report.metadata.items()):
        lines.append(f"| {key} | {_markdown_value(value)} |")
    lines.extend([
        "",
        "## Strategy Summary",
        "",
        "| Strategy | Chunk Count | Hit Rate | Citation Match Rate | Empty Handling Rate | Long-Section Hit Rate | Long-Section Citation Match Rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for strategy, smoke_report in zip(report.strategies, report.reports):
        summary = _chunking_comparison_summary(strategy, smoke_report)
        lines.append(
            f"| {strategy} | {summary['chunk_count']} | "
            f"{summary['hit_rate']:.4f} | "
            f"{summary['citation_match_rate']:.4f} | "
            f"{summary['empty_handling_rate']:.4f} | "
            f"{summary['long_section_hit_rate']:.4f} | "
            f"{summary['long_section_citation_match_rate']:.4f} |"
        )
    lines.extend(["", "## Case Results By Strategy", ""])
    for strategy, smoke_report in zip(report.strategies, report.reports):
        lines.extend([
            f"### {strategy}",
            "",
            "| Case | Category | Hit@K | Citation Match | Empty Handling | Returned Citations |",
            "| --- | --- | --- | --- | --- | --- |",
        ])
        for case in smoke_report.report.cases:
            empty = (
                ""
                if case.empty_query_handling is None
                else str(case.empty_query_handling).lower()
            )
            lines.append(
                f"| {case.id} | {case.category} | "
                f"{str(case.hit_at_k).lower()} | "
                f"{str(case.citation_match).lower()} | {empty} | "
                f"{', '.join(case.returned_citations)} |"
            )
        lines.append("")
    return "\n".join(lines)


def render_qdrant_threshold_recommendation_markdown(
    recommendation: QdrantThresholdRecommendation,
) -> str:
    metrics = recommendation.selected_metrics
    lines = [
        "# Qdrant BGE-M3 Threshold Recommendation",
        "",
        "## Recommendation",
        "",
        "| Selected Threshold | Approval Status | Source Sweep |",
        "| ---: | --- | --- |",
        (
            f"| {recommendation.selected_threshold:.4f} | "
            f"{recommendation.approval_status} | {recommendation.sweep_path} |"
        ),
        "",
        "## Gates",
        "",
        "| Min Hit Rate | Min Citation Match Rate | Min Empty Handling Rate |",
        "| ---: | ---: | ---: |",
        (
            f"| {recommendation.gates.min_hit_rate:.4f} | "
            f"{recommendation.gates.min_citation_match_rate:.4f} | "
            f"{recommendation.gates.min_empty_handling_rate:.4f} |"
        ),
        "",
        "## Selected Metrics",
        "",
        "| Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |",
        "| ---: | ---: | ---: | ---: |",
        (
            f"| {metrics['total_cases']} | {metrics['hit_rate']:.4f} | "
            f"{metrics['citation_match_rate']:.4f} | "
            f"{metrics['empty_handling_rate']:.4f} |"
        ),
        "",
        "## Caveats",
        "",
    ]
    lines.extend(f"- {caveat}" for caveat in recommendation.caveats)
    lines.append("")
    return "\n".join(lines)


def render_chunking_strategy_evaluation_markdown(
    evaluation: ChunkingStrategyEvaluation,
) -> str:
    lines = [
        "# Chunking Strategy Candidate Evaluation",
        "",
        "| Candidate | Status | Total Chunks | Citation Stability | Long-Section Support |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for result in evaluation.results:
        total_chunks = "" if result.total_chunks is None else str(result.total_chunks)
        lines.append(
            f"| {result.candidate.id} | {result.candidate.implementation_status} | "
            f"{total_chunks} | {result.citation_stability} | "
            f"{result.long_section_support} |"
        )
    lines.extend(["", "## Candidate Notes", ""])
    for result in evaluation.results:
        lines.extend([
            f"### {result.candidate.id}",
            "",
            f"- Description: {result.candidate.description}",
            f"- Expected fit: {result.candidate.expected_fit}",
            f"- Source ids: {', '.join(result.source_ids)}",
        ])
        lines.extend(f"- Trade-off: {tradeoff}" for tradeoff in result.candidate.tradeoffs)
        lines.extend(f"- Decision note: {note}" for note in result.decision_notes)
        lines.append("")
    return "\n".join(lines)


def render_query_rewrite_candidate_evaluation_markdown(
    evaluation: QueryRewriteCandidateEvaluation,
) -> str:
    lines = [
        "# Query Rewrite Candidate Evaluation",
        "",
        "## Summary",
        "",
        "| Candidate | Status | Total Cases | Rewritten Cases | Rewrite Rate | Expected-empty Rewrites | Hit Rate | Citation Match Rate | Empty Handling Rate |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in evaluation.results:
        summary = result.report.summary
        lines.append(
            f"| {result.candidate.id} | {result.candidate.implementation_status} | "
            f"{result.total_cases} | {result.rewritten_cases} | "
            f"{result.rewrite_rate:.4f} | {result.expected_empty_rewrites} | "
            f"{summary.hit_rate:.4f} | {summary.citation_match_rate:.4f} | "
            f"{summary.empty_handling_rate:.4f} |"
        )

    lines.extend(["", "## Candidate Notes", ""])
    for result in evaluation.results:
        lines.extend([
            f"### {result.candidate.id}",
            "",
            f"- Description: {result.candidate.description}",
            f"- Rewrite policy: {result.candidate.rewrite_policy}",
        ])
        lines.extend(f"- Risk note: {note}" for note in result.candidate.risk_notes)
        lines.extend(f"- Decision note: {note}" for note in result.decision_notes)
        lines.append("")

    lines.extend([
        "## Case Results",
        "",
        "| Candidate | Case | Category | Rewritten | Expected Empty | Hit@K | Citation Match | Empty Handling | Original Query | Rewritten Query |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for result in evaluation.results:
        for case in result.cases:
            empty = (
                ""
                if case.result.empty_query_handling is None
                else str(case.result.empty_query_handling).lower()
            )
            lines.append(
                f"| {result.candidate.id} | {case.case_id} | {case.category} | "
                f"{str(case.rewritten).lower()} | "
                f"{str(case.expect_empty).lower()} | "
                f"{str(case.result.hit_at_k).lower()} | "
                f"{str(case.result.citation_match).lower()} | {empty} | "
                f"{case.original_query} | {case.rewritten_query} |"
            )
    lines.append("")
    return "\n".join(lines)


def render_evidence_grading_candidate_evaluation_markdown(
    evaluation: EvidenceGradingCandidateEvaluation,
) -> str:
    lines = [
        "# Evidence Grading Candidate Evaluation",
        "",
        "## Summary",
        "",
        "| Candidate | Status | Total Cases | Answer-bearing Rate | Related-insufficient | Missing Evidence | Unexpected Evidence | Expected-empty Pass Rate |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in evaluation.results:
        lines.append(
            f"| {result.candidate.id} | {result.candidate.implementation_status} | "
            f"{result.total_cases} | {result.answer_bearing_rate:.4f} | "
            f"{result.related_insufficient_count} | "
            f"{result.missing_evidence_count} | "
            f"{result.unexpected_evidence_count} | "
            f"{result.expected_empty_pass_rate:.4f} |"
        )

    lines.extend(["", "## Candidate Notes", ""])
    for result in evaluation.results:
        lines.extend([
            f"### {result.candidate.id}",
            "",
            f"- Description: {result.candidate.description}",
            f"- Grading policy: {result.candidate.grading_policy}",
        ])
        lines.extend(f"- Risk note: {note}" for note in result.candidate.risk_notes)
        lines.extend(f"- Decision note: {note}" for note in result.decision_notes)
        lines.append("")

    lines.extend([
        "## Case Results",
        "",
        "| Candidate | Case | Category | Label | Reason | Expected Citation | Returned Citations |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for result in evaluation.results:
        for case in result.cases:
            lines.append(
                f"| {result.candidate.id} | {case.case_id} | {case.category} | "
                f"{case.grading_label} | {case.grading_reason} | "
                f"{case.expected_citation or ''} | "
                f"{', '.join(case.returned_citations)} |"
            )
    lines.append("")
    return "\n".join(lines)


def render_embedding_candidate_markdown(result: EmbeddingCandidateResult) -> str:
    candidate = result.candidate
    lines = [
        "# Embedding Candidate Evaluation",
        "",
        "## Candidate",
        "",
        "| ID | Provider Family | Model | Deployment | Approval Status |",
        "| --- | --- | --- | --- | --- |",
        (
            f"| {candidate.id} | {candidate.provider_family} | {candidate.model_name} | "
            f"{candidate.deployment_mode} | {candidate.approval_status} |"
        ),
        "",
        "## Enterprise Criteria",
        "",
        "| Criterion | Value | Covered |",
        "| --- | --- | --- |",
        f"| Language Profile | {candidate.language_profile} | {str(result.criteria_coverage['language_profile']).lower()} |",
        f"| Chinese-heavy Suitable | {str(candidate.chinese_heavy_suitable).lower()} | {str(result.criteria_coverage['chinese_heavy_suitable']).lower()} |",
        f"| Private Network Supported | {str(candidate.private_network_supported).lower()} | {str(result.criteria_coverage['private_network_supported']).lower()} |",
        f"| Vector Dimension | {candidate.vector_dimension or 'unknown'} | {str(result.criteria_coverage['vector_dimension']).lower()} |",
        f"| Data Residency | {candidate.data_residency} | {str(result.criteria_coverage['data_residency']).lower()} |",
        f"| Operational Complexity | {candidate.operational_complexity} | {str(result.criteria_coverage['operational_complexity']).lower()} |",
        f"| Reranker Compatibility | {candidate.reranker_compatibility} | {str(result.criteria_coverage['reranker_compatibility']).lower()} |",
        "",
        "## Readiness",
        "",
        f"- Status: {result.readiness_status}",
    ]
    if result.decision_notes:
        lines.extend(["", "## Decision Notes", ""])
        lines.extend(f"- {note}" for note in result.decision_notes)
    lines.append("")
    return "\n".join(lines)


def export_benchmark_report_markdown(
    report: RetrievalBenchmarkReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_benchmark_report_markdown(report), encoding="utf-8")
    return path


def export_candidate_evaluation_markdown(
    candidate: RetrievalCandidate,
    report: RetrievalBenchmarkReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_candidate_evaluation_markdown(candidate, report),
        encoding="utf-8",
    )
    return path


def export_embedding_candidate_markdown(
    result: EmbeddingCandidateResult,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_embedding_candidate_markdown(result), encoding="utf-8")
    return path


def export_qdrant_smoke_evidence_markdown(
    report: QdrantSmokeEvidenceReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_qdrant_smoke_evidence_markdown(report), encoding="utf-8")
    return path


def export_qdrant_hybrid_gating_evidence_markdown(
    report: QdrantHybridGatingEvidenceReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_qdrant_hybrid_gating_evidence_markdown(report),
        encoding="utf-8",
    )
    return path


def export_identifier_alias_governance_markdown(
    report: IdentifierAliasGovernanceReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_identifier_alias_governance_markdown(report),
        encoding="utf-8",
    )
    return path


def export_qdrant_threshold_sweep_evidence_markdown(
    report: QdrantThresholdSweepEvidenceReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_qdrant_threshold_sweep_evidence_markdown(report),
        encoding="utf-8",
    )
    return path


def export_qdrant_chunking_comparison_markdown(
    report: QdrantChunkingComparisonReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_qdrant_chunking_comparison_markdown(report),
        encoding="utf-8",
    )
    return path


def export_qdrant_threshold_recommendation_markdown(
    recommendation: QdrantThresholdRecommendation,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_qdrant_threshold_recommendation_markdown(recommendation),
        encoding="utf-8",
    )
    return path


def export_chunking_strategy_evaluation_markdown(
    evaluation: ChunkingStrategyEvaluation,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_chunking_strategy_evaluation_markdown(evaluation),
        encoding="utf-8",
    )
    return path


def export_query_rewrite_candidate_evaluation_markdown(
    evaluation: QueryRewriteCandidateEvaluation,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_query_rewrite_candidate_evaluation_markdown(evaluation),
        encoding="utf-8",
    )
    return path


def export_evidence_grading_candidate_evaluation_markdown(
    evaluation: EvidenceGradingCandidateEvaluation,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_evidence_grading_candidate_evaluation_markdown(evaluation),
        encoding="utf-8",
    )
    return path


def _index_qdrant_smoke_sources(
    client,
    settings: Settings,
    source_ids: list[str],
    embedding_adapter,
    chunking_strategy: str,
) -> dict[str, dict[str, str | int]]:
    status, reason = ensure_qdrant_collection(client, settings)
    if status != "ready":
        raise RuntimeError(reason or "Qdrant collection is not ready.")

    store = IndexLifecycleStore(settings)
    indexed_sources: dict[str, dict[str, str | int]] = {}
    for source_id in source_ids:
        job_id = f"smoke_{uuid4().hex}"
        chunks = embed_qdrant_chunks(
            _load_smoke_chunks(source_id, settings, chunking_strategy),
            embedding_adapter,
        )
        chunk_count = upsert_qdrant_chunks(client, chunks, settings)
        store.write_source_status(IndexStatusResponse(
            source_id=source_id,
            status="ready",
            backend="qdrant",
            indexed_at=datetime.now(UTC).isoformat(),
            latest_job_id=job_id,
            reason=f"Smoke upserted {chunk_count} Qdrant chunk(s).",
        ))
        indexed_sources[source_id] = {
            "job_id": job_id,
            "chunk_count": chunk_count,
            "status": "ready",
            "chunking_strategy": chunking_strategy,
        }
    return indexed_sources


def _index_qdrant_hybrid_smoke_sources(
    client,
    settings: Settings,
    source_ids: list[str],
    embedding_adapter,
    chunking_strategy: str,
    sparse_vector_name: str,
) -> dict[str, dict[str, str | int]]:
    status, reason = ensure_qdrant_hybrid_collection(
        client,
        settings,
        sparse_vector_name=sparse_vector_name,
    )
    if status != "ready":
        raise RuntimeError(reason or "Qdrant hybrid collection is not ready.")

    store = IndexLifecycleStore(settings)
    indexed_sources: dict[str, dict[str, str | int]] = {}
    for source_id in source_ids:
        job_id = f"hybrid_smoke_{uuid4().hex}"
        chunks = embed_qdrant_chunks(
            _load_smoke_chunks(source_id, settings, chunking_strategy),
            embedding_adapter,
        )
        chunk_count = upsert_qdrant_hybrid_chunks(
            client,
            chunks,
            settings,
            sparse_vector_name=sparse_vector_name,
        )
        store.write_source_status(IndexStatusResponse(
            source_id=source_id,
            status="ready",
            backend="qdrant",
            indexed_at=datetime.now(UTC).isoformat(),
            latest_job_id=job_id,
            reason=f"Hybrid smoke upserted {chunk_count} Qdrant chunk(s).",
        ))
        indexed_sources[source_id] = {
            "job_id": job_id,
            "chunk_count": chunk_count,
            "status": "ready",
            "chunking_strategy": chunking_strategy,
            "sparse_vector_name": sparse_vector_name,
        }
    return indexed_sources


def _run_qdrant_smoke_case(
    client,
    settings: Settings,
    embedding_adapter,
    case: RetrievalBenchmarkCase,
) -> RetrievalBenchmarkCaseResult:
    started_at = perf_counter()
    documents = query_qdrant_documents_for_text(
        client=client,
        query=case.query,
        source_ids=case.knowledge_base_ids,
        settings=settings,
        embedding_adapter=embedding_adapter,
        top_k=case.top_k,
    )
    latency_ms = (perf_counter() - started_at) * 1000
    returned_citations = [document.citation for document in documents]
    returned_source_ids = [document.source_id for document in documents]
    empty_query_handling = None
    if case.expect_empty:
        empty_query_handling = len(documents) == 0
    return RetrievalBenchmarkCaseResult(
        id=case.id,
        category=case.category,
        difficulty=case.difficulty,
        hit_at_k=(
            case.expected_source_id in returned_source_ids
            if case.expected_source_id is not None
            else len(documents) == 0
        ),
        citation_match=(
            case.expected_citation in returned_citations
            if case.expected_citation is not None
            else len(documents) == 0
        ),
        empty_query_handling=empty_query_handling,
        latency_ms=round(latency_ms, 3),
        returned_citations=returned_citations,
        returned_source_ids=returned_source_ids,
    )


def _run_qdrant_hybrid_smoke_case(
    client,
    settings: Settings,
    embedding_adapter,
    case: RetrievalBenchmarkCase,
    sparse_vector_name: str,
) -> RetrievalBenchmarkCaseResult:
    started_at = perf_counter()
    documents = query_qdrant_hybrid_documents_for_text(
        client=client,
        query=case.query,
        source_ids=case.knowledge_base_ids,
        settings=settings,
        embedding_adapter=embedding_adapter,
        top_k=case.top_k,
        sparse_vector_name=sparse_vector_name,
    )
    latency_ms = (perf_counter() - started_at) * 1000
    returned_citations = [document.citation for document in documents]
    returned_source_ids = [document.source_id for document in documents]
    empty_query_handling = None
    if case.expect_empty:
        empty_query_handling = len(documents) == 0
    return RetrievalBenchmarkCaseResult(
        id=case.id,
        category=case.category,
        difficulty=case.difficulty,
        hit_at_k=(
            case.expected_source_id in returned_source_ids
            if case.expected_source_id is not None
            else len(documents) == 0
        ),
        citation_match=(
            case.expected_citation in returned_citations
            if case.expected_citation is not None
            else len(documents) == 0
        ),
        empty_query_handling=empty_query_handling,
        latency_ms=round(latency_ms, 3),
        returned_citations=returned_citations,
        returned_source_ids=returned_source_ids,
    )


def apply_exact_identifier_containment_gate(
    query: str,
    documents: list[EvidenceDocument],
) -> tuple[list[EvidenceDocument], list[str], bool]:
    identifiers = extract_lexical_identifiers(query)
    if not identifiers:
        return documents, identifiers, False
    gated_documents = [
        document
        for document in documents
        if set(identifiers).issubset(set(extract_lexical_identifiers(document.snippet)))
    ]
    return gated_documents, identifiers, True


def extract_alias_aware_identifiers(text: str) -> list[str]:
    identifiers = {
        _canonicalize_identifier(identifier)
        for identifier in extract_lexical_identifiers(text)
    }
    identifiers.update(_local_noisy_identifier_aliases(text))
    return sorted(identifier for identifier in identifiers if identifier)


def load_identifier_alias_catalog(
    catalog_path: Path = Path("app/data/identifier_alias_catalog.json"),
) -> list[IdentifierAliasRule]:
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    aliases = [IdentifierAliasRule(**item) for item in payload]
    _validate_identifier_alias_catalog(aliases)
    return aliases


def apply_alias_aware_identifier_gate(
    query: str,
    documents: list[EvidenceDocument],
) -> tuple[list[EvidenceDocument], list[str], bool]:
    identifiers = extract_alias_aware_identifiers(query)
    if not identifiers:
        return documents, identifiers, False
    gated_documents = [
        document
        for document in documents
        if set(identifiers).issubset(set(extract_alias_aware_identifiers(document.snippet)))
    ]
    return gated_documents, identifiers, True


def apply_source_document_identifier_aggregation(
    query: str,
    documents: list[EvidenceDocument],
) -> tuple[list[EvidenceDocument], list[str], bool]:
    identifiers = extract_lexical_identifiers(query)
    if not identifiers:
        return documents, identifiers, False

    identifiers_set = set(identifiers)
    matching_groups: set[tuple[str, str]] = set()
    group_identifiers: dict[tuple[str, str], set[str]] = {}
    for document in documents:
        group_key = (document.source_id, document.document_id)
        group_identifiers.setdefault(group_key, set()).update(
            extract_lexical_identifiers(document.snippet)
        )
    for group_key, group_values in group_identifiers.items():
        if identifiers_set.issubset(group_values):
            matching_groups.add(group_key)

    aggregated_documents = [
        document
        for document in documents
        if (document.source_id, document.document_id) in matching_groups
    ]
    return aggregated_documents, identifiers, True


def _canonicalize_identifier(identifier: str) -> str:
    parts = []
    for part in identifier.lower().split("-"):
        if any(character.isdigit() for character in part):
            parts.append(part.replace("o", "0"))
        else:
            parts.append(part)
    return "-".join(parts)


def _local_noisy_identifier_aliases(text: str) -> set[str]:
    normalized = text.lower()
    compact = re.sub(r"[\s_\-]+", "", normalized)
    compact = re.sub(r"[：:，,。；;？?！!（）()【】\[\]]+", "", compact)
    aliases: set[str] = set()

    for alias in load_identifier_alias_catalog():
        for match in re.finditer(alias.match_pattern, compact):
            aliases.add(_canonical_identifier_from_alias_match(alias, match))
    return aliases


def _canonical_identifier_from_alias_match(
    alias: IdentifierAliasRule,
    match: re.Match,
) -> str:
    segments = []
    for index, value in enumerate(match.groups()):
        segment = _canonicalize_identifier(value)
        width = alias.segment_widths[index] if index < len(alias.segment_widths) else 0
        if width > 0:
            segment = segment.zfill(width)
        segments.append(segment)
    return "-".join([alias.canonical_prefix, *segments])


def _validate_identifier_alias_catalog(aliases: list[IdentifierAliasRule]) -> None:
    ids = [alias.id for alias in aliases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate identifier alias ids are not allowed.")
    for alias in aliases:
        if alias.status not in {"candidate", "approved", "deprecated"}:
            raise ValueError(f"Unsupported alias status for {alias.id}: {alias.status}")
        if alias.risk_level not in {"low", "medium", "high"}:
            raise ValueError(
                f"Unsupported alias risk level for {alias.id}: {alias.risk_level}"
            )
        if not alias.owner:
            raise ValueError(f"Alias owner is required for {alias.id}")
        re.compile(alias.match_pattern)


def _alias_governance_summary(
    aliases: list[IdentifierAliasRule],
) -> dict[str, int | dict[str, int]]:
    return {
        "total_aliases": len(aliases),
        "status_counts": dict(sorted(Counter(alias.status for alias in aliases).items())),
        "risk_counts": dict(
            sorted(Counter(alias.risk_level for alias in aliases).items())
        ),
    }


def _alias_governance_decision_notes(
    aliases: list[IdentifierAliasRule],
) -> list[str]:
    notes = [
        "This catalog is local evaluation evidence and is not a production alias service.",
        "Runtime retrieval defaults and public provider contracts remain unchanged.",
    ]
    candidate_count = sum(1 for alias in aliases if alias.status == "candidate")
    if candidate_count:
        notes.append(
            f"{candidate_count} alias rule(s) remain candidate status and require owner approval before production use."
        )
    high_risk_count = sum(1 for alias in aliases if alias.risk_level == "high")
    if high_risk_count:
        notes.append(f"{high_risk_count} high-risk alias rule(s) require review.")
    return notes


def _run_qdrant_hybrid_gated_smoke_case(
    client,
    settings: Settings,
    embedding_adapter,
    case: RetrievalBenchmarkCase,
    sparse_vector_name: str,
    gate_fn=apply_exact_identifier_containment_gate,
) -> HybridGatingCaseResult:
    started_at = perf_counter()
    raw_documents = query_qdrant_hybrid_documents_for_text(
        client=client,
        query=case.query,
        source_ids=case.knowledge_base_ids,
        settings=settings,
        embedding_adapter=embedding_adapter,
        top_k=case.top_k,
        sparse_vector_name=sparse_vector_name,
    )
    gated_documents, identifiers, gate_applied = gate_fn(
        query=case.query,
        documents=raw_documents,
    )
    latency_ms = (perf_counter() - started_at) * 1000
    return HybridGatingCaseResult(
        id=case.id,
        category=case.category,
        difficulty=case.difficulty,
        expect_empty=case.expect_empty,
        query_identifiers=identifiers,
        gate_applied=gate_applied,
        raw_returned_citations=[document.citation for document in raw_documents],
        raw_returned_source_ids=[document.source_id for document in raw_documents],
        gated_result=_benchmark_case_result_from_documents(
            case=case,
            documents=gated_documents,
            latency_ms=latency_ms,
        ),
    )


def _benchmark_case_result_from_documents(
    case: RetrievalBenchmarkCase,
    documents: list[EvidenceDocument],
    latency_ms: float,
) -> RetrievalBenchmarkCaseResult:
    returned_citations = [document.citation for document in documents]
    returned_source_ids = [document.source_id for document in documents]
    empty_query_handling = None
    if case.expect_empty:
        empty_query_handling = len(documents) == 0
    return RetrievalBenchmarkCaseResult(
        id=case.id,
        category=case.category,
        difficulty=case.difficulty,
        hit_at_k=(
            case.expected_source_id in returned_source_ids
            if case.expected_source_id is not None
            else len(documents) == 0
        ),
        citation_match=(
            case.expected_citation in returned_citations
            if case.expected_citation is not None
            else len(documents) == 0
        ),
        empty_query_handling=empty_query_handling,
        latency_ms=round(latency_ms, 3),
        returned_citations=returned_citations,
        returned_source_ids=returned_source_ids,
    )


def _qdrant_smoke_metadata(
    settings: Settings,
    source_ids: list[str],
    chunking_strategy: str = QDRANT_CHUNKING_STRATEGY,
) -> dict[str, str | list[str] | dict[str, str]]:
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "qdrant_url": settings.qdrant_url,
        "qdrant_collection": settings.qdrant_collection,
        "qdrant_vector_name": settings.qdrant_vector_name,
        "qdrant_vector_size": str(settings.qdrant_vector_size),
        "rag_score_threshold": str(settings.rag_score_threshold),
        "embedding_provider": settings.embedding_provider,
        "embedding_model": settings.embedding_model,
        "embedding_model_path": (
            str(settings.embedding_model_path)
            if settings.embedding_model_path is not None
            else ""
        ),
        "embedding_local_files_only": str(settings.embedding_local_files_only).lower(),
        "source_ids": source_ids,
        "chunking_strategy": chunking_strategy,
    }


def _qdrant_threshold_sweep_metadata(
    settings: Settings,
    source_ids: list[str],
    thresholds: list[float],
    chunking_strategy: str,
) -> dict[str, str | list[str] | dict[str, str]]:
    metadata = _qdrant_smoke_metadata(settings, source_ids, chunking_strategy)
    metadata["created_at"] = datetime.now(UTC).isoformat()
    metadata["thresholds"] = [str(threshold) for threshold in thresholds]
    metadata["rag_score_threshold"] = "sweep"
    return metadata


def _markdown_value(value) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        return ", ".join(f"{key}={item}" for key, item in sorted(value.items()))
    return str(value)


def _validate_candidates(candidates: list[RetrievalCandidate]) -> None:
    _validate_candidate_ids(candidates, "retrieval candidate")


def _validate_candidate_ids(candidates, label: str) -> None:
    seen = set()
    for candidate in candidates:
        if not re.fullmatch(r"[a-z0-9][a-z0-9_.-]*", candidate.id):
            raise ValueError(
                f"Invalid {label} id: {candidate.id}. "
                "Use lowercase letters, numbers, dots, underscores, or dashes."
            )
        if candidate.id in seen:
            raise ValueError(f"Duplicate {label} id: {candidate.id}")
        seen.add(candidate.id)


def _validate_thresholds(thresholds: list[float]) -> list[float]:
    if not thresholds:
        raise ValueError("At least one threshold is required.")
    normalized = [round(float(threshold), 4) for threshold in thresholds]
    if len(set(normalized)) != len(normalized):
        raise ValueError("Duplicate threshold values are not allowed.")
    invalid = [
        threshold
        for threshold in normalized
        if threshold < 0.0 or threshold > 1.0
    ]
    if invalid:
        raise ValueError("Threshold values must be between 0.0 and 1.0.")
    return sorted(normalized)


def _validate_chunking_strategies(strategies: list[str]) -> None:
    supported = {
        QDRANT_CHUNKING_STRATEGY,
        QDRANT_SECTION_CHUNKING_STRATEGY,
        QDRANT_TOKEN_WINDOW_CHUNKING_STRATEGY,
    }
    if not strategies:
        raise ValueError("At least one chunking strategy is required.")
    unsupported = [strategy for strategy in strategies if strategy not in supported]
    if unsupported:
        raise ValueError(f"Unsupported chunking strategies: {unsupported}")
    if len(set(strategies)) != len(strategies):
        raise ValueError("Duplicate chunking strategies are not allowed.")


def _validate_recommendation_gates(gates: ThresholdRecommendationGates) -> None:
    values = [
        gates.min_hit_rate,
        gates.min_citation_match_rate,
        gates.min_empty_handling_rate,
    ]
    if any(value < 0.0 or value > 1.0 for value in values):
        raise ValueError("Recommendation gates must be between 0.0 and 1.0.")


def _threshold_row_passes_gates(
    row: dict,
    gates: ThresholdRecommendationGates,
) -> bool:
    return (
        float(row["hit_rate"]) >= gates.min_hit_rate
        and float(row["citation_match_rate"]) >= gates.min_citation_match_rate
        and float(row["empty_handling_rate"]) >= gates.min_empty_handling_rate
    )


def _load_smoke_chunks(
    source_id: str,
    settings: Settings,
    chunking_strategy: str,
):
    if chunking_strategy == QDRANT_CHUNKING_STRATEGY:
        return load_qdrant_source_chunks(source_id, settings)
    if chunking_strategy == QDRANT_SECTION_CHUNKING_STRATEGY:
        return _load_section_candidate_chunks(source_id, settings)
    if chunking_strategy == QDRANT_TOKEN_WINDOW_CHUNKING_STRATEGY:
        return _load_token_window_candidate_chunks(source_id, settings)
    raise ValueError(f"Unsupported chunking strategy: {chunking_strategy}")


def _chunking_comparison_summary(
    strategy: str,
    smoke_report: QdrantSmokeEvidenceReport,
) -> dict[str, float | int | str]:
    category = smoke_report.report.summary.category_summaries.get(
        "long-section",
        {
            "hit_rate": 0.0,
            "citation_match_rate": 0.0,
        },
    )
    return {
        "strategy": strategy,
        "chunk_count": sum(
            int(source["chunk_count"])
            for source in smoke_report.indexed_sources.values()
        ),
        "hit_rate": smoke_report.report.summary.hit_rate,
        "citation_match_rate": smoke_report.report.summary.citation_match_rate,
        "empty_handling_rate": smoke_report.report.summary.empty_handling_rate,
        "long_section_hit_rate": float(category["hit_rate"]),
        "long_section_citation_match_rate": float(category["citation_match_rate"]),
    }


def _evaluate_chunking_candidate(
    candidate: ChunkingStrategyCandidate,
    source_ids: list[str],
    settings: Settings,
) -> ChunkingStrategyResult:
    if candidate.implementation_status == "planned":
        return ChunkingStrategyResult(
            candidate=candidate,
            source_ids=source_ids,
            total_chunks=None,
            citation_stability="planned",
            long_section_support="planned",
            decision_notes=[
                "Candidate is not runnable yet; no retrieval metrics are claimed.",
                "Implement runnable benchmark evidence before production promotion.",
            ],
        )

    if candidate.id == QDRANT_SECTION_CHUNKING_STRATEGY:
        chunks = [
            chunk
            for source_id in source_ids
            for chunk in _load_section_candidate_chunks(source_id, settings)
        ]
        citations_are_stable = all("#chunk-" not in chunk.citation for chunk in chunks)
        has_long_section_support = all(
            marker in " ".join(chunk.text for chunk in chunks)
            for marker in ("退款申诉复核", "批量物流异常")
        )
        return ChunkingStrategyResult(
            candidate=candidate,
            source_ids=source_ids,
            total_chunks=len(chunks),
            citation_stability="stable" if citations_are_stable else "mixed",
            long_section_support=(
                "covered-by-section" if has_long_section_support else "not-covered"
            ),
            decision_notes=[
                "Candidate can generate section chunks for local markdown sources.",
                "Runtime Qdrant ingestion still uses markdown-paragraph-v1.",
                "Retrieval metrics are not claimed until a future runnable retrieval benchmark is added.",
            ],
        )

    if candidate.id == QDRANT_TOKEN_WINDOW_CHUNKING_STRATEGY:
        chunks = [
            chunk
            for source_id in source_ids
            for chunk in _load_token_window_candidate_chunks(source_id, settings)
        ]
        citations_are_stable = all("#chunk-" not in chunk.citation for chunk in chunks)
        has_long_section_support = all(
            marker in " ".join(chunk.text for chunk in chunks)
            for marker in ("退款申诉复核", "批量物流异常")
        )
        return ChunkingStrategyResult(
            candidate=candidate,
            source_ids=source_ids,
            total_chunks=len(chunks),
            citation_stability="stable" if citations_are_stable else "mixed",
            long_section_support=(
                "covered-by-window" if has_long_section_support else "not-covered"
            ),
            decision_notes=[
                "Candidate can generate overlapping token-window chunks for local markdown sources.",
                "Runtime Qdrant ingestion still uses markdown-paragraph-v1.",
                "Use Qdrant+BGE smoke comparison before promoting this strategy.",
            ],
        )

    if candidate.id != QDRANT_CHUNKING_STRATEGY:
        raise ValueError(f"Implemented chunking candidate is not wired: {candidate.id}")

    chunks = [
        chunk
        for source_id in source_ids
        for chunk in load_qdrant_source_chunks(source_id, settings)
    ]
    citations_are_stable = all("#chunk-" not in chunk.citation for chunk in chunks)
    long_section_citations = {
        "refund_policy_2026#appeal-review",
        "logistics_faq_2026#batch-exception",
    }
    has_long_section_support = long_section_citations.issubset(
        {chunk.citation for chunk in chunks}
    )
    return ChunkingStrategyResult(
        candidate=candidate,
        source_ids=source_ids,
        total_chunks=len(chunks),
        citation_stability="stable" if citations_are_stable else "mixed",
        long_section_support="covered" if has_long_section_support else "not-covered",
        decision_notes=[
            "This is the current runtime Qdrant markdown ingestion baseline.",
            "Use retrieval benchmark evidence before deciding whether to replace it.",
        ],
    )


def _evaluate_query_rewrite_candidate(
    candidate: QueryRewriteCandidate,
    cases: list[RetrievalBenchmarkCase],
    settings: Settings,
) -> QueryRewriteCandidateResult:
    retriever = create_document_retriever(settings)
    case_results: list[QueryRewriteCaseResult] = []
    benchmark_results: list[RetrievalBenchmarkCaseResult] = []
    expected_empty_rewrites = 0

    for case in cases:
        rewritten_query = _rewrite_query_for_candidate(candidate, case)
        rewritten = rewritten_query != case.query
        if rewritten and case.expect_empty:
            expected_empty_rewrites += 1
        rewritten_case = replace(case, query=rewritten_query)
        benchmark_result = _run_case(retriever, rewritten_case)
        benchmark_results.append(benchmark_result)
        case_results.append(
            QueryRewriteCaseResult(
                case_id=case.id,
                category=case.category,
                difficulty=case.difficulty,
                original_query=case.query,
                rewritten_query=rewritten_query,
                rewritten=rewritten,
                expect_empty=case.expect_empty,
                result=benchmark_result,
            )
        )

    rewritten_cases = sum(1 for item in case_results if item.rewritten)
    report = RetrievalBenchmarkReport(
        summary=_summarize(f"{retriever.backend_name}:{candidate.id}", benchmark_results),
        cases=benchmark_results,
    )
    return QueryRewriteCandidateResult(
        candidate=candidate,
        total_cases=len(cases),
        rewritten_cases=rewritten_cases,
        rewrite_rate=round(rewritten_cases / len(cases), 4) if cases else 0.0,
        expected_empty_rewrites=expected_empty_rewrites,
        report=report,
        cases=case_results,
        decision_notes=_query_rewrite_decision_notes(
            candidate,
            rewritten_cases,
            expected_empty_rewrites,
            report,
        ),
    )


def _rewrite_query_for_candidate(
    candidate: QueryRewriteCandidate,
    case: RetrievalBenchmarkCase,
) -> str:
    if candidate.rewrite_policy == "none":
        return case.query
    if candidate.rewrite_policy == "controlled_support_rules":
        if case.expect_empty:
            return case.query
        return CONTROLLED_SUPPORT_QUERY_REWRITES.get(case.id, case.query)
    raise ValueError(
        f"Unsupported query rewrite policy for {candidate.id}: {candidate.rewrite_policy}"
    )


def _query_rewrite_decision_notes(
    candidate: QueryRewriteCandidate,
    rewritten_cases: int,
    expected_empty_rewrites: int,
    report: RetrievalBenchmarkReport,
) -> list[str]:
    if candidate.rewrite_policy == "none":
        return [
            "Baseline candidate preserves every original benchmark query.",
            "Use this as the comparison row for future rewrite strategies.",
        ]

    notes = [
        f"Candidate rewrote {rewritten_cases} benchmark case(s) with deterministic local rules.",
        "No LLM call, hosted provider, or runtime API behavior is introduced.",
    ]
    if expected_empty_rewrites == 0:
        notes.append("Expected-empty cases were preserved to protect negative controls.")
    else:
        notes.append(
            "Expected-empty cases were rewritten; this candidate must not be promoted."
        )
    if (
        report.summary.hit_rate == 1.0
        and report.summary.citation_match_rate == 1.0
        and report.summary.empty_handling_rate == 1.0
    ):
        notes.append("Current seed evidence does not show a regression against fixture retrieval.")
    else:
        notes.append("Current seed evidence shows a regression and requires investigation.")
    return notes


def _evaluate_evidence_grading_candidate(
    candidate: EvidenceGradingCandidate,
    cases: list[RetrievalBenchmarkCase],
    report: RetrievalBenchmarkReport,
) -> EvidenceGradingCandidateResult:
    case_results = [
        _grade_evidence_case(candidate, case, result)
        for case, result in zip(cases, report.cases)
    ]
    labels = [case.grading_label for case in case_results]
    empty_labels = [
        case.grading_label
        for case in case_results
        if case.expected_source_id is None and case.expected_citation is None
    ]
    related_insufficient_count = labels.count("related_insufficient")
    missing_evidence_count = labels.count("missing_evidence")
    unexpected_evidence_count = labels.count("unexpected_evidence")
    return EvidenceGradingCandidateResult(
        candidate=candidate,
        total_cases=len(case_results),
        answer_bearing_rate=_rate([
            label in {"answer_bearing", "no_evidence_expected"}
            for label in labels
        ]),
        related_insufficient_count=related_insufficient_count,
        missing_evidence_count=missing_evidence_count,
        unexpected_evidence_count=unexpected_evidence_count,
        expected_empty_pass_rate=_rate([
            label == "no_evidence_expected"
            for label in empty_labels
        ]),
        report=report,
        cases=case_results,
        decision_notes=_evidence_grading_decision_notes(
            candidate,
            related_insufficient_count,
            missing_evidence_count,
            unexpected_evidence_count,
        ),
    )


def _grade_evidence_case(
    candidate: EvidenceGradingCandidate,
    case: RetrievalBenchmarkCase,
    result: RetrievalBenchmarkCaseResult,
) -> EvidenceGradingCaseResult:
    label, reason = _evidence_grading_label(candidate, case, result)
    return EvidenceGradingCaseResult(
        case_id=case.id,
        category=case.category,
        difficulty=case.difficulty,
        expected_source_id=case.expected_source_id,
        expected_citation=case.expected_citation,
        returned_source_ids=result.returned_source_ids,
        returned_citations=result.returned_citations,
        grading_label=label,
        grading_reason=reason,
        result=result,
    )


def _evidence_grading_label(
    candidate: EvidenceGradingCandidate,
    case: RetrievalBenchmarkCase,
    result: RetrievalBenchmarkCaseResult,
) -> tuple[str, str]:
    if case.expect_empty:
        if result.returned_citations or result.returned_source_ids:
            return "unexpected_evidence", "Expected-empty case returned evidence."
        return "no_evidence_expected", "Expected-empty case returned no evidence."

    if candidate.grading_policy == "citation_match":
        if case.expected_citation in result.returned_citations:
            return "answer_bearing", "Expected citation was returned."
        if case.expected_source_id in result.returned_source_ids:
            return (
                "related_insufficient",
                "Expected source was returned but expected citation was missing.",
            )
        return "missing_evidence", "Expected source and citation were not returned."

    if candidate.grading_policy == "source_match":
        if case.expected_source_id in result.returned_source_ids:
            return "answer_bearing", "Expected source was returned."
        if result.returned_source_ids:
            return (
                "related_insufficient",
                "Evidence was returned, but not from the expected source.",
            )
        return "missing_evidence", "No evidence was returned for a non-empty case."

    raise ValueError(
        f"Unsupported evidence grading policy for {candidate.id}: {candidate.grading_policy}"
    )


def _evidence_grading_decision_notes(
    candidate: EvidenceGradingCandidate,
    related_insufficient_count: int,
    missing_evidence_count: int,
    unexpected_evidence_count: int,
) -> list[str]:
    notes = [
        "This evaluation is local evidence only and does not filter runtime answers.",
        f"Policy: {candidate.grading_policy}.",
    ]
    if related_insufficient_count:
        notes.append(
            f"{related_insufficient_count} case(s) returned related but insufficient evidence."
        )
    if missing_evidence_count:
        notes.append(f"{missing_evidence_count} case(s) missed expected evidence.")
    if unexpected_evidence_count:
        notes.append(
            f"{unexpected_evidence_count} expected-empty case(s) returned evidence."
        )
    if not (
        related_insufficient_count
        or missing_evidence_count
        or unexpected_evidence_count
    ):
        notes.append("Current seed evidence has no grading failures for this policy.")
    return notes


def _load_section_candidate_chunks(source_id: str, settings: Settings):
    source_path = settings.rag_source_dir / f"{source_id}.md"
    return markdown_source_to_section_chunks(
        source_id=source_id,
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
    )


def _load_token_window_candidate_chunks(source_id: str, settings: Settings):
    source_path = settings.rag_source_dir / f"{source_id}.md"
    return markdown_source_to_token_window_chunks(
        source_id=source_id,
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
    )


def _evaluate_embedding_candidate(
    candidate: EmbeddingCandidate,
) -> EmbeddingCandidateResult:
    criteria_coverage = {
        "language_profile": bool(candidate.language_profile),
        "chinese_heavy_suitable": candidate.chinese_heavy_suitable,
        "private_network_supported": candidate.private_network_supported,
        "vector_dimension": candidate.vector_dimension is not None,
        "data_residency": bool(candidate.data_residency),
        "operational_complexity": bool(candidate.operational_complexity),
        "reranker_compatibility": bool(candidate.reranker_compatibility),
    }
    readiness_status = (
        "baseline"
        if candidate.approval_status == "baseline"
        else "review_required"
    )
    decision_notes = [
        *candidate.notes,
        "This evaluation does not approve or invoke the embedding provider.",
    ]
    if not candidate.private_network_supported:
        decision_notes.append(
            "Public data egress must be approved before this candidate can be used."
        )
    if candidate.vector_dimension is None:
        decision_notes.append(
            "Vector dimension must be confirmed before Qdrant collection promotion."
        )
    return EmbeddingCandidateResult(
        candidate=candidate,
        readiness_status=readiness_status,
        criteria_coverage=criteria_coverage,
        decision_notes=decision_notes,
    )


def _run_case(retriever, case: RetrievalBenchmarkCase) -> RetrievalBenchmarkCaseResult:
    started_at = perf_counter()
    unknown_sources, documents = retriever.retrieve(
        query=case.query,
        knowledge_base_ids=case.knowledge_base_ids,
        top_k=case.top_k,
    )
    latency_ms = (perf_counter() - started_at) * 1000
    if unknown_sources:
        documents = []

    returned_citations = [document.citation for document in documents]
    returned_source_ids = [document.source_id for document in documents]
    empty_query_handling = None
    if case.expect_empty:
        empty_query_handling = len(documents) == 0

    return RetrievalBenchmarkCaseResult(
        id=case.id,
        category=case.category,
        difficulty=case.difficulty,
        hit_at_k=(
            case.expected_source_id in returned_source_ids
            if case.expected_source_id is not None
            else len(documents) == 0
        ),
        citation_match=(
            case.expected_citation in returned_citations
            if case.expected_citation is not None
            else len(documents) == 0
        ),
        empty_query_handling=empty_query_handling,
        latency_ms=round(latency_ms, 3),
        returned_citations=returned_citations,
        returned_source_ids=returned_source_ids,
    )


def _summarize(
    backend: str,
    results: list[RetrievalBenchmarkCaseResult],
) -> RetrievalBenchmarkSummary:
    total = len(results)
    empty_results = [
        result.empty_query_handling
        for result in results
        if result.empty_query_handling is not None
    ]
    return RetrievalBenchmarkSummary(
        backend=backend,
        total_cases=total,
        hit_rate=_rate([result.hit_at_k for result in results]),
        citation_match_rate=_rate([result.citation_match for result in results]),
        empty_handling_rate=_rate(empty_results),
        category_summaries=_category_summaries(results),
    )


def _rate(values: list[bool]) -> float:
    if not values:
        return 0.0
    return round(sum(1 for value in values if value) / len(values), 4)


def _category_summaries(
    results: list[RetrievalBenchmarkCaseResult],
) -> dict[str, dict[str, float | int]]:
    categories = sorted({result.category for result in results})
    summaries: dict[str, dict[str, float | int]] = {}
    for category in categories:
        category_results = [
            result for result in results if result.category == category
        ]
        empty_results = [
            result.empty_query_handling
            for result in category_results
            if result.empty_query_handling is not None
        ]
        summaries[category] = {
            "total_cases": len(category_results),
            "hit_rate": _rate([result.hit_at_k for result in category_results]),
            "citation_match_rate": _rate(
                [result.citation_match for result in category_results]
            ),
            "empty_handling_rate": _rate(empty_results),
        }
    return summaries
