## ADDED Requirements

### Requirement: Readiness probe fails HTTP when provider is degraded

The system SHALL encode traffic readiness in the HTTP status of `GET /ready` while preserving the readiness response body.

#### Scenario: Ready provider returns HTTP 200

- **WHEN** a caller requests `GET /ready` and the provider readiness body has `status=ok`
- **THEN** the endpoint returns HTTP 200 with the readiness response body

#### Scenario: Degraded provider returns HTTP 503

- **WHEN** a caller requests `GET /ready` and the provider readiness body has `status=degraded`
- **THEN** the endpoint returns HTTP 503 with the same readiness response body for diagnostics

#### Scenario: Health remains diagnostic compatible

- **WHEN** a caller requests `GET /health` and the provider readiness body has `status=degraded`
- **THEN** the endpoint still returns HTTP 200 with the readiness response body
