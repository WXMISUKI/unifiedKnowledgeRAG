## ADDED Requirements

### Requirement: Query rewrite candidates can be evaluated locally

The system SHALL evaluate query rewrite candidates against local retrieval benchmark cases without changing runtime retrieval behavior.

#### Scenario: Query rewrite candidate evidence is exported

- **WHEN** query rewrite candidate evaluation is run with benchmark cases and an output directory
- **THEN** the system writes JSON and Markdown evidence with one result per candidate

#### Scenario: Original and rewritten queries are retained

- **WHEN** a candidate rewrites a benchmark query
- **THEN** the evidence records the original query, rewritten query, rewrite flag, and benchmark outcome

#### Scenario: Expected-empty cases are protected

- **WHEN** a benchmark case expects empty retrieval
- **THEN** deterministic rewrite candidates avoid rewriting it unless a future approved change explicitly evaluates that risk

#### Scenario: Rewrite metrics are reported

- **WHEN** query rewrite evidence is exported
- **THEN** the output includes total cases, rewritten case count, rewrite rate, expected-empty rewrite count, hit rate, citation match rate, and empty handling rate

#### Scenario: Query rewrite remains local

- **WHEN** query rewrite candidate evidence is exported
- **THEN** runtime retrieval defaults and public HTTP APIs remain unchanged
