import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


LOCAL_BUSINESS_CORPUS_TRIAL_ID = "local-business-corpus-trial-loop-v1"
DEFAULT_MARKDOWN_PATH = Path("docs/local-run/pdf-derived-corpus/company_profile_2025_trial.md")
DEFAULT_SOURCE_ID = "company_profile_2025_trial"
DEFAULT_TITLE = "公司简介 2025 trial"
DEFAULT_QUERY = "公司主营业务是什么？"
DEFAULT_OWNER = "local_trial"
DEFAULT_DOMAIN = "company_profile"
DEFAULT_LANGUAGE = "zh-CN"
DEFAULT_SENSITIVITY = "local_private_trial"
DEFAULT_TOP_K = 3
DEFAULT_OUTPUT_DIR = Path("docs/local-run/business-corpus-trial")
OVERLAY_FILENAME = "local-business-corpus-source.json"
CHUNKS_FILENAME = "local-business-corpus-chunks.json"
OUTPUT_JSON_FILENAME = "local-business-corpus-trial.json"
OUTPUT_MARKDOWN_FILENAME = "local-business-corpus-trial.md"


@dataclass(frozen=True)
class LocalBusinessCorpusOverlay:
    source_id: str
    title: str
    source_path: str
    format: str
    owner: str
    domain: str
    language: str
    sensitivity: str
    trial_only: bool
    formal_registration_status: str


@dataclass(frozen=True)
class LocalBusinessCorpusChunk:
    chunk_id: str
    citation: str
    text: str
    char_count: int


@dataclass(frozen=True)
class LocalBusinessCorpusEvidence:
    chunk_id: str
    citation: str
    text: str
    score: float


@dataclass(frozen=True)
class LocalBusinessCorpusTrialReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    source_id: str
    title: str
    markdown_path: Path
    query: str
    top_k: int
    overlay_path: Path | None
    chunks_path: Path | None
    json_path: Path | None
    report_markdown_path: Path | None
    summary: dict[str, object]
    overlay: LocalBusinessCorpusOverlay | None
    evidence: list[LocalBusinessCorpusEvidence]
    answer: str
    citations: list[str]
    recommended_actions: list[str]
    notes: list[str]


