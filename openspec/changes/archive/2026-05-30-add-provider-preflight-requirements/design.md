## Context

`GET /api/provider/preflight` currently evaluates the provider against the default knowledge-provider contract. That is useful for local smoke and basic integration, but a real control plane needs to express its own minimum requirements, especially during version rollout or staged feature binding.

This slice keeps preflight read-only and simple: the caller can ask for one contract version and a list of required capability ids. The provider compares those requirements against its manifest and capability registry, then returns the same `bindable` envelope with additional requirement details.

## Goals / Non-Goals

**Goals:**

- Preserve current preflight behavior when no requirements are supplied.
- Support explicit required contract version checks.
- Support explicit required capability id checks.
- Apply schema-reference checks to the requested capability set.
- Return requested requirements in the response for audit and diagnostics.

**Non-Goals:**

- Do not implement semantic version ranges or negotiation.
- Do not implement MyPrivateAgent-side registration.
- Do not add auth, tenant policy, approval, or governance writes.
- Do not execute retrieval, ingestion, answer composition, or GraphRAG queries.

## Decisions

- Use query parameters on the existing GET endpoint.
  - Rationale: requirement checks are read-only and easy for MyPrivateAgent to call during provider binding.
  - Alternative considered: POST body. Rejected for this slice because the input shape is small and stable.

- Keep exact contract-version matching.
  - Rationale: current contract version is a named compatibility boundary, not a semantic version range.
  - Alternative considered: version range compatibility. Rejected until multiple provider contract versions exist.

- Use default required capabilities when none are provided.
  - Rationale: existing callers and smoke reports remain compatible.

- Check schema references only for required capabilities that exist.
  - Rationale: missing capability and missing schema reference are separate diagnostics; missing capabilities should not create duplicate schema failures.

## Risks / Trade-offs

- [Risk] Query parameter naming may need to align with MyPrivateAgent later. -> Use explicit names and keep default behavior stable.
- [Risk] Exact contract matching is strict. -> This is intentional for fail-closed binding until version negotiation is needed.
- [Risk] Callers may request unknown capability ids. -> The response marks `bindable=false` and reports missing capability ids.
