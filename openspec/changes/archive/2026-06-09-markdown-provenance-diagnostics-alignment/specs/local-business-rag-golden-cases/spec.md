## ADDED Requirements

### Requirement: Chunk diagnostics distinguish paged provenance from markdown provenance
The system SHALL evaluate page coverage only for sources whose chunk or anchor provenance is page-oriented.

#### Scenario: Paged sources still require page coverage
- **WHEN** a local business source exposes page-based chunk provenance such as `#page-1`
- **THEN** chunk-quality diagnostics continue to require page coverage
- **AND** missing page coverage can still contribute to a `review` result

#### Scenario: Non-page markdown sources do not fail page-coverage review by default
- **WHEN** a local business source exposes non-page provenance such as section or exact-term anchors without `#page-*`
- **THEN** chunk-quality diagnostics do not mark the source `review` solely because page ids are absent
- **AND** the report still records the source provenance expectation explicitly

### Requirement: Provenance alignment keeps remaining review causes visible
The system SHALL let remaining real case failures drive review after markdown provenance alignment.

#### Scenario: Markdown provenance alignment isolates negative-control leakage
- **WHEN** a markdown source previously reviewed because of page-coverage mismatch and negative-control leakage
- **THEN** the refreshed report no longer includes the markdown provenance mismatch as a review observation
- **AND** the source can still remain `review` if negative-control leakage persists
