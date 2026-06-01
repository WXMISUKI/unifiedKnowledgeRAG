## ADDED Requirements

### Requirement: BGE-M3 artifact manifests capture file inventory and checksum metadata

The system SHALL write a local BGE-M3 model manifest that records the artifact inventory and checksum metadata needed to validate a private-network copy of the model directory.

#### Scenario: Manifest writes inventory and checksum metadata

- **WHEN** the BGE-M3 bootstrap helper prepares a local model snapshot
- **THEN** the written `model-manifest.json` includes the model directory, required file inventory, detected weight files, and checksum metadata for the artifact files

#### Scenario: Manifest validation fails closed

- **WHEN** required BGE-M3 artifact files are missing or incomplete
- **THEN** the helper fails closed instead of writing a misleading ready manifest

#### Scenario: Manifest remains local and read-only

- **WHEN** the manifest is generated for offline or private-network reuse
- **THEN** the helper does not change runtime defaults, download policy, or embedding promotion state

### Requirement: BGE-M3 artifact readiness can be exported locally

The system SHALL export a local BGE-M3 artifact readiness report that summarizes checksum-aware model artifact status for deployment and Phase 3 bridge review.

#### Scenario: Readiness export writes artifacts

- **WHEN** the BGE-M3 artifact readiness export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/operations/bge-m3-artifact-readiness/`

#### Scenario: Readiness export summarizes artifact state

- **WHEN** the export completes
- **THEN** the report includes model path presence, manifest presence, required file inventory, checksum coverage, local-files-only posture, and deployment-readiness linkage

#### Scenario: Readiness export remains read-only

- **WHEN** the artifact readiness report is exported
- **THEN** runtime embedding defaults, public HTTP APIs, and promotion decisions remain unchanged
