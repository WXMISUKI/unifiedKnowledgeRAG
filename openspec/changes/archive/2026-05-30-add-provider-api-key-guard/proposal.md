## Why

The provider is now useful as an external HTTP component, but it still has no lightweight access guard for `/api/*` once deployed beyond local-only testing. A small optional API key boundary improves deployment safety without turning the provider into an identity, policy, or approval system.

## What Changes

- Add optional `PROVIDER_API_KEY` configuration.
- When configured, require either `Authorization: Bearer <token>` or `X-Provider-Api-Key: <token>` for `/api/*` requests.
- Keep `/health` public for local and deployment health checks.
- Return a structured 401 provider error for missing or invalid credentials.
- Expose access-guard configuration state in deployment readiness without revealing the secret value.
- Preserve current local developer behavior when `PROVIDER_API_KEY` is unset.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Provider API endpoints can be protected by an optional component access token without changing capability contracts.
- `provider-roadmap`: Phase 6 deployment work includes lightweight component access control while leaving identity, roles, approvals, and audit policy to the external control plane.

## Impact

- Affected runtime: FastAPI app request handling for `/api/*`.
- Affected configuration: new optional `PROVIDER_API_KEY` environment variable.
- Affected docs/evidence: README, deployment readiness, provider roadmap specs.
- No new dependencies, identity provider integration, role model, session handling, or authorization policy engine.
