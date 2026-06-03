## ADDED Requirements

### Requirement: Local integration contract exposes stable assumptions

The provider contract documentation and smoke outputs SHALL keep a single, stable set of assumptions for local MyPrivateAgent integration.

#### Scenario: Local assumption fields are present

- **WHEN** local integration evidence is consumed by a caller
- **THEN** it includes:
  - local base URL
  - API-key mode (`not_configured_local_dev` or `provider_key_protected_api`)
  - required pre-flight checks (capabilities, manifest, preflight, handoff, source-binding preview)
  - evidence-pack state and failure semantics

#### Scenario: Assumptions remain explicit across readiness exports

- **WHEN** readiness artifacts are regenerated
- **THEN** local assumptions remain in a machine-readable field and are not inferred from runtime side effects

### Requirement: Local integration readiness exports include handoff summary linkage

The provider SHALL provide a local integration readout that links readiness artifacts to handoff consistency.

#### Scenario: Hardening profile links to handoff

- **WHEN** the local hardening profile is exported
- **THEN** it links `provider_handoff_bundle` and core integration signals, and marks blockers without changing runtime behavior

#### Scenario: Hardening profile preserves caller ownership

- **WHEN** hardening readiness exports report blockers
- **THEN** they do not alter caller-controlled binding policy, approval flow, audit policy, or runtime answer strategy
