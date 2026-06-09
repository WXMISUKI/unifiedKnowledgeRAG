## ADDED Requirements

### Requirement: Diagnostics alignment precedes markdown-source hardening work
The project SHALL align markdown provenance diagnostics before proposing further markdown-source hardening or retrieval changes.

#### Scenario: Provenance alignment is a separate gate
- **WHEN** a markdown source review includes a provenance expectation mismatch and another remaining real failure
- **THEN** the next provider-side slice first removes the diagnostics mismatch
- **AND** only afterwards chooses whether to open negative-control hardening or another concrete follow-up gate
