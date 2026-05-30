## ADDED Requirements

### Requirement: Provider API supports optional component access token

The system SHALL support an optional component-level access token for provider API endpoints without changing successful capability contracts.

#### Scenario: Local provider remains open when token is unset

- **WHEN** `PROVIDER_API_KEY` is not configured
- **THEN** requests to `/api/*` continue to work without access credentials

#### Scenario: API request without token is rejected

- **WHEN** `PROVIDER_API_KEY` is configured and a caller requests `/api/provider/manifest` without credentials
- **THEN** the provider responds with HTTP 401 and a machine-readable provider error code

#### Scenario: API request accepts bearer token

- **WHEN** `PROVIDER_API_KEY` is configured and a caller sends `Authorization: Bearer <token>` with the matching value
- **THEN** the `/api/*` request is allowed to reach the underlying route

#### Scenario: API request accepts provider key header

- **WHEN** `PROVIDER_API_KEY` is configured and a caller sends `X-Provider-Api-Key` with the matching value
- **THEN** the `/api/*` request is allowed to reach the underlying route

#### Scenario: Health remains public

- **WHEN** `PROVIDER_API_KEY` is configured
- **THEN** `GET /health` remains callable without access credentials

#### Scenario: Access guard is not a policy engine

- **WHEN** provider API key protection is enabled
- **THEN** the provider still does not own user identity, roles, approvals, audit policy, or source-to-agent binding decisions
