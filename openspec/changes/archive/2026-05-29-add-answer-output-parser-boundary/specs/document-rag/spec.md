## ADDED Requirements

### Requirement: RAG answer parses cited output before validation
The system SHALL parse generated cited answer text into structured answer text and citations before applying output validation.

#### Scenario: Answered result includes parser metadata
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata` includes output parser metadata showing parser id and extracted citation count

#### Scenario: Parsed citations drive validation
- **WHEN** generated answer text contains bracketed citations
- **THEN** output validation uses the parsed citations from that text

#### Scenario: Missing citations fail validation
- **WHEN** generated answer text contains no citations
- **THEN** output validation treats the output as missing citations and the provider does not endorse it as an answered result
