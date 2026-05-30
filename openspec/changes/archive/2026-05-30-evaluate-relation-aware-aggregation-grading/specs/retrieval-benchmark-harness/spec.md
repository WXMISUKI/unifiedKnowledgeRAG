## ADDED Requirements

### Requirement: Relation-aware aggregation grading can be evaluated locally

The system SHALL provide an evaluation-only relation-aware grading path for multi-chunk aggregation evidence.

#### Scenario: Relation grading evidence is exported

- **WHEN** relation-aware aggregation grading is exported
- **THEN** the system evaluates multi-chunk aggregation case results and writes JSON and Markdown evidence files

#### Scenario: Positive split-chunk recovery remains answer-bearing

- **WHEN** a non-empty split-chunk case returns the expected citation
- **THEN** the relation-aware grader labels it as answer-bearing

#### Scenario: Unsupported relationship is labeled separately

- **WHEN** an expected-empty query asks for an unsupported relationship and aggregation returns citation-bearing evidence
- **THEN** the relation-aware grader labels the case as relation-unsupported rather than answer-bearing

#### Scenario: Relation grading remains evaluation-only

- **WHEN** relation-aware grading evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, answer generation behavior, production rerankers, graph stores, and LLM graders remain unchanged
