## ADDED Requirements

### Requirement: RAG answer composer is provider configurable
The system SHALL select the cited answer composer from provider configuration while preserving the existing answer endpoint contract.

#### Scenario: Deterministic composer is selected
- **WHEN** `RAG_ANSWER_COMPOSER` is unset or configured as `deterministic`
- **THEN** `POST /api/rag/answer` uses the deterministic cited composer and returns composer provider metadata

#### Scenario: Unsupported composer is selected
- **WHEN** `RAG_ANSWER_COMPOSER` is configured to an unsupported value
- **THEN** `POST /api/rag/answer` returns `ok=false` with a structured composer configuration error

### Requirement: Hosted and local answer composers fail closed until approved
The system SHALL expose hosted and local answer composer configuration names without calling hosted APIs or local LLM runtimes until explicit implementation changes approve them.

#### Scenario: Hosted composer is not implemented
- **WHEN** `RAG_ANSWER_COMPOSER=hosted`
- **THEN** `POST /api/rag/answer` returns `ok=false` with a structured composer not implemented error before generating an answer

#### Scenario: Local composer is not implemented
- **WHEN** `RAG_ANSWER_COMPOSER=local`
- **THEN** `POST /api/rag/answer` returns `ok=false` with a structured composer not implemented error before generating an answer
