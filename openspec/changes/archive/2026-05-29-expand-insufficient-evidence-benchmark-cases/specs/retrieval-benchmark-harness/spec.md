## ADDED Requirements

### Requirement: Evidence grading stress cases are maintained separately

The system SHALL maintain dedicated evidence grading stress cases that expose insufficient, missing, and unexpected evidence outcomes without replacing the baseline Chinese retrieval seed.

#### Scenario: Stress fixture is loaded separately

- **WHEN** evidence grading stress cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the baseline retrieval benchmark fixture

#### Scenario: Stress cases include related but insufficient evidence

- **WHEN** the stress fixture is evaluated by a strict citation grader
- **THEN** at least one case produces `related_insufficient`

#### Scenario: Stress cases include missing evidence

- **WHEN** the stress fixture is evaluated by an evidence grader
- **THEN** at least one non-empty expected case produces `missing_evidence`

#### Scenario: Stress cases include unexpected evidence

- **WHEN** the stress fixture is evaluated by an evidence grader
- **THEN** at least one expected-empty case produces `unexpected_evidence`

#### Scenario: Stress evidence remains local

- **WHEN** stress evidence is exported
- **THEN** runtime retrieval defaults, answer generation behavior, and public HTTP APIs remain unchanged
