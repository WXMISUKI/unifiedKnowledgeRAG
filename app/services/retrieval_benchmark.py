import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from app.config import Settings, get_settings
from app.models.contracts import IndexStatusResponse
from app.services.embedding_adapters import create_embedding_adapter
from app.services.index_lifecycle_store import IndexLifecycleStore
from app.services.qdrant_vector_store import (
    create_qdrant_client,
    embed_qdrant_chunks,
    ensure_qdrant_collection,
    load_qdrant_source_chunks,
    query_qdrant_documents_for_text,
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
class QdrantThresholdSweepEvidenceReport:
    candidate: RetrievalCandidate
    thresholds: list[float]
    reports: list[QdrantSmokeEvidenceReport]
    metadata: dict[str, str | list[str] | dict[str, str]]
    json_path: Path | None = None
    markdown_path: Path | None = None


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
        metadata=_qdrant_smoke_metadata(settings, source_ids),
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


def export_qdrant_bge_threshold_sweep_evidence(
    output_dir: Path,
    thresholds: list[float],
    cases_path: Path = Path("tests/fixtures/retrieval_benchmark_cases.json"),
    source_ids: list[str] | None = None,
    case_ids: list[str] | None = None,
    settings: Settings | None = None,
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


def _index_qdrant_smoke_sources(
    client,
    settings: Settings,
    source_ids: list[str],
    embedding_adapter,
) -> dict[str, dict[str, str | int]]:
    status, reason = ensure_qdrant_collection(client, settings)
    if status != "ready":
        raise RuntimeError(reason or "Qdrant collection is not ready.")

    store = IndexLifecycleStore(settings)
    indexed_sources: dict[str, dict[str, str | int]] = {}
    for source_id in source_ids:
        job_id = f"smoke_{uuid4().hex}"
        chunks = embed_qdrant_chunks(
            load_qdrant_source_chunks(source_id, settings),
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


def _qdrant_smoke_metadata(
    settings: Settings,
    source_ids: list[str],
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
    }


def _qdrant_threshold_sweep_metadata(
    settings: Settings,
    source_ids: list[str],
    thresholds: list[float],
) -> dict[str, str | list[str] | dict[str, str]]:
    metadata = _qdrant_smoke_metadata(settings, source_ids)
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
