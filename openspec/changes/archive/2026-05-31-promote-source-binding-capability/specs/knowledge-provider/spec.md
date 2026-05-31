## ADDED Requirements

### Requirement: Source binding review is a provider capability

The system SHALL expose source binding review as a discoverable provider capability while preserving the provider boundary.

#### Scenario: Capability catalog advertises source binding review

- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes capability id `knowledge.provider.source_bindings` with a `GET /api/provider/source-bindings` invocation and `ProviderSourceBindingSummaryResponse` response schema reference

#### Scenario: Provider manifest includes the source binding capability id

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest capability ids include `knowledge.provider.source_bindings`

#### Scenario: Preflight can require source binding review

- **WHEN** a caller requests provider preflight with `knowledge.provider.source_bindings` as a required capability id
- **THEN** the preflight passes required capability and schema reference checks when the endpoint contract is available

#### Scenario: Capability remains read-only evidence

- **WHEN** the provider advertises `knowledge.provider.source_bindings`
- **THEN** the capability description states that source-to-agent binding policy, approvals, audit, and final binding execution remain external control-plane responsibilities
