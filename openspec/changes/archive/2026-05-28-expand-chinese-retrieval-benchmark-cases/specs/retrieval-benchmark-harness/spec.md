## ADDED Requirements

### Requirement: Chinese benchmark cases cover enterprise support workflows

The system SHALL include Chinese-heavy benchmark cases that exercise representative enterprise support retrieval patterns before real embedding model approval.

#### Scenario: Enterprise workflow categories are present

- **WHEN** local benchmark cases are loaded
- **THEN** the set includes exception-policy, operational-escalation, SLA, cross-source, paraphrase, evidence, and empty retrieval categories

#### Scenario: Benchmark cases remain citation-bearing

- **WHEN** a non-empty Chinese benchmark case is defined
- **THEN** it includes an expected source id and expected citation tied to a local fixture source

#### Scenario: Empty cases remain business-like

- **WHEN** an empty benchmark case is defined
- **THEN** it represents a plausible enterprise question that is intentionally unsupported by the local fixture sources
