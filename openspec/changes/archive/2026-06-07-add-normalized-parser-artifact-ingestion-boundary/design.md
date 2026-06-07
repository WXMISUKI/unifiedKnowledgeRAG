## Context

The current provider path supports markdown-first local business corpus trials, approved source registration, acceptance smoke, live HTTP smoke, and an explicit local approved-source ingestion loop. The provider still intentionally rejects raw PDF as a directly supported ingestion format and does not start OCR or parser services.

Stage 3 needs a narrow bridge between external parsers and the existing markdown ingestion path. The practical contract is: external tools parse PDF/Word/Excel/OCR inputs, then hand this provider a normalized artifact with text, provenance, and citations. The provider validates and materializes that artifact into local markdown/source-overlay files that can feed the already implemented onboarding and ingestion loop.

## Goals / Non-Goals

**Goals:**
- Define a normalized parser artifact shape for external parser outputs.
- Validate artifact readiness with `go`, `review`, and `blocked` decisions.
- Materialize ready artifacts into markdown and source overlay files compatible with the existing local corpus/onboarding flow.
- Preserve traceable provenance from original file, parser id, pages/sheets/sections, content digest, and citations.
- Refresh roadmap/progress notes so Stage 3 is the active next slice after Stage 2 completion.

**Non-Goals:**
- No raw PDF parsing inside provider ingestion.
- No PaddleOCR, Word, Excel, or PDF parser startup from this provider.
- No directory crawler, batch parser platform, or background worker.
- No source-to-agent binding, MyPrivateAgent orchestration, `/api/chat` mutation, backend promotion, Qdrant/pgvector default switch, or GraphRAG execution.

## Decisions

- Use a file-based JSON artifact contract first. This matches the current lightweight local-run pattern, keeps external parser ownership explicit, and avoids adding a new HTTP mutation API before the operator flow is stable.
- Materialize artifacts into markdown plus source overlay rather than registering directly. This reuses the existing trial, handoff, registration, preflight, ingestion, and acceptance loop instead of creating a parallel ingestion path.
- Treat missing required provenance or text as `blocked`; treat missing recommended trace details such as section-level anchors as `review` only when enough content and source identity remain available for a human to fix. This keeps the path fail-closed without making every enrichment mandatory on day one.
- Keep citation anchors deterministic and provider-owned after materialization. External artifact citations are preserved in generated markdown comments/front matter and in report metadata, while markdown chunks can still use existing provider chunk/citation rules.

## Risks / Trade-offs

- External parsers may produce inconsistent JSON shapes -> Mitigation: require one minimal provider-owned artifact schema and reject unknown/partial shapes with machine-readable reasons.
- Generated markdown might look different from hand-authored markdown -> Mitigation: include provenance headers and deterministic section ordering so the output is reviewable and repeatable.
- Users may expect raw PDF upload support after this change -> Mitigation: specs and reports explicitly state raw PDF/OCR engines remain outside provider defaults.
- The first contract may be too small for complex Excel tables or layout-heavy PDFs -> Mitigation: preserve parser metadata and block/page/sheet provenance fields so later slices can expand the schema without changing ingestion ownership.
