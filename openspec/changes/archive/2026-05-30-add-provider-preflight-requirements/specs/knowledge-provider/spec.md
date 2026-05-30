## ADDED Requirements

### Requirement: Provider preflight accepts caller requirements
The system SHALL allow callers to supply binding requirements to provider preflight so an external control plane can fail closed on incompatible contract versions or missing capabilities.

#### Scenario: Required contract version matches
- **WHEN** a caller requests `GET /api/provider/preflight` with `required_contract_version=knowledge-provider-contract-v1`
- **THEN** the response includes a passed contract version check and remains bindable when other checks pass

#### Scenario: Required contract version mismatches
- **WHEN** a caller requests `GET /api/provider/preflight` with an unsupported `required_contract_version`
- **THEN** the response marks `bindable=false` and includes a failed contract version check with requested and actual contract versions

#### Scenario: Required capabilities match
- **WHEN** a caller requests `GET /api/provider/preflight` with repeated `required_capability_ids` that are all supported
- **THEN** required capability and schema-reference checks use the requested capability ids and pass when those capabilities expose schema references

#### Scenario: Required capability is missing
- **WHEN** a caller requests `GET /api/provider/preflight` with an unsupported required capability id
- **THEN** the response marks `bindable=false` and includes the missing capability id in machine-readable details

#### Scenario: Default preflight remains compatible
- **WHEN** a caller requests `GET /api/provider/preflight` without explicit requirements
- **THEN** the provider uses the default required knowledge capability ids and current contract version checks
