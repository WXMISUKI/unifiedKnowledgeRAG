## ADDED Requirements

### Requirement: Multi-chunk aggregation candidates can be evaluated locally

The system SHALL provide an evaluation-only path for measuring whether hybrid retrieval evidence can satisfy identifier coverage across multiple retrieved chunks from the same source document.

#### Scenario: Multi-chunk aggregation evidence is exported

- **WHEN** the multi-chunk aggregation helper runs with split-chunk identifier cases
- **THEN** it runs hybrid retrieval, groups raw evidence chunks by source document, applies identifier coverage over each group, and writes JSON and Markdown evidence files

#### Scenario: Split identifiers can be recovered across chunks

- **WHEN** a query contains multiple identifier-like tokens and raw hybrid retrieval returns those identifiers in separate chunks from the same source document
- **THEN** the aggregation candidate can retain the grouped evidence instead of requiring every identifier to appear in one chunk

#### Scenario: Aggregation evidence preserves raw diagnostics

- **WHEN** multi-chunk aggregation evidence is exported
- **THEN** the evidence includes query identifiers, raw returned citations, raw source ids, aggregated returned citations, and benchmark summary metrics

#### Scenario: Multi-chunk aggregation remains evaluation-only

- **WHEN** multi-chunk aggregation evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production parent-document stores, production rerankers, graph stores, and answer generation behavior remain unchanged
