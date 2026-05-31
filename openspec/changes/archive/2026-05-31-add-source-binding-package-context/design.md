## Context

`source_package` metadata already exists on source document manifest and ingestion preflight surfaces. It records business and parsing context such as domain, language, sensitivity, supported formats, and citation granularity. Source binding summary currently aggregates readiness and coverage signals, but not this package context, so an external control plane has to call lower-level diagnostics to understand what kind of source it is about to bind.

## Goals / Non-Goals

**Goals:**

- Add compact source package context fields to source binding rows.
- Reuse the `source_package` already returned by source document manifest.
- Include the fields in API responses and persisted source binding evidence.
- Keep source package fields informational and provider-owned.

**Non-Goals:**

- Do not make binding policy decisions based on sensitivity, domain, or language.
- Do not add source-to-agent binding creation, approvals, audit, or role policy.
- Do not add new parser dependencies or document format support.
- Do not execute ingestion, retrieval, answer composition, vector stores, embeddings, or GraphRAG.

## Decisions

- Flatten a small set of package fields onto `SourceBindingSummaryRow`.
  - Rationale: external control planes can scan one row per source without traversing nested diagnostics.
  - Alternative considered: embed the entire `source_package`; rejected because the binding summary should remain compact and not duplicate all lower-level metadata.
- Use fields from source document manifest rather than calling `get_source_package` separately.
  - Rationale: the summary already depends on the manifest response, and this preserves one source of package truth for binding review.
- Keep missing package context as `None` or empty lists.
  - Rationale: future sources may lack package metadata; absence should not fabricate business context or block binding by itself.

## Risks / Trade-offs

- Package context could be mistaken for authorization policy. Mitigation: documentation and operation notes keep binding policy outside the provider.
- Flattening fields duplicates a subset of source manifest data. Mitigation: only stable, review-oriented fields are included.
- Future package metadata may grow. Mitigation: new fields should be added through separate evidence-backed changes rather than copying the entire package object.
