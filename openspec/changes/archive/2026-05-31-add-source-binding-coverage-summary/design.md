## Context

The provider already exposes source document manifests, ingestion preflight diagnostics, and a provider-level source binding summary. External control planes can decide bindability from the summary, but they still need to call deeper endpoints to understand whether each source has citation anchors, deterministic chunk manifests, and parser-ready documents available for grounded answers.

## Goals / Non-Goals

**Goals:**

- Add compact coverage fields to each source binding row: citation anchor count, chunk manifest count, parser-ready document count, and unsupported document count.
- Derive counts only from existing source document manifest and ingestion preflight responses.
- Include the new fields in API and exported Markdown/JSON evidence.
- Preserve the existing `ready`, `review`, and `blocked` binding decision logic.

**Non-Goals:**

- Do not add new document parsers or parsing dependencies.
- Do not create ingestion jobs, rebuild indexes, or mutate lifecycle state.
- Do not call embedding models, vector stores, retrieval, answer composition, or GraphRAG.
- Do not move binding approval, policy, audit, or source-to-agent ownership into this provider.

## Decisions

- Add counts directly to `SourceBindingSummaryRow`.
  - Rationale: the fields describe per-source binding evidence and are useful for both the API endpoint and handoff export.
  - Alternative considered: nest a new `coverage` object; rejected for this slice because the existing row is flat and the additive counts are simple.
- Count citation anchors from source document manifests and chunk manifests from manifest diagnostics.
  - Rationale: source manifests are provider-owned citation evidence; reusing them avoids duplicating parser logic.
  - Alternative considered: count chunks from ingestion preflight previews; rejected because preview lists may be capped and are not the canonical chunk manifest.
- Count parser-ready and unsupported documents from ingestion preflight.
  - Rationale: the preflight already records `format_supported` and `parser_status`, which are the right indicators before binding.
- Keep counts informational.
  - Rationale: a source may be bindable even when a future source has zero chunks for a valid reason; changing binding decisions should be a separate evidence-backed change.

## Risks / Trade-offs

- Coverage fields could be mistaken for binding policy. Mitigation: operation notes continue to say external control planes own policy and approvals.
- Counts can duplicate deeper diagnostics. Mitigation: expose only aggregate counts and leave detailed entries in source manifests and preflight endpoints.
- Future parser expansion may add statuses beyond `ready`. Mitigation: unsupported count uses existing `format_supported=false`, while parser-ready count is strictly `parser_status=ready`.
