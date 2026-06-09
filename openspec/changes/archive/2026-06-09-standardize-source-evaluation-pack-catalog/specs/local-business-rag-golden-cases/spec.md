## ADDED Requirements

### Requirement: Existing source evaluation packs can be summarized by a common catalog
The system SHALL provide a common catalog view over existing source evaluation packs without changing their underlying evaluation behavior.

#### Scenario: Catalog lists baseline, failed-question, and confirmation packs
- **WHEN** the source evaluation pack catalog is exported
- **THEN** it includes entries for the existing baseline, failed-question, and confirmation artifacts when those artifacts are present
- **AND** each entry records `pack_id`, `pack_type`, `source_scope`, `decision`, `case_count`, and `recommended_next_gate`

#### Scenario: Missing pack artifacts remain visible
- **WHEN** a known source evaluation pack artifact is missing
- **THEN** the catalog records that entry as missing or blocked evidence
- **AND** it does not silently drop the pack from the catalog

### Requirement: Catalog remains evidence-only and strategy-neutral
The system SHALL use the source evaluation pack catalog as a provider-level evidence index rather than a runtime strategy switch.

#### Scenario: Catalog exposes next gate without changing runtime behavior
- **WHEN** the catalog summarizes a `review` pack
- **THEN** it records a conservative `recommended_next_gate`
- **AND** it does not automatically enable query rewrite, rerank, hybrid retrieval, chunk-default changes, parser ownership changes, source binding changes, or GraphRAG execution

#### Scenario: Catalog gives callers a unified evaluation overview
- **WHEN** a caller or maintainer needs to inspect current provider evaluation posture
- **THEN** the catalog provides a single JSON and Markdown overview over the current pack set
- **AND** callers do not need to infer the overall gate posture by manually reading each pack artifact first
