## Context

The previous PDF-derived markdown trial showed that the first pages of the company profile PDF can be converted into usable markdown. However, that trial evaluated the extracted text in isolation. The provider still needs a small local loop that treats a markdown file as a trial business corpus and reports whether it is ready for possible future source registration.

Current provider source catalog entries are static fixtures. Private or user-supplied business material should not be added to default source catalog as a side effect of a local trial.

## Goals / Non-Goals

**Goals:**

- Validate a caller-supplied local markdown file as a trial source.
- Write a local source overlay JSON for traceability.
- Generate deterministic chunks and citations.
- Run lightweight evidence retrieval and cited answer checks.
- Return `go`, `review`, or `blocked` with recommended actions.
- Use the PDF-derived `company_profile_2025_trial.md` artifact as a real smoke input.

**Non-Goals:**

- Do not modify the default provider source catalog.
- Do not make the trial source available through provider HTTP APIs.
- Do not run formal ingestion jobs or persist index lifecycle state.
- Do not introduce raw PDF parsing, OCR, Qdrant, BGE-M3, pgvector, GraphRAG, or MyPrivateAgent orchestration.

## Decisions

- Use a local overlay file instead of editing `source_catalog.py`.
  - Rationale: keeps private business material local and reversible.

- Use markdown chunking compatible with existing lightweight diagnostics.
  - Rationale: preserves the current markdown baseline and avoids parser expansion.

- Keep retrieval deterministic and local to the trial service.
  - Rationale: the purpose is to decide whether this corpus is worth formal registration, not to change provider runtime behavior.

- Export report files under `docs/local-run/business-corpus-trial/`.
  - Rationale: aligns with the existing local run-loop artifacts while keeping them distinct from canonical fixtures.

## Risks / Trade-offs

- Trial results are not identical to formal provider HTTP retrieval -> acceptable because this is a pre-registration local check.
- Extracted markdown may contain private business content -> keep it local and avoid source catalog promotion unless explicitly approved.
- Weak query matching may produce `review` even when the corpus is useful -> report query and evidence details for manual adjustment.
