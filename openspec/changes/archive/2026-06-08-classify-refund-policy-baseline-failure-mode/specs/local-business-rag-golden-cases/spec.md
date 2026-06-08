## ADDED Requirements

### Requirement: Aggregate review evidence distinguishes leakage from markdown provenance mismatch
The system SHALL classify real-business aggregate review evidence so callers can distinguish negative-control leakage from markdown provenance/chunk-diagnostic mismatch without changing runtime retrieval behavior.

#### Scenario: Refund-policy review exposes negative-control leakage explicitly
- **WHEN** an aggregate baseline source has expected-empty cases that return evidence or citations
- **THEN** the source report records that review signal as negative-control leakage evidence
- **AND** the aggregate report keeps the source in `review`

#### Scenario: Markdown provenance mismatch stays separate from OCR-like chunk degradation
- **WHEN** a markdown source fails chunk-quality review only because page-level provenance is absent
- **THEN** the source report records a markdown provenance mismatch observation
- **AND** it does not collapse that observation into tiny/noisy chunk degradation

### Requirement: Classified review evidence drives conservative next-step recommendations
The system SHALL use classified review evidence to recommend the next gate without promoting advanced retrieval strategies automatically.

#### Scenario: Leakage review recommends negative-control hardening
- **WHEN** aggregate review evidence includes negative-control leakage
- **THEN** the report recommends reviewing negative-control handling before advanced retrieval strategy changes

#### Scenario: Markdown provenance mismatch recommends diagnostics alignment
- **WHEN** aggregate review evidence includes markdown provenance mismatch
- **THEN** the report recommends reviewing markdown diagnostics or provenance expectations before chunking-default changes
- **AND** runtime retrieval defaults remain unchanged