def export_local_business_corpus_trial_report(
    *,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    owner: str = DEFAULT_OWNER,
    domain: str = DEFAULT_DOMAIN,
    language: str = DEFAULT_LANGUAGE,
    sensitivity: str = DEFAULT_SENSITIVITY,
    top_k: int = DEFAULT_TOP_K,
) -> LocalBusinessCorpusTrialReport:
    report = run_local_business_corpus_trial(
        markdown_path=markdown_path,
        output_dir=output_dir,
        source_id=source_id,
        title=title,
        query=query,
        owner=owner,
        domain=domain,
        language=language,
        sensitivity=sensitivity,
        top_k=top_k,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    report_markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported_report = LocalBusinessCorpusTrialReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        source_id=report.source_id,
        title=report.title,
        markdown_path=report.markdown_path,
        query=report.query,
        top_k=report.top_k,
        overlay_path=report.overlay_path,
        chunks_path=report.chunks_path,
        json_path=json_path,
        report_markdown_path=report_markdown_path,
        summary=report.summary,
        overlay=report.overlay,
        evidence=report.evidence,
        answer=report.answer,
        citations=report.citations,
        recommended_actions=report.recommended_actions,
        notes=report.notes,
    )
    json_path.write_text(
        json.dumps(
            local_business_corpus_trial_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    report_markdown_path.write_text(
        render_local_business_corpus_trial_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def run_local_business_corpus_trial(
    *,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    owner: str = DEFAULT_OWNER,
    domain: str = DEFAULT_DOMAIN,
    language: str = DEFAULT_LANGUAGE,
    sensitivity: str = DEFAULT_SENSITIVITY,
    top_k: int = DEFAULT_TOP_K,
) -> LocalBusinessCorpusTrialReport:
    normalized_markdown_path = markdown_path.expanduser().resolve()
    if top_k < 1:
        raise ValueError("top_k must be greater than or equal to 1")
    if normalized_markdown_path.suffix.lower() not in {".md", ".markdown"}:
        return _blocked_report(
            markdown_path=normalized_markdown_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            reason_code="unsupported_trial_format",
            error="Local business corpus trial only supports markdown files.",
        )
    if not normalized_markdown_path.exists():
        return _blocked_report(
            markdown_path=normalized_markdown_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            reason_code="markdown_file_missing",
            error="Markdown file does not exist.",
        )

    markdown_text = normalized_markdown_path.read_text(encoding="utf-8")
    chunks = _markdown_chunks(markdown_text, source_id=source_id)
    if not chunks:
        return _blocked_report(
            markdown_path=normalized_markdown_path,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            reason_code="markdown_content_empty",
            error="Markdown file has no chunkable content.",
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    overlay = LocalBusinessCorpusOverlay(
        source_id=source_id,
        title=title,
        source_path=str(normalized_markdown_path),
        format="markdown",
        owner=owner,
        domain=domain,
        language=language,
        sensitivity=sensitivity,
        trial_only=True,
        formal_registration_status="not_registered",
    )
    overlay_path = output_dir / OVERLAY_FILENAME
    chunks_path = output_dir / CHUNKS_FILENAME
    overlay_path.write_text(
        json.dumps(asdict(overlay), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    chunks_path.write_text(
        json.dumps([asdict(chunk) for chunk in chunks], ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )

    evidence = _retrieve_evidence(chunks=chunks, query=query, top_k=top_k)
    answer, citations = _compose_trial_answer(evidence)
    allowed_citations = {item.citation for item in evidence}
    invalid_citations = [
        citation for citation in citations if citation not in allowed_citations
    ]
    decision, reason_code = _decision(
        evidence=evidence,
        citations=citations,
        invalid_citations=invalid_citations,
    )
    return LocalBusinessCorpusTrialReport(
        id=LOCAL_BUSINESS_CORPUS_TRIAL_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        source_id=source_id,
        title=title,
        markdown_path=normalized_markdown_path,
        query=query,
        top_k=top_k,
        overlay_path=overlay_path,
        chunks_path=chunks_path,
        json_path=None,
        report_markdown_path=None,
        summary={
            "decision": decision,
            "source_id": source_id,
            "markdown_char_count": len(markdown_text),
            "chunk_count": len(chunks),
            "retrieved_evidence_count": len(evidence),
            "answer_citation_count": len(citations),
            "invalid_citation_count": len(invalid_citations),
            "trial_overlay_status": "written",
            "formal_registration_status": "not_registered",
            "default_source_catalog_status": "unchanged",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        overlay=overlay,
        evidence=evidence,
        answer=answer,
        citations=citations,
        recommended_actions=_recommended_actions(decision, reason_code),
        notes=_notes(),
    )


def local_business_corpus_trial_report_to_dict(
    report: LocalBusinessCorpusTrialReport,
) -> dict[str, object]:
    payload = asdict(report)
    for key in ["markdown_path", "overlay_path", "chunks_path", "json_path", "report_markdown_path"]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_local_business_corpus_trial_markdown(
    report: LocalBusinessCorpusTrialReport,
) -> str:
    lines = [
        "# Local Business Corpus Trial",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source ID: `{report.source_id}`",
        f"- Title: `{report.title}`",
        f"- Markdown Path: `{report.markdown_path}`",
        f"- Query: `{report.query}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")

    lines.extend(["", "## Overlay", ""])
    if report.overlay is None:
        lines.append("No overlay written.")
    else:
        lines.extend(
            [
                f"- Overlay Path: `{report.overlay_path}`",
                f"- Owner: `{report.overlay.owner}`",
                f"- Domain: `{report.overlay.domain}`",
                f"- Sensitivity: `{report.overlay.sensitivity}`",
                f"- Formal Registration: `{report.overlay.formal_registration_status}`",
            ]
        )

    lines.extend(["", "## Retrieved Evidence", ""])
    if report.evidence:
        lines.extend(["| Citation | Score | Preview |", "|---|---:|---|"])
        for item in report.evidence:
            preview = item.text[:140].replace("|", "\\|")
            lines.append(f"| `{item.citation}` | `{item.score:.4f}` | {preview} |")
    else:
        lines.append("No retrieved evidence.")

    lines.extend(["", "## Trial Answer", ""])
    lines.append(report.answer or "No cited answer produced.")
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    return "\n".join(lines).rstrip() + "\n"


def _blocked_report(
    *,
    markdown_path: Path,
    source_id: str,
    title: str,
    query: str,
    top_k: int,
    reason_code: str,
    error: str,
) -> LocalBusinessCorpusTrialReport:
    return LocalBusinessCorpusTrialReport(
        id=LOCAL_BUSINESS_CORPUS_TRIAL_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision="blocked",
        reason_code=reason_code,
        source_id=source_id,
        title=title,
        markdown_path=markdown_path,
        query=query,
        top_k=top_k,
        overlay_path=None,
        chunks_path=None,
        json_path=None,
        report_markdown_path=None,
        summary={
            "decision": "blocked",
            "source_id": source_id,
            "error": error,
            "trial_overlay_status": "not_written",
            "formal_registration_status": "not_registered",
            "default_source_catalog_status": "unchanged",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        overlay=None,
        evidence=[],
        answer="",
        citations=[],
        recommended_actions=_recommended_actions("blocked", reason_code),
        notes=_notes(),
    )


def _markdown_chunks(
    markdown_text: str,
    *,
    source_id: str,
) -> list[LocalBusinessCorpusChunk]:
    chunks: list[LocalBusinessCorpusChunk] = []
    current_lines: list[str] = []
    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()
        if not line:
            _append_chunk(chunks, current_lines, source_id=source_id)
            current_lines = []
            continue
        if line.startswith("#") or line.startswith("- "):
            continue
        current_lines.append(line)
    _append_chunk(chunks, current_lines, source_id=source_id)
    return chunks


def _append_chunk(
    chunks: list[LocalBusinessCorpusChunk],
    current_lines: list[str],
    *,
    source_id: str,
) -> None:
    if not current_lines:
        return
    text = " ".join(current_lines).strip()
    if len(text) < 12:
        return
    index = len(chunks) + 1
    chunks.append(
        LocalBusinessCorpusChunk(
            chunk_id=f"chunk-{index}",
            citation=f"{source_id}#chunk-{index}",
            text=text,
            char_count=len(text),
        )
    )


def _retrieve_evidence(
    *,
    chunks: list[LocalBusinessCorpusChunk],
    query: str,
    top_k: int,
) -> list[LocalBusinessCorpusEvidence]:
    scored = [
        LocalBusinessCorpusEvidence(
            chunk_id=chunk.chunk_id,
            citation=chunk.citation,
            text=chunk.text,
            score=_score(query, chunk.text),
        )
        for chunk in chunks
    ]
    return [
        item
        for item in sorted(scored, key=lambda evidence: evidence.score, reverse=True)
        if item.score > 0
    ][:top_k]


def _compose_trial_answer(
    evidence: list[LocalBusinessCorpusEvidence],
) -> tuple[str, list[str]]:
    if not evidence:
        return "", []
    citations = [item.citation for item in evidence]
    snippets = "；".join(_first_sentence(item.text) for item in evidence)
    answer = f"{snippets}。引用：{' '.join(f'[{citation}]' for citation in citations)}"
    return answer, citations


def _decision(
    *,
    evidence: list[LocalBusinessCorpusEvidence],
    citations: list[str],
    invalid_citations: list[str],
) -> tuple[str, str]:
    if invalid_citations:
        return "blocked", "trial_answer_citation_blocked"
    if not evidence or not citations:
        return "review", "business_corpus_evidence_needs_review"
    return "go", "local_business_corpus_usable"


def _recommended_actions(decision: str, reason_code: str) -> list[str]:
    if decision == "go":
        return [
            "review_local_business_corpus_quality_before_formal_registration",
            "use_trial_overlay_as_input_for_future_source_registration_design",
            "keep_default_source_catalog_unchanged",
        ]
    if reason_code == "markdown_file_missing":
        return [
            "check_markdown_path",
            "rerun_pdf_derived_markdown_trial_if_needed",
        ]
    if reason_code == "markdown_content_empty":
        return [
            "repair_or_regenerate_markdown_content",
            "rerun_local_business_corpus_trial",
        ]
    if decision == "review":
        return [
            "review_query_and_markdown_content_quality",
            "try_a_more_specific_business_query",
            "rerun_local_business_corpus_trial",
        ]
    return ["inspect_trial_report_error_and_rerun_after_fix"]


def _notes() -> list[str]:
    return [
        "This is a local business corpus trial, not formal provider source registration.",
        "The default provider source catalog and HTTP source list remain unchanged.",
        "The trial does not run formal ingestion jobs, persist index lifecycle state, create source bindings, promote retrieval backends, parse raw PDFs, start OCR services, execute GraphRAG, or run MyPrivateAgent orchestration.",
    ]


def _score(query: str, text: str) -> float:
    query_tokens = _tokens(query)
    if not query_tokens:
        return 0.0
    text_tokens = set(_tokens(text))
    matched = sum(1 for token in query_tokens if token in text_tokens)
    return matched / len(query_tokens)


def _tokens(value: str) -> list[str]:
    cleaned = re.sub(r"\s+", "", value.lower())
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", cleaned)
    ascii_terms = re.findall(r"[a-z0-9]{2,}", cleaned)
    return chinese_chars + ascii_terms


def _first_sentence(text: str) -> str:
    parts = re.split(r"[。！？!?]\s*", text)
    first = next((part.strip() for part in parts if part.strip()), text.strip())
    return first[:180]


def _format_value(value: object) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
