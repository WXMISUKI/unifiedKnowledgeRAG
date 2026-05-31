## ADDED Requirements

### Requirement: Phase 4 caller-consumption smoke can be exported

The system SHALL export a local Phase 4 caller-consumption smoke report that validates the caller-facing `evidence_pack-v1` allowlist and fail-closed rules using the shared evidence-pack helper.

#### Scenario: Caller-consumption smoke is exported

- **WHEN** the Phase 4 caller-consumption smoke export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/smoke/evidence-pack-consumption/`

#### Scenario: Caller-consumption smoke covers answerable evidence

- **WHEN** the smoke completes its answerable-case check
- **THEN** it confirms that `allowed_citations` matches the returned evidence set and that the citation policy remains `use_only_returned_citations`

#### Scenario: Caller-consumption smoke covers fail-closed evidence

- **WHEN** the smoke completes its empty-evidence check
- **THEN** it confirms that the evidence pack stays `insufficient_evidence` with `reason=no_documents` and no allowed citations

#### Scenario: Caller-consumption smoke remains read-only

- **WHEN** the caller-consumption smoke is exported
- **THEN** runtime retrieval defaults, caller ownership, and provider HTTP contracts remain unchanged
