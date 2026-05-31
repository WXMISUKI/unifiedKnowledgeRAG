## ADDED Requirements

### Requirement: Provider publishes evidence pack consumption contract
The system SHALL maintain a read-only local evidence pack consumption contract artifact that explains the stable `evidence_pack-v1` fields, caller rules, and fail-closed behavior.

#### Scenario: Contract artifact is discoverable
- **WHEN** the Phase 4 evidence pack consumption contract is reviewed
- **THEN** it points at the local contract document under `docs/benchmark/chinese-seed/evidence-pack-consumption-contract/`

#### Scenario: Contract artifact stays local and read-only
- **WHEN** the contract document is published or refreshed
- **THEN** it remains a local review artifact and does not change runtime retrieval defaults, final answer policy, or provider HTTP contracts

#### Scenario: Contract artifact describes caller ownership
- **WHEN** the contract document is reviewed
- **THEN** it explains that `allowed_citations` is the caller allowlist, `insufficient_evidence` is a valid fail-closed envelope, and diagnostic fields remain diagnostic
