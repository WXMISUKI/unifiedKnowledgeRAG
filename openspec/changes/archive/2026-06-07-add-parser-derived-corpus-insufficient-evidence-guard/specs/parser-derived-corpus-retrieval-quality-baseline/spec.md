# parser-derived-corpus-retrieval-quality-baseline Specification Delta

## MODIFIED Requirements

### Requirement: Parser-derived corpus retrieval quality baseline can be exported
The system SHALL export a local retrieval quality baseline for an approved parser-derived corpus source and SHALL treat unsupported field-like questions as insufficient evidence.

#### Scenario: Quality baseline passes
- **WHEN** the parser-derived source is visible and ready
- **AND** every answerable case returns the expected source and expected citation
- **AND** every expected-empty case returns no evidence and no endorsed answer citations
- **AND** invalid citation count is zero
- **THEN** the quality baseline report has `decision=go`
- **AND** it records source id, case count, hit rate, citation match rate, empty handling rate, invalid citation count, per-case results, and recommended next action

#### Scenario: Expected-empty field-like query is guarded
- **WHEN** a parser-derived corpus query asks for a field-like fact such as contract amount or staff roster
- **AND** the returned candidate snippets do not contain supporting evidence for that field-like fact
- **THEN** the retrieval result contains no documents
- **AND** the answer result has `answer_status=insufficient_evidence`
- **AND** no answer citations are endorsed

#### Scenario: Quality baseline needs review
- **WHEN** the parser-derived source is ready
- **AND** at least one answerable case misses expected evidence, one expected-empty case returns evidence, or one citation does not match the expected citation
- **THEN** the quality baseline report has `decision=review`
- **AND** it records the review case ids and machine-readable reason code

#### Scenario: Quality baseline is blocked
- **WHEN** the parser-derived source is not visible, its manifest is unavailable, or the RAG retrieve/answer contract fails
- **THEN** the quality baseline report has `decision=blocked`
- **AND** it records the blocking source readiness or contract reason code
