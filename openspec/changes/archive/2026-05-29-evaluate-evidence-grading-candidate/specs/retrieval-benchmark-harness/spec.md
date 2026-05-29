## ADDED Requirements

### Requirement: Evidence grading candidates can be evaluated locally

The system SHALL evaluate evidence grading candidates against local retrieval benchmark results without changing runtime retrieval or answer generation behavior.

#### Scenario: Evidence grading candidate evidence is exported

- **WHEN** evidence grading candidate evaluation is run with benchmark cases and an output directory
- **THEN** the system writes JSON and Markdown evidence with one result per candidate

#### Scenario: Retrieved evidence is graded per case

- **WHEN** a benchmark case is evaluated by an evidence grading candidate
- **THEN** the evidence records the case id, expected source id, expected citation, returned source ids, returned citations, grading label, and grading reason

#### Scenario: Expected-empty cases are protected

- **WHEN** a benchmark case expects empty retrieval
- **THEN** the grading evidence distinguishes `no_evidence_expected` from `unexpected_evidence`

#### Scenario: Evidence grading metrics are reported

- **WHEN** evidence grading evidence is exported
- **THEN** the output includes total cases, answer-bearing rate, related-insufficient count, missing-evidence count, unexpected-evidence count, and expected-empty pass rate

#### Scenario: Evidence grading remains local

- **WHEN** evidence grading candidate evidence is exported
- **THEN** runtime retrieval defaults, answer generation behavior, and public HTTP APIs remain unchanged
