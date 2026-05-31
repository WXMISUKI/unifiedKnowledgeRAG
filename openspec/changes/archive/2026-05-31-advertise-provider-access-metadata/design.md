## Context

The provider has a default-off API key guard: `/health` remains public while `/api/*` can require either `Authorization: Bearer <token>` or `X-Provider-Api-Key`. This is a component access guard, not user identity or policy. A machine-readable manifest field keeps external callers from scraping README text or duplicating hard-coded assumptions.

## Goals / Non-Goals

**Goals:**

- Expose stable access metadata from `GET /api/provider/manifest`.
- Indicate whether a component API key is configured without revealing its value.
- Describe accepted headers and public/protected path scopes.
- Preserve provider/caller responsibility boundaries.

**Non-Goals:**

- Do not implement user identity, RBAC, tenant policy, approvals, or audit.
- Do not change auth behavior or require API keys by default.
- Do not generate secrets or manage secret rotation.

## Decisions

- Add an `access` object to `ProviderIntegrationManifest`.
  - Rationale: access metadata is part of integration discovery, like endpoints and capabilities.
  - Alternative considered: add a separate endpoint; rejected because this metadata is small and belongs in discovery.
- Report `provider_api_key_configured` as a boolean only.
  - Rationale: external tooling needs to know if credentials are expected, but secret values must never appear in manifest output.
- Use provider-neutral field names and avoid OpenAPI security scheme mutation in this slice.
  - Rationale: the goal is manifest discovery; full OpenAPI security annotation can remain a later polish if needed.

## Risks / Trade-offs

- Manifest access metadata can drift from middleware behavior. Mitigation: keep fields driven by the same settings and add tests for configured/unconfigured states.
- Some callers may confuse component API key with user identity. Mitigation: include explicit boundary text in metadata and docs.
