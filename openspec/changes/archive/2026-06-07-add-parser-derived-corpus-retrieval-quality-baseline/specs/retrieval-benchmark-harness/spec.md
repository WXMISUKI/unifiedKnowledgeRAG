## ADDED Requirements

### Requirement: Parser-derived corpus baselines inform candidate review
The retrieval benchmark harness SHALL treat parser-derived corpus quality baselines as local evidence for deciding whether candidate backend review is useful, not as automatic runtime promotion evidence.

#### Scenario: Parser-derived baseline is available
- **WHEN** a parser-derived corpus quality baseline report has `decision=go`
- **THEN** later candidate backend review can reference the baseline source id, case fixture, hit rate, citation match rate, empty handling rate, and invalid citation count
- **AND** runtime retrieval defaults remain unchanged

#### Scenario: Parser-derived baseline needs review
- **WHEN** a parser-derived corpus quality baseline report has `decision=review` or `decision=blocked`
- **THEN** candidate backend promotion remains out of scope
- **AND** reviewers first address corpus quality, citation stability, query cases, or source readiness
