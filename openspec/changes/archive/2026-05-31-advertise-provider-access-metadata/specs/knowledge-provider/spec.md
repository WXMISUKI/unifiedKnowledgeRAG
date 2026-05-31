## ADDED Requirements

### Requirement: Provider manifest advertises component access metadata

The system SHALL expose machine-readable component access metadata in the provider integration manifest without revealing secret values.

#### Scenario: Manifest identifies public and protected paths

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest access metadata identifies `/health` as public and `/api/*` as protected when provider API key protection is configured

#### Scenario: Manifest lists accepted access headers

- **WHEN** a caller inspects manifest access metadata
- **THEN** it lists `Authorization: Bearer <token>` and `X-Provider-Api-Key: <token>` as accepted component access header schemes

#### Scenario: Manifest redacts secret values

- **WHEN** `PROVIDER_API_KEY` is configured
- **THEN** the manifest reports that a provider API key is configured without including the secret value

#### Scenario: Access metadata preserves provider boundary

- **WHEN** manifest access metadata is exposed
- **THEN** it states that the provider access token is component-level access control and does not represent user identity, RBAC, approvals, audit policy, or source-to-agent binding
