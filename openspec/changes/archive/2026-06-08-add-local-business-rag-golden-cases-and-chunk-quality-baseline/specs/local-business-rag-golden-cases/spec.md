## ADDED Requirements

### Requirement: Local business golden cases are reusable
The system SHALL maintain a local business RAG golden-case baseline for approved local business corpora without changing runtime retrieval defaults.

#### Scenario: Golden case fixture defines answer expectations
- **WHEN** the local business RAG golden-case baseline is exported
- **THEN** the exported report includes stable case ids, queries, expected modes, expected source ids, expected citation prefixes, and business question types

#### Scenario: Answerable cases require cited evidence
- **WHEN** an answerable golden case is evaluated
- **THEN** the report records whether the provider returned answerable evidence from the expected source and citation prefix

#### Scenario: Expected-empty cases fail closed
- **WHEN** an expected-empty golden case is evaluated
- **THEN** the report records whether the provider returned insufficient evidence without endorsed citations

### Requirement: Chunk quality diagnostics are exported
The system SHALL export chunk-quality diagnostics for the same approved local business corpus used by the golden cases.

#### Scenario: Chunk quality summary is available
- **WHEN** the local business RAG golden-case baseline is exported
- **THEN** the report includes total chunk count, tiny chunk count and ratio, noisy chunk samples, citation anchor count, citation coverage ratio, page coverage, and retrieval case outcomes

#### Scenario: Missing artifacts block the report
- **WHEN** required source, chunk, or case artifacts are missing or invalid
- **THEN** the report decision is `blocked` and the report includes recommended operator actions

#### Scenario: Quality concerns require review
- **WHEN** answerable cases miss expected evidence, expected-empty cases return citations, or chunk-quality thresholds are not satisfied
- **THEN** the report decision is `review` and the report includes the failing reasons

#### Scenario: Passing baseline remains evidence-only
- **WHEN** all golden cases pass and chunk-quality diagnostics meet the local thresholds
- **THEN** the report decision is `go`
- **AND** runtime retrieval defaults, public HTTP APIs, parser ownership, source bindings, vector backends, rerankers, hybrid retrieval, and GraphRAG execution remain unchanged
