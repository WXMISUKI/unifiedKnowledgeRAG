import json
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable


PDF_DERIVED_MARKDOWN_TRIAL_ID = "pdf-derived-markdown-corpus-trial-v1"
DEFAULT_SOURCE_ID = "company_profile_2025_trial"
DEFAULT_QUERY = "公司主营业务是什么？"
DEFAULT_MAX_PAGES = 5
DEFAULT_OUTPUT_DIR = Path("docs/local-run/pdf-derived-corpus")
OUTPUT_JSON_FILENAME = "pdf-derived-markdown-trial.json"
OUTPUT_MARKDOWN_FILENAME = "pdf-derived-markdown-trial.md"

PdfTextExtractor = Callable[[Path, int], "PdfExtractionResult"]


@dataclass(frozen=True)
class PdfExtractionResult:
    status: str
    text_by_page: list[str] = field(default_factory=list)
    page_count: int | None = None
    extractor: str = "unknown"
    error: str | None = None


@dataclass(frozen=True)
class PdfTrialDocument:
    chunk_id: str
    citation: str
    text: str
    score: float


@dataclass(frozen=True)
class PdfDerivedMarkdownTrialReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    pdf_path: str
    source_id: str
    query: str
    max_pages: int
    extractor: str
    markdown_path: Path | None
    json_path: Path | None
    report_markdown_path: Path | None
    summary: dict[str, object]
    documents: list[PdfTrialDocument]
    answer: str
    citations: list[str]
    recommended_actions: list[str]
    notes: list[str]


