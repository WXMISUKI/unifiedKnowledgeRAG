## ADDED Requirements

### Requirement: Phase 12b candidate backend evaluation readiness stays provider-first and evaluation-only

The project SHALL treat Phase 12b candidate backend evaluation readiness as lightweight review work that consolidates candidate backend evidence without changing runtime defaults or ownership boundaries.

#### Scenario: Candidate backend readiness is phase-aligned

- **WHEN** the candidate backend evaluation readiness report is exported
- **THEN** it records which candidate backend families are review-ready, which gates remain open, and which engines remain reference-only
- **AND** it keeps runtime defaults unchanged

#### Scenario: Candidate backend readiness preserves boundaries

- **WHEN** the report is published or refreshed
- **THEN** it does not add backend dependencies, GraphRAG execution, parser expansion, or caller control-plane ownership changes

### Requirement: Phase 12b candidate backend review uses explicit decision states

The project SHALL use a small, reversible decision vocabulary for candidate backend evaluation review.

#### Scenario: Candidate evaluation decision states remain explicit

- **WHEN** candidate backend evidence is summarized
- **THEN** the report uses `keep_current_default`, `continue_spike`, `eligible_for_promotion_review`, or `reference_only` as the review decision state

#### Scenario: Candidate evaluation decisions do not imply promotion

- **WHEN** the report is reviewed
- **THEN** a favorable review state still preserves the current provider contract and requires a separate promotion change before any runtime default can move
