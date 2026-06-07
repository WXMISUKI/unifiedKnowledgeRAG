## Context

The provider now has two separate local capabilities:

- `normalized-parser-artifact-ingestion-boundary` validates an external parser artifact and materializes markdown/source-overlay files.
- `local-approved-source-ingestion-loop` verifies markdown source onboarding, ingestion preflight, explicit ingestion job creation, index status, and acceptance smoke.

The next practical step is orchestration, not a new parser stack. A normalized artifact should be able to flow through the existing markdown path and produce one operator-friendly decision report.

## Goals / Non-Goals

**Goals:**
- Run artifact validation/materialization first.
- Stop early with `review` or `blocked` if the artifact boundary is not `go`.
- Pass the materialized markdown, source id, and title into the existing approved-source ingestion loop.
- Export one JSON/Markdown report with step-level statuses and artifact paths.
- Keep failure semantics machine-readable and compact.

**Non-Goals:**
- No raw PDF parsing, OCR startup, PaddleOCR invocation, or parser engine orchestration.
- No new HTTP mutation API, background worker, queue, or directory crawler.
- No MyPrivateAgent call, source-to-agent binding, `/api/chat` mutation, backend promotion, vector database promotion, or GraphRAG execution.

## Decisions

- Build a provider-side orchestration service rather than extending either existing service. This keeps the artifact boundary and ingestion loop independently reusable.
- Use dependency-injected exporters for tests. The default path calls the real local artifact boundary exporter and approved-source ingestion loop exporter, while tests can replace each step without touching real registries.
- Treat artifact `review` as loop `review` and artifact `blocked` as loop `blocked`. The loop does not attempt onboarding or ingestion unless the parser artifact boundary returns `go`.
- Use materialized markdown as the canonical bridge into existing ingestion. The source overlay remains evidence and metadata; the current ingestion loop still receives explicit markdown/source/title inputs.

## Risks / Trade-offs

- Generated markdown quality depends on external parser output -> Mitigation: keep artifact validation and citation checks before ingestion.
- Running the default CLI can mutate local approved-source registry through existing ingestion loop behavior -> Mitigation: keep this as an explicit operator command and preserve non-goal/status evidence.
- The loop may look like raw PDF support to users -> Mitigation: report non-goals explicitly and block raw-file inputs before ingestion.
- It does not solve quality/rerank/chunking maturity -> Mitigation: leave those for Stage 4/5 after parser-derived corpus entry is proven.