def export_pdf_derived_markdown_trial_report(
    *,
    pdf_path: Path,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    source_id: str = DEFAULT_SOURCE_ID,
    query: str = DEFAULT_QUERY,
    max_pages: int = DEFAULT_MAX_PAGES,
    extractor: PdfTextExtractor | None = None,
) -> PdfDerivedMarkdownTrialReport:
    report = run_pdf_derived_markdown_trial(
        pdf_path=pdf_path,
        output_dir=output_dir,
        source_id=source_id,
        query=query,
        max_pages=max_pages,
        extractor=extractor,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    report_markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported_report = PdfDerivedMarkdownTrialReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        pdf_path=report.pdf_path,
        source_id=report.source_id,
        query=report.query,
        max_pages=report.max_pages,
        extractor=report.extractor,
        markdown_path=report.markdown_path,
        json_path=json_path,
        report_markdown_path=report_markdown_path,
        summary=report.summary,
        documents=report.documents,
        answer=report.answer,
        citations=report.citations,
        recommended_actions=report.recommended_actions,
        notes=report.notes,
    )
    json_path.write_text(
        json.dumps(
            pdf_derived_markdown_trial_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    report_markdown_path.write_text(
        render_pdf_derived_markdown_trial_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def run_pdf_derived_markdown_trial(
    *,
    pdf_path: Path,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    source_id: str = DEFAULT_SOURCE_ID,
    query: str = DEFAULT_QUERY,
    max_pages: int = DEFAULT_MAX_PAGES,
    extractor: PdfTextExtractor | None = None,
) -> PdfDerivedMarkdownTrialReport:
    normalized_pdf_path = pdf_path.expanduser().resolve()
    if max_pages < 1:
        raise ValueError("max_pages must be greater than or equal to 1")
    if not normalized_pdf_path.exists():
        return _blocked_report(
            pdf_path=normalized_pdf_path,
            source_id=source_id,
            query=query,
            max_pages=max_pages,
            reason_code="pdf_file_missing",
            extractor="not_run",
            error="PDF file does not exist.",
            markdown_path=None,
        )

    extract = extractor or extract_pdf_pages_with_pypdf
    extraction = extract(normalized_pdf_path, max_pages)
    markdown_path = output_dir / f"{source_id}.md"
    if extraction.status != "ready":
        return _blocked_report(
            pdf_path=normalized_pdf_path,
            source_id=source_id,
            query=query,
            max_pages=max_pages,
            reason_code="pdf_text_extraction_unavailable",
            extractor=extraction.extractor,
            error=extraction.error or "PDF text extraction did not return text.",
            markdown_path=None,
        )

    markdown_text = _render_derived_markdown(
        source_id=source_id,
        pdf_path=normalized_pdf_path,
        query=query,
        text_by_page=extraction.text_by_page,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(markdown_text, encoding="utf-8")

    chunks = _markdown_chunks(markdown_text)
    documents = _retrieve_documents(
        chunks=chunks,
        query=query,
        source_id=source_id,
        top_k=3,
    )
    answer, citations = _compose_trial_answer(documents)
    invalid_citations = [
        citation
        for citation in citations
        if citation not in {document.citation for document in documents}
    ]
    decision, reason_code = _decision(
        markdown_text=markdown_text,
        documents=documents,
        citations=citations,
        invalid_citations=invalid_citations,
    )
    return PdfDerivedMarkdownTrialReport(
        id=PDF_DERIVED_MARKDOWN_TRIAL_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        pdf_path=str(normalized_pdf_path),
        source_id=source_id,
        query=query,
        max_pages=max_pages,
        extractor=extraction.extractor,
        markdown_path=markdown_path,
        json_path=None,
        report_markdown_path=None,
        summary={
            "decision": decision,
            "source_id": source_id,
            "requested_pages": max_pages,
            "extracted_pages": len(extraction.text_by_page),
            "pdf_page_count": extraction.page_count,
            "markdown_char_count": len(markdown_text),
            "chunk_count": len(chunks),
            "retrieved_document_count": len(documents),
            "answer_citation_count": len(citations),
            "invalid_citation_count": len(invalid_citations),
            "raw_pdf_ingestion_status": "unsupported_by_provider",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        documents=documents,
        answer=answer,
        citations=citations,
        recommended_actions=_recommended_actions(decision, reason_code),
        notes=_notes(),
    )


def extract_pdf_pages_with_pypdf(pdf_path: Path, max_pages: int) -> PdfExtractionResult:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as error:
        return PdfExtractionResult(
            status="blocked",
            extractor="pypdf",
            error=f"{error.__class__.__name__}: pypdf is not installed.",
        )

    try:
        reader = PdfReader(str(pdf_path))
        page_count = len(reader.pages)
        text_by_page = []
        for page in reader.pages[:max_pages]:
            text = page.extract_text() or ""
            normalized = _normalize_text(text)
            if normalized:
                text_by_page.append(normalized)
    except Exception as error:  # pragma: no cover - exercised with real PDFs.
        return PdfExtractionResult(
            status="blocked",
            extractor="pypdf",
            error=f"{error.__class__.__name__}: {error}",
        )
    if not text_by_page:
        return PdfExtractionResult(
            status="blocked",
            page_count=page_count,
            extractor="pypdf",
            error="No extractable text found in the requested PDF page range.",
        )
    return PdfExtractionResult(
        status="ready",
        text_by_page=text_by_page,
        page_count=page_count,
        extractor="pypdf",
    )


def pdf_derived_markdown_trial_report_to_dict(
    report: PdfDerivedMarkdownTrialReport,
) -> dict[str, object]:
    payload = asdict(report)
    for key in ["markdown_path", "json_path", "report_markdown_path"]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_pdf_derived_markdown_trial_markdown(
    report: PdfDerivedMarkdownTrialReport,
) -> str:
    lines = [
        "# PDF Derived Markdown Corpus Trial",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source ID: `{report.source_id}`",
        f"- Query: `{report.query}`",
        f"- Max Pages: `{report.max_pages}`",
        f"- Extractor: `{report.extractor}`",
        f"- Markdown Artifact: `{report.markdown_path or 'n/a'}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")

    lines.extend(["", "## Retrieved Evidence", ""])
    if report.documents:
        lines.extend(["| Citation | Score | Preview |", "|---|---:|---|"])
        for document in report.documents:
            preview = document.text[:140].replace("|", "\\|")
            lines.append(f"| `{document.citation}` | `{document.score:.4f}` | {preview} |")
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
    pdf_path: Path,
    source_id: str,
    query: str,
    max_pages: int,
    reason_code: str,
    extractor: str,
    error: str,
    markdown_path: Path | None,
) -> PdfDerivedMarkdownTrialReport:
    return PdfDerivedMarkdownTrialReport(
        id=PDF_DERIVED_MARKDOWN_TRIAL_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision="blocked",
        reason_code=reason_code,
        pdf_path=str(pdf_path),
        source_id=source_id,
        query=query,
        max_pages=max_pages,
        extractor=extractor,
        markdown_path=markdown_path,
        json_path=None,
        report_markdown_path=None,
        summary={
            "decision": "blocked",
            "source_id": source_id,
            "requested_pages": max_pages,
            "error": error,
            "raw_pdf_ingestion_status": "unsupported_by_provider",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        documents=[],
        answer="",
        citations=[],
        recommended_actions=_recommended_actions("blocked", reason_code),
        notes=_notes(),
    )


def _render_derived_markdown(
    *,
    source_id: str,
    pdf_path: Path,
    query: str,
    text_by_page: list[str],
) -> str:
    lines = [
        f"# PDF Derived Corpus Trial: {source_id}",
        "",
        f"- Source PDF: `{pdf_path}`",
        f"- Trial Query: `{query}`",
        "- Raw PDF ingestion status: `unsupported_by_provider`",
        "",
    ]
    for index, text in enumerate(text_by_page, start=1):
        lines.extend(
            [
                f"## Page {index}",
                "",
                text,
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _markdown_chunks(text: str) -> list[str]:
    chunks: list[str] = []
    current_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current_lines:
                chunks.append(" ".join(current_lines))
                current_lines = []
            continue
        if line.startswith("#") or line.startswith("- "):
            continue
        current_lines.append(line)
    if current_lines:
        chunks.append(" ".join(current_lines))
    return [chunk for chunk in chunks if len(chunk) >= 12]


def _retrieve_documents(
    *,
    chunks: list[str],
    query: str,
    source_id: str,
    top_k: int,
) -> list[PdfTrialDocument]:
    scored = [
        PdfTrialDocument(
            chunk_id=f"chunk-{index}",
            citation=f"{source_id}#chunk-{index}",
            text=chunk,
            score=_score(query, chunk),
        )
        for index, chunk in enumerate(chunks, start=1)
    ]
    return [
        document
        for document in sorted(scored, key=lambda item: item.score, reverse=True)
        if document.score > 0
    ][:top_k]


def _compose_trial_answer(documents: list[PdfTrialDocument]) -> tuple[str, list[str]]:
    if not documents:
        return "", []
    citations = [document.citation for document in documents]
    snippets = "；".join(_first_sentence(document.text) for document in documents)
    answer = f"{snippets}。引用：{' '.join(f'[{citation}]' for citation in citations)}"
    return answer, citations


def _decision(
    *,
    markdown_text: str,
    documents: list[PdfTrialDocument],
    citations: list[str],
    invalid_citations: list[str],
) -> tuple[str, str]:
    if not markdown_text.strip():
        return "blocked", "derived_markdown_empty"
    if invalid_citations:
        return "blocked", "trial_answer_citation_blocked"
    if not documents or not citations:
        return "review", "derived_evidence_needs_review"
    return "go", "pdf_derived_markdown_usable"


def _recommended_actions(decision: str, reason_code: str) -> list[str]:
    if decision == "go":
        return [
            "review_derived_markdown_quality_before_formal_source_registration",
            "use_pdf_derived_markdown_for_small_local_rag_trial",
            "keep_raw_pdf_ingestion_unsupported_until_parser_change_is_approved",
        ]
    if reason_code == "pdf_file_missing":
        return ["check_pdf_path_and_rerun_trial"]
    if reason_code == "pdf_text_extraction_unavailable":
        return [
            "run_external_ocr_or_layout_provider_for_pdf_text_extraction",
            "rerun_trial_with_pdf_derived_markdown_after_extraction",
        ]
    if decision == "review":
        return [
            "review_query_page_range_and_extracted_markdown_quality",
            "try_a_more_specific_company_profile_query",
            "rerun_trial_after_adjustment",
        ]
    return ["inspect_trial_report_error_and_rerun_after_fix"]


def _notes() -> list[str]:
    return [
        "This is a local trial over PDF-derived markdown, not raw PDF ingestion support.",
        "The trial does not register a default provider source or create source bindings.",
        "PaddleOCR or PP-Structure can remain external providers for OCR/Layout extraction.",
        "The original PDF is not copied into the repository by this trial.",
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


def _normalize_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def _format_value(value: object) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
